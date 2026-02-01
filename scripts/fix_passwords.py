"""
One-time migration to replace plain-text passwords with bcrypt hashes.

Requirements:
    - Environment variables:
            MONGODB_URI
        Optional:
            MONGODB_DB (default: "rag_prototype")
            MONGODB_USERS_COLLECTION (default: "users")
"""

from __future__ import annotations

import logging
import os
import re
import sys
from typing import Iterable, Optional, Tuple, Union

import bcrypt
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv


# Load environment variables from the repo root .env for local runs.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))

# Match standard bcrypt hashes ($2b$, $2a$, $2y$, $2x$, $2$).
_BCRYPT_RE = re.compile(r"^\$2[abxy]?\$\d{2}\$[./A-Za-z0-9]{53}$")


def _mongo_uri() -> str:
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI must be set.")
    return uri


def _mongo_db_name() -> str:
    return os.getenv("MONGODB_DB", "rag_prototype")


def _mongo_users_collection() -> str:
    return os.getenv("MONGODB_USERS_COLLECTION", "users")


def get_users_collection():
    client = MongoClient(_mongo_uri(), serverSelectionTimeoutMS=3000)
    return client[_mongo_db_name()][_mongo_users_collection()]


def is_bcrypt_hash(value: Optional[Union[str, bytes, memoryview]]) -> bool:
    """Return True if the stored value is a bcrypt hash."""
    if not value:
        return False
    if isinstance(value, memoryview):
        value = value.tobytes()
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            return False
    return _BCRYPT_RE.match(value) is not None


def hash_password(plaintext: Union[str, bytes, memoryview]) -> str:
    """Hash a plain-text password using bcrypt."""
    # Bcrypt hashes are salted and slow by design, reducing offline attack risk.
    return bcrypt.hashpw(_bcrypt_input(plaintext), bcrypt.gensalt()).decode("utf-8")


def verify_password(
    plaintext: Union[str, bytes, memoryview],
    stored_hash: Optional[Union[str, bytes, memoryview]],
) -> bool:
    """Verify a user password against a stored bcrypt hash."""
    # Only bcrypt hashes are accepted; plaintext is treated as invalid.
    if not stored_hash or not is_bcrypt_hash(stored_hash):
        return False
    try:
        return bcrypt.checkpw(_bcrypt_input(plaintext), _to_bytes(stored_hash))
    except ValueError:
        return False


def _to_bytes(value: Union[str, bytes, memoryview]) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, memoryview):
        return value.tobytes()
    return value.encode("utf-8")


def _bcrypt_input(plaintext: Union[str, bytes, memoryview]) -> bytes:
    """Prepare password bytes for bcrypt (72-byte input limit)."""
    pwd_bytes = _to_bytes(plaintext)
    return pwd_bytes[:72]


def fetch_users() -> Iterable[Tuple[object, str, Optional[str]]]:
    """Yield user records for migration."""
    collection = get_users_collection()
    cursor = collection.find({}, {"username": 1, "password_hash": 1, "passwordHash": 1})
    for doc in cursor:
        stored_hash = doc.get("password_hash") or doc.get("passwordHash")
        yield doc.get("_id"), doc.get("username"), stored_hash


def update_password(user_id: object, new_hash: str) -> None:
    """Update a user's password hash safely."""
    collection = get_users_collection()
    collection.update_one({"_id": user_id}, {"$set": {"password_hash": new_hash}})


def fix_plaintext_passwords() -> int:
    """Migrate plain-text passwords to bcrypt hashes. Returns count of fixes."""
    fixed = 0
    try:
        for user_id, username, stored_hash in fetch_users():
            if is_bcrypt_hash(stored_hash):
                continue
            if not stored_hash:
                logging.warning("Skipping user %s (empty password hash).", username)
                continue

            if len(_to_bytes(stored_hash)) > 72:
                logging.warning(
                    "Password for user %s exceeds 72 bytes; truncating for bcrypt.",
                    username,
                )
            new_hash = hash_password(stored_hash)
            update_password(user_id, new_hash)
            fixed += 1

        return fixed
    except PyMongoError:
        raise


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        fixed = fix_plaintext_passwords()
    except Exception as exc:
        logging.error("Password migration failed: %s", exc)
        return 1

    # Safe summary: no passwords are logged.
    logging.info("Password migration completed. Accounts fixed: %d", fixed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

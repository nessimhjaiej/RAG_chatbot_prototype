"""
Initialize MongoDB database and users collection for ICC agent.

Creates:
- Database: ICC agent ("icc_agent")
- Collection: users
- Index on username (unique)
- Seed admin/user accounts with bcrypt hashes

Environment variables:
  MONGODB_URI (required)
  MONGODB_DB (default: "icc_agent")
  MONGODB_USERS_COLLECTION (default: "users")
  ADMIN_USERNAME (default: "admin")
  ADMIN_PASSWORD (required to create admin)
  USER_USERNAME (default: "user")
  USER_PASSWORD (required to create user)
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

import bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv


# Load environment variables from the repo root .env for local runs.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be set.")
    return value


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def main() -> int:
    uri = _required("MONGODB_URI")
    db_name = _env("MONGODB_DB", "icc_agent")
    collection_name = _env("MONGODB_USERS_COLLECTION", "users")

    admin_username = _env("ADMIN_USERNAME", "admin")
    admin_password = _required("ADMIN_PASSWORD")
    user_username = _env("USER_USERNAME", "user")
    user_password = _required("USER_PASSWORD")

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]
    users = db[collection_name]

    # Ensure unique usernames
    users.create_index("username", unique=True)

    now = _utc_now()

    def ensure_user(username: str, password: str, role: str, user_id: int) -> None:
        existing = users.find_one({"username": username})
        if existing:
            return
        # Hash password with bcrypt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        users.insert_one(
            {
                "id": user_id,
                "username": username,
                "password_hash": password_hash,
                "role": role,
                "created_at": now,
            }
        )

    ensure_user(admin_username, admin_password, "admin", 1)
    ensure_user(user_username, user_password, "user", 2)

    print(
        f"Initialized MongoDB database '{db_name}' and users collection '{collection_name}'."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

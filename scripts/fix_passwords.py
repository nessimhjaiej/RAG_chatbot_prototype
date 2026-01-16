"""
One-time migration to replace plain-text passwords with bcrypt hashes.

Requirements:
  - Environment variables:
      MSSQL_SERVER, MSSQL_DATABASE
    Optional:
      MSSQL_DRIVER (default: "ODBC Driver 18 for SQL Server")
      MSSQL_UID, MSSQL_PWD (for SQL authentication)
      MSSQL_ENCRYPT (default: "yes"), MSSQL_TRUST_CERT (default: "yes")
"""

from __future__ import annotations

import logging
import os
import re
import sys
from typing import Iterable, Optional, Tuple, Union

import bcrypt
import pyodbc
from dotenv import load_dotenv


# Load environment variables from the repo root .env for local runs.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))

# Match standard bcrypt hashes ($2b$, $2a$, $2y$, $2x$, $2$).
_BCRYPT_RE = re.compile(r"^\$2[abxy]?\$\d{2}\$[./A-Za-z0-9]{53}$")


def build_connection_string() -> str:
    """Build a SQL Server connection string using SQL or Windows auth."""
    server = os.getenv("MSSQL_SERVER")
    database = os.getenv("MSSQL_DATABASE")
    driver = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
    uid = os.getenv("MSSQL_UID")
    pwd = os.getenv("MSSQL_PWD")
    encrypt = os.getenv("MSSQL_ENCRYPT", "yes")
    trust_cert = os.getenv("MSSQL_TRUST_CERT", "yes")

    if not server or not database:
        raise ValueError("MSSQL_SERVER and MSSQL_DATABASE must be set.")

    if uid and pwd:
        return (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={uid};PWD={pwd};Encrypt={encrypt};TrustServerCertificate={trust_cert};"
        )

    # Fall back to Windows auth when no SQL credentials are provided.
    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"


def get_connection() -> pyodbc.Connection:
    """Open a database connection with explicit transaction control."""
    conn_str = build_connection_string()
    return pyodbc.connect(conn_str, autocommit=False)


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


def fetch_users(cursor: pyodbc.Cursor) -> Iterable[Tuple[int, str, Optional[str]]]:
    """Yield user records for migration."""
    # Parameterless query; no user input is injected.
    cursor.execute("SELECT Id, Username, PasswordHash FROM dbo.Users")
    return cursor.fetchall()


def update_password(cursor: pyodbc.Cursor, user_id: int, new_hash: str) -> None:
    """Update a user's password hash safely."""
    # Parameterized query prevents SQL injection.
    cursor.execute("UPDATE dbo.Users SET PasswordHash = ? WHERE Id = ?", new_hash, user_id)


def fix_plaintext_passwords() -> int:
    """Migrate plain-text passwords to bcrypt hashes. Returns count of fixes."""
    fixed = 0
    conn = get_connection()
    try:
        cursor = conn.cursor()
        users = fetch_users(cursor)
        for user_id, username, stored_hash in users:
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
            update_password(cursor, user_id, new_hash)
            fixed += 1

        conn.commit()
        return fixed
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


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

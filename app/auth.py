"""
Application authentication utilities.

Provides database-backed user authentication and role fetching for Streamlit UI.

Environment variables (same as scripts/fix_passwords.py):
  MSSQL_SERVER, MSSQL_DATABASE
Optional:
  MSSQL_DRIVER (default: "ODBC Driver 18 for SQL Server")
  MSSQL_UID, MSSQL_PWD (for SQL authentication)
  MSSQL_ENCRYPT (default: "yes"), MSSQL_TRUST_CERT (default: "yes")
"""

from __future__ import annotations

import os
import logging
from typing import Optional, Dict

import pyodbc
from passlib.hash import bcrypt as passlib_bcrypt
from dotenv import load_dotenv

# Load .env from repo root to ease local dev
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))


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

    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"


def get_connection() -> pyodbc.Connection:
    """Open a database connection with explicit transaction control."""
    conn_str = build_connection_string()
    return pyodbc.connect(conn_str, autocommit=True)


def fetch_user(username: str) -> Optional[Dict]:
    """Fetch a user record by username.

    Expects table dbo.Users with columns: Id, Username, PasswordHash, Role (optional).
    Returns dict or None if not found.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Parameterized query prevents SQL injection.
        cursor.execute(
            "SELECT Id, Username, PasswordHash, Role FROM dbo.Users WHERE Username = ?",
            username,
        )
        row = cursor.fetchone()
        if not row:
            return None
        # pyodbc returns a Row; index by position
        # Fall back if Role column is missing
        try:
            role = row[3]
        except Exception:
            role = None
        return {
            "id": row[0],
            "username": row[1],
            "password_hash": row[2],
            "role": (str(role).lower() if role else None),
        }
    finally:
        conn.close()


def verify_password(plaintext: str, stored_hash: Optional[str]) -> bool:
    """Verify a password against a bcrypt hash using passlib."""
    if not stored_hash:
        return False
    try:
        return passlib_bcrypt.verify(plaintext, stored_hash)
    except Exception:
        return False


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate a user and return a session dict with role.

    Returns dict: {"id": int, "username": str, "role": "admin"|"user"} on success; None on failure.
    Missing or unknown role defaults to "user".
    """
    user = fetch_user(username)
    if not user:
        logging.warning("Login failed: user '%s' not found", username)
        return None
    if not verify_password(password, user.get("password_hash")):
        logging.warning("Login failed: invalid password for '%s'", username)
        return None
    role = user.get("role") or "user"
    role = "admin" if role == "admin" else "user"
    return {"id": user["id"], "username": user["username"], "role": role}

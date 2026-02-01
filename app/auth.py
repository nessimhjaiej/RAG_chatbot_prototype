"""
Application authentication utilities.

Provides database-backed user authentication and role fetching for Streamlit UI.

Environment variables:
    MONGODB_URI
    MONGODB_DB (default: "rag_prototype")
    MONGODB_USERS_COLLECTION (default: "users")
"""

from __future__ import annotations

import os
import logging
from typing import Optional, Dict

import bcrypt
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

# Load .env from repo root to ease local dev
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))


def _mongo_uri() -> str:
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI must be set.")
    return uri


def _mongo_db_name() -> str:
    return os.getenv("MONGODB_DB", "rag_prototype")


def _mongo_users_collection() -> str:
    return os.getenv("MONGODB_USERS_COLLECTION", "users")


def get_mongo_client() -> MongoClient:
    """Create a MongoDB client with a short server selection timeout."""
    return MongoClient(_mongo_uri(), serverSelectionTimeoutMS=3000)


def get_users_collection():
    client = get_mongo_client()
    return client[_mongo_db_name()][_mongo_users_collection()]


def ping_mongo() -> None:
    """Raise on MongoDB connectivity issues."""
    client = get_mongo_client()
    client.admin.command("ping")


def fetch_user(username: str) -> Optional[Dict]:
    """Fetch a user record by username from MongoDB.

    Expects collection documents with fields:
      - username
      - password_hash (or passwordHash)
      - role (optional)
    """
    try:
        collection = get_users_collection()
        doc = collection.find_one({"username": username})
        if not doc:
            return None
        role = doc.get("role")
        password_hash = doc.get("password_hash") or doc.get("passwordHash")
        user_id = doc.get("id") or str(doc.get("_id"))
        return {
            "id": user_id,
            "username": doc.get("username"),
            "password_hash": password_hash,
            "role": (str(role).lower() if role else None),
        }
    except PyMongoError as exc:
        logging.error("MongoDB error while fetching user: %s", exc)
        return None


def verify_password(plaintext: str, stored_hash: Optional[str]) -> bool:
    """Verify a password against a bcrypt hash using native bcrypt."""
    if not stored_hash:
        return False
    try:
        return bcrypt.checkpw(plaintext.encode("utf-8"), stored_hash.encode("utf-8"))
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

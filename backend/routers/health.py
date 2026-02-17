"""Health check router for system status.

Provides endpoint for checking MongoDB, ChromaDB, and Ollama status.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sys
from pathlib import Path

# Add parent directory to path to import app modules
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.auth import ping_mongo
from app.vectorstore import DEFAULT_PERSIST_DIR, DEFAULT_COLLECTION_NAME, get_client

router = APIRouter()


class HealthStatus(BaseModel):
    status: str
    checks: List[str]


def _collection_count_safe(collection) -> int | None:
    """Return count of items in a Chroma collection without triggering embeddings."""
    try:
        return int(collection.count())
    except Exception:
        try:
            data = collection.get()
            ids = data.get("ids", []) or []
            return len(ids)
        except Exception:
            return None


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Check system health status.
    Returns status for MongoDB, Ollama, and ChromaDB.
    """
    checks: List[str] = []

    # Check MongoDB connection
    try:
        ping_mongo()
        checks.append("MongoDB: connected")
    except Exception as exc:
        checks.append(f"MongoDB: disconnected ({str(exc)[:50]}...)")

    # Check Ollama availability
    ollama_available = False
    try:
        import ollama
        # Try to list models to verify Ollama is running
        ollama.list()
        checks.append("Ollama: running")
        ollama_available = True
    except Exception as exc:
        checks.append(f"Ollama: unavailable ({str(exc)[:50]}...)")

    # Check Chroma persistence directory and sqlite file existence
    persist_path = Path(DEFAULT_PERSIST_DIR)
    sqlite_path = persist_path / "chroma.sqlite3"
    chroma_dir_ok = persist_path.exists()
    chroma_db_ok = sqlite_path.exists()
    checks.append(
        f"Chroma dir '{persist_path}': {'exists' if chroma_dir_ok else 'missing'}"
    )
    checks.append(
        f"Chroma DB '{sqlite_path.name}': {'exists' if chroma_db_ok else 'missing'}"
    )

    # Try to open Chroma client and collection
    try:
        client = get_client(persist_dir=persist_path)
        checks.append("Chroma client: initialized")

        if ollama_available:
            try:
                from app.vectorstore import get_collection

                collection = get_collection(client, name=DEFAULT_COLLECTION_NAME)
                count = _collection_count_safe(collection)
                count_txt = f"{count}" if count is not None else "unknown"
                checks.append(
                    f"Collection '{DEFAULT_COLLECTION_NAME}': ready (count={count_txt})"
                )
            except Exception as exc:
                checks.append(f"Chroma collection error: {exc}")
        else:
            checks.append(
                f"Collection '{DEFAULT_COLLECTION_NAME}': skipped (Ollama unavailable)"
            )
    except Exception as exc:
        checks.append(f"Chroma client error: {exc}")

    return HealthStatus(status="ok", checks=checks)

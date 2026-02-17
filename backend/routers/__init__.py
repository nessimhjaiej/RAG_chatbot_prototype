"""Router initialization for FastAPI backend."""

from . import auth, query, health

__all__ = ["auth", "query", "health"]

"""
FastAPI backend server for ICC RAG chatbot.

Exposes REST API endpoints for authentication, RAG queries, and health checks.
Reuses existing Python modules from app/ directory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.routers import auth, query, health

app = FastAPI(
    title="ICC RAG Knowledge Assistant API",
    description="REST API for ICC policy document Q&A system",
    version="1.0.0",
)

# CORS configuration for frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev port
    os.getenv("FRONTEND_URL", ""),  # Production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(health.router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ICC RAG Knowledge Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

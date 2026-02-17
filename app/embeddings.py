"""
Convert text chunks into Ollama embeddings ready for Chroma.

Usage example with Chroma:
    from chromadb import Client
    from app.embeddings import OllamaEmbeddingFunction

    client = Client()
    collection = client.get_or_create_collection(
        "icc-policies",
        embedding_function=OllamaEmbeddingFunction(),
    )
    collection.add(ids=["1"], documents=["some chunk"])
"""

from __future__ import annotations

import os
from typing import List, Sequence

import ollama
from chromadb.api.types import EmbeddingFunction
from dotenv import load_dotenv

# Load .env early so environment variables are available.
load_dotenv()

DEFAULT_MODEL = "qwen2.5:7b"


def _get_ollama_model() -> str:
    """Return the Ollama model name from environment or default."""
    return (
        os.getenv("OLLAMA_EMBEDDING_MODEL")
        or os.getenv("OLLAMA_MODEL")
        or DEFAULT_MODEL
    )


def embed_chunks(
    chunks: Sequence[str],
    *,
    model: str | None = None,
) -> List[List[float]]:
    """
    Convert a list of text chunks into embedding vectors using Ollama.

    The vectors can be stored in Chroma collections for similarity search.
    """
    if not chunks:
        return []

    model_name = model or _get_ollama_model()
    vectors: List[List[float]] = []

    for chunk in chunks:
        response = ollama.embeddings(
            model=model_name,
            prompt=chunk,
        )
        vectors.append(response["embedding"])

    return vectors


class OllamaEmbeddingFunction(EmbeddingFunction):
    """
    Chroma embedding function backed by Ollama.

    Pass an instance of this class to Chroma's collection factory methods.
    """

    def __init__(
        self,
        *,
        model: str | None = None,
    ) -> None:
        self.model = model or _get_ollama_model()

    def __call__(self, texts: Sequence[str]) -> List[List[float]]:
        return embed_chunks(
            texts,
            model=self.model,
        )

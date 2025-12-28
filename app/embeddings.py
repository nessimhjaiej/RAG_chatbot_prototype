"""
Convert text chunks into Gemini embeddings ready for Chroma.

Usage example with Chroma:
    from chromadb import Client
    from app.embeddings import GeminiEmbeddingFunction

    client = Client()
    collection = client.get_or_create_collection(
        "icc-policies",
        embedding_function=GeminiEmbeddingFunction(),
    )
    collection.add(ids=["1"], documents=["some chunk"])
"""

from __future__ import annotations

import os
from typing import List, Sequence

from google import genai
from chromadb.utils.embedding_functions import EmbeddingFunction
from dotenv import load_dotenv

# Load .env early so GEMINI_API_KEY is available when resolving the key.
load_dotenv()

DEFAULT_MODEL = "gemini-embedding-001"

_client: genai.Client | None = None


def _resolve_api_key(explicit_key: str | None = None) -> str:
    """Return a Gemini API key or fail fast with a helpful message."""
    api_key = explicit_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini API key not found. Set GEMINI_API_KEY in your environment.")
    return api_key


def _get_client(api_key: str | None = None) -> genai.Client:
    """Return a singleton google.genai Client."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=_resolve_api_key(api_key))
    return _client


def embed_chunks(
    chunks: Sequence[str],
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> List[List[float]]:
    """
    Convert a list of text chunks into embedding vectors using Gemini.

    The vectors can be stored in Chroma collections for similarity search.
    """
    if not chunks:
        return []

    client = _get_client(api_key)
    vectors: List[List[float]] = []

    for chunk in chunks:
        response = client.models.embed_content(
            model=model,
            contents=chunk,
        )
        vectors.append(response.embeddings[0].values)

    return vectors


class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Chroma embedding function backed by google.genai embed_content.

    Pass an instance of this class to Chroma's collection factory methods.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.api_key = api_key
        self.model = model
        _get_client(api_key)

    def __call__(self, texts: Sequence[str]) -> List[List[float]]:
        return embed_chunks(
            texts,
            api_key=self.api_key,
            model=self.model,
        )

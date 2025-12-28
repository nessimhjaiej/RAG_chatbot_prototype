"""
Chroma persistence utilities for the ICC knowledge base.

This module creates and loads a persistent Chroma client, wires in the Gemini
embedding function, and provides small helpers to add/query documents.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Mapping, MutableSequence, Sequence

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models import Collection

from app.embeddings import GeminiEmbeddingFunction

DEFAULT_PERSIST_DIR = Path("chromadb")
DEFAULT_COLLECTION_NAME = "icc-policies"


def get_client(persist_dir: Path | str = DEFAULT_PERSIST_DIR) -> ClientAPI:
    """
    Return a Chroma PersistentClient, creating the storage directory if needed.
    """
    path = Path(persist_dir)
    path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(path))


def get_collection(
    client: ClientAPI,
    name: str = DEFAULT_COLLECTION_NAME,
    *,
    embedding_function=None,
    metadata: Mapping[str, str] | None = None,
) -> Collection.Collection:
    """
    Return a Chroma collection configured for Gemini embeddings.

    Embedding function defaults to GeminiEmbeddingFunction() when not provided.
    """
    embedding_fn = embedding_function or GeminiEmbeddingFunction()
    collection_metadata = {"hnsw:space": "cosine"}
    if metadata:
        collection_metadata.update(metadata)

    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_fn,
        metadata=collection_metadata,
    )


def add_documents(
    collection: Collection.Collection,
    *,
    ids: Sequence[str],
    documents: Sequence[str],
    metadatas: Sequence[Mapping] | None = None,
) -> None:
    """
    Add documents to the collection with their IDs and optional metadata.

    Raises ValueError when inputs are empty or lengths differ.
    """
    if not ids or not documents:
        raise ValueError("ids and documents must be non-empty")
    if len(ids) != len(documents):
        raise ValueError("ids and documents must have the same length")
    if metadatas and len(metadatas) != len(ids):
        raise ValueError("metadatas must match the length of ids when provided")

    collection.add(
        ids=list(ids),
        documents=list(documents),
        metadatas=list(metadatas) if metadatas else None,
    )


def query_collection(
    collection: Collection.Collection,
    query_text: str,
    *,
    n_results: int = 5,
    where: Mapping | None = None,
    include: MutableSequence[str] | None = None,
) -> Mapping:
    """
    Query the collection and return Chroma's raw response dict.

    include may contain any of: ["documents", "distances", "metadatas", "embeddings"].
    """
    include_parts: List[str] = list(include) if include else ["documents", "metadatas", "distances"]
    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where,
        include=include_parts,
    )

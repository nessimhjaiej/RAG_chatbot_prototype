"""
One-time ingestion pipeline: read ICC text, chunk it, and persist to Chroma.

Run from repository root:
    python scripts/ingest.py --input data/raw/file_utf8.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

# Ensure project root is on sys.path when run from scripts/ directory.
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.splitter import chunk_text
from app.vectorstore import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_PERSIST_DIR,
    add_documents,
    get_client,
    get_collection,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest ICC text into Chroma with Gemini embeddings."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/file_utf8.txt"),
        help="Path to the UTF-8 ICC source text file.",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default=DEFAULT_COLLECTION_NAME,
        help="Chroma collection name.",
    )
    parser.add_argument(
        "--persist-dir",
        type=Path,
        default=DEFAULT_PERSIST_DIR,
        help="Directory for Chroma persistence.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Max characters per chunk.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=120,
        help="Overlap in characters between chunks.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the existing collection before ingesting.",
    )
    return parser.parse_args()


def ingest_file(
    input_path: Path,
    collection_name: str,
    persist_dir: Path,
    chunk_size: int,
    chunk_overlap: int,
    reset: bool,
) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    chunks: List[str] = chunk_text(
        text, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    ids = [f"{collection_name}-chunk-{i + 1}" for i in range(len(chunks))]
    metadatas = [
        {"source": input_path.name, "chunk_index": i + 1, "total_chunks": len(chunks)}
        for i in range(len(chunks))
    ]

    client = get_client(persist_dir=persist_dir)
    if reset:
        try:
            client.delete_collection(collection_name)
        except Exception:
            # If collection does not exist yet, ignore.
            pass

    collection = get_collection(client, name=collection_name)
    add_documents(collection, ids=ids, documents=chunks, metadatas=metadatas)

    print(
        f"Ingested {len(chunks)} chunks into collection '{collection_name}' at {persist_dir}"
    )


def main() -> None:
    args = parse_args()
    ingest_file(
        input_path=args.input,
        collection_name=args.collection,
        persist_dir=args.persist_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        reset=args.reset,
    )


if __name__ == "__main__":
    main()

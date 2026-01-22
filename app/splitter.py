"""
Split a UTF-8 ICC policy document into overlapping text chunks for retrieval.

Usage:
    python app/splitter.py --input data/raw/file_utf8.txt --output data/processed/file_utf8.txt

This keeps chunking simple and explainable: fixed-size windows with overlap to
preserve context between adjacent chunks.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> List[str]:
    """
    Split text into overlapping chunks for retrieval.

    Simple heuristic: keep paragraphs together when they fit; otherwise
    roll a sliding window with overlap to preserve context.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []

    for para in paragraphs:
        if len(para) <= chunk_size:
            chunks.append(para)
            continue

        start = 0
        end = len(para)
        while start < end:
            stop = min(start + chunk_size, end)
            chunks.append(para[start:stop])
            start = stop - chunk_overlap
            if start < 0:
                start = 0

    return chunks


def write_chunks(chunks: Iterable[str], output_path: Path) -> None:
    """Persist chunks as a numbered list to the output file."""
    lines = []
    for idx, chunk in enumerate(chunks, start=1):
        lines.append(f"[chunk {idx}]\n{chunk}\n")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a UTF-8 text file into overlapping chunks for retrieval."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to the UTF-8 source text file. If omitted, a common default is used.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/file_utf8.txt"),
        help="Path to write chunked output.",
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
        help="Overlap in characters between consecutive chunks.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    default_candidates = [
        Path("data/raw/file_utf8.txt"),
        Path("data/raw/file.txt"),
    ]
    input_path = args.input or next(
        (p for p in default_candidates if p.exists()), default_candidates[0]
    )
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found. Specify --input explicitly "
            f"(checked: {', '.join(str(p) for p in default_candidates)})"
        )

    text = input_path.read_text(encoding="utf-8")
    chunks = chunk_text(
        text, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_chunks(chunks, args.output)
    print(
        f"Wrote {len(chunks)} chunks from {input_path} to {args.output} "
        f"(size={args.chunk_size}, overlap={args.chunk_overlap})"
    )


if __name__ == "__main__":
    main()

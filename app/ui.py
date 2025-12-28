"""
Minimal Streamlit UI to query the ICC RAG system.

Provides a text box for questions, calls the RAG chain, and renders the answer
with supporting source passages from Chroma.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Mapping

import streamlit as st

# Ensure repo root is on sys.path when launched from arbitrary cwd.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import rag_chain


def _render_contexts(contexts: List[Mapping]) -> None:
    """Show retrieved passages with metadata and distance."""
    if not contexts:
        st.info("No supporting passages were found for this question.")
        return

    st.subheader("Sources")
    for idx, ctx in enumerate(contexts, start=1):
        meta = ctx.get("metadata", {}) or {}
        source = meta.get("source") or meta.get("file") or "unknown"
        distance = ctx.get("distance")
        header = f"Passage {idx} (source: {source})"
        with st.expander(header, expanded=False):
            st.write(ctx.get("text", ""))
            meta_lines = []
            if distance is not None:
                meta_lines.append(f"distance={distance:.4f}")
            for key, value in meta.items():
                meta_lines.append(f"{key}={value}")
            if meta_lines:
                st.caption(" | ".join(meta_lines))


def main() -> None:
    st.set_page_config(page_title="ICC RAG QA", page_icon="ICC")
    st.title("ICC Knowledge Assistant")
    st.write(
        "Ask a question about ICC policy documents. Answers are grounded in "
        "retrieved passages from the Chroma vector store."
    )

    if not os.getenv("GEMINI_API_KEY"):
        st.warning("GEMINI_API_KEY is not set; responses will fail until configured.")

    question = st.text_area("Your question", height=120, placeholder="What are the ICC membership criteria?")
    top_k = st.slider("Passages to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Get answer", type="primary"):
        if not question.strip():
            st.error("Please enter a question.")
            return

        with st.spinner("Retrieving passages and generating answer..."):
            try:
                answer, contexts = rag_chain.answer_question(question, top_k=top_k)
            except Exception as exc:  # pragma: no cover - UI error surface
                st.error(f"Failed to generate answer: {exc}")
                return

        st.subheader("Answer")
        st.write(answer or "No answer generated.")

        _render_contexts(contexts)


if __name__ == "__main__":
    main()

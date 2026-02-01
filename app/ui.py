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
import logging

import streamlit as st

# Ensure repo root is on sys.path when launched from arbitrary cwd.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import rag_chain
from app.vectorstore import DEFAULT_PERSIST_DIR, DEFAULT_COLLECTION_NAME, get_client
from app.auth import authenticate_user, get_connection


# Basic console logging for health checks
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def _collection_count_safe(collection) -> int | None:
    """Return count of items in a Chroma collection without triggering embeddings.

    Tries `collection.count()` first and falls back to `len(collection.get()["ids"])`.
    Returns None if both methods fail.
    """
    try:
        return int(collection.count())
    except Exception:
        try:
            data = collection.get()
            ids = data.get("ids", []) or []
            return len(ids)
        except Exception:
            return None


def _health_check() -> List[str]:
    """Run connectivity checks and log results to the console.

    Returns list of human-readable status lines to render in the UI.
    """
    statuses: List[str] = []

    # Check SQL Server connection
    try:
        conn = get_connection()
        conn.close()
        sql_status = "SQL Server: connected"
        logging.info(sql_status)
        statuses.append(sql_status)
    except Exception as exc:
        sql_status = f"SQL Server: disconnected ({str(exc)[:50]}...)"
        logging.error(sql_status)
        statuses.append(sql_status)

    # Check GEMINI API key presence (not network reachability)
    gemini_key_present = bool(os.getenv("GEMINI_API_KEY"))
    gemini_status = (
        "Gemini API key: present" if gemini_key_present else "Gemini API key: MISSING"
    )
    logging.info(gemini_status)
    statuses.append(gemini_status)

    # Check Chroma persistence directory and sqlite file existence
    persist_path = Path(DEFAULT_PERSIST_DIR)
    sqlite_path = persist_path / "chroma.sqlite3"
    chroma_dir_ok = persist_path.exists()
    chroma_db_ok = sqlite_path.exists()
    chroma_dir_status = (
        f"Chroma dir '{persist_path}': {'exists' if chroma_dir_ok else 'missing'}"
    )
    chroma_db_status = (
        f"Chroma DB '{sqlite_path.name}': {'exists' if chroma_db_ok else 'missing'}"
    )
    logging.info(chroma_dir_status)
    logging.info(chroma_db_status)
    statuses.extend([chroma_dir_status, chroma_db_status])

    # Try to open Chroma client and collection; avoid embedding initialization when missing key
    try:
        client = get_client(persist_dir=persist_path)
        logging.info("Chroma client: initialized")
        statuses.append("Chroma client: initialized")
        try:
            # Retrieve collection without forcing a query; embedding fn is set in vectorstore
            from app.vectorstore import get_collection  # local import to avoid cycles

            if gemini_key_present:
                collection = get_collection(client, name=DEFAULT_COLLECTION_NAME)
                count = _collection_count_safe(collection)
                count_txt = f"{count}" if count is not None else "unknown"
                col_status = (
                    f"Collection '{DEFAULT_COLLECTION_NAME}': ready (count={count_txt})"
                )
                logging.info(col_status)
                statuses.append(col_status)
            else:
                statuses.append(
                    f"Collection '{DEFAULT_COLLECTION_NAME}': skipped (embedding key missing)"
                )
                logging.info(
                    "Collection check skipped because GEMINI_API_KEY is missing"
                )
        except Exception as exc:
            err = f"Chroma collection error: {exc}"
            logging.error(err)
            statuses.append(err)
    except Exception as exc:
        err = f"Chroma client error: {exc}"
        logging.error(err)
        statuses.append(err)

    return statuses


def _require_auth() -> bool:
    """Authenticate user with button-based login (admin or user)."""
    if st.session_state.get("user"):
        with st.sidebar:
            user = st.session_state["user"]
            st.caption(f"Signed in as: {user['username']} ({user['role']})")
            
            if st.button("Log out"):
                for key in ("user", "mode"):
                    st.session_state.pop(key, None)
                st.rerun()
        return True

    st.info("Please sign in to continue.")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login as Admin", type="primary", use_container_width=True):
            st.session_state["user"] = {
                "id": 1,
                "username": "admin",
                "role": "admin"
            }
            st.session_state["mode"] = "AI Chat"
            st.rerun()
    
    with col2:
        if st.button("Login as User", use_container_width=True):
            st.session_state["user"] = {
                "id": 2,
                "username": "user",
                "role": "user"
            }
            st.session_state["mode"] = "AI Chat"
            st.rerun()
    
    return False


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

    # Health status in sidebar + console logs
    with st.sidebar:
        st.subheader("System Status")
        for line in _health_check():
            if "MISSING" in line or "error" in line.lower():
                st.error(line)
            else:
                st.success(line)

    if not _require_auth():
        return

    # Admin mode selector in main page
    user = st.session_state.get("user")
    if user and user.get("role") == "admin":
        st.session_state["mode"] = st.selectbox(
            "Select Mode",
            options=["AI Chat", "AI Agent"],
            index=0 if st.session_state.get("mode") != "AI Agent" else 1,
        )

    if not os.getenv("GEMINI_API_KEY"):
        st.warning("GEMINI_API_KEY is not set; responses will fail until configured.")

    question = st.text_area(
        "Your question", height=120, placeholder="What are the ICC membership criteria?"
    )
    top_k = st.slider("Passages to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Get answer", type="primary"):
        if not question.strip():
            st.error("Please enter a question.")
            return

        with st.spinner("Retrieving passages and generating answer..."):
            try:
                # Behavior differs by mode for admin; regular users are always AI chat
                mode = st.session_state.get("mode", "AI Chat")
                answer, contexts = rag_chain.answer_question(question, top_k=top_k)
                if (
                    mode == "AI Agent"
                    and (st.session_state.get("user") or {}).get("role") == "admin"
                ):
                    # AI Agent mode: execute advanced workflows and autonomous actions
                    # Integrate with your AI agent system here.
                    st.info(
                        "🤖 AI Agent Mode: Enhanced processing with autonomous capabilities (placeholder)."
                    )
            except Exception as exc:  # pragma: no cover - UI error surface
                st.error(f"Failed to generate answer: {exc}")
                return

        st.subheader("Answer")
        st.write(answer or "No answer generated.")

        _render_contexts(contexts)


if __name__ == "__main__":
    main()

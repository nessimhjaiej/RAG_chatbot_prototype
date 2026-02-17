"""Query router for RAG functionality.

Provides endpoint for submitting questions and getting answers with sources.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add parent directory to path to import app modules
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import rag_chain

router = APIRouter()


class QueryRequest(BaseModel):
    question: str = Field(
        ..., min_length=1, description="Question to ask the RAG system"
    )
    top_k: int = Field(
        default=5, ge=1, le=10, description="Number of passages to retrieve"
    )


class Context(BaseModel):
    text: str
    metadata: Dict
    distance: float


class QueryResponse(BaseModel):
    answer: str
    contexts: List[Context]


@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Submit a question to the RAG system.
    Returns the generated answer and retrieved source passages.
    """
    try:
        print(f"Received question: {request.question}")
        print(f"Retrieving top_k={request.top_k} passages...")
        
        answer, contexts = rag_chain.answer_question(
            request.question, top_k=request.top_k
        )
        
        print(f"Retrieved {len(contexts)} contexts from RAG chain")
        print(f"Answer length: {len(answer) if answer else 0}")
        print(f"Context types: {[type(ctx) for ctx in contexts[:2]]}")
        
        # Convert contexts to Pydantic models
        formatted_contexts = []
        for i, ctx in enumerate(contexts):
            print(f"Context {i}: keys={ctx.keys() if isinstance(ctx, dict) else 'not a dict'}")
            formatted_ctx = Context(
                text=ctx["text"], 
                metadata=ctx["metadata"], 
                distance=ctx["distance"]
            )
            formatted_contexts.append(formatted_ctx)
            print(f"  Formatted context {i}: {type(formatted_ctx)}")
        
        print(f"Total formatted contexts: {len(formatted_contexts)}")
        
        response = QueryResponse(
            answer=answer or "No answer generated.", 
            contexts=formatted_contexts
        )
        print(f"Response has {len(response.contexts)} contexts")
        
        return response
    except Exception as e:
        import traceback
        print(f"Error in query_rag: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Failed to generate answer: {str(e)}"
        )

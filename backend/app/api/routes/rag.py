"""
RAG (Retrieval-Augmented Generation) API Routes.

Provides endpoints to build and query the vector search index
over AlgoMentor's knowledge base.

Endpoints:
    POST /api/rag/index         - Index a single knowledge point
    POST /api/rag/index/all     - Rebuild full index
    GET  /api/rag/search        - Semantic search (for testing/demo)

Author: Yue Liang
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.rag_service import (
    index_knowledge_point,
    index_all_knowledge_points,
    search_relevant_chunks
)

router = APIRouter()


class IndexRequest(BaseModel):
    knowledge_point_id: int


@router.post("/index")
async def index_single_point(
    request: IndexRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Index (or re-index) a single knowledge point's article.

    Chunks the article content, generates embeddings with
    sentence-transformers, and stores in pgvector.

    Args:
        request: IndexRequest with knowledge_point_id.
        db: Database session dependency.

    Returns:
        Result dict with success status and chunks_indexed count.
    """
    if request.knowledge_point_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid knowledge_point_id"
        )

    result = await index_knowledge_point(request.knowledge_point_id, db)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Indexing failed")
        )

    return result


@router.post("/index/all")
async def index_all_points(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Rebuild the full RAG index for all knowledge points.

    Processes all knowledge points that have article content.
    Existing embeddings are replaced.

    Args:
        db: Database session dependency.

    Returns:
        Summary dict with points_indexed, points_failed, total_chunks.
    """
    result = await index_all_knowledge_points(db)
    return result


@router.get("/search")
async def semantic_search(
    q: str = Query(..., min_length=1, description="Search query"),
    knowledge_point_id: Optional[int] = Query(None, description="Filter by knowledge point"),
    top_k: int = Query(3, ge=1, le=10, description="Number of results"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Semantic search over the knowledge base (for demo and testing).

    Converts the query to an embedding and retrieves the most
    similar article chunks from pgvector.

    Args:
        q: Search query string.
        knowledge_point_id: Optional filter for a specific knowledge point.
        top_k: Number of top results to return (1-10).
        db: Database session dependency.

    Returns:
        Dictionary with results list, each containing text, score,
        knowledge_point_id, and chunk_index.
    """
    chunks = await search_relevant_chunks(
        query=q,
        db=db,
        knowledge_point_id=knowledge_point_id,
        top_k=top_k
    )

    return {
        "query": q,
        "results": chunks,
        "count": len(chunks)
    }

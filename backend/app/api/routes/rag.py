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

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import QuizQuestion
from app.services.rag_service import (
    index_knowledge_point,
    index_all_knowledge_points,
    search_relevant_chunks,
    get_embedding_model
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


@router.get("/problems/search")
async def semantic_search_problems(
    q: str = Query(..., min_length=1, description="Search query"),
    top_k: int = Query(8, ge=1, le=20, description="Number of results"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Semantic search over LeetCode problems using sentence embeddings.

    Encodes the query and computes cosine similarity against all problem
    titles and descriptions in-memory. Returns the most semantically
    similar problems.

    Args:
        q: Natural language search query (e.g. "sliding window substring").
        top_k: Number of results to return.
        db: Database session.

    Returns:
        List of matching problems with similarity scores.
    """
    try:
        import numpy as np

        # Fetch all problems (deduplicated by leetcode_id)
        result = await db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.leetcode_id.isnot(None))
            .order_by(QuizQuestion.leetcode_id, QuizQuestion.id)
        )
        all_problems = result.scalars().all()

        # Dedup: prefer record with test_cases
        seen: Dict[int, Any] = {}
        for prob in all_problems:
            lid = prob.leetcode_id
            if lid not in seen:
                seen[lid] = prob
            else:
                if not (seen[lid].test_cases and len(seen[lid].test_cases) > 0) and \
                   prob.test_cases and len(prob.test_cases) > 0:
                    seen[lid] = prob
        problems = list(seen.values())

        if not problems:
            return {"query": q, "results": [], "count": 0}

        # Encode query + all problem texts
        model = get_embedding_model()
        query_emb = model.encode([q])[0]
        texts = [
            f"#{p.leetcode_id} {p.title} {p.description or ''}"
            for p in problems
        ]
        prob_embs = model.encode(texts, show_progress_bar=False)

        # Cosine similarity
        q_norm = np.linalg.norm(query_emb)
        scores = []
        for emb, prob in zip(prob_embs, problems):
            sim = float(np.dot(query_emb, emb) / (q_norm * np.linalg.norm(emb) + 1e-9))
            scores.append((sim, prob))

        scores.sort(key=lambda x: -x[0])

        return {
            "query": q,
            "results": [
                {
                    "id": prob.id,
                    "leetcode_id": prob.leetcode_id,
                    "title": prob.title,
                    "difficulty": prob.difficulty,
                    "score": round(score, 3),
                    "has_hints": bool(prob.hints and len(prob.hints) > 0)
                }
                for score, prob in scores[:top_k]
                if score > 0.25
            ],
            "count": len([s for s, _ in scores[:top_k] if s > 0.25])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Semantic search failed: {str(e)}"
        ) from e

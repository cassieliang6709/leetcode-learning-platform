"""
RAG (Retrieval-Augmented Generation) Service.

Implements a semantic search pipeline over the AlgoMentor knowledge base.
Knowledge point articles are split into overlapping chunks, embedded using
sentence-transformers (all-MiniLM-L6-v2), and stored in PostgreSQL via
pgvector.

When users ask questions in AI chat, this service retrieves the most
relevant article chunks (by cosine similarity) to ground the LLM response
in course-specific content.

Author: Yue Liang
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text

from app.models import KnowledgePoint, KnowledgeEmbedding

# Lazy-load the embedding model to avoid startup delay when RAG is not used
_embedding_model = None


def get_embedding_model():
    """
    Get or initialize the sentence-transformers embedding model.

    Uses singleton pattern. Model is loaded once and reused.
    all-MiniLM-L6-v2: 384-dim, fast local inference, good semantic similarity.

    Returns:
        SentenceTransformer model instance.
    """
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split article text into overlapping chunks for embedding.

    Overlapping windows prevent important context from being cut at
    chunk boundaries.

    Args:
        text: Article content to chunk.
        chunk_size: Maximum characters per chunk. Defaults to 500.
        overlap: Characters shared between adjacent chunks. Defaults to 50.

    Returns:
        List of text chunks.
    """
    if not text or not isinstance(text, str):
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start += chunk_size - overlap

    return chunks


async def index_knowledge_point(
    point_id: int,
    db: AsyncSession
) -> Dict[str, Any]:
    """
    Build vector embeddings for a single knowledge point's article.

    Deletes any existing embeddings for this point, then re-indexes.
    Should be called after article content is created or updated.

    Args:
        point_id: ID of the knowledge point to index.
        db: Database session.

    Returns:
        Dictionary with:
            - success: bool
            - chunks_indexed: number of chunks created
            - error: error message if failed
    """
    try:
        result = await db.execute(
            select(KnowledgePoint).where(KnowledgePoint.id == point_id)
        )
        point = result.scalar_one_or_none()

        if not point:
            return {"success": False, "error": f"Knowledge point {point_id} not found"}

        if not point.article_content:
            return {"success": False, "error": "Knowledge point has no article content"}

        # Remove stale embeddings
        await db.execute(
            delete(KnowledgeEmbedding).where(
                KnowledgeEmbedding.knowledge_point_id == point_id
            )
        )

        # Chunk the article
        chunks = chunk_text(point.article_content)
        if not chunks:
            return {"success": False, "error": "No content to index after chunking"}

        # Generate embeddings in batch (fast local inference)
        model = get_embedding_model()
        embeddings = model.encode(chunks, show_progress_bar=False)

        # Persist to DB
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db.add(KnowledgeEmbedding(
                knowledge_point_id=point_id,
                chunk_text=chunk,
                chunk_index=i,
                embedding=embedding.tolist()
            ))

        await db.commit()

        return {"success": True, "chunks_indexed": len(chunks)}

    except Exception as e:
        await db.rollback()
        return {"success": False, "error": str(e)}


async def index_all_knowledge_points(db: AsyncSession) -> Dict[str, Any]:
    """
    Build embeddings for all knowledge points that have article content.

    Args:
        db: Database session.

    Returns:
        Summary of indexing results.
    """
    result = await db.execute(
        select(KnowledgePoint).where(KnowledgePoint.article_content.isnot(None))
    )
    points = result.scalars().all()

    indexed = 0
    failed = 0
    total_chunks = 0

    for point in points:
        res = await index_knowledge_point(point.id, db)
        if res["success"]:
            indexed += 1
            total_chunks += res.get("chunks_indexed", 0)
        else:
            failed += 1

    return {
        "success": True,
        "points_indexed": indexed,
        "points_failed": failed,
        "total_chunks": total_chunks
    }


async def search_relevant_chunks(
    query: str,
    db: AsyncSession,
    knowledge_point_id: Optional[int] = None,
    top_k: int = 3,
    min_score: float = 0.4
) -> List[Dict[str, Any]]:
    """
    Retrieve the most semantically relevant article chunks for a query.

    Uses pgvector cosine similarity search. Results below min_score
    are filtered out to avoid injecting noisy context.

    Args:
        query: User's question or message.
        db: Database session.
        knowledge_point_id: If set, restricts search to this point's chunks.
        top_k: Maximum number of chunks to return. Defaults to 3.
        min_score: Minimum cosine similarity threshold. Defaults to 0.4.

    Returns:
        List of dicts with keys: text, score, knowledge_point_id, chunk_index.
        Sorted by score descending. Empty list if no results above threshold.
    """
    if not query or not isinstance(query, str):
        return []

    try:
        model = get_embedding_model()
        query_embedding = model.encode([query])[0].tolist()

        # pgvector: <=> is cosine distance, 1 - distance = similarity
        # We cast the Python list to a vector literal for the query
        distance_expr = KnowledgeEmbedding.embedding.cosine_distance(query_embedding)

        stmt = (
            select(
                KnowledgeEmbedding.chunk_text,
                KnowledgeEmbedding.knowledge_point_id,
                KnowledgeEmbedding.chunk_index,
                (1 - distance_expr).label("score")
            )
            .order_by(text("score DESC"))
            .limit(top_k * 2)  # fetch extra, then filter by min_score
        )

        if knowledge_point_id:
            stmt = stmt.where(
                KnowledgeEmbedding.knowledge_point_id == knowledge_point_id
            )

        results = await db.execute(stmt)
        rows = results.fetchall()

        chunks = [
            {
                "text": row.chunk_text,
                "score": float(row.score),
                "knowledge_point_id": row.knowledge_point_id,
                "chunk_index": row.chunk_index
            }
            for row in rows
            if float(row.score) >= min_score
        ]

        return chunks[:top_k]

    except Exception as e:
        # RAG failure should not break the chat — return empty
        print(f"[RAG] search_relevant_chunks failed: {e}")
        return []


def build_rag_context(chunks: List[Dict[str, Any]]) -> str:
    """
    Format retrieved chunks into a context string for the LLM prompt.

    Args:
        chunks: List of chunk dicts from search_relevant_chunks.

    Returns:
        Formatted context string, or empty string if no chunks.
    """
    if not chunks:
        return ""

    lines = ["**Relevant Course Materials:**\n"]
    for i, chunk in enumerate(chunks, 1):
        lines.append(f"[Source {i}]\n{chunk['text']}\n")

    return "\n".join(lines)

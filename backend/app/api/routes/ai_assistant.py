"""
AI Assistant API Routes.

Provides AI-powered suggestions, chat functionality, and optimization
recommendations for coding problems. Integrates with SiliconFlow AI
service for intelligent tutoring features.

Author: Yue Liang
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import QuizQuestion
from app.services.siliconflow_ai import get_ai_service
from app.services.rag_service import search_relevant_chunks, build_rag_context

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


# Request/Response Models
class FailureSuggestionRequest(BaseModel):
    """
    Request model for AI suggestion on failed tests.

    Attributes:
        question_id: ID of the question.
        code: User's code that failed tests.
        language: Programming language.
        test_results: List of test result dictionaries.
    """
    question_id: int
    code: str
    language: str
    test_results: List[Dict[str, Any]]


class ChatMessage(BaseModel):
    """
    Chat message model.

    Attributes:
        role: Message role ("user" or "assistant").
        content: Message content.
    """
    role: str
    content: str


class ChatRequest(BaseModel):
    """
    Request model for AI chat.

    Attributes:
        question_id: ID of the question being discussed.
        code: Current user code.
        language: Programming language.
        message: User's message.
        chat_history: Optional previous chat messages.
    """
    question_id: int
    code: str
    language: str
    message: str
    chat_history: Optional[List[ChatMessage]] = None


class OptimizationRequest(BaseModel):
    """
    Request model for optimization suggestions.

    Attributes:
        question_id: ID of the question.
        code: Working code to optimize.
        language: Programming language.
    """
    question_id: int
    code: str
    language: str


@router.post("/suggestion/failure")
async def get_failure_suggestion(
    request: FailureSuggestionRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get AI suggestion when test cases fail.

    Automatically called when user fails test cases. Provides
    targeted feedback to help fix the code.

    Args:
        request: FailureSuggestionRequest with question, code, and test results.
        db: Database session dependency.

    Returns:
        Dictionary containing AI suggestion and metadata.

    Raises:
        HTTPException: If question not found (404) or AI service fails (500).
    """
    if not isinstance(request.question_id, int) or request.question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not request.code or not isinstance(request.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )

    try:
        # Get problem description
        stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Get AI service
        ai_service = get_ai_service()
        
        # Get suggestion
        suggestion_result = await ai_service.get_failure_suggestion(
            code=request.code,
            language=request.language,
            problem_description=question.description or "",
            test_results=request.test_results
        )
        
        if not suggestion_result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"AI service error: "
                    f"{suggestion_result.get('error', 'Unknown error')}"
                )
            )
        
        return {
            "success": True,
            "suggestion": suggestion_result.get("suggestion", ""),
            "failed_count": suggestion_result.get("failed_count", 0),
            "question_title": question.title
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get failure suggestion: {str(e)}"
        ) from e


@router.post("/chat")
@limiter.limit("20/minute")
async def chat_with_ai(
    request: ChatRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Chat with AI about the code problem.

    Provides interactive conversation about coding problems with
    context awareness from chat history.

    Args:
        request: ChatRequest with question, code, message, and optional history.
        db: Database session dependency.

    Returns:
        Dictionary containing AI response and usage information.

    Raises:
        HTTPException: If question not found (404) or AI service fails (500).
    """
    if not isinstance(request.question_id, int) or request.question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not request.message or not isinstance(request.message, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message must be a non-empty string"
        )

    try:
        # Get problem description
        stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Convert chat history to dict format
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
                if isinstance(msg, ChatMessage)
            ]
        
        # RAG: retrieve relevant course material for this question
        rag_chunks = await search_relevant_chunks(
            query=request.message,
            db=db,
            knowledge_point_id=question.knowledge_point_id,
            top_k=3
        )
        rag_context = build_rag_context(rag_chunks)

        # Get AI service
        ai_service = get_ai_service()

        # Get chat response (with RAG context injected into system prompt)
        chat_result = await ai_service.chat_about_code(
            user_message=request.message,
            code=request.code,
            language=request.language,
            problem_description=question.description or "",
            chat_history=chat_history,
            rag_context=rag_context
        )

        if not chat_result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"AI service error: "
                    f"{chat_result.get('error', 'Unknown error')}"
                )
            )

        return {
            "success": True,
            "response": chat_result.get("response", ""),
            "usage": chat_result.get("usage", {}),
            "rag_sources": [c["knowledge_point_id"] for c in rag_chunks]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to chat with AI: {str(e)}"
        ) from e


@router.post("/suggestion/optimization")
async def get_optimization_suggestion(
    request: OptimizationRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get optimization suggestions for working code.

    Called when all test cases pass. Provides suggestions for
    improving code quality, efficiency, and best practices.

    Args:
        request: OptimizationRequest with question, code, and language.
        db: Database session dependency.

    Returns:
        Dictionary containing optimization suggestions.

    Raises:
        HTTPException: If question not found (404) or AI service fails (500).
    """
    if not isinstance(request.question_id, int) or request.question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not request.code or not isinstance(request.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )

    try:
        # Get problem description
        stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Get AI service
        ai_service = get_ai_service()
        
        # Get optimization suggestions
        opt_result = await ai_service.get_optimization_suggestions(
            code=request.code,
            language=request.language,
            problem_description=question.description or ""
        )
        
        if not opt_result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"AI service error: "
                    f"{opt_result.get('error', 'Unknown error')}"
                )
            )
        
        return {
            "success": True,
            "suggestion": opt_result.get("suggestions", ""),
            "question_title": question.title
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimization suggestion: {str(e)}"
        ) from e


@router.get("/health")
async def ai_health_check() -> Dict[str, Any]:
    """
    Check if AI service is available.

    Performs a simple test request to verify AI service connectivity.

    Returns:
        Dictionary containing health status and service information.
    """
    try:
        ai_service = get_ai_service()
        
        # Simple test request
        test_result = await ai_service._make_request(
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return {
            "status": "healthy" if test_result.get("success", False) else "unhealthy",
            "service": "SiliconFlow AI",
            "model": ai_service.model,
            "fallback_mode": ai_service.fallback_mode
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "SiliconFlow AI",
            "error": str(e)
        }


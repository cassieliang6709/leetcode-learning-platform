"""
AI Assistant API Routes
Provides AI suggestions and chat functionality
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.database import get_db
from app.models import QuizQuestion
from app.services.siliconflow_ai import get_ai_service


router = APIRouter()


# Request/Response Models
class FailureSuggestionRequest(BaseModel):
    """Request for AI suggestion on failed tests"""
    question_id: int
    code: str
    language: str
    test_results: List[Dict[str, Any]]


class ChatMessage(BaseModel):
    """Chat message"""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request for AI chat"""
    question_id: int
    code: str
    language: str
    message: str
    chat_history: Optional[List[ChatMessage]] = None


class OptimizationRequest(BaseModel):
    """Request for optimization suggestions"""
    question_id: int
    code: str
    language: str


@router.post("/suggestion/failure")
async def get_failure_suggestion(
    request: FailureSuggestionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI suggestion when test cases fail
    Automatically called when user fails test cases
    """
    # Get problem description
    stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get AI service
    ai_service = get_ai_service()
    
    # Get suggestion
    suggestion_result = await ai_service.get_failure_suggestion(
        code=request.code,
        language=request.language,
        problem_description=question.description,
        test_results=request.test_results
    )
    
    if not suggestion_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {suggestion_result.get('error', 'Unknown error')}"
        )
    
    return {
        "success": True,
        "suggestion": suggestion_result["suggestion"],
        "failed_count": suggestion_result["failed_count"],
        "question_title": question.title
    }


@router.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with AI about the code problem
    Used in the chat dialog
    """
    # Get problem description
    stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Convert chat history to dict format
    chat_history = None
    if request.chat_history:
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.chat_history
        ]
    
    # Get AI service
    ai_service = get_ai_service()
    
    # Get chat response
    chat_result = await ai_service.chat_about_code(
        user_message=request.message,
        code=request.code,
        language=request.language,
        problem_description=question.description,
        chat_history=chat_history
    )
    
    if not chat_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {chat_result.get('error', 'Unknown error')}"
        )
    
    return {
        "success": True,
        "response": chat_result["response"],
        "usage": chat_result.get("usage", {})
    }


@router.post("/suggestion/optimization")
async def get_optimization_suggestion(
    request: OptimizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get optimization suggestions for working code
    Called when all test cases pass
    """
    # Get problem description
    stmt = select(QuizQuestion).where(QuizQuestion.id == request.question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get AI service
    ai_service = get_ai_service()
    
    # Get optimization suggestions
    opt_result = await ai_service.get_optimization_suggestions(
        code=request.code,
        language=request.language,
        problem_description=question.description
    )
    
    if not opt_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {opt_result.get('error', 'Unknown error')}"
        )
    
    return {
        "success": True,
        "suggestion": opt_result["suggestions"], 
        "question_title": question.title
    }


@router.get("/health")
async def ai_health_check():
    """Check if AI service is available"""
    ai_service = get_ai_service()
    
    # Simple test request
    test_result = await ai_service._make_request(
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    
    return {
        "status": "healthy" if test_result["success"] else "unhealthy",
        "service": "SiliconFlow AI",
        "model": ai_service.model
    }


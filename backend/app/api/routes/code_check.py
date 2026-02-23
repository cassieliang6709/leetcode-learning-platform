"""
Code check routes for code analysis and hint retrieval.

This module provides API endpoints for:
- Quick code analysis without saving
- Code checking with database persistence
- Hint retrieval by level
- Problem listing and details
- User submission history

Author: Yue Liang
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import CodeSubmission, QuizQuestion, User
from app.schemas import CodeSubmissionCreate, CodeCheckResponse
from app.services.ai_service import get_hint_by_level
from app.services.siliconflow_ai import get_ai_service
from app.services.auth_service import get_current_user

router = APIRouter()


class QuickCodeCheck(BaseModel):
    """
    Request model for quick code check.

    Attributes:
        code: Source code to analyze.
        language: Programming language (default: "python").
    """
    code: str
    language: str = "python"


class HintRequest(BaseModel):
    """
    Request model for hint retrieval.

    Attributes:
        code: Current user code.
        hint_level: Hint level (1-3, default: 1).
    """
    code: str
    hint_level: int = 1


@router.post("/analyze", response_model=CodeCheckResponse)
async def analyze_code_quick(
    request: QuickCodeCheck
) -> CodeCheckResponse:
    """
    Quick code analysis without saving to database.

    Provides immediate code analysis feedback without persisting
    the submission.

    Args:
        request: QuickCodeCheck with code and language.

    Returns:
        CodeCheckResponse with analysis results.

    Raises:
        HTTPException: If code or language is invalid.
    """
    if not request.code or not isinstance(request.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )

    try:
        ai = get_ai_service()
        # Use a minimal problem_description for standalone analysis
        result = await ai.get_optimization_suggestions(
            code=request.code,
            language=request.language,
            problem_description="Analyze this code for errors and improvements."
        )
        suggestions = [result.get("suggestions", "")] if result.get("success") else []
        return CodeCheckResponse(
            has_errors=False,
            errors=[result.get("error", "")] if not result.get("success") else [],
            suggestions=suggestions,
            corrected_code=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze code: {str(e)}"
        ) from e


@router.post("/check", response_model=CodeCheckResponse)
async def check_code(
    submission: CodeSubmissionCreate,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> CodeCheckResponse:
    """
    Check code for errors and provide AI feedback, optionally save to database.

    Analyzes code using SiliconFlow AI and saves the submission to database
    for authenticated users. Guest users receive analysis without persistence.

    Args:
        submission: CodeSubmissionCreate with code, language, and optional notes.
        current_user: Authenticated user from JWT token, or None for guests.
        db: Database session dependency.

    Returns:
        CodeCheckResponse with analysis results.

    Raises:
        HTTPException: If question not found (404) or analysis fails (500).
    """
    if not submission.code or not isinstance(submission.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )

    try:
        ai = get_ai_service()
        result = await ai.get_optimization_suggestions(
            code=submission.code,
            language=submission.language,
            problem_description="Analyze this code for errors and improvements."
        )

        suggestions = [result.get("suggestions", "")] if result.get("success") else []
        errors = [result.get("error", "")] if not result.get("success") else []
        analysis = {"suggestions": suggestions, "errors": errors, "has_errors": bool(errors)}

        # Verify question exists if provided
        if submission.question_id:
            q_result = await db.execute(
                select(QuizQuestion).where(QuizQuestion.id == submission.question_id)
            )
            if not q_result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found"
                )

        # Save submission only for authenticated users
        if current_user:
            code_sub = CodeSubmission(
                user_id=current_user.id,
                question_id=submission.question_id,
                code=submission.code,
                language=submission.language,
                ai_feedback=analysis,
                notes=submission.notes
            )
            db.add(code_sub)
            await db.commit()

        return CodeCheckResponse(
            has_errors=bool(errors),
            errors=errors,
            suggestions=suggestions,
            corrected_code=None
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check code: {str(e)}"
        ) from e


@router.get("/hint/{question_id}/{hint_level}")
async def request_hint(
    question_id: int,
    hint_level: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Request hint based on difficulty level.

    Hint levels:
        Level 1: Algorithm strategy (English)
        Level 2: Core code implementation
        Level 3: YouTube video recommendation

    Args:
        question_id: ID of the question.
        hint_level: Hint level (1-3).
        db: Database session dependency.

    Returns:
        Dictionary containing hint information with optional video link.

    Raises:
        HTTPException: If hint level is invalid (400), question not found (404),
            or hint not available (404).
    """
    if not isinstance(question_id, int) or question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not isinstance(hint_level, int) or not 1 <= hint_level <= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hint level must be between 1 and 3"
        )

    try:
        # Get question
        result = await db.execute(
            select(QuizQuestion).where(QuizQuestion.id == question_id)
        )
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        if not question.hints or not isinstance(question.hints, list):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hints not available for this question"
            )
        
        if len(question.hints) < hint_level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hint level {hint_level} not available"
            )
        
        hint = question.hints[hint_level - 1]
        if not isinstance(hint, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid hint format"
            )
        
        response: Dict[str, Any] = {
            "hint_level": hint_level,
            "hint_type": hint.get("type", "unknown"),
            "content": hint.get("content", ""),
            "question_title": question.title,
            "leetcode_id": question.leetcode_id
        }
        
        # Add video link for level 3
        if hint_level == 3 and question.video_link:
            response["video_link"] = question.video_link
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get hint: {str(e)}"
        ) from e


@router.get("/problems")
async def get_problems(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get LeetCode problems, optionally filtered by category or difficulty.

    Args:
        category: Optional category filter (not currently implemented).
        difficulty: Optional difficulty filter ("easy", "medium", "hard").
        db: Database session dependency.

    Returns:
        Dictionary containing list of problems with metadata.

    Raises:
        HTTPException: If database error occurs.
    """
    try:
        query = select(QuizQuestion)
        
        if difficulty:
            if difficulty not in ["easy", "medium", "hard"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Difficulty must be 'easy', 'medium', or 'hard'"
                )
            query = query.where(QuizQuestion.difficulty == difficulty)
        
        result = await db.execute(query.order_by(QuizQuestion.leetcode_id))
        problems = result.scalars().all()
        
        return {
            "problems": [
                {
                    "id": prob.id,
                    "leetcode_id": prob.leetcode_id,
                    "title": prob.title,
                    "description": prob.description,
                    "difficulty": prob.difficulty,
                    "has_hints": (
                        prob.hints is not None
                        and isinstance(prob.hints, list)
                        and len(prob.hints) > 0
                    ),
                    "video_link": prob.video_link
                }
                for prob in problems
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get problems: {str(e)}"
        ) from e


@router.get("/problem/{question_id}")
async def get_problem_detail(
    question_id: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific problem.

    Args:
        question_id: ID of the question.
        db: Database session dependency.

    Returns:
        Dictionary containing full problem details including test cases
        and starter code.

    Raises:
        HTTPException: If problem not found (404).
    """
    if not isinstance(question_id, int) or question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )

    try:
        result = await db.execute(
            select(QuizQuestion).where(QuizQuestion.id == question_id)
        )
        problem = result.scalar_one_or_none()
        
        if not problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )
        
        hints_available = []
        if problem.hints and isinstance(problem.hints, list):
            hints_available = [i + 1 for i in range(min(3, len(problem.hints)))]
        
        return {
            "id": problem.id,
            "leetcode_id": problem.leetcode_id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "test_cases": problem.test_cases,
            "starter_code": problem.starter_code,
            "video_link": problem.video_link,
            "hints_available": hints_available
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get problem detail: {str(e)}"
        ) from e


@router.get("/submissions/{user_id}")
async def get_user_submissions(
    user_id: int,
    question_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's code submissions.

    Args:
        user_id: ID of the user.
        question_id: Optional question ID to filter submissions.
        db: Database session dependency.

    Returns:
        Dictionary containing list of user submissions.

    Raises:
        HTTPException: If user_id is invalid or database error occurs.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )

    try:
        query = select(CodeSubmission).where(CodeSubmission.user_id == user_id)
        if question_id:
            if not isinstance(question_id, int) or question_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid question_id"
                )
            query = query.where(CodeSubmission.question_id == question_id)

        result = await db.execute(
            query.order_by(CodeSubmission.created_at.desc())
        )
        submissions = result.scalars().all()

        return {
            "submissions": [
                {
                    "id": sub.id,
                    "question_id": sub.question_id,
                    "code": sub.code,
                    "language": sub.language,
                    "ai_feedback": sub.ai_feedback,
                    "notes": sub.notes,
                    "created_at": sub.created_at
                }
                for sub in submissions
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get submissions: {str(e)}"
        ) from e



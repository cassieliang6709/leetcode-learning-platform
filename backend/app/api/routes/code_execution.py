"""
Code Execution API Routes.

Handles code running and testing with Piston API integration.
Provides endpoints for code submission, test execution, starter code
retrieval, and submission history.

Author: Yue Liang
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import QuizQuestion, CodeSubmission
from app.services.code_executor import execute_user_code, get_executor

router = APIRouter()


# Request/Response Models
class CodeExecutionRequest(BaseModel):
    """
    Request model for code execution.

    Attributes:
        code: Source code to execute.
        language: Programming language.
        question_id: Optional question ID for context.
    """
    code: str
    language: str
    question_id: Optional[int] = None


@router.post("/submit/{question_id}")
async def submit_code(
    question_id: int,
    request: CodeExecutionRequest,
    user_id: int = 1,  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Submit code for a specific question and run test cases.

    Executes user code against test cases and saves the submission
    to the database.

    Args:
        question_id: ID of the question.
        request: CodeExecutionRequest with code and language.
        user_id: ID of the user (temporary, should come from auth).
        db: Database session dependency.

    Returns:
        Dictionary containing execution results with test results
        and summary.

    Raises:
        HTTPException: If question not found (404), no test cases (400),
            or execution fails (500).
    """
    if not isinstance(question_id, int) or question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not request.code or not isinstance(request.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )
    if not request.language or not isinstance(request.language, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language must be specified"
        )

    try:
        # Get question with test cases
        stmt = select(QuizQuestion).where(QuizQuestion.id == question_id)
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        if not question.test_cases:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This question has no test cases configured"
            )
        
        # Execute code with test cases
        execution_result = await execute_user_code(
            code=request.code,
            language=request.language,
            test_cases=question.test_cases
        )
        
        # Save submission
        submission = CodeSubmission(
            user_id=user_id,
            question_id=question_id,
            code=request.code,
            language=request.language,
            ai_feedback={
                "test_results": execution_result.get("test_results", []),
                "summary": execution_result.get("summary", {})
            }
        )
        db.add(submission)
        await db.commit()
        
        return execution_result
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit code: {str(e)}"
        ) from e


@router.get("/question/{question_id}/starter-code")
async def get_starter_code(
    question_id: int,
    language: str = "python",
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get starter code template for a question.

    Args:
        question_id: ID of the question.
        language: Programming language (default: "python").
        db: Database session dependency.

    Returns:
        Dictionary containing:
            - question_id: Question ID
            - language: Programming language
            - code: Starter code template
            - available_languages: List of available languages

    Raises:
        HTTPException: If question not found (404).
    """
    if not isinstance(question_id, int) or question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )

    try:
        stmt = select(QuizQuestion).where(QuizQuestion.id == question_id)
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        starter_code = question.starter_code or {}
        if not isinstance(starter_code, dict):
            starter_code = {}
        
        code = starter_code.get(language, "")
        
        return {
            "question_id": question_id,
            "language": language,
            "code": code,
            "available_languages": (
                list(starter_code.keys()) if starter_code else []
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get starter code: {str(e)}"
        ) from e


@router.get("/supported-languages")
async def get_supported_languages() -> Dict[str, Any]:
    """
    Get list of supported programming languages.

    Returns languages supported by the Piston execution engine
    with fallback to common languages if API call fails.

    Returns:
        Dictionary containing:
            - languages: List of language dictionaries
            - default: Default language ("python")
    """
    try:
        executor = get_executor()
        languages = await executor.get_supported_languages()
        
        # Fallback to common languages if API call fails
        common = [
            {"language": "python", "version": "3.x", "display_name": "Python 3"},
            {"language": "javascript", "version": "Node.js", "display_name": "JavaScript"},
            {"language": "java", "version": "17", "display_name": "Java"},
            {"language": "cpp", "version": "C++17", "display_name": "C++"},
            {"language": "c", "version": "C11", "display_name": "C"},
            {"language": "go", "version": "1.x", "display_name": "Go"},
            {"language": "rust", "version": "1.x", "display_name": "Rust"},
        ]
        
        return {
            "languages": languages if languages else common,
            "default": "python"
        }
    except Exception as e:
        # Return fallback languages on error
        return {
            "languages": [
                {"language": "python", "version": "3.x", "display_name": "Python 3"},
                {"language": "javascript", "version": "Node.js", "display_name": "JavaScript"},
            ],
            "default": "python"
        }


@router.get("/submissions/{user_id}/recent")
async def get_recent_submissions(
    user_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's recent code submissions.

    Args:
        user_id: ID of the user.
        limit: Maximum number of submissions to return (default: 10).
        db: Database session dependency.

    Returns:
        Dictionary containing list of recent submissions with metadata.

    Raises:
        HTTPException: If user_id is invalid or database error occurs.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )
    if not isinstance(limit, int) or limit <= 0 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 100"
        )

    try:
        stmt = select(CodeSubmission).where(
            CodeSubmission.user_id == user_id
        ).order_by(
            CodeSubmission.created_at.desc()
        ).limit(limit)
        
        result = await db.execute(stmt)
        submissions = result.scalars().all()
        
        return {
            "submissions": [
                {
                    "id": sub.id,
                    "question_id": sub.question_id,
                    "language": sub.language,
                    "created_at": sub.created_at,
                    "passed": (
                        sub.ai_feedback.get("summary", {}).get("passed", 0)
                        == sub.ai_feedback.get("summary", {}).get("total", 0)
                        if sub.ai_feedback and isinstance(sub.ai_feedback, dict)
                        else False
                    )
                }
                for sub in submissions
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get submissions: {str(e)}"
        ) from e


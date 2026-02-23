"""
Code Execution API Routes.

Handles code running and testing with Piston API integration.
Provides endpoints for code submission, test execution, starter code
retrieval, and submission history.

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
from app.models import QuizQuestion, CodeSubmission, User
from app.services.code_executor import execute_user_code, get_executor
from app.services.auth_service import get_current_user

limiter = Limiter(key_func=get_remote_address)

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
@limiter.limit("10/minute")
async def submit_code(
    question_id: int,
    body: CodeExecutionRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Submit code for a specific question and run test cases.

    Executes user code against test cases and saves the submission
    to the database. Guest users (unauthenticated) can still run
    code but their submissions are not persisted.

    Args:
        question_id: ID of the question.
        request: CodeExecutionRequest with code and language.
        current_user: Authenticated user from JWT token, or None for guests.
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
    if not body.code or not isinstance(body.code, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code must be a non-empty string"
        )
    if not body.language or not isinstance(body.language, str):
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
            code=body.code,
            language=body.language,
            test_cases=question.test_cases
        )

        # Save submission only for authenticated users
        if current_user:
            submission = CodeSubmission(
                user_id=current_user.id,
                question_id=question_id,
                code=body.code,
                language=body.language,
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


@router.get("/submissions/me/recent")
async def get_recent_submissions(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the authenticated user's recent code submissions.

    Args:
        limit: Maximum number of submissions to return (default: 10).
        current_user: Authenticated user from JWT token.
        db: Database session dependency.

    Returns:
        Dictionary containing list of recent submissions with metadata.

    Raises:
        HTTPException: 401 if not authenticated, 400 if limit invalid.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if not isinstance(limit, int) or limit <= 0 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 100"
        )

    try:
        stmt = select(CodeSubmission).where(
            CodeSubmission.user_id == current_user.id
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get submissions: {str(e)}"
        ) from e


"""
Code Execution API Routes
Handles code running and testing with Piston API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from pydantic import BaseModel

from app.database import get_db
from app.models import QuizQuestion, CodeSubmission
from app.services.code_executor import execute_user_code, get_executor


router = APIRouter()


# Request/Response Models
class CodeExecutionRequest(BaseModel):
    code: str
    language: str
    question_id: int = None
    test_mode: bool = False  # True for test cases, False for simple run


class TestCase(BaseModel):
    input: str
    expected: str


class CodeRunResponse(BaseModel):
    success: bool
    output: str
    error: str = None
    compile_output: str = None
    run_time: int = 0
    memory: int = 0


class TestResultResponse(BaseModel):
    test_case_id: int
    input: str
    expected: str
    actual: str
    passed: bool
    error: str = None
    run_time: int = 0


class CodeExecutionResponse(BaseModel):
    mode: str  # "run" or "test"
    result: CodeRunResponse = None
    test_results: List[TestResultResponse] = None
    summary: Dict[str, Any] = None


@router.post("/run", response_model=CodeExecutionResponse)
async def run_code(
    request: CodeExecutionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute code without test cases (simple run)
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await execute_user_code(
        code=request.code,
        language=request.language,
        test_cases=None
    )
    
    return result


@router.post("/submit/{question_id}", response_model=CodeExecutionResponse)
async def submit_code(
    question_id: int,
    request: CodeExecutionRequest,
    user_id: int = 1,  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Submit code for a specific question and run test cases
    """
    # Get question with test cases
    stmt = select(QuizQuestion).where(QuizQuestion.id == question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if not question.test_cases:
        raise HTTPException(
            status_code=400,
            detail="This question has no test cases configured"
        )
    
    # Execute code with test cases
    execution_result = await execute_user_code(
        code=request.code,
        language=request.language,
        test_cases=question.test_cases
    )
    
    # Save submission
    all_passed = execution_result.get("summary", {}).get("passed", 0) == \
                  execution_result.get("summary", {}).get("total", 0)
    
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


@router.get("/question/{question_id}/starter-code")
async def get_starter_code(
    question_id: int,
    language: str = "python",
    db: AsyncSession = Depends(get_db)
):
    """
    Get starter code template for a question
    """
    stmt = select(QuizQuestion).where(QuizQuestion.id == question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    starter_code = question.starter_code or {}
    code = starter_code.get(language, "")
    
    return {
        "question_id": question_id,
        "language": language,
        "code": code,
        "available_languages": list(starter_code.keys()) if starter_code else []
    }


@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported programming languages
    """
    executor = get_executor()
    languages = await executor.get_supported_languages()
    
    # Add our common languages even if API call fails
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


@router.post("/test-custom")
async def test_with_custom_cases(
    code: str,
    language: str,
    test_cases: List[TestCase]
):
    """
    Run code with custom test cases (for testing/debugging)
    """
    formatted_cases = [
        {"input": tc.input, "expected": tc.expected}
        for tc in test_cases
    ]
    
    result = await execute_user_code(
        code=code,
        language=language,
        test_cases=formatted_cases
    )
    
    return result


@router.get("/submissions/{user_id}/recent")
async def get_recent_submissions(
    user_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's recent code submissions
    """
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
                "passed": sub.ai_feedback.get("summary", {}).get("passed", 0)
                         == sub.ai_feedback.get("summary", {}).get("total", 0)
                         if sub.ai_feedback else False
            }
            for sub in submissions
        ]
    }


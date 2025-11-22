from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.database import get_db
from app.models import CodeSubmission, QuizQuestion
from app.schemas import CodeSubmissionCreate, CodeCheckResponse
from app.services.ai_service import analyze_code, get_hint_by_level

router = APIRouter()


class QuickCodeCheck(BaseModel):
    """Quick code check without saving to database"""
    code: str
    language: str = "python"


class HintRequest(BaseModel):
    """Request hint with code"""
    code: str
    hint_level: int = 1


@router.post("/analyze", response_model=CodeCheckResponse)
async def analyze_code_quick(request: QuickCodeCheck):
    """Quick code analysis without saving to database"""
    analysis = await analyze_code(request.code, request.language)
    
    return CodeCheckResponse(
        has_errors=analysis.get("has_errors", False),
        errors=analysis.get("errors", []),
        suggestions=analysis.get("suggestions", []),
        corrected_code=analysis.get("corrected_code")
    )


@router.post("/check/{user_id}", response_model=CodeCheckResponse)
async def check_code(
    user_id: int,
    submission: CodeSubmissionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Check code for errors and provide AI feedback, save to database"""
    # Analyze code using AI
    analysis = await analyze_code(submission.code, submission.language)

    try:
        # Verify question exists if provided
        if submission.question_id:
            result = await db.execute(
                select(QuizQuestion).where(QuizQuestion.id == submission.question_id)
            )
            question = result.scalar_one_or_none()
            if not question:
                raise HTTPException(status_code=404, detail="Question not found")
        
        # Save submission
        code_sub = CodeSubmission(
            user_id=user_id,
            question_id=submission.question_id,
            code=submission.code,
            language=submission.language,
            ai_feedback=analysis,
            notes=submission.notes
        )
        db.add(code_sub)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Error saving code submission: {str(e)}")
        # Still return analysis even if save fails
    
    return CodeCheckResponse(
        has_errors=analysis.get("has_errors", False),
        errors=analysis.get("errors", []),
        suggestions=analysis.get("suggestions", []),
        corrected_code=analysis.get("corrected_code")
    )


@router.get("/hint/{question_id}/{hint_level}")
async def request_hint(
    question_id: int,
    hint_level: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Request hint based on difficulty level
    Level 1: Algorithm strategy (English)
    Level 2: Core code implementation
    Level 3: YouTube video recommendation
    """
    if hint_level < 1 or hint_level > 3:
        raise HTTPException(status_code=400, detail="Hint level must be between 1 and 3")
    
    # Get question
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.id == question_id)
    )
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if not question.hints or len(question.hints) < hint_level:
        raise HTTPException(status_code=404, detail="Hint not available")
    
    hint = question.hints[hint_level - 1]
    
    response = {
        "hint_level": hint_level,
        "hint_type": hint.get("type"),
        "content": hint.get("content"),
        "question_title": question.title,
        "leetcode_id": question.leetcode_id
    }
    
    # Add video link for level 3
    if hint_level == 3 and question.video_link:
        response["video_link"] = question.video_link
    
    return response


@router.get("/problems")
async def get_problems(
    category: str = None,
    difficulty: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get LeetCode problems, optionally filtered by category or difficulty"""
    query = select(QuizQuestion)
    
    if difficulty:
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
                "has_hints": prob.hints is not None and len(prob.hints) > 0,
                "video_link": prob.video_link
            }
            for prob in problems
        ]
    }


@router.get("/problem/{question_id}")
async def get_problem_detail(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific problem"""
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.id == question_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return {
        "id": problem.id,
        "leetcode_id": problem.leetcode_id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty,
        "test_cases": problem.test_cases,
        "starter_code": problem.starter_code,
        "video_link": problem.video_link,
        "hints_available": [1, 2, 3] if problem.hints and len(problem.hints) >= 3 else []
    }


@router.get("/submissions/{user_id}")
async def get_user_submissions(
    user_id: int,
    question_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """Get user's code submissions"""
    from sqlalchemy import select

    query = select(CodeSubmission).where(CodeSubmission.user_id == user_id)
    if question_id:
        query = query.where(CodeSubmission.question_id == question_id)

    result = await db.execute(query.order_by(CodeSubmission.created_at.desc()))
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



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import CodeSubmission
from app.schemas import CodeSubmissionCreate, CodeCheckResponse
from app.services.ai_service import analyze_code, get_hint_by_level

router = APIRouter()


@router.post("/check/{user_id}", response_model=CodeCheckResponse)
async def check_code(
    user_id: int,
    submission: CodeSubmissionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Check code for errors and provide AI feedback"""
    # Analyze code using AI
    analysis = await analyze_code(submission.code, submission.language)

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

    return CodeCheckResponse(
        has_errors=analysis.get("has_errors", False),
        errors=analysis.get("errors", []),
        suggestions=analysis.get("suggestions", []),
        corrected_code=analysis.get("corrected_code")
    )


@router.post("/hint/{question_id}/{user_id}")
async def request_hint(
    question_id: int,
    user_id: int,
    code: str,
    hint_level: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """Request hint based on current code and difficulty level"""
    hint = await get_hint_by_level(question_id, code, hint_level, db)

    return {
        "hint_level": hint_level,
        "hint_type": hint.get("type"),  # strategy, code, or video
        "content": hint.get("content"),
        "video_link": hint.get("video_link")
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



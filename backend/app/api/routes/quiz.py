from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import QuizQuestion, QuizAttempt, KnowledgePoint
from app.schemas import QuizQuestionResponse
from app.services.ai_service import generate_quiz_questions

router = APIRouter()


@router.get("/by-knowledge/{knowledge_point_id}", response_model=List[QuizQuestionResponse])
async def get_quizzes_by_knowledge(
    knowledge_point_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get quiz questions for a specific knowledge point"""
    # Check if knowledge point exists
    kp_result = await db.execute(
        select(KnowledgePoint).where(KnowledgePoint.id == knowledge_point_id)
    )
    knowledge_point = kp_result.scalar_one_or_none()
    if not knowledge_point:
        raise HTTPException(status_code=404, detail="Knowledge point not found")

    # Get existing questions
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.knowledge_point_id == knowledge_point_id)
    )
    questions = result.scalars().all()

    # If no questions exist, generate some using AI
    if not questions:
        generated = await generate_quiz_questions(knowledge_point.name, knowledge_point.category)
        for q_data in generated:
            question = QuizQuestion(
                knowledge_point_id=knowledge_point_id,
                leetcode_id=q_data.get("leetcode_id"),
                title=q_data.get("title"),
                description=q_data.get("description"),
                difficulty=q_data.get("difficulty"),
                solution=q_data.get("solution"),
                hints=q_data.get("hints"),
                video_link=q_data.get("video_link")
            )
            db.add(question)
        await db.commit()

        # Re-fetch questions
        result = await db.execute(
            select(QuizQuestion).where(QuizQuestion.knowledge_point_id == knowledge_point_id)
        )
        questions = result.scalars().all()

    return questions


@router.get("/{question_id}", response_model=QuizQuestionResponse)
async def get_quiz_detail(question_id: int, db: AsyncSession = Depends(get_db)):
    """Get detailed quiz question"""
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/{question_id}/attempt/{user_id}")
async def submit_quiz_attempt(
    question_id: int,
    user_id: int,
    is_correct: bool,
    hints_used: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Submit quiz attempt"""
    attempt = QuizAttempt(
        user_id=user_id,
        question_id=question_id,
        is_correct=is_correct,
        hints_used=hints_used
    )
    db.add(attempt)
    await db.commit()

    return {
        "message": "Attempt recorded successfully",
        "is_correct": is_correct
    }


@router.get("/{question_id}/hint/{level}")
async def get_hint(
    question_id: int,
    level: int,
    db: AsyncSession = Depends(get_db)
):
    """Get hint for a question (multi-level)"""
    result = await db.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    hints = question.hints or []
    if level < 1 or level > len(hints):
        raise HTTPException(status_code=400, detail="Invalid hint level")

    hint = hints[level - 1]
    return {
        "level": level,
        "total_levels": len(hints),
        "hint": hint,
        "video_link": question.video_link if level == len(hints) else None
    }



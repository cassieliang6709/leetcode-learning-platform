from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models import QuizQuestion, QuizAttempt, KnowledgePoint, DailyKnowledgeQuestion, DailyKnowledgeAttempt
from app.schemas import QuizQuestionResponse, DailyQuizQuestion, QuizAnswerSubmit, DailyProgressResponse
from app.services.ai_service import generate_quiz_questions

router = APIRouter()

# ------> home page
"""Get daily knowledge challenge questions (3 random questions excluding already answered today)"""
@router.get("/daily/{user_id}", response_model=DailyProgressResponse)
async def get_daily_quiz(user_id: int, db: AsyncSession = Depends(get_db)):
    # Get today's start time
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get questions answered today by this user (from daily_knowledge_attempts)
    answered_today_query = select(DailyKnowledgeAttempt.question_id).where(
        and_(
            DailyKnowledgeAttempt.user_id == user_id,
            DailyKnowledgeAttempt.completed_at >= today_start
        )
    )
    answered_today_result = await db.execute(answered_today_query)
    answered_today_ids = [row[0] for row in answered_today_result.fetchall()]
    
    # Get all questions excluding ones answered today (from daily_knowledge_questions)
    if answered_today_ids:
        questions_query = select(DailyKnowledgeQuestion).where(
            DailyKnowledgeQuestion.id.not_in(answered_today_ids)
        )
    else:
        questions_query = select(DailyKnowledgeQuestion)
    
    questions_result = await db.execute(questions_query)
    # return a list that includes objects of DailyKnowledgeQuestion according to query_set
    all_questions = list(questions_result.scalars().all())
    
    # If we have less than 3 questions total, return what we have
    # Otherwise, randomly select 3 questions
    num_questions = min(3, len(all_questions))
    if len(all_questions) > 3:
        selected_questions = random.sample(all_questions, 3)
    else:
        selected_questions = all_questions
    
    # Get answered questions for today to build progress
    answered_query = select(DailyKnowledgeAttempt).where(
        and_(
            DailyKnowledgeAttempt.user_id == user_id,
            DailyKnowledgeAttempt.completed_at >= today_start
        )
    )
    answered_result = await db.execute(answered_query)
    answered_attempts = list(answered_result.scalars().all())
    
    # Prepare response
    daily_questions = []
    for q in selected_questions:
        # Get knowledge point name
        kp_name = None
        if q.knowledge_point_id:
            kp_result = await db.execute(
                select(KnowledgePoint.name).where(KnowledgePoint.id == q.knowledge_point_id)
            )
            kp_name = kp_result.scalar_one_or_none()
        
        # For frontend compatibility: use question as both title and description
        # create objects of daily_quiz_question used on frontend
        daily_questions.append(DailyQuizQuestion(
            id=q.id,
            title=q.question,  # Use question text as title
            description=q.explanation or "",  # Use explanation as description (empty if None)
            difficulty=q.difficulty or "medium",
            options=q.options,
            knowledge_point_name=kp_name,
            is_answered=False
        ))
    
    correct_count = sum(1 for attempt in answered_attempts if attempt.is_correct)
    
    return DailyProgressResponse(
        total_questions=3,
        answered_count=len(answered_today_ids),
        correct_count=correct_count,
        questions=daily_questions
    )

# ------> Homepage
"""Submit answer for a daily knowledge question"""
@router.post("/answer/{user_id}")
async def submit_answer(
    user_id: int,
    answer: QuizAnswerSubmit,
    db: AsyncSession = Depends(get_db)
):
    
    # Get the question from daily_knowledge_questions
    question_result = await db.execute(
        select(DailyKnowledgeQuestion).where(DailyKnowledgeQuestion.id == answer.question_id)
    )
    question = question_result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if answer is correct
    is_correct = answer.selected_option == question.correct_answer
    
    # Save attempt to daily_knowledge_attempts
    attempt = DailyKnowledgeAttempt(
        user_id=user_id,
        question_id=answer.question_id,
        is_correct=is_correct
    )
    db.add(attempt)
    await db.commit()
    
    return {
        "is_correct": is_correct,
        "message": "Great job! 🎉" if is_correct else "Not quite right. Try again tomorrow!",
        "explanation": question.explanation if not is_correct else None
    }


@router.get("/progress/{user_id}")
async def get_daily_progress(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get today's daily knowledge challenge progress"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get attempts today from daily_knowledge_attempts
    attempts_query = select(DailyKnowledgeAttempt).where(
        and_(
            DailyKnowledgeAttempt.user_id == user_id,
            DailyKnowledgeAttempt.completed_at >= today_start
        )
    )
    attempts_result = await db.execute(attempts_query)
    attempts = list(attempts_result.scalars().all())
    
    correct_count = sum(1 for attempt in attempts if attempt.is_correct)
    
    return {
        "answered_count": len(attempts),
        "correct_count": correct_count,
        "total_questions": 3,
        "percentage": (len(attempts) / 3) * 100 if len(attempts) > 0 else 0
    }


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



"""
Quiz routes for daily challenges and quiz question management.

This module provides API endpoints for:
- Daily knowledge challenge questions
- Quiz question retrieval and submission
- Progress tracking
- Quiz attempts recording

Author: Yue Liang
"""

from datetime import datetime
from typing import List, Dict, Any
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models import (
    QuizQuestion, QuizAttempt, KnowledgePoint,
    DailyKnowledgeQuestion, DailyKnowledgeAttempt, User
)
from app.schemas import (
    QuizQuestionResponse, DailyQuizQuestion,
    QuizAnswerSubmit, DailyProgressResponse
)
from app.services.ai_service import generate_quiz_questions
from app.services.auth_service import get_current_user_required

router = APIRouter()

@router.get("/daily", response_model=DailyProgressResponse)
async def get_daily_quiz(
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
) -> DailyProgressResponse:
    """
    Get daily knowledge challenge questions for the authenticated user.

    Returns 3 random questions excluding ones already answered today.
    """
    user_id = current_user.id
    try:
        # Get today's start time
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        # Get questions answered today by this user
        answered_today_query = select(DailyKnowledgeAttempt.question_id).where(
            and_(
                DailyKnowledgeAttempt.user_id == user_id,
                DailyKnowledgeAttempt.completed_at >= today_start
            )
        )
        answered_today_result = await db.execute(answered_today_query)
        answered_today_ids = [
            row[0] for row in answered_today_result.fetchall()
        ]
        
        # Get all questions excluding ones answered today
        if answered_today_ids:
            questions_query = select(DailyKnowledgeQuestion).where(
                DailyKnowledgeQuestion.id.not_in(answered_today_ids)
            )
        else:
            questions_query = select(DailyKnowledgeQuestion)
        
        questions_result = await db.execute(questions_query)
        all_questions = list(questions_result.scalars().all())
        
        # Randomly select 3 questions (or all if less than 3 available)
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
        daily_questions: List[DailyQuizQuestion] = []
        for q in selected_questions:
            # Get knowledge point name
            kp_name = None
            if q.knowledge_point_id:
                kp_result = await db.execute(
                    select(KnowledgePoint.name).where(
                        KnowledgePoint.id == q.knowledge_point_id
                    )
                )
                kp_name = kp_result.scalar_one_or_none()
            
            daily_questions.append(DailyQuizQuestion(
                id=q.id,
                title=q.question,
                description=q.explanation or "",
                difficulty=q.difficulty or "medium",
                options=q.options,
                knowledge_point_name=kp_name,
                is_answered=False
            ))
        
        correct_count = sum(
            1 for attempt in answered_attempts if attempt.is_correct
        )
        
        return DailyProgressResponse(
            total_questions=3,
            answered_count=len(answered_today_ids),
            correct_count=correct_count,
            questions=daily_questions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get daily quiz: {str(e)}"
        ) from e

@router.post("/answer")
async def submit_answer(
    answer: QuizAnswerSubmit,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Submit answer for a daily knowledge question."""
    user_id = current_user.id
    try:
        # Get the question from daily_knowledge_questions
        question_result = await db.execute(
            select(DailyKnowledgeQuestion).where(
                DailyKnowledgeQuestion.id == answer.question_id
            )
        )
        question = question_result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Validate selected option
        if not 0 <= answer.selected_option < len(question.options):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid option index"
            )
        
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
            "message": (
                "Great job! 🎉" if is_correct
                else "Not quite right. Try again tomorrow!"
            ),
            "explanation": question.explanation if not is_correct else None
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit answer: {str(e)}"
        ) from e


@router.get("/progress")
async def get_daily_progress(
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Get today's daily knowledge challenge progress for the authenticated user."""
    user_id = current_user.id
    try:
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get progress: {str(e)}"
        ) from e


@router.get(
    "/by-knowledge/{knowledge_point_id}",
    response_model=List[QuizQuestionResponse]
)
async def get_quizzes_by_knowledge(
    knowledge_point_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[QuizQuestionResponse]:
    """
    Get quiz questions for a specific knowledge point.

    If no questions exist, generates new questions using AI service.

    Args:
        knowledge_point_id: ID of the knowledge point.
        db: Database session dependency.

    Returns:
        List of QuizQuestionResponse objects.

    Raises:
        HTTPException: If knowledge point not found (404) or
            generation fails (500).
    """
    if not isinstance(knowledge_point_id, int) or knowledge_point_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid knowledge_point_id"
        )

    try:
        # Check if knowledge point exists
        kp_result = await db.execute(
            select(KnowledgePoint).where(
                KnowledgePoint.id == knowledge_point_id
            )
        )
        knowledge_point = kp_result.scalar_one_or_none()
        
        if not knowledge_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge point not found"
            )

        # Get existing questions
        result = await db.execute(
            select(QuizQuestion).where(
                QuizQuestion.knowledge_point_id == knowledge_point_id
            )
        )
        questions = result.scalars().all()

        # If no questions exist, generate some using AI
        if not questions:
            generated = await generate_quiz_questions(
                knowledge_point.name or "",
                knowledge_point.category or ""
            )
            for q_data in generated:
                question = QuizQuestion(
                    knowledge_point_id=knowledge_point_id,
                    leetcode_id=q_data.get("leetcode_id"),
                    title=q_data.get("title", ""),
                    description=q_data.get("description", ""),
                    difficulty=q_data.get("difficulty"),
                    solution=q_data.get("solution"),
                    hints=q_data.get("hints"),
                    video_link=q_data.get("video_link")
                )
                db.add(question)
            await db.commit()

            # Re-fetch questions
            result = await db.execute(
                select(QuizQuestion).where(
                    QuizQuestion.knowledge_point_id == knowledge_point_id
                )
            )
            questions = result.scalars().all()

        return list(questions)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quizzes: {str(e)}"
        ) from e


@router.get("/{question_id}", response_model=QuizQuestionResponse)
async def get_quiz_detail(
    question_id: int,
    db: AsyncSession = Depends(get_db)
) -> QuizQuestionResponse:
    """
    Get detailed quiz question information.

    Args:
        question_id: ID of the quiz question.
        db: Database session dependency.

    Returns:
        QuizQuestionResponse with question details.

    Raises:
        HTTPException: If question not found (404).
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
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        return question
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quiz detail: {str(e)}"
        ) from e


@router.post("/{question_id}/attempt")
async def submit_quiz_attempt(
    question_id: int,
    is_correct: bool,
    hints_used: int = 0,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Record the authenticated user's attempt at a quiz question."""
    if not isinstance(question_id, int) or question_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question_id"
        )
    if not isinstance(hints_used, int) or hints_used < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="hints_used must be a non-negative integer"
        )

    try:
        attempt = QuizAttempt(
            user_id=current_user.id,
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
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit attempt: {str(e)}"
        ) from e



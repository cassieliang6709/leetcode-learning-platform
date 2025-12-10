"""
Knowledge routes for learning content and knowledge point management.

This module provides API endpoints for:
- Knowledge point retrieval and details
- Knowledge tests and learning plan generation
- Quiz questions by knowledge point

Author: Yue Liang
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import (
    User, KnowledgePoint, KnowledgeTest, LearningPlan, QuizQuestion
)
from app.schemas import (
    KnowledgePointResponse,
    KnowledgeTestCreate,
    KnowledgeTestResponse,
    KnowledgePointDetailResponse,
    QuizQuestionResponse
)
from app.services.ai_service import generate_learning_plan

router = APIRouter()


@router.get("/points", response_model=List[KnowledgePointResponse])
async def get_knowledge_points(
    db: AsyncSession = Depends(get_db)
) -> List[KnowledgePointResponse]:
    """
    Get all knowledge points for roadmap.

    Returns all knowledge points ordered by their order_index.

    Args:
        db: Database session dependency.

    Returns:
        List of KnowledgePointResponse objects.

    Raises:
        HTTPException: If database error occurs.
    """
    try:
        result = await db.execute(
            select(KnowledgePoint).order_by(KnowledgePoint.order_index)
        )
        points = result.scalars().all()
        return list(points)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get knowledge points: {str(e)}"
        ) from e


@router.get(
    "/points/{point_id}",
    response_model=KnowledgePointDetailResponse
)
async def get_knowledge_point_detail(
    point_id: int,
    db: AsyncSession = Depends(get_db)
) -> KnowledgePointDetailResponse:
    """
    Get detailed knowledge point with article and reading questions.

    Args:
        point_id: ID of the knowledge point.
        db: Database session dependency.

    Returns:
        KnowledgePointDetailResponse with full content.

    Raises:
        HTTPException: If knowledge point not found (404).
    """
    if not isinstance(point_id, int) or point_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid point_id"
        )

    try:
        result = await db.execute(
            select(KnowledgePoint).where(KnowledgePoint.id == point_id)
        )
        point = result.scalar_one_or_none()
        
        if not point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge point not found"
            )
        
        return point
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get knowledge point: {str(e)}"
        ) from e


@router.get(
    "/points/{point_id}/questions",
    response_model=List[QuizQuestionResponse]
)
async def get_knowledge_point_questions(
    point_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[QuizQuestionResponse]:
    """
    Get all LeetCode questions related to a knowledge point.

    Args:
        point_id: ID of the knowledge point.
        db: Database session dependency.

    Returns:
        List of QuizQuestionResponse objects, ordered by difficulty
        and LeetCode ID.

    Raises:
        HTTPException: If point_id is invalid or database error occurs.
    """
    if not isinstance(point_id, int) or point_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid point_id"
        )

    try:
        result = await db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.knowledge_point_id == point_id)
            .order_by(QuizQuestion.difficulty, QuizQuestion.leetcode_id)
        )
        questions = result.scalars().all()
        return list(questions)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get questions: {str(e)}"
        ) from e


@router.post("/test/{user_id}", response_model=KnowledgeTestResponse)
async def submit_knowledge_test(
    user_id: int,
    test_data: KnowledgeTestCreate,
    db: AsyncSession = Depends(get_db)
) -> KnowledgeTestResponse:
    """
    Submit knowledge test and generate learning plan.

    Calculates test score, saves the result, and generates an AI-powered
    learning plan with recommended knowledge points.

    Args:
        user_id: ID of the user taking the test.
        test_data: Test data containing answers.
        db: Database session dependency.

    Returns:
        KnowledgeTestResponse with test results and AI-generated plan.

    Raises:
        HTTPException: If user not found (404) or processing fails (500).
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )

    try:
        # Check if user exists
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Calculate score
        score = calculate_test_score(test_data.test_data)

        # Save test result
        test = KnowledgeTest(
            user_id=user_id,
            test_data=test_data.test_data,
            score=score
        )
        db.add(test)
        await db.flush()

        # Generate AI learning plan
        ai_plan = await generate_learning_plan(test_data.test_data, score)

        # Create learning plan entries
        for point_id in ai_plan.get("recommended_points", []):
            plan = LearningPlan(
                user_id=user_id,
                knowledge_point_id=point_id,
                ai_recommendations=ai_plan
            )
            db.add(plan)

        await db.commit()

        return {
            "id": test.id,
            "score": score,
            "completed_at": test.completed_at,
            "ai_plan": ai_plan
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit test: {str(e)}"
        ) from e


@router.get("/plan/{user_id}")
async def get_learning_plan(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's active learning plan.

    Args:
        user_id: ID of the user.
        db: Database session dependency.

    Returns:
        Dictionary containing list of active learning plans.

    Raises:
        HTTPException: If no active plan found (404) or database error.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )

    try:
        result = await db.execute(
            select(LearningPlan)
            .where(LearningPlan.user_id == user_id)
            .where(LearningPlan.status == "in_progress")
        )
        plans = result.scalars().all()

        if not plans:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active learning plan found"
            )

        return {
            "plans": [
                {
                    "id": plan.id,
                    "knowledge_point_id": plan.knowledge_point_id,
                    "status": plan.status,
                    "recommendations": plan.ai_recommendations
                }
                for plan in plans
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get learning plan: {str(e)}"
        ) from e


def calculate_test_score(test_data: Dict[str, Any]) -> int:
    """
    Calculate test score based on answers.

    Args:
        test_data: Dictionary containing test answers with structure:
            {"answers": [{"is_correct": bool}, ...]}

    Returns:
        Score as percentage (0-100).

    Raises:
        ValueError: If test_data is invalid.
    """
    if not isinstance(test_data, dict):
        raise ValueError("test_data must be a dictionary")

    answers = test_data.get("answers", [])
    if not isinstance(answers, list):
        return 0

    total_questions = len(answers)
    if total_questions == 0:
        return 0

    correct_answers = sum(
        1 for answer in answers
        if isinstance(answer, dict) and answer.get("is_correct", False)
    )
    
    return int((correct_answers / total_questions) * 100)


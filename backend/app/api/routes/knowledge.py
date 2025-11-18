from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import User, KnowledgePoint, KnowledgeTest, LearningPlan
from app.schemas import KnowledgePointResponse, KnowledgeTestCreate, KnowledgeTestResponse
from app.services.ai_service import generate_learning_plan

router = APIRouter()


@router.get("/points", response_model=List[KnowledgePointResponse])
async def get_knowledge_points(db: AsyncSession = Depends(get_db)):
    """Get all knowledge points for roadmap"""
    result = await db.execute(
        select(KnowledgePoint).order_by(KnowledgePoint.order_index)
    )
    points = result.scalars().all()
    return points


@router.post("/test/{user_id}", response_model=KnowledgeTestResponse)
async def submit_knowledge_test(
    user_id: int,
    test_data: KnowledgeTestCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit knowledge test and generate learning plan"""
    # Check if user exists
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Calculate score (simplified)
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


@router.get("/plan/{user_id}")
async def get_learning_plan(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user's learning plan"""
    result = await db.execute(
        select(LearningPlan)
        .where(LearningPlan.user_id == user_id)
        .where(LearningPlan.status == "in_progress")
    )
    plans = result.scalars().all()

    if not plans:
        raise HTTPException(status_code=404, detail="No active learning plan found")

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


def calculate_test_score(test_data: dict) -> int:
    """Calculate test score based on answers"""
    # Simplified scoring logic
    total_questions = len(test_data.get("answers", []))
    correct_answers = sum(1 for answer in test_data.get("answers", []) if answer.get("is_correct"))
    return int((correct_answers / total_questions) * 100) if total_questions > 0 else 0


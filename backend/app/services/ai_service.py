"""
AI Service - Learning plan generation and hint retrieval.

Handles personalized learning plan generation based on test results,
and multi-level hint retrieval for quiz questions.

Note: Code analysis is handled by siliconflow_ai.py (SiliconFlowAI class).
This module focuses on learning-path logic.

Author: Yue Liang
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def generate_quiz_questions(
    knowledge_point_name: str,
    category: str
) -> list:
    """
    Return starter quiz questions for a knowledge point.
    Used as a fallback when no questions exist in the database.
    """
    return [
        {
            "leetcode_id": 1,
            "title": f"{knowledge_point_name} - Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "difficulty": "easy",
            "solution": "Use hash map to store complements",
            "hints": [
                {"type": "strategy", "content": "Think about using a hash map. For each number, check if its complement (target - current) exists."},
                {"type": "code", "content": "seen = {}\nfor i, num in enumerate(nums):\n    if target - num in seen:\n        return [seen[target-num], i]\n    seen[num] = i"},
                {"type": "video", "content": "Watch detailed explanation"}
            ],
            "video_link": "https://www.youtube.com/watch?v=KLlXCFG5TnA"
        }
    ]


async def generate_learning_plan(
    test_data: Dict[str, Any], score: int
) -> Dict[str, Any]:
    """
    Generate personalized learning plan based on test results.

    Analyzes test performance to identify weak areas and recommend
    appropriate knowledge points for further study.

    Args:
        test_data: Dictionary containing test answers with structure:
            {"answers": [{"is_correct": bool, "topic": str}, ...]}
        score: Test score (0-100).

    Returns:
        Dictionary containing:
            - score: Test score
            - recommended_points: List of knowledge point IDs
            - weak_areas: List of topics that need improvement
            - study_time_estimate: Estimated study time
            - next_steps: List of recommended actions

    Raises:
        ValueError: If test_data is invalid or score is out of range.
    """
    if not isinstance(test_data, dict):
        raise ValueError("test_data must be a dictionary")
    if not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("score must be an integer between 0 and 100")

    answers = test_data.get("answers", [])
    if not isinstance(answers, list):
        raise ValueError("test_data must contain 'answers' as a list")

    # Collect weak topic areas from wrong answers
    weak_areas = [
        answer["topic"]
        for answer in answers
        if isinstance(answer, dict)
        and not answer.get("is_correct", False)
        and answer.get("topic")
    ]

    # Recommend knowledge points based on score band
    if score < 40:
        recommended_points = [1, 2, 3]
    elif score < 70:
        recommended_points = [4, 5, 6]
    else:
        recommended_points = [7, 8, 9]

    return {
        "score": score,
        "recommended_points": recommended_points,
        "weak_areas": weak_areas,
        "study_time_estimate": f"{len(recommended_points) * 2} weeks",
        "next_steps": [
            "Start with basic array problems",
            "Practice daily for at least 1 hour",
            "Complete all exercises before moving to next topic"
        ]
    }


async def get_hint_by_level(
    question_id: int,
    code: str,
    level: int,
    db: AsyncSession
) -> Dict[str, Any]:
    """
    Get hint based on level for a quiz question.

    Hint levels:
        1: Strategy hint (general approach)
        2: Code hint (implementation details)
        3: Video hint (full explanation)

    Args:
        question_id: ID of the quiz question.
        code: User's current code (reserved for future AI-based hints).
        level: Hint level (1-3).
        db: Database session.

    Returns:
        Dictionary containing:
            - type: Hint type ("strategy", "code", "video", or "none")
            - content: Hint content
            - video_link: Optional video link (for level 3)

    Raises:
        ValueError: If question_id or level is invalid.
    """
    if not isinstance(question_id, int) or question_id <= 0:
        raise ValueError("question_id must be a positive integer")
    if not isinstance(level, int) or not 1 <= level <= 3:
        raise ValueError("level must be an integer between 1 and 3")

    from app.models import QuizQuestion

    try:
        result = await db.execute(
            select(QuizQuestion).where(QuizQuestion.id == question_id)
        )
        question = result.scalar_one_or_none()

        if not question or not question.hints:
            return {"type": "none", "content": "No hints available"}

        hints = question.hints
        if not isinstance(hints, list) or len(hints) == 0:
            return {"type": "none", "content": "No hints available"}

        # Clamp level to available hints
        hint_index = min(level, len(hints)) - 1
        hint = hints[hint_index]

        if not isinstance(hint, dict):
            return {"type": "none", "content": "Invalid hint format"}

        hint_data = {
            "type": hint.get("type", "none"),
            "content": hint.get("content", "No content available")
        }

        if level == 3 and question.video_link:
            hint_data["video_link"] = question.video_link

        return hint_data
    except Exception as e:
        return {"type": "error", "content": f"Error retrieving hint: {str(e)}"}

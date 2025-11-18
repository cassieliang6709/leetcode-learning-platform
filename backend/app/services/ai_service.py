"""
AI Service for generating learning plans, quiz questions, and code analysis
This uses simple logic for demo. Replace with actual OpenAI API calls in production.
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re


async def generate_learning_plan(test_data: Dict, score: int) -> Dict[str, Any]:
    """Generate personalized learning plan based on test results"""
    # Demo implementation - replace with actual AI API call
    weak_areas = []
    for answer in test_data.get("answers", []):
        if not answer.get("is_correct"):
            weak_areas.append(answer.get("topic"))

    recommended_points = []
    if score < 40:
        recommended_points = [1, 2, 3]  # Basic topics
    elif score < 70:
        recommended_points = [4, 5, 6]  # Intermediate topics
    else:
        recommended_points = [7, 8, 9]  # Advanced topics

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


async def generate_quiz_questions(
    knowledge_point_name: str,
    category: str
) -> List[Dict[str, Any]]:
    """Generate quiz questions for a knowledge point"""
    # Demo data - replace with actual AI generation or database
    return [
        {
            "leetcode_id": 1,
            "title": f"{knowledge_point_name} - Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "difficulty": "easy",
            "solution": "Use hash map to store complements",
            "hints": [
                {
                    "type": "strategy",
                    "content": "Think about using a hash map to store numbers you've seen. For each number, check if its complement (target - current) exists in the map."
                },
                {
                    "type": "code",
                    "content": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i"
                },
                {
                    "type": "video",
                    "content": "Watch detailed explanation"
                }
            ],
            "video_link": "https://www.youtube.com/watch?v=KLlXCFG5TnA"
        }
    ]


async def analyze_code(code: str, language: str) -> Dict[str, Any]:
    """Analyze code for errors and provide suggestions"""
    # Simple static analysis - replace with actual AI analysis
    errors = []
    suggestions = []
    has_errors = False

    # Basic syntax checks
    if language == "python":
        if "def " not in code:
            errors.append("No function definition found")
            has_errors = True
        if "return" not in code:
            suggestions.append("Consider adding a return statement")

        # Check for common mistakes
        if re.search(r'if.*==.*None', code):
            suggestions.append("Use 'if x is None' instead of 'if x == None'")

    # Generate corrected code suggestion
    corrected_code = None
    if has_errors:
        corrected_code = generate_corrected_code(code, errors, language)

    return {
        "has_errors": has_errors,
        "errors": errors,
        "suggestions": suggestions,
        "corrected_code": corrected_code,
        "complexity_analysis": "Time: O(n), Space: O(1)"
    }


async def get_hint_by_level(
    question_id: int,
    code: str,
    level: int,
    db: AsyncSession
) -> Dict[str, Any]:
    """Get hint based on level (1: strategy, 2: code, 3: video)"""
    from app.models import QuizQuestion

    result = await db.execute(select(QuizQuestion).where(QuizQuestion.id == question_id))
    question = result.scalar_one_or_none()

    if not question or not question.hints:
        return {"type": "none", "content": "No hints available"}

    hints = question.hints
    if level > len(hints):
        level = len(hints)

    hint = hints[level - 1]
    hint_data = {
        "type": hint.get("type"),
        "content": hint.get("content")
    }

    if level == 3:  # Video hint
        hint_data["video_link"] = question.video_link

    return hint_data


def generate_corrected_code(code: str, errors: List[str], language: str) -> str:
    """Generate corrected version of code based on errors"""
    # Simple demo - replace with AI
    if "No function definition found" in errors:
        return f"def solution():\n    {code}\n    return result"
    return code



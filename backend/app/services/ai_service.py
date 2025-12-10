"""
AI Service for generating learning plans, quiz questions, and code analysis.

This module provides AI-powered functionality for the LeetCode Learning Platform,
including personalized learning plan generation, quiz question generation,
code analysis, and hint retrieval. It integrates with SiliconFlow AI API
for advanced code analysis capabilities.

Author: Yue Liang
"""

import os
import re
import json
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Ensure .env is loaded
load_dotenv()


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

    weak_areas = []
    answers = test_data.get("answers", [])
    
    if not isinstance(answers, list):
        raise ValueError("test_data must contain 'answers' as a list")

    for answer in answers:
        if not isinstance(answer, dict):
            continue
        if not answer.get("is_correct", False):
            topic = answer.get("topic")
            if topic and isinstance(topic, str):
                weak_areas.append(topic)

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
    """
    Generate quiz questions for a knowledge point.

    Args:
        knowledge_point_name: Name of the knowledge point.
        category: Category of the knowledge point.

    Returns:
        List of quiz question dictionaries with structure:
            - leetcode_id: Optional LeetCode problem ID
            - title: Question title
            - description: Problem description
            - difficulty: Difficulty level
            - solution: Solution approach
            - hints: List of hints
            - video_link: Optional video explanation link

    Raises:
        ValueError: If knowledge_point_name or category is empty.
    """
    if not knowledge_point_name or not isinstance(knowledge_point_name, str):
        raise ValueError("knowledge_point_name must be a non-empty string")
    if not category or not isinstance(category, str):
        raise ValueError("category must be a non-empty string")

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
    """
    Analyze code using SiliconFlow AI API.

    Provides comprehensive code analysis including error detection,
    improvement suggestions, and complexity analysis.

    Args:
        code: Source code to analyze.
        language: Programming language (e.g., "python", "javascript").

    Returns:
        Dictionary containing:
            - has_errors: Boolean indicating if errors were found
            - errors: List of error messages
            - suggestions: List of improvement suggestions
            - corrected_code: Optional corrected/optimized code
            - complexity_analysis: Time and space complexity analysis

    Raises:
        ValueError: If code or language is empty or invalid.
    """
    if not code or not isinstance(code, str):
        raise ValueError("code must be a non-empty string")
    if not language or not isinstance(language, str):
        raise ValueError("language must be a non-empty string")

    api_key = os.getenv("SILICONFLOW_API_KEY")
    
    if not api_key:
        # Fallback to simple analysis if no API key
        return await _simple_code_analysis(code, language)
    
    try:
        # Construct prompt for AI code review
        prompt = f"""You are a professional code review expert. Please analyze the following {language} code and provide:
1. Errors in the code (if any)
2. Improvement suggestions
3. Optimized code (if needed)
4. Time and space complexity analysis

Code:
```{language}
{code}
```

Please return the result in JSON format as follows:
{{
  "has_errors": true/false,
  "errors": ["error1", "error2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "corrected_code": "optimized code (if needed)",
  "complexity_analysis": "time and space complexity analysis"
}}

Return only JSON, no other content."""

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.siliconflow.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "Qwen/Qwen2.5-7B-Instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional code review assistant, skilled at finding code issues and providing improvement suggestions."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # Parse AI response
                try:
                    # Extract JSON from response
                    json_start = ai_response.find("{")
                    json_end = ai_response.rfind("}") + 1
                    if json_start != -1 and json_end > json_start:
                        json_str = ai_response[json_start:json_end]
                        analysis = json.loads(json_str)
                        return analysis
                    else:
                        # If no JSON found, return raw response in suggestions
                        return {
                            "has_errors": False,
                            "errors": [],
                            "suggestions": [ai_response],
                            "corrected_code": None,
                            "complexity_analysis": "Please refer to suggestions"
                        }
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    return {
                        "has_errors": False,
                        "errors": [],
                        "suggestions": [ai_response],
                        "corrected_code": None,
                        "complexity_analysis": "Analyzing..."
                    }
            else:
                # API error - fallback to simple analysis
                return await _simple_code_analysis(code, language)
                
    except httpx.TimeoutException:
        return await _simple_code_analysis(code, language)
    except httpx.HTTPError as e:
        return await _simple_code_analysis(code, language)
    except Exception as e:
        # Unexpected error - fallback to simple analysis
        return await _simple_code_analysis(code, language)


async def _simple_code_analysis(
    code: str, language: str
) -> Dict[str, Any]:
    """
    Simple fallback code analysis without AI.

    Provides basic static analysis when AI API is unavailable.

    Args:
        code: Source code to analyze.
        language: Programming language.

    Returns:
        Dictionary with basic analysis results.
    """
    errors: List[str] = []
    suggestions: List[str] = []
    has_errors = False

    if not code or not isinstance(code, str):
        return {
            "has_errors": True,
            "errors": ["Invalid code input"],
            "suggestions": [],
            "corrected_code": None,
            "complexity_analysis": "N/A"
        }

    if language.lower() == "python":
        if "def " not in code and "class " not in code:
            errors.append("No function or class definition found in code")
            has_errors = True
        if "return" not in code and "def " in code:
            suggestions.append("Consider adding a return statement")
        if re.search(r'if.*==.*None', code):
            suggestions.append(
                "Consider using 'if x is None' instead of 'if x == None'"
            )
    
    return {
        "has_errors": has_errors,
        "errors": errors,
        "suggestions": suggestions if suggestions else ["Code looks good!"],
        "corrected_code": None,
        "complexity_analysis": (
            "Please use AI analysis to get detailed complexity information"
        )
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
        code: User's current code (for context, not currently used).
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
        if level > len(hints):
            level = len(hints)

        hint = hints[level - 1]
        if not isinstance(hint, dict):
            return {"type": "none", "content": "Invalid hint format"}

        hint_data = {
            "type": hint.get("type", "none"),
            "content": hint.get("content", "No content available")
        }

        if level == 3 and question.video_link:  # Video hint
            hint_data["video_link"] = question.video_link

        return hint_data
    except Exception as e:
        return {
            "type": "error",
            "content": f"Error retrieving hint: {str(e)}"
        }





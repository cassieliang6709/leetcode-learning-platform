"""
AI Service for generating learning plans, quiz questions, and code analysis
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re
import httpx
import os
import json
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()


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
    """Analyze code using SiliconFlow AI API"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    
    print(f"[DEBUG] API Key loaded: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"[DEBUG] API Key starts with: {api_key[:20]}...")
    
    if not api_key:
        print("[DEBUG] Using fallback simple analysis")
        # Fallback to simple analysis if no API key
        return await _simple_code_analysis(code, language)
    
    try:
        # Construct prompt for AI code review
        prompt = f"""你是一位专业的代码审查专家。请分析以下 {language} 代码，并提供：
1. 代码中的错误（如果有）
2. 改进建议
3. 优化后的代码（如果需要）
4. 时间和空间复杂度分析

代码：
```{language}
{code}
```

请以 JSON 格式返回结果，格式如下：
{{
  "has_errors": true/false,
  "errors": ["错误1", "错误2"],
  "suggestions": ["建议1", "建议2"],
  "corrected_code": "优化后的代码（如果需要）",
  "complexity_analysis": "时间复杂度和空间复杂度分析"
}}

只返回 JSON，不要其他内容。"""

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
                            "content": "你是一位专业的代码审查助手，擅长发现代码问题并提供改进建议。"
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
                            "complexity_analysis": "请参考建议"
                        }
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    return {
                        "has_errors": False,
                        "errors": [],
                        "suggestions": [ai_response],
                        "corrected_code": None,
                        "complexity_analysis": "分析中..."
                    }
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return await _simple_code_analysis(code, language)
                
    except Exception as e:
        print(f"Error calling AI API: {str(e)}")
        return await _simple_code_analysis(code, language)


async def _simple_code_analysis(code: str, language: str) -> Dict[str, Any]:
    """Simple fallback code analysis without AI"""
    errors = []
    suggestions = []
    has_errors = False

    if language == "python":
        if "def " not in code and "class " not in code:
            errors.append("代码中未找到函数或类定义")
            has_errors = True
        if "return" not in code and "def " in code:
            suggestions.append("考虑添加 return 语句")
        if re.search(r'if.*==.*None', code):
            suggestions.append("建议使用 'if x is None' 而不是 'if x == None'")
    
    return {
        "has_errors": has_errors,
        "errors": errors,
        "suggestions": suggestions if suggestions else ["代码看起来不错！"],
        "corrected_code": None,
        "complexity_analysis": "请使用 AI 分析获取详细的复杂度信息"
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





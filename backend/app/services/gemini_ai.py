"""
Google Gemini AI Service.

Integrates with Google Gemini API for AI-powered code suggestions,
chat functionality, and optimization recommendations.

This service provides intelligent tutoring features including:
- Failure analysis and suggestions
- Code optimization recommendations
- Interactive chat about coding problems

Author: Yue Liang
"""

import os
import json
from typing import Dict, List, Any, Optional
import aiohttp


class GeminiAI:
    """
    Google Gemini AI client for code suggestions and chat.

    Provides AI-powered features for code analysis, suggestions,
    and interactive tutoring. Falls back to basic responses if
    API key is not configured.

    Attributes:
        api_key: API key from environment variable.
        fallback_mode: Boolean indicating if fallback mode is active.
        model: AI model identifier.
        api_url: Gemini API endpoint URL.
    """

    def __init__(self) -> None:
        """
        Initialize Gemini AI client.

        Reads API key from environment variable and sets up
        fallback mode if key is not available.
        """
        self.api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.fallback_mode: bool = not bool(self.api_key)
        self.api_url: str = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key or ''}"
        )

    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Make a request to Google Gemini API.

        Accepts OpenAI-style messages (role/content) and converts them
        to Gemini format internally.

        Args:
            messages: List of message dicts with "role" and "content".
                      The first "system" role message becomes systemInstruction.
            temperature: Sampling temperature (0.0-2.0). Defaults to 0.7.
            max_tokens: Maximum tokens in response. Defaults to 2000.

        Returns:
            Dictionary containing:
                - success: Boolean indicating request success
                - content: AI response content (if successful)
                - usage: Token usage information (if successful)
                - error: Error message (if failed)
        """
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")
        if max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")

        if self.fallback_mode:
            return {
                "success": True,
                "content": (
                    "AI features are not yet configured. Please add "
                    "GEMINI_API_KEY to the backend/.env file to enable "
                    "full AI tutoring functionality."
                ),
                "usage": {}
            }

        # Split system message from conversation messages
        system_instruction = None
        contents = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                # Gemini uses systemInstruction, not a system message in contents
                system_instruction = {"parts": [{"text": content}]}
            else:
                # Map OpenAI "assistant" -> Gemini "model"
                gemini_role = "model" if role == "assistant" else "user"
                contents.append({
                    "role": gemini_role,
                    "parts": [{"text": content}]
                })

        # Gemini requires contents to start with "user" role
        # If the first item is "model", prepend an empty user message
        if contents and contents[0]["role"] == "model":
            contents.insert(0, {"role": "user", "parts": [{"text": "."}]})

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }

        if system_instruction:
            payload["system_instruction"] = system_instruction

        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=60)
                async with session.post(
                    self.api_url,
                    json=payload,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        candidates = result.get("candidates", [])
                        if not candidates:
                            return {
                                "success": False,
                                "error": "No candidates in Gemini response"
                            }
                        text = (
                            candidates[0]
                            .get("content", {})
                            .get("parts", [{}])[0]
                            .get("text", "")
                        )
                        usage_meta = result.get("usageMetadata", {})
                        return {
                            "success": True,
                            "content": text,
                            "usage": {
                                "prompt_tokens": usage_meta.get("promptTokenCount", 0),
                                "completion_tokens": usage_meta.get("candidatesTokenCount", 0),
                                "total_tokens": usage_meta.get("totalTokenCount", 0),
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"API Error {response.status}: {error_text}"
                        }
        except aiohttp.ClientError as e:
            return {"success": False, "error": f"Network error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}

    async def get_failure_suggestion(
        self,
        code: str,
        language: str,
        problem_description: str,
        test_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get AI suggestion when test cases fail.

        Args:
            code: User's code that failed tests.
            language: Programming language.
            problem_description: Problem description text.
            test_results: List of test result dictionaries.

        Returns:
            Dictionary with success, suggestion, failed_count, or error.
        """
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not problem_description or not isinstance(problem_description, str):
            raise ValueError("problem_description must be a non-empty string")
        if not isinstance(test_results, list):
            raise ValueError("test_results must be a list")

        failed_tests = [
            t for t in test_results
            if isinstance(t, dict) and not t.get("passed", False)
        ]

        failed_info = "\n".join([
            f"Test Case {t['test_case_id']}:\n"
            f"  Input: {t['input']}\n"
            f"  Expected: {t['expected']}\n"
            f"  Your Output: {t['actual']}\n"
            f"  Error: {t.get('error', 'Wrong output')}"
            for t in failed_tests[:3]
        ])

        prompt = f"""A student's code failed some test cases. Help them fix it.

**Problem:**
{problem_description}

**Code ({language}):**
```{language}
{code}
```

**Failed Tests:**
{failed_info}

Provide a brief analysis:
1. **Issue**: What's wrong? (1-2 sentences)
2. **Hint**: How to fix it? (don't give full solution)
3. **Edge cases**: What to consider?

Be concise and encouraging. Use markdown formatting."""

        messages = [
            {
                "role": "system",
                "content": "You are a concise programming tutor. Give brief, focused feedback using markdown. No excessive spacing."
            },
            {"role": "user", "content": prompt}
        ]

        result = await self._make_request(messages, temperature=0.7)

        if result["success"]:
            return {
                "success": True,
                "suggestion": result["content"],
                "failed_count": len(failed_tests)
            }
        return {"success": False, "error": result["error"]}

    async def chat_about_code(
        self,
        user_message: str,
        code: str,
        language: str,
        problem_description: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        rag_context: str = ""
    ) -> Dict[str, Any]:
        """
        Chat with AI about the code problem.

        Args:
            user_message: User's question or message.
            code: Current code being discussed.
            language: Programming language.
            problem_description: Problem description text.
            chat_history: Optional list of previous chat messages.
            rag_context: Optional RAG course material context.

        Returns:
            Dictionary with success, response, usage, or error.
        """
        if not user_message or not isinstance(user_message, str):
            raise ValueError("user_message must be a non-empty string")
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not problem_description or not isinstance(problem_description, str):
            raise ValueError("problem_description must be a non-empty string")

        context = f"""**Problem:**
{problem_description}

**Current Code ({language}):**
```{language}
{code}
```"""

        rag_section = f"\n\n{rag_context}" if rag_context else ""
        system_prompt = (
            f"You are a concise and helpful programming tutor for AlgoMentor. "
            f"Help students understand coding problems, debug issues, and improve solutions."
            f"{rag_section}"
            f"\n\n**Response guidelines:**"
            f"\n- Be brief and to the point - no unnecessary explanations"
            f"\n- Use markdown formatting (headings, lists, bold, etc.)"
            f"\n- Code blocks MUST use proper markdown: ```python or ```javascript etc."
            f"\n- Use bullet points for multiple points"
            f"\n- Maximum 2-3 short paragraphs unless asked for detail"
            f"\n- Avoid excessive blank lines between paragraphs"
            f"\n- Be encouraging but concise"
            + ("\n- Reference the course materials above when relevant" if rag_context else "")
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}"}
        ]

        if chat_history:
            messages.extend(chat_history[-10:])

        messages.append({"role": "user", "content": user_message})

        result = await self._make_request(messages, temperature=0.8)

        if result["success"]:
            return {
                "success": True,
                "response": result["content"],
                "usage": result.get("usage", {})
            }
        return {"success": False, "error": result["error"]}

    async def get_dynamic_hint(
        self,
        code: str,
        language: str,
        problem_description: str,
        hint_level: int,
        test_results: Optional[List[Dict[str, Any]]] = None,
        rag_context: str = ""
    ) -> Dict[str, Any]:
        """
        Generate a dynamic, AI-powered hint for a coding problem.

        Args:
            code: User's current code.
            language: Programming language.
            problem_description: Problem description text.
            hint_level: 1=Socratic question, 2=Direction hint, 3=Pseudocode.
            test_results: Optional list of test results (for context).
            rag_context: Optional RAG course material context.

        Returns:
            Dictionary with success, hint, or error.
        """
        if not isinstance(hint_level, int) or hint_level not in (1, 2, 3):
            raise ValueError("hint_level must be 1, 2, or 3")

        test_context = ""
        if test_results:
            failed = [t for t in test_results if not t.get("passed", False)]
            if failed:
                lines = [f"- Input: {t['input']} | Expected: {t['expected']} | Got: {t.get('actual','')}"
                         for t in failed[:2]]
                test_context = "**Failing test cases:**\n" + "\n".join(lines)

        rag_section = f"\n\n**Relevant course material:**\n{rag_context}" if rag_context else ""

        if hint_level == 1:
            level_instruction = (
                "Ask the student ONE short Socratic question to guide their thinking. "
                "Do NOT name the algorithm or give any solution. "
                "The question should make them realize what they're missing. "
                "Max 2 sentences."
            )
        elif hint_level == 2:
            level_instruction = (
                "Tell the student: (1) the algorithm/pattern name to use, "
                "(2) the high-level approach in 2-3 bullet points. "
                "Do NOT write any code. Keep it under 100 words."
            )
        else:
            level_instruction = (
                "Write pseudocode for the solution. "
                "Use TODO comments to mark the key steps the student needs to fill in. "
                "Include a brief complexity note at the end."
            )

        prompt = f"""You are an expert coding tutor giving a Level {hint_level} hint.

**Problem:**
{problem_description}

**Student's current code ({language}):**
```{language}
{code}
```
{test_context}{rag_section}

**Your task:** {level_instruction}"""

        system_prompt = (
            "You are a concise and Socratic programming tutor. "
            "Never give away full solutions. Guide students to discover answers themselves. "
            "Use markdown formatting."
            + ("\n\nReference the course material above when relevant." if rag_context else "")
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        result = await self._make_request(messages, temperature=0.7, max_tokens=600)
        if result["success"]:
            return {"success": True, "hint": result["content"]}
        return {"success": False, "error": result["error"]}

    async def get_optimization_suggestions(
        self,
        code: str,
        language: str,
        problem_description: str
    ) -> Dict[str, Any]:
        """
        Get optimization suggestions for working code.

        Args:
            code: User's working code that passes tests.
            language: Programming language.
            problem_description: Problem description text.

        Returns:
            Dictionary with success, suggestions, or error.
        """
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not problem_description or not isinstance(problem_description, str):
            raise ValueError("problem_description must be a non-empty string")

        prompt = f"""You are an expert code reviewer. A student has solved a coding problem successfully. Help them optimize their solution.

**Problem:**
{problem_description}

**Student's Code ({language}):**
```{language}
{code}
```

Please provide:
1. **Time Complexity Analysis**: Current time and space complexity
2. **Optimization Opportunities**: How can this be improved?
3. **Best Practices**: Code quality improvements
4. **Alternative Approaches**: Other ways to solve this problem

Be specific and educational."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert code reviewer who helps students write better, more efficient code."
            },
            {"role": "user", "content": prompt}
        ]

        result = await self._make_request(messages, temperature=0.7)

        if result["success"]:
            return {"success": True, "suggestions": result["content"]}
        return {"success": False, "error": result["error"]}


# Singleton instance
_ai_service = None


def get_ai_service() -> GeminiAI:
    """
    Get or create Gemini AI service instance (singleton).

    Returns:
        Global GeminiAI instance.
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = GeminiAI()
    return _ai_service

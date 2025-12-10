"""
SiliconFlow AI Service.

Integrates with SiliconFlow API for AI-powered code suggestions,
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


class SiliconFlowAI:
    """
    SiliconFlow AI client for code suggestions and chat.

    Provides AI-powered features for code analysis, suggestions,
    and interactive tutoring. Falls back to basic responses if
    API key is not configured.

    Attributes:
        api_url: SiliconFlow API endpoint URL.
        api_key: API key from environment variable.
        fallback_mode: Boolean indicating if fallback mode is active.
        model: AI model identifier.
        headers: HTTP headers for API requests.
    """
    
    def __init__(self) -> None:
        """
        Initialize SiliconFlow AI client.

        Reads API key from environment variable and sets up
        fallback mode if key is not available.
        """
        self.api_url: str = "https://api.siliconflow.cn/v1/chat/completions"
        self.api_key: Optional[str] = os.getenv("SILICONFLOW_API_KEY")
        
        # Make API key optional - will use fallback mode if not set
        if not self.api_key:
            self.fallback_mode: bool = True
        else:
            self.fallback_mode: bool = False
        
        self.model: str = "Qwen/Qwen3-30B-A3B-Instruct-2507"
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key or ''}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Make a request to SiliconFlow API.

        Args:
            messages: List of message dictionaries with "role" and "content".
            temperature: Sampling temperature (0.0-1.0). Defaults to 0.7.
            max_tokens: Maximum tokens in response. Defaults to 2000.

        Returns:
            Dictionary containing:
                - success: Boolean indicating request success
                - content: AI response content (if successful)
                - usage: Token usage information (if successful)
                - error: Error message (if failed)

        Raises:
            ValueError: If messages is empty or invalid.
        """
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")
        if max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")

        # Use fallback if API key not configured
        if self.fallback_mode:
            return {
                "success": True,
                "content": (
                    "AI features are not yet configured. Please add "
                    "SILICONFLOW_API_KEY to the backend/.env file to enable "
                    "full AI tutoring functionality"
                ),
                "usage": {}
            }

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=60)
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "choices" not in result or len(result["choices"]) == 0:
                            return {
                                "success": False,
                                "error": "Invalid API response format"
                            }
                        return {
                            "success": True,
                            "content": result["choices"][0]["message"]["content"],
                            "usage": result.get("usage", {})
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"API Error {response.status}: {error_text}"
                        }
        except aiohttp.ClientError as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Invalid JSON response: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    async def get_failure_suggestion(
        self,
        code: str,
        language: str,
        problem_description: str,
        test_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get AI suggestion when test cases fail.

        Analyzes failed test cases and provides targeted feedback
        to help users fix their code.

        Args:
            code: User's code that failed tests.
            language: Programming language.
            problem_description: Problem description text.
            test_results: List of test result dictionaries with keys:
                - passed: Boolean indicating if test passed
                - test_case_id: Test case identifier
                - input: Test input
                - expected: Expected output
                - actual: Actual output
                - error: Error message (if any)

        Returns:
            Dictionary containing:
                - success: Boolean indicating if suggestion was generated
                - suggestion: AI-generated suggestion text
                - failed_count: Number of failed test cases
                - error: Error message (if request failed)

        Raises:
            ValueError: If any required parameter is invalid.
        """
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not problem_description or not isinstance(problem_description, str):
            raise ValueError("problem_description must be a non-empty string")
        if not isinstance(test_results, list):
            raise ValueError("test_results must be a list")

        # Format failed test cases
        failed_tests = [
            test for test in test_results 
            if isinstance(test, dict) and not test.get("passed", False)
        ]
        
        failed_info = "\n".join([
            f"Test Case {test['test_case_id']}:\n"
            f"  Input: {test['input']}\n"
            f"  Expected: {test['expected']}\n"
            f"  Your Output: {test['actual']}\n"
            f"  Error: {test.get('error', 'Wrong output')}"
            for test in failed_tests[:3]  # Limit to first 3 failed tests
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
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        result = await self._make_request(messages, temperature=0.7)
        
        if result["success"]:
            return {
                "success": True,
                "suggestion": result["content"],
                "failed_count": len(failed_tests)
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    async def chat_about_code(
        self,
        user_message: str,
        code: str,
        language: str,
        problem_description: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Chat with AI about the code problem.

        Provides interactive conversation about coding problems with
        context awareness from chat history.

        Args:
            user_message: User's question or message.
            code: Current code being discussed.
            language: Programming language.
            problem_description: Problem description text.
            chat_history: Optional list of previous chat messages.
                Each message should have "role" and "content" keys.

        Returns:
            Dictionary containing:
                - success: Boolean indicating if chat was successful
                - response: AI response text
                - usage: Token usage information
                - error: Error message (if request failed)

        Raises:
            ValueError: If any required parameter is invalid.
        """
        if not user_message or not isinstance(user_message, str):
            raise ValueError("user_message must be a non-empty string")
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not problem_description or not isinstance(problem_description, str):
            raise ValueError("problem_description must be a non-empty string")
        # Build context
        context = f"""**Problem:**
{problem_description}

**Current Code ({language}):**
```{language}
{code}
```"""
        
        # Build messages
        messages = [
            {
                "role": "system",
                "content": """You are a concise and helpful programming tutor. Help students understand coding problems, debug issues, and improve solutions.

**Response guidelines:**
- Be brief and to the point - no unnecessary explanations
- Use markdown formatting (headings, lists, bold, etc.)
- Code blocks MUST use proper markdown: ```python or ```javascript etc.
- Use bullet points for multiple points
- Maximum 2-3 short paragraphs unless asked for detail
- Avoid excessive blank lines between paragraphs
- Be encouraging but concise"""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}"
            }
        ]
        
        # Add chat history
        if chat_history:
            messages.extend(chat_history[-10:])  # Keep last 10 messages
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        result = await self._make_request(messages, temperature=0.8)
        
        if result["success"]:
            return {
                "success": True,
                "response": result["content"],
                "usage": result.get("usage", {})
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    async def get_optimization_suggestions(
        self,
        code: str,
        language: str,
        problem_description: str
    ) -> Dict[str, Any]:
        """
        Get optimization suggestions for working code.

        Analyzes successfully working code and provides suggestions
        for improvement including complexity analysis and best practices.

        Args:
            code: User's working code that passes tests.
            language: Programming language.
            problem_description: Problem description text.

        Returns:
            Dictionary containing:
                - success: Boolean indicating if suggestions were generated
                - suggestions: AI-generated optimization suggestions
                - error: Error message (if request failed)

        Raises:
            ValueError: If any required parameter is invalid.
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
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        result = await self._make_request(messages, temperature=0.7)
        
        if result["success"]:
            return {
                "success": True,
                "suggestions": result["content"]
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }


# Singleton instance
_ai_service = None


def get_ai_service() -> SiliconFlowAI:
    """
    Get or create AI service instance.

    Uses singleton pattern to ensure only one AI service instance
    is created and reused across the application.

    Returns:
        Global SiliconFlowAI instance.
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = SiliconFlowAI()
    return _ai_service


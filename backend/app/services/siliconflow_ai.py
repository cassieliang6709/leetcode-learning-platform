"""
SiliconFlow AI Service
Integrates with SiliconFlow API for AI suggestions and chat
"""
import aiohttp
import json
from typing import Dict, List, Any, Optional


class SiliconFlowAI:
    """SiliconFlow AI client for code suggestions and chat"""
    
    def __init__(self):
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.api_key = "sk-ywiqoiuhlfyfsknsjsdmyvdllhwxsajvvafmszzbarckwzdv"
        self.model = "Qwen/Qwen3-30B-A3B-Instruct-2507"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Make a request to SiliconFlow API"""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
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
        Get AI suggestion when test cases fail
        
        Args:
            code: User's code
            language: Programming language
            problem_description: Problem description
            test_results: Failed test case results
            
        Returns:
            AI suggestion with analysis and hints
        """
        # Format failed test cases
        failed_tests = [
            test for test in test_results 
            if not test.get("passed", False)
        ]
        
        failed_info = "\n".join([
            f"Test Case {test['test_case_id']}:\n"
            f"  Input: {test['input']}\n"
            f"  Expected: {test['expected']}\n"
            f"  Your Output: {test['actual']}\n"
            f"  Error: {test.get('error', 'Wrong output')}"
            for test in failed_tests[:3]  # Limit to first 3 failed tests
        ])
        
        prompt = f"""You are an expert programming tutor. A student is solving a coding problem and their solution failed some test cases.

**Problem Description:**
{problem_description}

**Student's Code ({language}):**
```{language}
{code}
```

**Failed Test Cases:**
{failed_info}

Please provide:
1. **Root Cause Analysis**: What's wrong with the code?
2. **Key Insights**: What concept or logic is missing?
3. **Hints** (without giving away the solution): Guide them to fix it
4. **Edge Cases**: What scenarios should they consider?

Keep your response concise, educational, and encouraging. Focus on helping them learn, not just fixing the code."""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful programming tutor who guides students to understand and fix their code mistakes."
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
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Chat with AI about the code problem
        
        Args:
            user_message: User's question
            code: Current code
            language: Programming language
            problem_description: Problem description
            chat_history: Previous chat messages
            
        Returns:
            AI response
        """
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
                "content": "You are a helpful programming tutor. Help students understand coding problems, debug issues, and improve their solutions. Be encouraging and educational."
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
        Get optimization suggestions for working code
        
        Args:
            code: User's working code
            language: Programming language
            problem_description: Problem description
            
        Returns:
            Optimization suggestions
        """
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
    """Get or create AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = SiliconFlowAI()
    return _ai_service


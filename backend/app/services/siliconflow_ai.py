"""
SiliconFlow AI Service
Integrates with SiliconFlow API for AI suggestions and chat
"""
import os
import aiohttp
import json
from typing import Dict, List, Any, Optional


class SiliconFlowAI:
    """SiliconFlow AI client for code suggestions and chat"""
    
    def __init__(self):
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        # Read API key from environment variable for security
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        
        # Make API key optional - will use fallback mode if not set
        if not self.api_key:
            print("[WARNING] SILICONFLOW_API_KEY not set. AI features will use fallback mode.")
            print("[INFO] To enable AI features, add SILICONFLOW_API_KEY to backend/.env file")
            self.fallback_mode = True
        else:
            self.fallback_mode = False
        
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
        # Use fallback if API key not configured
        if self.fallback_mode:
            return {
                "success": True,
                "content": "AI 功能暂未配置。请在 backend/.env 文件中添加 SILICONFLOW_API_KEY 以启用完整的 AI 辅导功能。\n\n当前您可以继续使用其他功能，如：\n- 查看题目描述和测试用例\n- 运行代码并查看测试结果\n- 查看参考答案和题解",
                "usage": {}
            }
        
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


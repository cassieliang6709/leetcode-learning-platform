"""
Code Execution Service using Piston API
Safely executes user code in isolated sandboxes
"""
import httpx
from typing import Dict, List, Any, Optional
import asyncio


class PistonExecutor:
    """
    Piston API client for executing code in multiple languages
    Official API: https://github.com/engineer-man/piston
    """
    
    BASE_URL = "https://emkc.org/api/v2/piston"
    
    # Language runtime mappings
    LANGUAGE_MAP = {
        "python": "python",
        "javascript": "javascript",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "go": "go",
        "rust": "rust",
        "typescript": "typescript",
        "php": "php",
        "ruby": "ruby",
        "swift": "swift",
        "kotlin": "kotlin",
    }
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def execute_code(
        self,
        code: str,
        language: str,
        stdin: str = "",
        args: List[str] = None
    ) -> Dict[str, Any]:
        """
        Execute code using Piston API
        
        Args:
            code: Source code to execute
            language: Programming language
            stdin: Standard input for the program
            args: Command line arguments
            
        Returns:
            Execution result with output, errors, and stats
        """
        runtime = self.LANGUAGE_MAP.get(language.lower())
        if not runtime:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "output": "",
                "compile_output": "",
                "run_time": 0,
                "memory": 0
            }
        
        payload = {
            "language": runtime,
            "version": "*",  # Use latest version
            "files": [
                {
                    "name": self._get_filename(language),
                    "content": code
                }
            ],
            "stdin": stdin,
            "args": args or [],
            "compile_timeout": 10000,  # 10 seconds
            "run_timeout": 5000,       # 5 seconds
            "compile_memory_limit": -1,
            "run_memory_limit": -1
        }
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/execute",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            return self._parse_result(result)
            
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Execution timeout (5 seconds limit)",
                "output": "",
                "compile_output": "",
                "run_time": 5000,
                "memory": 0
            }
        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"API error: {str(e)}",
                "output": "",
                "compile_output": "",
                "run_time": 0,
                "memory": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "output": "",
                "compile_output": "",
                "run_time": 0,
                "memory": 0
            }
    
    async def run_test_cases(
        self,
        code: str,
        language: str,
        test_cases: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Run multiple test cases against the code
        
        Args:
            code: Source code to test
            language: Programming language
            test_cases: List of test cases with input and expected output
            
        Returns:
            List of test results
        """
        results = []
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected = str(test_case.get("expected", "")).strip()
            
            # Execute code with test input
            result = await self.execute_code(
                code=code,
                language=language,
                stdin=input_data
            )
            
            actual = result.get("output", "").strip()
            
            # Compare output
            passed = actual == expected and result.get("success", False)
            
            results.append({
                "test_case_id": i + 1,
                "input": input_data,
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "error": result.get("error"),
                "run_time": result.get("run_time", 0),
                "memory": result.get("memory", 0)
            })
        
        return results
    
    def _parse_result(self, result: Dict) -> Dict[str, Any]:
        """Parse Piston API response"""
        run_result = result.get("run", {})
        compile_result = result.get("compile", {})
        
        stdout = run_result.get("stdout", "")
        stderr = run_result.get("stderr", "")
        compile_output = compile_result.get("output", "") if compile_result else ""
        
        # Check for compilation errors
        if compile_result and compile_result.get("code", 0) != 0:
            return {
                "success": False,
                "error": "Compilation failed",
                "output": stdout,
                "compile_output": compile_output,
                "run_time": 0,
                "memory": 0
            }
        
        # Check for runtime errors
        if run_result.get("code", 0) != 0:
            return {
                "success": False,
                "error": stderr or "Runtime error",
                "output": stdout,
                "compile_output": compile_output,
                "run_time": 0,
                "memory": 0
            }
        
        return {
            "success": True,
            "error": None,
            "output": stdout,
            "compile_output": compile_output,
            "run_time": 0,  # Piston doesn't provide detailed timing
            "memory": 0     # Piston doesn't provide memory stats
        }
    
    def _get_filename(self, language: str) -> str:
        """Get appropriate filename for the language"""
        extensions = {
            "python": "main.py",
            "javascript": "main.js",
            "typescript": "main.ts",
            "java": "Main.java",
            "cpp": "main.cpp",
            "c": "main.c",
            "go": "main.go",
            "rust": "main.rs",
            "php": "main.php",
            "ruby": "main.rb",
            "swift": "main.swift",
            "kotlin": "main.kt"
        }
        return extensions.get(language.lower(), "main.txt")
    
    async def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages from Piston"""
        try:
            response = await self.client.get(f"{self.BASE_URL}/runtimes")
            response.raise_for_status()
            runtimes = response.json()
            
            # Filter to languages we support
            supported = []
            for runtime in runtimes:
                lang = runtime.get("language")
                if lang in self.LANGUAGE_MAP.values():
                    supported.append({
                        "language": lang,
                        "version": runtime.get("version"),
                        "aliases": runtime.get("aliases", [])
                    })
            
            return supported
        except Exception as e:
            print(f"Error fetching runtimes: {e}")
            return []
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global executor instance
_executor = None


def get_executor() -> PistonExecutor:
    """Get or create the global executor instance"""
    global _executor
    if _executor is None:
        _executor = PistonExecutor()
    return _executor


async def execute_user_code(
    code: str,
    language: str,
    test_cases: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    High-level function to execute user code with optional test cases
    
    Args:
        code: Source code
        language: Programming language
        test_cases: Optional list of test cases
        
    Returns:
        Execution results
    """
    executor = get_executor()
    
    if test_cases:
        # Run with test cases
        results = await executor.run_test_cases(code, language, test_cases)
        
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        
        return {
            "mode": "test",
            "test_results": results,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": (passed / total * 100) if total > 0 else 0
            }
        }
    else:
        # Simple execution
        result = await executor.execute_code(code, language)
        return {
            "mode": "run",
            "result": result
        }


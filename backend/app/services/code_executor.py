"""
Code Execution Service using Piston API.

This module provides safe code execution in isolated sandboxes using
the Piston API. It supports multiple programming languages and includes
test case execution capabilities.

The service handles code preprocessing, execution, and result parsing
with comprehensive error handling and timeout management.

Author: Yue Liang
"""

import os
from typing import Dict, List, Any, Optional
import httpx


class PistonExecutor:
    """
    Piston API client for executing code in multiple languages.

    Provides safe code execution in isolated Docker sandboxes with support
    for multiple programming languages. Handles code preprocessing,
    execution, and result parsing.

    By default, connects to the self-hosted Piston instance defined by
    PISTON_URL environment variable. Falls back to the public Piston API
    when PISTON_URL is not set (for Railway/cloud deployment without Docker).

    Official API: https://github.com/engineer-man/piston

    Attributes:
        BASE_URL: Base URL for Piston API (from PISTON_URL env var).
        LANGUAGE_MAP: Mapping of language names to runtime identifiers.
        client: HTTP client for API requests.
    """

    # PISTON_URL: self-hosted e.g. http://piston:2000/api/v2 (Docker) or http://localhost:2000/api/v2
    # Public API (emkc.org) requires PISTON_API_KEY as of Feb 2026 — get token from https://discord.gg/engineerman
    BASE_URL: str = os.getenv(
        "PISTON_URL", "https://emkc.org/api/v2/piston"
    )
    PISTON_API_KEY: str = os.getenv("PISTON_API_KEY", "")
    
    # Language runtime mappings (Piston runtime names)
    # Self-hosted: js=javascript, cpp=c++, c=c
    LANGUAGE_MAP: Dict[str, str] = {
        "python": "python",
        "javascript": "javascript",
        "java": "java",
        "cpp": "c++",
        "c": "c",
        "go": "go",
        "rust": "rust",
        "typescript": "typescript",
        "php": "php",
        "ruby": "ruby",
        "swift": "swift",
        "kotlin": "kotlin",
    }
    
    def __init__(self) -> None:
        """
        Initialize PistonExecutor with HTTP client.

        Creates an async HTTP client with 30-second timeout for
        API requests.
        """
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def execute_code(
        self,
        code: str,
        language: str,
        stdin: str = "",
        args: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute code using Piston API.

        Args:
            code: Source code to execute.
            language: Programming language (e.g., "python", "javascript").
            stdin: Standard input for the program. Defaults to empty string.
            args: Command line arguments. Defaults to None.

        Returns:
            Dictionary containing:
                - success: Boolean indicating execution success
                - error: Error message if execution failed
                - output: Program output
                - compile_output: Compilation output (if applicable)
                - run_time: Execution time in milliseconds
                - memory: Memory usage (not provided by Piston)

        Raises:
            ValueError: If code or language is empty or invalid.
        """
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")

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
        
        # Preprocess code to add necessary imports (especially for Python)
        code = self._preprocess_code(code, language)
        
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
            "compile_timeout": 3000,            # 3 seconds (self-hosted Piston limit)
            "run_timeout": 3000,                # 3 seconds (self-hosted Piston limit)
            "compile_memory_limit": 268435456,  # 256MB
            "run_memory_limit": 134217728       # 128MB
        }
        
        headers = {}
        if "emkc.org" in self.BASE_URL and self.PISTON_API_KEY:
            headers["Authorization"] = f"Bearer {self.PISTON_API_KEY}"
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/execute",
                json=payload,
                headers=headers or None
            )
            if response.status_code == 401:
                return {
                    "success": False,
                    "error": "Piston 公共 API 需要授权。请在 backend/.env 中设置 PISTON_API_KEY（向 https://discord.gg/engineerman 申请），或自建 Piston 并设置 PISTON_URL（如 http://localhost:2000/api/v2）。",
                    "output": "",
                    "compile_output": "",
                    "run_time": 0,
                    "memory": 0
                }
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
        Run multiple test cases against the code.

        Executes code with each test case and compares output
        with expected results.

        Args:
            code: Source code to test.
            language: Programming language.
            test_cases: List of test case dictionaries with keys:
                - input: Test input data
                - expected: Expected output

        Returns:
            List of test result dictionaries containing:
                - test_case_id: Test case number
                - input: Test input
                - expected: Expected output
                - actual: Actual output
                - passed: Boolean indicating if test passed
                - error: Error message if execution failed
                - run_time: Execution time
                - memory: Memory usage

        Raises:
            ValueError: If code, language, or test_cases is invalid.
        """
        if not code or not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("language must be a non-empty string")
        if not isinstance(test_cases, list):
            raise ValueError("test_cases must be a list")

        results: List[Dict[str, Any]] = []
        
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
    
    def _preprocess_code(self, code: str, language: str) -> str:
        """
        Preprocess code to add necessary imports and setup.

        Especially important for LeetCode-style Python code with type hints.
        Adds common typing imports if not already present.

        Args:
            code: Source code to preprocess.
            language: Programming language.

        Returns:
            Preprocessed code with necessary imports added.
        """
        if not code or not isinstance(code, str):
            return code

        language = language.lower()
        
        if language == "python":
            # Check if typing imports are already present
            has_typing_import = "from typing import" in code or "import typing" in code
            
            if not has_typing_import:
                # Add common typing imports for LeetCode-style problems
                typing_imports = "from typing import List, Dict, Optional, Set, Tuple, Any\n\n"
                code = typing_imports + code
        
        return code
    
    def _parse_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Piston API response into standardized format.

        Args:
            result: Raw response from Piston API.

        Returns:
            Standardized result dictionary with success status,
            output, errors, and execution metadata.
        """
        if not isinstance(result, dict):
            return {
                "success": False,
                "error": "Invalid API response format",
                "output": "",
                "compile_output": "",
                "run_time": 0,
                "memory": 0
            }

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
            "error": "",  # Empty string instead of None
            "output": stdout,
            "compile_output": compile_output,
            "run_time": 0,  # Piston doesn't provide detailed timing
            "memory": 0     # Piston doesn't provide memory stats
        }
    
    def _get_filename(self, language: str) -> str:
        """
        Get appropriate filename for the language.

        Args:
            language: Programming language name.

        Returns:
            Filename with appropriate extension for the language.
        """
        if not language or not isinstance(language, str):
            return "main.txt"

        extensions: Dict[str, str] = {
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
            "kotlin": "Main.kt"
        }
        return extensions.get(language.lower(), "main.txt")
    
    async def get_supported_languages(self) -> List[Dict[str, Any]]:
        """
        Get list of supported languages from Piston API.

        Returns:
            List of language dictionaries containing:
                - language: Language name
                - version: Runtime version
                - aliases: List of language aliases

        Note:
            Returns empty list if API request fails.
        """
        headers = {}
        if "emkc.org" in self.BASE_URL and self.PISTON_API_KEY:
            headers["Authorization"] = f"Bearer {self.PISTON_API_KEY}"
        try:
            response = await self.client.get(f"{self.BASE_URL}/runtimes", headers=headers or None)
            if response.status_code == 401:
                return []
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
    
    async def close(self) -> None:
        """
        Close the HTTP client.

        Should be called when the executor is no longer needed
        to properly clean up resources.
        """
        await self.client.aclose()


# Global executor instance
_executor = None


def get_executor() -> PistonExecutor:
    """
    Get or create the global executor instance.

    Uses singleton pattern to ensure only one executor instance
    is created and reused across the application.

    Returns:
        Global PistonExecutor instance.
    """
    global _executor
    if _executor is None:
        _executor = PistonExecutor()
    return _executor


async def execute_user_code(
    code: str,
    language: str,
    test_cases: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    High-level function to execute user code with optional test cases.

    Provides a convenient interface for code execution that handles
    both simple execution and test case validation.

    Args:
        code: Source code to execute.
        language: Programming language.
        test_cases: Optional list of test cases. If provided, runs
            in test mode. If None, runs in simple execution mode.

    Returns:
        Dictionary containing execution results:
            - mode: "test" or "run"
            - test_results: List of test results (if test mode)
            - summary: Test summary with pass/fail counts (if test mode)
            - result: Execution result (if run mode)

    Raises:
        ValueError: If code or language is invalid.
    """
    if not code or not isinstance(code, str):
        raise ValueError("code must be a non-empty string")
    if not language or not isinstance(language, str):
        raise ValueError("language must be a non-empty string")
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


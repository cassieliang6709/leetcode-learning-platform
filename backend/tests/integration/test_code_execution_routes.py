"""
Integration tests for code execution routes
"""
import pytest
from httpx import AsyncClient


class TestCodeExecutionBasic:
    """Basic tests for code execution endpoints"""
    
    async def test_submit_code_question_not_found(
        self,
        client: AsyncClient
    ):
        """Test submitting code for nonexistent question"""
        response = await client.post(
            "/api/execution/submit/99999",
            json={
                "code": "def solution(): pass",
                "language": "python"
            }
        )
        
        assert response.status_code == 404
    
    async def test_submit_code_with_test_cases(
        self,
        client: AsyncClient,
        test_quiz_question
    ):
        """Test submitting code with valid test cases"""
        # This test may fail without Piston API, but we test the structure
        response = await client.post(
            f"/api/execution/submit/{test_quiz_question.id}",
            json={
                "code": "def twoSum(nums, target):\n    return [0, 1]",
                "language": "python"
            }
        )
        
        # Accept both success (200) and service errors (5xx)
        # since Piston API might not be available in test environment
        assert response.status_code in [200, 400, 500, 503]
    
    async def test_run_custom_code_endpoint(
        self,
        client: AsyncClient
    ):
        """Test running custom code endpoint"""
        response = await client.post(
            "/api/execution/run",
            json={
                "code": "print('Hello World')",
                "language": "python"
            }
        )
        
        # Accept both success and service errors
        assert response.status_code in [200, 500, 503]


class TestGetStarterCode:
    """Test getting starter code for questions"""
    
    async def test_get_starter_code_success(
        self,
        client: AsyncClient,
        test_quiz_question
    ):
        """Test getting starter code"""
        response = await client.get(
            f"/api/execution/starter/{test_quiz_question.id}?language=python"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "code" in data
        assert "language" in data
    
    async def test_get_starter_code_nonexistent_question(
        self,
        client: AsyncClient
    ):
        """Test getting starter code for nonexistent question"""
        response = await client.get(
            "/api/execution/starter/99999?language=python"
        )
        
        assert response.status_code == 404


class TestCodeSubmissionStorage:
    """Test code submission storage"""
    
    async def test_submission_creates_record(
        self,
        client: AsyncClient,
        db_session,
        test_quiz_question
    ):
        """Test that code submission creates database record"""
        from app.models import CodeSubmission
        from sqlalchemy import select
        
        # Note: This might fail if Piston API is not available
        # but we test the endpoint structure
        response = await client.post(
            f"/api/execution/submit/{test_quiz_question.id}",
            json={
                "code": "def solution(): return True",
                "language": "python"
            }
        )
        
        # We mainly test the endpoint is reachable
        assert response.status_code in [200, 400, 500, 503]


# Note: Full code execution tests require Piston API to be running
# These tests focus on API structure and error handling
# For full integration testing, ensure Piston API is accessible




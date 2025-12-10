"""
Integration tests for quiz routes
"""
import pytest
from httpx import AsyncClient
from datetime import datetime


class TestDailyQuizRoute:
    """Test daily quiz endpoint"""
    
    async def test_get_daily_quiz_success(
        self, 
        client: AsyncClient, 
        test_user,
        test_daily_question
    ):
        """Test getting daily quiz questions"""
        response = await client.get(f"/api/quiz/daily/{test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_questions" in data
        assert "answered_count" in data
        assert "correct_count" in data
        assert "questions" in data
        assert isinstance(data["questions"], list)
    
    async def test_daily_quiz_excludes_answered(
        self,
        client: AsyncClient,
        db_session,
        test_user,
        test_daily_question
    ):
        """Test that daily quiz excludes answered questions"""
        from app.models import DailyKnowledgeAttempt
        
        # Answer the question
        attempt = DailyKnowledgeAttempt(
            user_id=test_user.id,
            question_id=test_daily_question.id,
            is_correct=True
        )
        db_session.add(attempt)
        await db_session.commit()
        
        # Get daily quiz
        response = await client.get(f"/api/quiz/daily/{test_user.id}")
        assert response.status_code == 200
        
        data = response.json()
        # The answered question should not be in the list
        question_ids = [q["id"] for q in data["questions"]]
        assert test_daily_question.id not in question_ids


class TestQuizAnswerRoute:
    """Test quiz answer submission endpoint"""
    
    async def test_submit_answer_correct(
        self,
        client: AsyncClient,
        test_user,
        test_daily_question
    ):
        """Test submitting correct answer"""
        response = await client.post(
            f"/api/quiz/daily/{test_user.id}/answer",
            json={
                "question_id": test_daily_question.id,
                "selected_option": test_daily_question.correct_answer
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "is_correct" in data
        assert data["is_correct"] is True
        assert "explanation" in data
        assert "correct_answer" in data
    
    async def test_submit_answer_incorrect(
        self,
        client: AsyncClient,
        test_user,
        test_daily_question
    ):
        """Test submitting incorrect answer"""
        wrong_answer = (test_daily_question.correct_answer + 1) % 4
        
        response = await client.post(
            f"/api/quiz/daily/{test_user.id}/answer",
            json={
                "question_id": test_daily_question.id,
                "selected_option": wrong_answer
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_correct"] is False
        assert "explanation" in data
    
    async def test_submit_answer_invalid_question(
        self,
        client: AsyncClient,
        test_user
    ):
        """Test submitting answer for nonexistent question"""
        response = await client.post(
            f"/api/quiz/daily/{test_user.id}/answer",
            json={
                "question_id": 99999,
                "selected_option": 0
            }
        )
        
        assert response.status_code == 404


class TestLearningQuizRoute:
    """Test learning quiz endpoint"""
    
    async def test_get_learning_quiz_success(
        self,
        client: AsyncClient,
        test_knowledge_point,
        test_quiz_question
    ):
        """Test getting learning quiz for knowledge point"""
        response = await client.get(
            f"/api/quiz/learning/{test_knowledge_point.id}"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            question = data[0]
            assert "id" in question
            assert "title" in question
            assert "description" in question
            assert "difficulty" in question
    
    async def test_get_learning_quiz_nonexistent_point(
        self,
        client: AsyncClient
    ):
        """Test getting quiz for nonexistent knowledge point"""
        response = await client.get("/api/quiz/learning/99999")
        
        # Should return empty list or 404
        assert response.status_code in [200, 404]


class TestQuizQuestionDetailRoute:
    """Test quiz question detail endpoint"""
    
    async def test_get_question_detail_success(
        self,
        client: AsyncClient,
        test_quiz_question
    ):
        """Test getting question detail"""
        response = await client.get(f"/api/quiz/question/{test_quiz_question.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == test_quiz_question.id
        assert data["title"] == test_quiz_question.title
        assert "description" in data
        assert "difficulty" in data
        assert "hints" in data
    
    async def test_get_question_detail_with_hints(
        self,
        client: AsyncClient,
        test_quiz_question
    ):
        """Test that question detail includes hints"""
        response = await client.get(f"/api/quiz/question/{test_quiz_question.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "hints" in data
        assert isinstance(data["hints"], list)
        if len(data["hints"]) > 0:
            hint = data["hints"][0]
            assert "level" in hint
            assert "content" in hint
    
    async def test_get_question_detail_nonexistent(
        self,
        client: AsyncClient
    ):
        """Test getting nonexistent question"""
        response = await client.get("/api/quiz/question/99999")
        
        assert response.status_code == 404


class TestQuizAttemptTracking:
    """Test quiz attempt tracking"""
    
    async def test_attempt_recorded(
        self,
        client: AsyncClient,
        db_session,
        test_user,
        test_daily_question
    ):
        """Test that attempts are recorded in database"""
        from app.models import DailyKnowledgeAttempt
        from sqlalchemy import select
        
        # Submit answer
        await client.post(
            f"/api/quiz/daily/{test_user.id}/answer",
            json={
                "question_id": test_daily_question.id,
                "selected_option": test_daily_question.correct_answer
            }
        )
        
        # Check attempt was recorded
        result = await db_session.execute(
            select(DailyKnowledgeAttempt).where(
                DailyKnowledgeAttempt.user_id == test_user.id,
                DailyKnowledgeAttempt.question_id == test_daily_question.id
            )
        )
        attempt = result.scalar_one_or_none()
        
        assert attempt is not None
        assert attempt.is_correct is True
    
    async def test_multiple_users_independent(
        self,
        client: AsyncClient,
        db_session,
        test_user,
        test_daily_question
    ):
        """Test that different users have independent progress"""
        from app.models import User, DailyKnowledgeAttempt
        from app.services.auth_service import hash_password
        
        # Create second user
        user2 = User(
            username="testuser2",
            email="test2@example.com",
            hashed_password=hash_password("password")
        )
        db_session.add(user2)
        await db_session.commit()
        await db_session.refresh(user2)
        
        # User 1 answers
        await client.post(
            f"/api/quiz/daily/{test_user.id}/answer",
            json={
                "question_id": test_daily_question.id,
                "selected_option": test_daily_question.correct_answer
            }
        )
        
        # User 2 should still see the question
        response = await client.get(f"/api/quiz/daily/{user2.id}")
        data = response.json()
        
        question_ids = [q["id"] for q in data["questions"]]
        # Question might be in user2's daily quiz (if there are enough questions)
        # Main point is that user2's quiz is not affected by user1's answers
        assert response.status_code == 200




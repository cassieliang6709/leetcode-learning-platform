"""
Unit tests for database models
"""
import pytest
from datetime import datetime

from app.models import (
    User, KnowledgePoint, QuizQuestion, 
    QuizAttempt, CodeSubmission, DailyKnowledgeQuestion
)


class TestUserModel:
    """Test User model"""
    
    async def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
    
    async def test_user_relationships(self, db_session, test_user):
        """Test user relationships are initialized"""
        assert hasattr(test_user, 'knowledge_tests')
        assert hasattr(test_user, 'learning_plans')
        assert hasattr(test_user, 'quiz_attempts')
        assert hasattr(test_user, 'code_submissions')


class TestKnowledgePointModel:
    """Test KnowledgePoint model"""
    
    async def test_create_knowledge_point(self, db_session):
        """Test creating a knowledge point"""
        kp = KnowledgePoint(
            name="Arrays",
            description="Array basics",
            difficulty="easy",
            category="array",
            order_index=1
        )
        db_session.add(kp)
        await db_session.commit()
        await db_session.refresh(kp)
        
        assert kp.id is not None
        assert kp.name == "Arrays"
        assert kp.difficulty == "easy"
        assert kp.category == "array"
    
    async def test_knowledge_point_with_content(self, test_knowledge_point):
        """Test knowledge point with article content"""
        assert test_knowledge_point.article_content is not None
        assert test_knowledge_point.reading_questions is not None
        assert isinstance(test_knowledge_point.reading_questions, list)


class TestQuizQuestionModel:
    """Test QuizQuestion model"""
    
    async def test_create_quiz_question(self, test_quiz_question):
        """Test creating a quiz question"""
        assert test_quiz_question.id is not None
        assert test_quiz_question.title == "Two Sum"
        assert test_quiz_question.difficulty == "easy"
        assert isinstance(test_quiz_question.options, list)
        assert test_quiz_question.correct_answer == 1
    
    async def test_quiz_question_relationships(self, test_quiz_question):
        """Test quiz question relationships"""
        assert hasattr(test_quiz_question, 'knowledge_point')
        assert hasattr(test_quiz_question, 'attempts')
    
    async def test_quiz_question_with_hints(self, test_quiz_question):
        """Test quiz question with hints"""
        assert test_quiz_question.hints is not None
        assert isinstance(test_quiz_question.hints, list)
        assert len(test_quiz_question.hints) > 0
    
    async def test_quiz_question_with_test_cases(self, test_quiz_question):
        """Test quiz question with test cases"""
        assert test_quiz_question.test_cases is not None
        assert isinstance(test_quiz_question.test_cases, list)
    
    async def test_quiz_question_with_starter_code(self, test_quiz_question):
        """Test quiz question with starter code"""
        assert test_quiz_question.starter_code is not None
        assert isinstance(test_quiz_question.starter_code, dict)
        assert "python" in test_quiz_question.starter_code


class TestQuizAttemptModel:
    """Test QuizAttempt model"""
    
    async def test_create_quiz_attempt(self, db_session, test_user, test_quiz_question):
        """Test creating a quiz attempt"""
        attempt = QuizAttempt(
            user_id=test_user.id,
            question_id=test_quiz_question.id,
            is_correct=True,
            hints_used=1
        )
        db_session.add(attempt)
        await db_session.commit()
        await db_session.refresh(attempt)
        
        assert attempt.id is not None
        assert attempt.user_id == test_user.id
        assert attempt.question_id == test_quiz_question.id
        assert attempt.is_correct is True
        assert attempt.hints_used == 1
        assert attempt.completed_at is not None


class TestCodeSubmissionModel:
    """Test CodeSubmission model"""
    
    async def test_create_code_submission(self, db_session, test_user, test_quiz_question):
        """Test creating a code submission"""
        submission = CodeSubmission(
            user_id=test_user.id,
            question_id=test_quiz_question.id,
            code="def solution(): pass",
            language="python",
            notes="First attempt"
        )
        db_session.add(submission)
        await db_session.commit()
        await db_session.refresh(submission)
        
        assert submission.id is not None
        assert submission.user_id == test_user.id
        assert submission.code == "def solution(): pass"
        assert submission.language == "python"
        assert submission.created_at is not None


class TestDailyKnowledgeQuestionModel:
    """Test DailyKnowledgeQuestion model"""
    
    async def test_create_daily_question(self, test_daily_question):
        """Test creating a daily knowledge question"""
        assert test_daily_question.id is not None
        assert test_daily_question.question is not None
        assert isinstance(test_daily_question.options, list)
        assert len(test_daily_question.options) == 4
        assert test_daily_question.correct_answer in [0, 1, 2, 3]
        assert test_daily_question.difficulty == "easy"
        assert test_daily_question.category == "concept"







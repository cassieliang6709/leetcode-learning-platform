"""
Unit tests for Pydantic schemas
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    KnowledgePointResponse, QuizQuestionResponse,
    CodeSubmissionCreate, QuizAnswerSubmit
)


class TestUserSchemas:
    """Test user-related schemas"""
    
    def test_user_create_valid(self):
        """Test valid user creation schema"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        user = UserCreate(**user_data)
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"
    
    def test_user_create_invalid_email(self):
        """Test user creation with invalid email"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123"
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_create_missing_fields(self):
        """Test user creation with missing fields"""
        with pytest.raises(ValidationError):
            UserCreate(username="testuser")
    
    def test_user_login_valid(self):
        """Test valid login schema"""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login = UserLogin(**login_data)
        
        assert login.username == "testuser"
        assert login.password == "password123"
    
    def test_user_response_valid(self):
        """Test user response schema"""
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.now()
        }
        user = UserResponse(**user_data)
        
        assert user.id == 1
        assert user.username == "testuser"
        assert isinstance(user.created_at, datetime)


class TestKnowledgeSchemas:
    """Test knowledge-related schemas"""
    
    def test_knowledge_point_response(self):
        """Test knowledge point response schema"""
        kp_data = {
            "id": 1,
            "name": "Arrays",
            "description": "Array basics",
            "difficulty": "easy",
            "category": "array"
        }
        kp = KnowledgePointResponse(**kp_data)
        
        assert kp.id == 1
        assert kp.name == "Arrays"
        assert kp.difficulty == "easy"


class TestQuizSchemas:
    """Test quiz-related schemas"""
    
    def test_quiz_question_response(self):
        """Test quiz question response schema"""
        question_data = {
            "id": 1,
            "leetcode_id": 1,
            "title": "Two Sum",
            "description": "Find two numbers...",
            "difficulty": "easy",
            "hints": [{"level": "1", "content": "Use hash map"}],  # level as string
            "video_link": "https://example.com/video"
        }
        question = QuizQuestionResponse(**question_data)
        
        assert question.id == 1
        assert question.title == "Two Sum"
        assert question.difficulty == "easy"
    
    def test_quiz_answer_submit_valid(self):
        """Test quiz answer submission"""
        answer_data = {
            "question_id": 1,
            "selected_option": 2
        }
        answer = QuizAnswerSubmit(**answer_data)
        
        assert answer.question_id == 1
        assert answer.selected_option == 2
    
    def test_quiz_answer_submit_invalid(self):
        """Test invalid quiz answer submission"""
        with pytest.raises(ValidationError):
            QuizAnswerSubmit(question_id="invalid")


class TestCodeSchemas:
    """Test code-related schemas"""
    
    def test_code_submission_create_valid(self):
        """Test valid code submission"""
        submission_data = {
            "question_id": 1,
            "code": "def solution(): pass",
            "language": "python",
            "notes": "First attempt"
        }
        submission = CodeSubmissionCreate(**submission_data)
        
        assert submission.question_id == 1
        assert submission.code == "def solution(): pass"
        assert submission.language == "python"
        assert submission.notes == "First attempt"
    
    def test_code_submission_default_language(self):
        """Test code submission with default language"""
        submission_data = {
            "question_id": 1,
            "code": "def solution(): pass"
        }
        submission = CodeSubmissionCreate(**submission_data)
        
        assert submission.language == "python"
    
    def test_code_submission_optional_notes(self):
        """Test code submission without notes"""
        submission_data = {
            "question_id": 1,
            "code": "def solution(): pass",
            "language": "python"
        }
        submission = CodeSubmissionCreate(**submission_data)
        
        assert submission.notes is None


class TestTokenResponse:
    """Test token response schema"""
    
    def test_token_response_valid(self):
        """Test valid token response"""
        token_data = {
            "access_token": "fake.jwt.token",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "created_at": datetime.now()
            }
        }
        token = TokenResponse(**token_data)
        
        assert token.access_token == "fake.jwt.token"
        assert token.token_type == "bearer"
        assert token.user.id == 1
        assert token.user.username == "testuser"


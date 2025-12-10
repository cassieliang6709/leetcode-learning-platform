"""
Pydantic schemas for request/response validation.

This module defines all Pydantic models used for API request validation
and response serialization. These schemas ensure type safety and data
validation for all API endpoints.

Author: Yue Liang
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Schema for user registration requests.

    Attributes:
        username: Unique username for the user account.
        email: Valid email address for the user account.
        password: Plain text password (will be hashed before storage).
    """

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        username: User's username or email.
        password: User's password in plain text.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for user information in API responses.

    Excludes sensitive information like passwords.
    """

    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class TokenResponse(BaseModel):
    """
    Schema for authentication token responses.

    Returns JWT access token along with user information.
    """

    access_token: str
    token_type: str
    user: UserResponse


class KnowledgePointResponse(BaseModel):
    """
    Schema for knowledge point summary in API responses.

    Basic information about a learning topic without full content.
    """

    id: int
    name: str
    description: Optional[str]
    difficulty: str
    category: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ReadingQuestion(BaseModel):
    """
    Schema for reading comprehension questions.

    Used within knowledge point articles for interactive learning.
    """

    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class KnowledgePointDetailResponse(BaseModel):
    """
    Schema for detailed knowledge point information.

    Includes full article content and reading questions.
    """

    id: int
    name: str
    description: Optional[str]
    difficulty: str
    category: str
    article_content: Optional[str]
    reading_questions: Optional[List[Dict[str, Any]]]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class KnowledgeTestCreate(BaseModel):
    """
    Schema for creating a knowledge test.

    Attributes:
        test_data: Dictionary containing test answers and metadata.
    """

    test_data: Dict[str, Any]


class KnowledgeTestResponse(BaseModel):
    """
    Schema for knowledge test results in API responses.

    Includes test score, completion time, and AI-generated learning plan.
    """

    id: int
    score: int
    completed_at: datetime
    ai_plan: Dict[str, Any]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class QuizQuestionResponse(BaseModel):
    """
    Schema for quiz question information in API responses.

    Includes problem details, hints, and video links.
    """

    id: int
    leetcode_id: Optional[int]
    title: str
    description: str
    difficulty: str
    hints: Optional[List[Dict[str, str]]]
    video_link: Optional[str]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CodeSubmissionCreate(BaseModel):
    """
    Schema for code submission requests.

    Attributes:
        question_id: ID of the question being solved.
        code: User's code solution.
        language: Programming language (default: python).
        notes: Optional notes or comments.
    """

    question_id: int
    code: str
    language: str = "python"
    notes: Optional[str] = None


class CodeCheckResponse(BaseModel):
    """
    Schema for code check/analysis results.

    Includes error detection, suggestions, and optional hints.
    """

    has_errors: bool
    errors: List[str]
    suggestions: List[str]
    corrected_code: Optional[str]
    hint_level: Optional[int] = None
    hint_content: Optional[str] = None


class LearningPlanResponse(BaseModel):
    """
    Schema for learning plan information in API responses.

    Includes recommended knowledge points and AI suggestions.
    """

    id: int
    status: str
    knowledge_points: List[KnowledgePointResponse]
    ai_recommendations: Dict[str, Any]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class DailyQuizQuestion(BaseModel):
    """
    Schema for daily quiz questions in API responses.

    Includes question details and user's answer status.
    """

    id: int
    title: str
    description: str
    difficulty: str
    options: List[str]
    knowledge_point_name: Optional[str]
    is_answered: bool = False

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class QuizAnswerSubmit(BaseModel):
    """
    Schema for submitting quiz answers.

    Attributes:
        question_id: ID of the question being answered.
        selected_option: Index of the selected option (0-3).
    """

    question_id: int
    selected_option: int


class DailyProgressResponse(BaseModel):
    """
    Schema for daily progress summary in API responses.

    Includes statistics and list of questions for the day.
    """

    total_questions: int
    answered_count: int
    correct_count: int
    questions: List[DailyQuizQuestion]


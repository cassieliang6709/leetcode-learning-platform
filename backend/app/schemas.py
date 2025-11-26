from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class KnowledgePointResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    difficulty: str
    category: str

    class Config:
        from_attributes = True


class ReadingQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class KnowledgePointDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    difficulty: str
    category: str
    article_content: Optional[str]
    reading_questions: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class KnowledgeTestCreate(BaseModel):
    test_data: Dict[str, Any]


class KnowledgeTestResponse(BaseModel):
    id: int
    score: int
    completed_at: datetime
    ai_plan: Dict[str, Any]

    class Config:
        from_attributes = True


class QuizQuestionResponse(BaseModel):
    id: int
    leetcode_id: Optional[int]
    title: str
    description: str
    difficulty: str
    hints: Optional[List[Dict[str, str]]]
    video_link: Optional[str]

    class Config:
        from_attributes = True


class CodeSubmissionCreate(BaseModel):
    question_id: int
    code: str
    language: str = "python"
    notes: Optional[str] = None


class CodeCheckResponse(BaseModel):
    has_errors: bool
    errors: List[str]
    suggestions: List[str]
    corrected_code: Optional[str]
    hint_level: Optional[int] = None
    hint_content: Optional[str] = None


class LearningPlanResponse(BaseModel):
    id: int
    status: str
    knowledge_points: List[KnowledgePointResponse]
    ai_recommendations: Dict[str, Any]

    class Config:
        from_attributes = True


class DailyQuizQuestion(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    options: List[str]
    knowledge_point_name: Optional[str]
    is_answered: bool = False

    class Config:
        from_attributes = True


class QuizAnswerSubmit(BaseModel):
    question_id: int
    selected_option: int


class DailyProgressResponse(BaseModel):
    total_questions: int
    answered_count: int
    correct_count: int
    questions: List[DailyQuizQuestion]


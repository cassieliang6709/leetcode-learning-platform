"""
SQLAlchemy database models for the LeetCode Learning Platform.

This module defines all database table models using SQLAlchemy ORM.
Each model represents a table in the PostgreSQL database and includes
relationships, constraints, and field definitions.

Models include:
- User: User accounts and authentication
- KnowledgePoint: Learning topics and concepts
- QuizQuestion: Coding problems and quiz questions
- CodeSubmission: User code submissions
- LearningPlan: Personalized learning paths
- DailyKnowledgeQuestion: Daily practice questions

Author: Yue Liang
"""

from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model representing application users.

    Stores user authentication information and maintains relationships
    with user activities including tests, learning plans, quiz attempts,
    and code submissions.
    """

    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    knowledge_tests: Mapped[List["KnowledgeTest"]] = relationship(
        "KnowledgeTest", back_populates="user"
    )
    learning_plans: Mapped[List["LearningPlan"]] = relationship(
        "LearningPlan", back_populates="user"
    )
    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="user"
    )
    code_submissions: Mapped[List["CodeSubmission"]] = relationship(
        "CodeSubmission", back_populates="user"
    )


class KnowledgePoint(Base):
    """
    Knowledge point model representing learning topics.

    Each knowledge point represents a specific topic or concept
    (e.g., Arrays, Binary Trees, Dynamic Programming) that users
    can learn. Includes article content and reading questions.
    """

    __tablename__ = "knowledge_points"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    description: Mapped[Optional[str]] = Column(Text)
    difficulty: Mapped[Optional[str]] = Column(String(20))  # easy, medium, hard
    category: Mapped[Optional[str]] = Column(String(50))  # array, tree, graph, etc.
    order_index: Mapped[int] = Column(Integer, default=0)
    
    # Learning content fields
    article_content: Mapped[Optional[str]] = Column(Text)  # English article
    reading_questions: Mapped[Optional[dict]] = Column(JSON)  # Q&A questions
    # Format: [{"question": "...", "options": ["A", "B", "C", "D"], 
    #          "correct_answer": 1, "explanation": "..."}]

    # Relationships
    quiz_questions: Mapped[List["QuizQuestion"]] = relationship(
        "QuizQuestion", back_populates="knowledge_point"
    )


class KnowledgeTest(Base):
    """
    Knowledge test model for user assessment results.

    Stores the results of user knowledge assessments including
    test answers, scores, and completion timestamps.
    """

    __tablename__ = "knowledge_tests"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_data: Mapped[Optional[dict]] = Column(JSON)  # Store test answers and results
    score: Mapped[Optional[int]] = Column(Integer)
    completed_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="knowledge_tests")


class LearningPlan(Base):
    """
    Learning plan model for personalized learning paths.

    Tracks user progress through knowledge points with AI-generated
    recommendations and status tracking.
    """

    __tablename__ = "learning_plans"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    knowledge_point_id: Mapped[Optional[int]] = Column(
        Integer, ForeignKey("knowledge_points.id")
    )
    status: Mapped[str] = Column(String(20), default="in_progress")  # in_progress, completed
    ai_recommendations: Mapped[Optional[dict]] = Column(JSON)
    created_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = Column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="learning_plans")


class QuizQuestion(Base):
    """
    Quiz question model for coding problems and practice questions.

    Represents a coding problem or quiz question with multiple choice
    options, hints, test cases, and starter code templates.
    """

    __tablename__ = "quiz_questions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    knowledge_point_id: Mapped[Optional[int]] = Column(
        Integer, ForeignKey("knowledge_points.id")
    )
    leetcode_id: Mapped[Optional[int]] = Column(Integer)  # LeetCode problem number
    title: Mapped[str] = Column(String(200), nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    difficulty: Mapped[Optional[str]] = Column(String(20))
    options: Mapped[Optional[list]] = Column(JSON)  # Multiple choice options
    correct_answer: Mapped[Optional[int]] = Column(Integer)  # Index 0-3
    explanation: Mapped[Optional[str]] = Column(Text)  # Explanation of answer
    solution: Mapped[Optional[str]] = Column(Text)
    hints: Mapped[Optional[list]] = Column(JSON)  # Multi-level hints
    video_link: Mapped[Optional[str]] = Column(String(200))
    test_cases: Mapped[Optional[list]] = Column(JSON)  # Test cases for execution
    starter_code: Mapped[Optional[dict]] = Column(JSON)  # Starter code templates

    # Relationships
    knowledge_point: Mapped[Optional["KnowledgePoint"]] = relationship(
        "KnowledgePoint", back_populates="quiz_questions"
    )
    attempts: Mapped[List["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="question"
    )


class QuizAttempt(Base):
    """
    Quiz attempt model for tracking user question attempts.

    Records user answers to quiz questions, whether they were correct,
    and how many hints were used.
    """

    __tablename__ = "quiz_attempts"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id: Mapped[int] = Column(
        Integer, ForeignKey("quiz_questions.id"), nullable=False
    )
    is_correct: Mapped[bool] = Column(Boolean, default=False)
    hints_used: Mapped[int] = Column(Integer, default=0)
    completed_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="quiz_attempts")
    question: Mapped["QuizQuestion"] = relationship(
        "QuizQuestion", back_populates="attempts"
    )


class CodeSubmission(Base):
    """
    Code submission model for user code solutions.

    Stores user-submitted code with language, AI feedback,
    and optional notes for learning purposes.
    """

    __tablename__ = "code_submissions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("quiz_questions.id"))
    code: Mapped[str] = Column(Text, nullable=False)
    language: Mapped[str] = Column(String(20), default="python")
    ai_feedback: Mapped[Optional[dict]] = Column(JSON)  # AI analysis
    notes: Mapped[Optional[str]] = Column(Text)
    created_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="code_submissions")


class DailyKnowledgeQuestion(Base):
    """
    Daily knowledge question model for daily practice.

    Represents questions used for daily practice sessions with
    multiple choice options and explanations.
    """

    __tablename__ = "daily_knowledge_questions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    knowledge_point_id: Mapped[Optional[int]] = Column(
        Integer, ForeignKey("knowledge_points.id")
    )
    question: Mapped[str] = Column(Text, nullable=False)  # Question text
    options: Mapped[list] = Column(JSON, nullable=False)  # Array of 4 options
    correct_answer: Mapped[int] = Column(Integer, nullable=False)  # Index 0-3
    explanation: Mapped[Optional[str]] = Column(Text)  # Answer explanation
    difficulty: Mapped[str] = Column(String(20), default="medium")  # easy, medium, hard
    category: Mapped[Optional[str]] = Column(String(50))  # concept, etc.
    created_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    knowledge_point: Mapped[Optional["KnowledgePoint"]] = relationship("KnowledgePoint")
    attempts: Mapped[List["DailyKnowledgeAttempt"]] = relationship(
        "DailyKnowledgeAttempt", back_populates="question"
    )


class DailyKnowledgeAttempt(Base):
    """
    Daily knowledge attempt model for tracking daily question attempts.

    Records user attempts on daily knowledge questions with
    correctness tracking and timestamps.
    """

    __tablename__ = "daily_knowledge_attempts"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id: Mapped[int] = Column(
        Integer, ForeignKey("daily_knowledge_questions.id"), nullable=False
    )
    is_correct: Mapped[bool] = Column(Boolean, default=False)
    completed_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    question: Mapped["DailyKnowledgeQuestion"] = relationship(
        "DailyKnowledgeQuestion", back_populates="attempts"
    )



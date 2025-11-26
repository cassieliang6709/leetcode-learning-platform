from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    knowledge_tests = relationship("KnowledgeTest", back_populates="user")
    learning_plans = relationship("LearningPlan", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    code_submissions = relationship("CodeSubmission", back_populates="user")


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty = Column(String(20))  # easy, medium, hard
    category = Column(String(50))  # array, tree, graph, etc.
    order_index = Column(Integer, default=0)
    
    # Learning content fields
    article_content = Column(Text)  # English article explaining the concept
    reading_questions = Column(JSON)  # Q&A questions after reading
    # Format: [{"question": "...", "options": ["A", "B", "C", "D"], "correct_answer": 1, "explanation": "..."}]

    # Relationships
    quiz_questions = relationship("QuizQuestion", back_populates="knowledge_point")


class KnowledgeTest(Base):
    __tablename__ = "knowledge_tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_data = Column(JSON)  # Store test answers and results
    score = Column(Integer)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="knowledge_tests")


class LearningPlan(Base):
    __tablename__ = "learning_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    status = Column(String(20), default="in_progress")  # in_progress, completed
    ai_recommendations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_plans")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    leetcode_id = Column(Integer)  # LeetCode problem number
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20))
    options = Column(JSON)  # Multiple choice options [str, str, str, str]
    correct_answer = Column(Integer)  # Index of correct option (0-3)
    explanation = Column(Text)  # Explanation of the answer
    solution = Column(Text)
    hints = Column(JSON)  # Multi-level hints
    video_link = Column(String(200))
    test_cases = Column(JSON)  # Test cases for code execution
    starter_code = Column(JSON)  # Starter code templates for different languages

    # Relationships
    knowledge_point = relationship("KnowledgePoint", back_populates="quiz_questions")
    attempts = relationship("QuizAttempt", back_populates="question")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    is_correct = Column(Boolean, default=False)
    hints_used = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    question = relationship("QuizQuestion", back_populates="attempts")


class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    code = Column(Text, nullable=False)
    language = Column(String(20), default="python")
    ai_feedback = Column(JSON)  # AI analysis of code errors and suggestions
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="code_submissions")


class DailyKnowledgeQuestion(Base):
    __tablename__ = "daily_knowledge_questions"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    question = Column(Text, nullable=False)  # Question text in English
    options = Column(JSON, nullable=False)  # Array of 4 options
    correct_answer = Column(Integer, nullable=False)  # Index 0-3
    explanation = Column(Text)  # Answer explanation
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    category = Column(String(50))  # concept, complexity, data_structure, algorithm
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    knowledge_point = relationship("KnowledgePoint")
    attempts = relationship("DailyKnowledgeAttempt", back_populates="question")


class DailyKnowledgeAttempt(Base):
    __tablename__ = "daily_knowledge_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("daily_knowledge_questions.id"), nullable=False)
    is_correct = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    question = relationship("DailyKnowledgeQuestion", back_populates="attempts")



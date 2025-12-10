"""
Pytest configuration and fixtures for testing
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from faker import Faker

# Add parent directory to path to import app
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import Base, get_db
from main import app
from app.models import User, KnowledgePoint, QuizQuestion, DailyKnowledgeQuestion
from app.services.auth_service import hash_password

# Use test database
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://localhost:5432/leetcode_learning_test"
)

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

fake = Faker()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpassword123")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_user_token(client: AsyncClient, test_user: User) -> str:
    """Get authentication token for test user"""
    response = await client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
async def authenticated_client(
    client: AsyncClient, 
    test_user_token: str
) -> AsyncClient:
    """Create authenticated client with token"""
    client.headers["Authorization"] = f"Bearer {test_user_token}"
    return client


@pytest.fixture
async def test_knowledge_point(db_session: AsyncSession) -> KnowledgePoint:
    """Create a test knowledge point"""
    kp = KnowledgePoint(
        name="Array Basics",
        description="Introduction to arrays and basic operations",
        difficulty="easy",
        category="array",
        order_index=1,
        article_content="# Arrays\n\nArrays are fundamental data structures...",
        reading_questions=[
            {
                "question": "What is an array?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": 0,
                "explanation": "Arrays are contiguous memory blocks"
            }
        ]
    )
    db_session.add(kp)
    await db_session.commit()
    await db_session.refresh(kp)
    return kp


@pytest.fixture
async def test_quiz_question(
    db_session: AsyncSession,
    test_knowledge_point: KnowledgePoint
) -> QuizQuestion:
    """Create a test quiz question"""
    question = QuizQuestion(
        knowledge_point_id=test_knowledge_point.id,
        leetcode_id=1,
        title="Two Sum",
        description="Given an array of integers, return indices of two numbers...",
        difficulty="easy",
        options=["O(n^2)", "O(n)", "O(log n)", "O(1)"],
        correct_answer=1,
        explanation="Using a hash map gives O(n) complexity",
        solution="Use hash map to store complements",
        hints=[
            {"level": 1, "content": "Think about storing seen numbers"},
            {"level": 2, "content": "Use a hash map"},
            {"level": 3, "content": "Store complement as key"}
        ],
        test_cases=[
            {"input": "[2,7,11,15], 9", "output": "[0,1]"}
        ],
        starter_code={
            "python": "def twoSum(nums: List[int], target: int) -> List[int]:\n    pass"
        }
    )
    db_session.add(question)
    await db_session.commit()
    await db_session.refresh(question)
    return question


@pytest.fixture
async def test_daily_question(
    db_session: AsyncSession,
    test_knowledge_point: KnowledgePoint
) -> DailyKnowledgeQuestion:
    """Create a test daily knowledge question"""
    question = DailyKnowledgeQuestion(
        knowledge_point_id=test_knowledge_point.id,
        question="What is the time complexity of accessing an element in an array?",
        options=["O(n)", "O(log n)", "O(1)", "O(n^2)"],
        correct_answer=2,
        explanation="Array access is O(1) because elements are stored contiguously",
        difficulty="easy",
        category="concept"
    )
    db_session.add(question)
    await db_session.commit()
    await db_session.refresh(question)
    return question


@pytest.fixture
def sample_test_data() -> dict:
    """Sample test data for knowledge tests"""
    return {
        "answers": [
            {"topic": "arrays", "is_correct": True},
            {"topic": "trees", "is_correct": False},
            {"topic": "graphs", "is_correct": False},
            {"topic": "dynamic programming", "is_correct": True}
        ]
    }


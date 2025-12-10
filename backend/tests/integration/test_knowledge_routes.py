"""
Integration tests for knowledge routes
"""
import pytest
from httpx import AsyncClient


class TestGetKnowledgePoints:
    """Test getting all knowledge points"""
    
    async def test_get_all_points(
        self,
        client: AsyncClient,
        test_knowledge_point
    ):
        """Test getting all knowledge points"""
        response = await client.get("/api/knowledge/points")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        point = data[0]
        assert "id" in point
        assert "name" in point
        assert "difficulty" in point
        assert "category" in point
    
    async def test_points_ordered(
        self,
        client: AsyncClient,
        db_session
    ):
        """Test that points are returned in order"""
        from app.models import KnowledgePoint
        
        # Create multiple points with different order_index
        points = [
            KnowledgePoint(name="C", difficulty="easy", category="test", order_index=3),
            KnowledgePoint(name="A", difficulty="easy", category="test", order_index=1),
            KnowledgePoint(name="B", difficulty="easy", category="test", order_index=2),
        ]
        for point in points:
            db_session.add(point)
        await db_session.commit()
        
        response = await client.get("/api/knowledge/points")
        data = response.json()
        
        # Check if ordered by order_index
        names = [p["name"] for p in data]
        assert names.index("A") < names.index("B") < names.index("C")


class TestGetKnowledgePointDetail:
    """Test getting knowledge point details"""
    
    async def test_get_point_detail_success(
        self,
        client: AsyncClient,
        test_knowledge_point
    ):
        """Test getting knowledge point detail"""
        response = await client.get(f"/api/knowledge/points/{test_knowledge_point.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == test_knowledge_point.id
        assert data["name"] == test_knowledge_point.name
        assert "article_content" in data
        assert "reading_questions" in data
    
    async def test_get_point_detail_with_content(
        self,
        client: AsyncClient,
        test_knowledge_point
    ):
        """Test that detail includes article content"""
        response = await client.get(f"/api/knowledge/points/{test_knowledge_point.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["article_content"] is not None
        assert len(data["article_content"]) > 0
    
    async def test_get_point_detail_with_questions(
        self,
        client: AsyncClient,
        test_knowledge_point
    ):
        """Test that detail includes reading questions"""
        response = await client.get(f"/api/knowledge/points/{test_knowledge_point.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["reading_questions"] is not None
        assert isinstance(data["reading_questions"], list)
        
        if len(data["reading_questions"]) > 0:
            question = data["reading_questions"][0]
            assert "question" in question
            assert "options" in question
            assert "correct_answer" in question
    
    async def test_get_nonexistent_point(
        self,
        client: AsyncClient
    ):
        """Test getting nonexistent knowledge point"""
        response = await client.get("/api/knowledge/points/99999")
        
        assert response.status_code == 404


class TestGetKnowledgePointQuestions:
    """Test getting questions for a knowledge point"""
    
    async def test_get_point_questions_success(
        self,
        client: AsyncClient,
        test_knowledge_point,
        test_quiz_question
    ):
        """Test getting questions for knowledge point"""
        response = await client.get(
            f"/api/knowledge/points/{test_knowledge_point.id}/questions"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        question = data[0]
        assert "id" in question
        assert "title" in question
        assert "difficulty" in question
    
    async def test_get_questions_for_empty_point(
        self,
        client: AsyncClient,
        db_session
    ):
        """Test getting questions for point with no questions"""
        from app.models import KnowledgePoint
        
        # Create point without questions
        point = KnowledgePoint(
            name="Empty Point",
            difficulty="easy",
            category="test"
        )
        db_session.add(point)
        await db_session.commit()
        await db_session.refresh(point)
        
        response = await client.get(f"/api/knowledge/points/{point.id}/questions")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestSubmitKnowledgeTest:
    """Test submitting knowledge test"""
    
    async def test_submit_test_success(
        self,
        client: AsyncClient,
        test_user,
        sample_test_data
    ):
        """Test submitting knowledge test"""
        response = await client.post(
            f"/api/knowledge/test/{test_user.id}",
            json={"test_data": sample_test_data}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "score" in data
        assert "completed_at" in data
        assert "ai_plan" in data
        
        # Check AI plan structure
        plan = data["ai_plan"]
        assert "score" in plan
        assert "recommended_points" in plan
        assert "weak_areas" in plan
    
    async def test_submit_test_creates_record(
        self,
        client: AsyncClient,
        db_session,
        test_user,
        sample_test_data
    ):
        """Test that submitting test creates database record"""
        from app.models import KnowledgeTest
        from sqlalchemy import select
        
        response = await client.post(
            f"/api/knowledge/test/{test_user.id}",
            json={"test_data": sample_test_data}
        )
        
        assert response.status_code == 200
        test_id = response.json()["id"]
        
        # Verify record exists
        result = await db_session.execute(
            select(KnowledgeTest).where(KnowledgeTest.id == test_id)
        )
        test = result.scalar_one_or_none()
        
        assert test is not None
        assert test.user_id == test_user.id
    
    async def test_submit_test_with_empty_data(
        self,
        client: AsyncClient,
        test_user
    ):
        """Test submitting test with empty data"""
        response = await client.post(
            f"/api/knowledge/test/{test_user.id}",
            json={"test_data": {"answers": []}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "score" in data


class TestGetLearningPlan:
    """Test getting user's learning plan"""
    
    async def test_get_plan_no_plan(
        self,
        client: AsyncClient,
        test_user
    ):
        """Test getting plan when user has no plan"""
        response = await client.get(f"/api/knowledge/plan/{test_user.id}")
        
        assert response.status_code == 404
    
    async def test_get_plan_with_existing_plan(
        self,
        client: AsyncClient,
        db_session,
        test_user,
        test_knowledge_point
    ):
        """Test getting existing learning plan"""
        from app.models import LearningPlan
        
        # Create learning plan
        plan = LearningPlan(
            user_id=test_user.id,
            knowledge_point_id=test_knowledge_point.id,
            status="in_progress",
            ai_recommendations={
                "recommended_points": [1, 2, 3],
                "weak_areas": ["arrays"]
            }
        )
        db_session.add(plan)
        await db_session.commit()
        
        response = await client.get(f"/api/knowledge/plan/{test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "status" in data
        assert "ai_recommendations" in data


class TestHealthEndpoint:
    """Test application health endpoint"""
    
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint"""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "status" in data
    
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"




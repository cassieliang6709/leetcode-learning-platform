"""
Unit tests for AI service
"""
import pytest
from app.services.ai_service import generate_learning_plan


class TestGenerateLearningPlan:
    """Test learning plan generation"""
    
    async def test_generate_plan_low_score(self, sample_test_data):
        """Test learning plan for low score"""
        plan = await generate_learning_plan(sample_test_data, score=30)
        
        assert plan is not None
        assert "score" in plan
        assert plan["score"] == 30
        assert "recommended_points" in plan
        assert "weak_areas" in plan
        assert "study_time_estimate" in plan
        assert "next_steps" in plan
        
        # Low score should recommend basic topics
        assert isinstance(plan["recommended_points"], list)
        assert len(plan["recommended_points"]) > 0
    
    async def test_generate_plan_medium_score(self, sample_test_data):
        """Test learning plan for medium score"""
        plan = await generate_learning_plan(sample_test_data, score=50)
        
        assert plan["score"] == 50
        assert len(plan["recommended_points"]) > 0
    
    async def test_generate_plan_high_score(self, sample_test_data):
        """Test learning plan for high score"""
        plan = await generate_learning_plan(sample_test_data, score=80)
        
        assert plan["score"] == 80
        assert len(plan["recommended_points"]) > 0
    
    async def test_identify_weak_areas(self, sample_test_data):
        """Test identifying weak areas from test data"""
        plan = await generate_learning_plan(sample_test_data, score=50)
        
        assert "weak_areas" in plan
        weak_areas = plan["weak_areas"]
        
        # Should identify trees and graphs as weak (is_correct=False)
        assert "trees" in weak_areas
        assert "graphs" in weak_areas
    
    async def test_plan_structure(self, sample_test_data):
        """Test that plan has correct structure"""
        plan = await generate_learning_plan(sample_test_data, score=50)
        
        # Check all required fields
        assert "score" in plan
        assert "recommended_points" in plan
        assert "weak_areas" in plan
        assert "study_time_estimate" in plan
        assert "next_steps" in plan
        
        # Check types
        assert isinstance(plan["score"], int)
        assert isinstance(plan["recommended_points"], list)
        assert isinstance(plan["weak_areas"], list)
        assert isinstance(plan["study_time_estimate"], str)
        assert isinstance(plan["next_steps"], list)
    
    async def test_plan_with_empty_data(self):
        """Test plan generation with empty test data"""
        empty_data = {"answers": []}
        plan = await generate_learning_plan(empty_data, score=0)
        
        assert plan is not None
        assert plan["score"] == 0
        assert isinstance(plan["recommended_points"], list)
    
    async def test_study_time_estimate(self, sample_test_data):
        """Test study time estimation"""
        plan = await generate_learning_plan(sample_test_data, score=50)
        
        assert "study_time_estimate" in plan
        assert "weeks" in plan["study_time_estimate"] or "week" in plan["study_time_estimate"]
    
    async def test_next_steps_provided(self, sample_test_data):
        """Test that next steps are provided"""
        plan = await generate_learning_plan(sample_test_data, score=50)
        
        assert "next_steps" in plan
        assert len(plan["next_steps"]) > 0
        assert all(isinstance(step, str) for step in plan["next_steps"])




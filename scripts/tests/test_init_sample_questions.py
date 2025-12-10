"""
Unit tests for init_sample_questions module.

This module tests the functionality of question initialization,
validation, and database operations with comprehensive coverage.

Test cases follow unittest.TestCase patterns and use async fixtures
for database operations.

Author: Yue Liang
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

# Add backend directory to path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from init_sample_questions import (
    validate_question_data,
    get_knowledge_points_map,
    count_existing_questions,
    add_question_to_database,
    initialize_questions,
    SAMPLE_QUESTIONS
)
from app.models import KnowledgePoint, QuizQuestion


class TestValidateQuestionData(unittest.TestCase):
    """Test cases for validate_question_data function."""

    def test_valid_question_data(self):
        """Test validation with valid question data."""
        valid_data = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers that sum to target",
            "difficulty": "easy",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 1,
            "explanation": "Use hash table"
        }
        is_valid, error_msg = validate_question_data(valid_data)
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)

    def test_missing_required_field(self):
        """Test validation with missing required field."""
        invalid_data = {
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field", error_msg)

    def test_empty_knowledge_point_name(self):
        """Test validation with empty knowledge_point_name."""
        invalid_data = {
            "knowledge_point_name": "",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("knowledge_point_name", error_msg)

    def test_invalid_difficulty(self):
        """Test validation with invalid difficulty level."""
        invalid_data = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "very_hard",
            "options": ["A", "B"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("difficulty", error_msg)

    def test_insufficient_options(self):
        """Test validation with less than 2 options."""
        invalid_data = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("options", error_msg)

    def test_invalid_correct_answer_index(self):
        """Test validation with correct_answer out of bounds."""
        invalid_data = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B", "C"],
            "correct_answer": 5,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("correct_answer", error_msg)

    def test_negative_correct_answer(self):
        """Test validation with negative correct_answer."""
        invalid_data = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B"],
            "correct_answer": -1,
            "explanation": "Use hash"
        }
        is_valid, error_msg = validate_question_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("correct_answer", error_msg)


class TestGetKnowledgePointsMap(unittest.IsolatedAsyncioTestCase):
    """Test cases for get_knowledge_points_map function."""

    async def test_successful_retrieval(self):
        """Test successful retrieval of knowledge points."""
        mock_session = AsyncMock()
        mock_kp1 = MagicMock(spec=KnowledgePoint)
        mock_kp1.name = "Array"
        mock_kp2 = MagicMock(spec=KnowledgePoint)
        mock_kp2.name = "String"

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_kp1, mock_kp2]
        mock_session.execute.return_value = mock_result

        result = await get_knowledge_points_map(mock_session)

        self.assertEqual(len(result), 2)
        self.assertIn("Array", result)
        self.assertIn("String", result)
        self.assertEqual(result["Array"], mock_kp1)
        self.assertEqual(result["String"], mock_kp2)

    async def test_database_error(self):
        """Test handling of database errors."""
        mock_session = AsyncMock()
        mock_session.execute.side_effect = Exception("Database connection failed")

        with self.assertRaises(Exception) as context:
            await get_knowledge_points_map(mock_session)

        self.assertIn("Failed to retrieve knowledge points", str(context.exception))


class TestCountExistingQuestions(unittest.IsolatedAsyncioTestCase):
    """Test cases for count_existing_questions function."""

    async def test_count_zero_questions(self):
        """Test counting when no questions exist."""
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        count = await count_existing_questions(mock_session)
        self.assertEqual(count, 0)

    async def test_count_multiple_questions(self):
        """Test counting when multiple questions exist."""
        mock_session = AsyncMock()
        mock_questions = [MagicMock(), MagicMock(), MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_questions
        mock_session.execute.return_value = mock_result

        count = await count_existing_questions(mock_session)
        self.assertEqual(count, 3)

    async def test_database_error(self):
        """Test handling of database errors."""
        mock_session = AsyncMock()
        mock_session.execute.side_effect = Exception("Query failed")

        with self.assertRaises(Exception) as context:
            await count_existing_questions(mock_session)

        self.assertIn("Failed to count existing questions", str(context.exception))


class TestAddQuestionToDatabase(unittest.IsolatedAsyncioTestCase):
    """Test cases for add_question_to_database function."""

    async def test_successful_addition(self):
        """Test successful addition of question."""
        mock_session = AsyncMock()
        mock_kp = MagicMock(spec=KnowledgePoint)
        mock_kp.id = 1

        question_data = {
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }

        result = await add_question_to_database(mock_session, question_data, mock_kp)

        self.assertTrue(result)
        mock_session.add.assert_called_once()

    async def test_database_error(self):
        """Test handling of database errors."""
        mock_session = AsyncMock()
        mock_session.add.side_effect = Exception("Insert failed")
        mock_kp = MagicMock(spec=KnowledgePoint)
        mock_kp.id = 1

        question_data = {
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B"],
            "correct_answer": 0,
            "explanation": "Use hash"
        }

        with self.assertRaises(Exception) as context:
            await add_question_to_database(mock_session, question_data, mock_kp)

        self.assertIn("Failed to create question", str(context.exception))


class TestInitializeQuestions(unittest.IsolatedAsyncioTestCase):
    """Test cases for initialize_questions function."""

    async def test_skip_when_enough_exist(self):
        """Test skipping when threshold is met."""
        mock_session = AsyncMock()

        # Mock get_knowledge_points_map
        with patch('init_sample_questions.get_knowledge_points_map') as mock_get_kp:
            mock_get_kp.return_value = {"Array": MagicMock()}

            # Mock count_existing_questions
            with patch('init_sample_questions.count_existing_questions') as mock_count:
                mock_count.return_value = 5  # Above threshold of 3

                added, skipped = await initialize_questions(
                    mock_session, SAMPLE_QUESTIONS[:1], min_existing_threshold=3
                )

                self.assertEqual(added, 0)
                self.assertEqual(skipped, 1)

    async def test_add_valid_questions(self):
        """Test adding valid questions."""
        mock_session = AsyncMock()
        mock_kp = MagicMock(spec=KnowledgePoint)
        mock_kp.id = 1
        mock_kp.name = "Array"

        valid_question = {
            "knowledge_point_name": "Array",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B", "C", "D"],
            "correct_answer": 1,
            "explanation": "Use hash"
        }

        with patch('init_sample_questions.get_knowledge_points_map') as mock_get_kp:
            mock_get_kp.return_value = {"Array": mock_kp}

            with patch('init_sample_questions.count_existing_questions') as mock_count:
                mock_count.return_value = 0  # Below threshold

                with patch('init_sample_questions.add_question_to_database') as mock_add:
                    mock_add.return_value = True

                    added, skipped = await initialize_questions(
                        mock_session, [valid_question], min_existing_threshold=3
                    )

                    self.assertEqual(added, 1)
                    self.assertEqual(skipped, 0)
                    mock_add.assert_called_once()

    async def test_skip_invalid_questions(self):
        """Test skipping invalid questions."""
        mock_session = AsyncMock()
        invalid_question = {
            "title": "Two Sum",
            # Missing required fields
        }

        with patch('init_sample_questions.get_knowledge_points_map') as mock_get_kp:
            mock_get_kp.return_value = {"Array": MagicMock()}

            with patch('init_sample_questions.count_existing_questions') as mock_count:
                mock_count.return_value = 0

                added, skipped = await initialize_questions(
                    mock_session, [invalid_question], min_existing_threshold=3
                )

                self.assertEqual(added, 0)
                self.assertEqual(skipped, 1)

    async def test_skip_missing_knowledge_point(self):
        """Test skipping questions with missing knowledge points."""
        mock_session = AsyncMock()
        valid_question = {
            "knowledge_point_name": "NonExistent",
            "title": "Two Sum",
            "description": "Find two numbers",
            "difficulty": "easy",
            "options": ["A", "B", "C", "D"],
            "correct_answer": 1,
            "explanation": "Use hash"
        }

        with patch('init_sample_questions.get_knowledge_points_map') as mock_get_kp:
            mock_get_kp.return_value = {"Array": MagicMock()}  # Different KP

            with patch('init_sample_questions.count_existing_questions') as mock_count:
                mock_count.return_value = 0

                added, skipped = await initialize_questions(
                    mock_session, [valid_question], min_existing_threshold=3
                )

                self.assertEqual(added, 0)
                self.assertEqual(skipped, 1)


if __name__ == "__main__":
    unittest.main()

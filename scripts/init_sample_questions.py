#!/usr/bin/env python3
"""
Initialize sample quiz questions with options and correct answers.

This module provides functionality to initialize the database with sample
quiz questions for testing and development purposes. It validates knowledge
points, checks for existing questions, and adds new questions only if needed.

The module follows PEP8 style guidelines and includes comprehensive error
handling, input validation, and modular design for testability.

Author: Yue Liang
"""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models import QuizQuestion, KnowledgePoint


# Sample questions data
SAMPLE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "knowledge_point_name": "Array",
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "easy",
        "options": [
            "Use brute force to iterate through all possible combinations",
            "Use hash table to store traversed elements and their indices",
            "Sort the array first, then use two pointers",
            "Use recursive method to find"
        ],
        "correct_answer": 1,
        "explanation": "Using a hash table can solve the problem in O(n) time complexity, with O(n) space complexity."
    },
    {
        "knowledge_point_name": "String",
        "title": "Longest Palindromic Substring",
        "description": "Given a string s, return the longest palindromic substring in s.",
        "difficulty": "medium",
        "options": [
            "Brute force enumerate all substrings and check if palindrome",
            "Use dynamic programming to record if substring is palindrome",
            "Expand from center to find palindrome",
            "Use hash table to record character positions"
        ],
        "correct_answer": 2,
        "explanation": "Center expansion is the most common method, with O(n²) time complexity and O(1) space complexity."
    },
    {
        "knowledge_point_name": "Linked List",
        "title": "Reverse Linked List",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "difficulty": "easy",
        "options": [
            "Use recursive method to reverse",
            "Use stack to store all nodes then rebuild",
            "Use two pointers to iterate and reverse",
            "Create new linked list and copy nodes"
        ],
        "correct_answer": 2,
        "explanation": "Two-pointer iteration is optimal, with O(n) time complexity and O(1) space complexity."
    },
    {
        "knowledge_point_name": "Binary Tree",
        "title": "Maximum Depth of Binary Tree",
        "description": "Given the root of a binary tree, return its maximum depth.",
        "difficulty": "easy",
        "options": [
            "Use depth-first search (DFS) recursive calculation",
            "Use breadth-first search (BFS) level-order traversal",
            "Use stack to simulate recursive process",
            "Use queue to record number of nodes per level"
        ],
        "correct_answer": 0,
        "explanation": "DFS recursion is the most concise method: max_depth = max(left, right) + 1"
    },
    {
        "knowledge_point_name": "Dynamic Programming",
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "difficulty": "easy",
        "options": [
            "Use recursion to calculate directly",
            "Use dynamic programming, dp[i] = dp[i-1] + dp[i-2]",
            "Use greedy algorithm to choose optimal steps",
            "Use backtracking to enumerate all possibilities"
        ],
        "correct_answer": 1,
        "explanation": "This is a classic Fibonacci sequence problem. Using DP can avoid repeated calculations."
    }
]


def validate_question_data(question_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate question data structure and content.

    Args:
        question_data: Dictionary containing question information with keys:
            - knowledge_point_name: str
            - title: str
            - description: str
            - difficulty: str
            - options: List[str]
            - correct_answer: int
            - explanation: str

    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str]).
        If valid, error_message is None.
    """
    required_fields = [
        "knowledge_point_name", "title", "description", "difficulty",
        "options", "correct_answer", "explanation"
    ]

    for field in required_fields:
        if field not in question_data:
            return False, f"Missing required field: {field}"

    if not isinstance(question_data["knowledge_point_name"], str) or not question_data["knowledge_point_name"]:
        return False, "knowledge_point_name must be a non-empty string"

    if not isinstance(question_data["title"], str) or not question_data["title"]:
        return False, "title must be a non-empty string"

    if not isinstance(question_data["description"], str) or not question_data["description"]:
        return False, "description must be a non-empty string"

    if question_data["difficulty"] not in ["easy", "medium", "hard"]:
        return False, "difficulty must be 'easy', 'medium', or 'hard'"

    if not isinstance(question_data["options"], list) or len(question_data["options"]) < 2:
        return False, "options must be a list with at least 2 items"

    if not all(isinstance(opt, str) and opt for opt in question_data["options"]):
        return False, "all options must be non-empty strings"

    correct_answer = question_data["correct_answer"]
    if not isinstance(correct_answer, int) or not 0 <= correct_answer < len(question_data["options"]):
        return False, f"correct_answer must be an integer between 0 and {len(question_data['options']) - 1}"

    if not isinstance(question_data["explanation"], str) or not question_data["explanation"]:
        return False, "explanation must be a non-empty string"

    return True, None


async def get_knowledge_points_map(session: AsyncSession) -> Dict[str, KnowledgePoint]:
    """
    Retrieve all knowledge points from the database and return as a dictionary.

    Args:
        session: Async database session.

    Returns:
        Dictionary mapping knowledge point names to KnowledgePoint objects.

    Raises:
        Exception: If database query fails.
    """
    try:
        result = await session.execute(select(KnowledgePoint))
        knowledge_points = result.scalars().all()
        return {kp.name: kp for kp in knowledge_points}
    except Exception as e:
        raise Exception(f"Failed to retrieve knowledge points: {e}") from e


async def count_existing_questions(session: AsyncSession) -> int:
    """
    Count the number of existing quiz questions in the database.

    Args:
        session: Async database session.

    Returns:
        Number of existing questions.

    Raises:
        Exception: If database query fails.
    """
    try:
        result = await session.execute(select(QuizQuestion))
        return len(list(result.scalars().all()))
    except Exception as e:
        raise Exception(f"Failed to count existing questions: {e}") from e


async def add_question_to_database(
    session: AsyncSession,
    question_data: Dict[str, Any],
    knowledge_point: KnowledgePoint
) -> bool:
    """
    Add a single question to the database.

    Args:
        session: Async database session.
        question_data: Validated question data dictionary.
        knowledge_point: KnowledgePoint object to associate with the question.

    Returns:
        True if question was added successfully, False otherwise.

    Raises:
        Exception: If database operation fails.
    """
    try:
        question = QuizQuestion(
            knowledge_point_id=knowledge_point.id,
            title=question_data["title"],
            description=question_data["description"],
            difficulty=question_data["difficulty"],
            options=question_data["options"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"]
        )
        session.add(question)
        return True
    except Exception as e:
        raise Exception(f"Failed to create question '{question_data.get('title', 'unknown')}': {e}") from e


async def initialize_questions(
    session: AsyncSession,
    questions_data: List[Dict[str, Any]],
    min_existing_threshold: int = 3
) -> Tuple[int, int]:
    """
    Initialize quiz questions in the database.

    This function validates questions, checks for existing questions,
    and adds new questions only if the count is below the threshold.

    Args:
        session: Async database session.
        questions_data: List of question data dictionaries.
        min_existing_threshold: Minimum number of existing questions
            to skip initialization. Default is 3.

    Returns:
        Tuple of (added_count: int, skipped_count: int).

    Raises:
        Exception: If database operations fail.
    """
    knowledge_points_map = await get_knowledge_points_map(session)
    print(f"Found {len(knowledge_points_map)} knowledge points")

    existing_count = await count_existing_questions(session)
    print(f"Existing questions: {existing_count}")

    if existing_count >= min_existing_threshold:
        print("✓ Enough questions already exist, skipping initialization")
        return 0, len(questions_data)

    added_count = 0
    skipped_count = 0

    for question_data in questions_data:
        is_valid, error_msg = validate_question_data(question_data)
        if not is_valid:
            print(f"⚠ Skipping invalid question: {error_msg}")
            skipped_count += 1
            continue

        kp_name = question_data["knowledge_point_name"]
        if kp_name not in knowledge_points_map:
            print(f"⚠ Knowledge point '{kp_name}' not found, skipping question")
            skipped_count += 1
            continue

        try:
            await add_question_to_database(session, question_data, knowledge_points_map[kp_name])
            added_count += 1
            print(f"✓ Added: {question_data['title']}")
        except Exception as e:
            print(f"⚠ Failed to add question '{question_data['title']}': {e}")
            skipped_count += 1

    return added_count, skipped_count


async def init_questions() -> None:
    """
    Main function to initialize sample quiz questions.

    This function creates a database session, initializes questions,
    commits changes, and handles errors appropriately.

    Raises:
        Exception: If initialization fails critically.
    """
    try:
        async with AsyncSessionLocal() as session:
            added_count, skipped_count = await initialize_questions(
                session, SAMPLE_QUESTIONS, min_existing_threshold=3
            )

            if added_count > 0:
                await session.commit()
                print(f"\n✅ Successfully added {added_count} sample questions!")
            else:
                print(f"\n✓ No new questions added ({skipped_count} skipped)")

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        raise


def main() -> None:
    """
    Entry point for the script.

    Runs the async initialization function and handles system exit.
    """
    try:
        asyncio.run(init_questions())
    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


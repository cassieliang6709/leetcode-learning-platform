#!/usr/bin/env python3
"""
Initialize sample quiz questions with options and correct answers
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import select
from app.database import AsyncSessionLocal, engine
from app.models import QuizQuestion, KnowledgePoint


# Sample questions data
SAMPLE_QUESTIONS = [
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


async def init_questions():
    """Initialize sample quiz questions"""
    
    async with AsyncSessionLocal() as db:
        # Get knowledge points
        result = await db.execute(select(KnowledgePoint))
        knowledge_points = {kp.name: kp for kp in result.scalars().all()}
        
        print(f"Found {len(knowledge_points)} knowledge points")
        
        # Check if questions already exist
        result = await db.execute(select(QuizQuestion))
        existing_count = len(list(result.scalars().all()))
        print(f"Existing questions: {existing_count}")
        
        if existing_count >= 3:
            print("✓ Enough questions already exist, skipping initialization")
            return
        
        # Add sample questions
        added_count = 0
        for q_data in SAMPLE_QUESTIONS:
            kp_name = q_data["knowledge_point_name"]
            
            # Find or create knowledge point
            if kp_name not in knowledge_points:
                print(f"⚠ Knowledge point '{kp_name}' not found, skipping question")
                continue
            
            kp = knowledge_points[kp_name]
            
            # Create question
            question = QuizQuestion(
                knowledge_point_id=kp.id,
                title=q_data["title"],
                description=q_data["description"],
                difficulty=q_data["difficulty"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"]
            )
            db.add(question)
            added_count += 1
            print(f"✓ Added: {q_data['title']}")
        
        await db.commit()
        print(f"\n✅ Successfully added {added_count} sample questions!")


if __name__ == "__main__":
    asyncio.run(init_questions())


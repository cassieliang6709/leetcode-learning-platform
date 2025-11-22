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
        "title": "两数之和 (Two Sum)",
        "description": "给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，并返回它们的数组下标。",
        "difficulty": "easy",
        "options": [
            "使用暴力循环遍历所有可能的组合",
            "使用哈希表存储已遍历的元素及其索引",
            "先排序数组，然后使用双指针",
            "使用递归方法查找"
        ],
        "correct_answer": 1,
        "explanation": "使用哈希表可以在O(n)时间复杂度内解决问题，空间复杂度为O(n)。"
    },
    {
        "knowledge_point_name": "String",
        "title": "最长回文子串 (Longest Palindromic Substring)",
        "description": "给你一个字符串 s，找到 s 中最长的回文子串。",
        "difficulty": "medium",
        "options": [
            "暴力枚举所有子串并检查是否回文",
            "使用动态规划记录子串是否为回文",
            "从中心向两边扩展寻找回文",
            "使用哈希表记录字符出现位置"
        ],
        "correct_answer": 2,
        "explanation": "中心扩展法是最常用的方法，时间复杂度O(n²)，空间复杂度O(1)。"
    },
    {
        "knowledge_point_name": "Linked List",
        "title": "反转链表 (Reverse Linked List)",
        "description": "给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。",
        "difficulty": "easy",
        "options": [
            "使用递归方法反转",
            "使用栈存储所有节点再重建",
            "使用双指针迭代反转",
            "创建新链表并复制节点"
        ],
        "correct_answer": 2,
        "explanation": "双指针迭代法最优，时间复杂度O(n)，空间复杂度O(1)。"
    },
    {
        "knowledge_point_name": "Binary Tree",
        "title": "二叉树的最大深度",
        "description": "给定一个二叉树 root ，返回其最大深度。",
        "difficulty": "easy",
        "options": [
            "使用深度优先搜索(DFS)递归计算",
            "使用广度优先搜索(BFS)层序遍历",
            "使用栈模拟递归过程",
            "使用队列记录每层节点数"
        ],
        "correct_answer": 0,
        "explanation": "DFS递归是最简洁的方法：max_depth = max(left, right) + 1"
    },
    {
        "knowledge_point_name": "Dynamic Programming",
        "title": "爬楼梯 (Climbing Stairs)",
        "description": "假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？",
        "difficulty": "easy",
        "options": [
            "使用递归直接计算",
            "使用动态规划，dp[i] = dp[i-1] + dp[i-2]",
            "使用贪心算法选择最优步数",
            "使用回溯法枚举所有可能"
        ],
        "correct_answer": 1,
        "explanation": "这是经典的斐波那契数列问题，使用DP可以避免重复计算。"
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


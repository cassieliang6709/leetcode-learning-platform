#!/usr/bin/env python3
"""
数据库初始化脚本
创建表结构并插入基础数据
"""

import asyncio
import sys
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import engine, Base, init_db
from app.models import User, KnowledgePoint, QuizQuestion
from sqlalchemy import text


async def create_sample_data():
    """创建示例数据"""
    from app.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        try:
            # 检查是否已有数据
            result = await session.execute(text("SELECT COUNT(*) FROM knowledge_points"))
            count = result.scalar()
            
            if count > 0:
                print("✅ 数据库已有数据，跳过初始化")
                return
            
            # 创建知识点
            knowledge_points = [
                KnowledgePoint(
                    id=1,
                    name="Array & String",
                    description="基础数组和字符串操作",
                    difficulty_level=1
                ),
                KnowledgePoint(
                    id=2,
                    name="Hash Table",
                    description="哈希表的应用",
                    difficulty_level=1
                ),
                KnowledgePoint(
                    id=3,
                    name="Two Pointers",
                    description="双指针技巧",
                    difficulty_level=2
                ),
                KnowledgePoint(
                    id=4,
                    name="Binary Search",
                    description="二分查找及其变体",
                    difficulty_level=2
                ),
                KnowledgePoint(
                    id=5,
                    name="Linked List",
                    description="链表操作和技巧",
                    difficulty_level=2
                ),
                KnowledgePoint(
                    id=6,
                    name="Stack & Queue",
                    description="栈和队列的应用",
                    difficulty_level=2
                ),
                KnowledgePoint(
                    id=7,
                    name="Binary Tree",
                    description="二叉树遍历和操作",
                    difficulty_level=3
                ),
                KnowledgePoint(
                    id=8,
                    name="Dynamic Programming",
                    description="动态规划基础",
                    difficulty_level=3
                ),
                KnowledgePoint(
                    id=9,
                    name="Graph",
                    description="图的遍历和算法",
                    difficulty_level=3
                ),
            ]
            
            session.add_all(knowledge_points)
            await session.commit()
            print("✅ 创建了 9 个知识点")
            
            # 创建示例题目
            sample_questions = [
                QuizQuestion(
                    knowledge_point_id=1,
                    title="Two Sum",
                    description="Given an array of integers, return indices of two numbers that add up to a target.",
                    difficulty="Easy",
                    leetcode_url="https://leetcode.com/problems/two-sum/",
                    hint_strategy="Use a hash map to store values and their indices as you iterate.",
                    hint_code_example="Create a dictionary to map values to indices.",
                    hint_video_url="https://www.youtube.com/watch?v=KLlXCFG5TnA"
                ),
                QuizQuestion(
                    knowledge_point_id=2,
                    title="Valid Anagram",
                    description="Given two strings, determine if they are anagrams of each other.",
                    difficulty="Easy",
                    leetcode_url="https://leetcode.com/problems/valid-anagram/",
                    hint_strategy="Count the frequency of each character in both strings.",
                    hint_code_example="Use a hash map or array to count characters.",
                    hint_video_url="https://www.youtube.com/watch?v=9UtInBqnCgA"
                ),
            ]
            
            session.add_all(sample_questions)
            await session.commit()
            print("✅ 创建了示例题目")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            await session.rollback()
            raise


async def main():
    """主函数"""
    print("🚀 初始化数据库...")
    
    try:
        # 创建表
        print("📊 创建表结构...")
        await init_db()
        print("✅ 表创建成功")
        
        # 创建示例数据
        print("📝 创建示例数据...")
        await create_sample_data()
        
        print("✅ 数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


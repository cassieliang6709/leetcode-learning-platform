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
                    name="Array",
                    description="基础数组操作",
                    difficulty="easy",
                    category="basics",
                    order_index=1
                ),
                KnowledgePoint(
                    name="String",
                    description="字符串处理",
                    difficulty="easy",
                    category="basics",
                    order_index=2
                ),
                KnowledgePoint(
                    name="Hash Table",
                    description="哈希表的应用",
                    difficulty="easy",
                    category="data_structure",
                    order_index=3
                ),
                KnowledgePoint(
                    name="Two Pointers",
                    description="双指针技巧",
                    difficulty="medium",
                    category="technique",
                    order_index=4
                ),
                KnowledgePoint(
                    name="Linked List",
                    description="链表操作和技巧",
                    difficulty="medium",
                    category="data_structure",
                    order_index=5
                ),
                KnowledgePoint(
                    name="Binary Search",
                    description="二分查找及其变体",
                    difficulty="medium",
                    category="algorithm",
                    order_index=6
                ),
                KnowledgePoint(
                    name="Binary Tree",
                    description="二叉树遍历和操作",
                    difficulty="medium",
                    category="data_structure",
                    order_index=7
                ),
                KnowledgePoint(
                    name="Dynamic Programming",
                    description="动态规划基础",
                    difficulty="hard",
                    category="algorithm",
                    order_index=8
                ),
                KnowledgePoint(
                    name="Graph",
                    description="图的遍历和算法",
                    difficulty="hard",
                    category="algorithm",
                    order_index=9
                ),
            ]
            
            session.add_all(knowledge_points)
            await session.commit()
            print("✅ 创建了 9 个知识点")
            
            print("✅ 知识点创建成功，运行 init_sample_questions.py 添加题目")
            
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


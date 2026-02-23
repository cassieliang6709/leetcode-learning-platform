#!/usr/bin/env python3
"""
Database initialization script
Create table structure and insert basic data
"""

import asyncio
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from app.database import engine, Base, init_db
from app.models import User, KnowledgePoint, QuizQuestion
from sqlalchemy import text


async def create_sample_data():
    """Create sample data"""
    from app.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if data already exists
            result = await session.execute(text("SELECT COUNT(*) FROM knowledge_points"))
            count = result.scalar()
            
            if count > 0:
                print("✅ Database already has data, skipping initialization")
                return
            
            # Create knowledge points
            knowledge_points = [
                KnowledgePoint(
                    name="Array",
                    description="Basic array operations",
                    difficulty="easy",
                    category="basics",
                    order_index=1
                ),
                KnowledgePoint(
                    name="String",
                    description="String processing",
                    difficulty="easy",
                    category="basics",
                    order_index=2
                ),
                KnowledgePoint(
                    name="Hash Table",
                    description="Hash table applications",
                    difficulty="easy",
                    category="data_structure",
                    order_index=3
                ),
                KnowledgePoint(
                    name="Two Pointers",
                    description="Two pointer technique",
                    difficulty="medium",
                    category="technique",
                    order_index=4
                ),
                KnowledgePoint(
                    name="Linked List",
                    description="Linked list operations and techniques",
                    difficulty="medium",
                    category="data_structure",
                    order_index=5
                ),
                KnowledgePoint(
                    name="Binary Search",
                    description="Binary search and its variants",
                    difficulty="medium",
                    category="algorithm",
                    order_index=6
                ),
                KnowledgePoint(
                    name="Binary Tree",
                    description="Binary tree traversal and operations",
                    difficulty="medium",
                    category="data_structure",
                    order_index=7
                ),
                KnowledgePoint(
                    name="Dynamic Programming",
                    description="Dynamic programming basics",
                    difficulty="hard",
                    category="algorithm",
                    order_index=8
                ),
                KnowledgePoint(
                    name="Graph",
                    description="Graph traversal and algorithms",
                    difficulty="hard",
                    category="algorithm",
                    order_index=9
                ),
            ]
            
            session.add_all(knowledge_points)
            await session.commit()
            print("✅ Created 9 knowledge points")
            
            print("✅ Knowledge points created successfully, run init_sample_questions.py to add questions")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()
            raise


async def main():
    """Main function"""
    print("🚀 Initializing database...")
    
    try:
        # Create tables
        print("📊 Creating table structure...")
        await init_db()
        print("✅ Tables created successfully")
        
        # Create sample data
        print("📝 Creating sample data...")
        await create_sample_data()
        
        print("✅ Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


"""
Database initialization script
Creates tables and seeds initial data
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import engine, Base
from app.models import KnowledgePoint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async def init_database():
    """Initialize database with tables"""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created successfully")


async def seed_knowledge_points():
    """Seed initial knowledge points"""
    print("\nSeeding knowledge points...")

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        knowledge_points = [
            {
                "name": "Array Basics",
                "description": "Understanding arrays and basic operations",
                "difficulty": "easy",
                "category": "array",
                "order_index": 1
            },
            {
                "name": "Two Pointers",
                "description": "Using two pointer technique for array problems",
                "difficulty": "easy",
                "category": "array",
                "order_index": 2
            },
            {
                "name": "Hash Table",
                "description": "Using hash maps for O(1) lookups",
                "difficulty": "medium",
                "category": "hash_table",
                "order_index": 3
            },
            {
                "name": "Binary Search",
                "description": "Efficient searching in sorted arrays",
                "difficulty": "medium",
                "category": "search",
                "order_index": 4
            },
            {
                "name": "Sliding Window",
                "description": "Technique for subarray problems",
                "difficulty": "medium",
                "category": "array",
                "order_index": 5
            },
            {
                "name": "Linked List",
                "description": "Understanding and manipulating linked lists",
                "difficulty": "medium",
                "category": "linked_list",
                "order_index": 6
            },
            {
                "name": "Binary Tree Traversal",
                "description": "DFS and BFS on trees",
                "difficulty": "medium",
                "category": "tree",
                "order_index": 7
            },
            {
                "name": "Dynamic Programming",
                "description": "Solving problems with optimal substructure",
                "difficulty": "hard",
                "category": "dp",
                "order_index": 8
            },
            {
                "name": "Graph Algorithms",
                "description": "Graph traversal and shortest path",
                "difficulty": "hard",
                "category": "graph",
                "order_index": 9
            }
        ]

        for kp_data in knowledge_points:
            kp = KnowledgePoint(**kp_data)
            session.add(kp)

        await session.commit()
        print(f"✓ Seeded {len(knowledge_points)} knowledge points")


async def create_demo_user():
    """Create a demo user for testing"""
    print("\nCreating demo user...")
    from app.models import User

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        demo_user = User(
            username="demo_user",
            email="demo@example.com"
        )
        session.add(demo_user)
        await session.commit()
        print(f"✓ Created demo user (ID: {demo_user.id})")
        print(f"  Username: {demo_user.username}")
        print(f"  Email: {demo_user.email}")


async def main():
    """Run all initialization tasks"""
    print("=" * 50)
    print("DATABASE INITIALIZATION")
    print("=" * 50)

    try:
        await init_database()
        await seed_knowledge_points()
        await create_demo_user()

        print("\n" + "=" * 50)
        print("✓ Database initialization completed successfully!")
        print("=" * 50)
        print("\nYou can now start the backend server:")
        print("  cd backend && uvicorn main:app --reload")

    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


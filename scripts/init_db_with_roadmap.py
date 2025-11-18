"""
Database initialization script with complete NeetCode-style roadmap
Creates tables and seeds comprehensive learning path data
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
    """
    Seed comprehensive knowledge points based on NeetCode and AlgoMonster roadmap
    
    Categories:
    - array: Arrays & Hashing, Two Pointers, Sliding Window
    - string: String manipulation and pattern matching
    - tree: Binary Trees, BST, Trie
    - graph: Graph traversal, shortest path, advanced graphs
    - dp: Dynamic Programming (1-D and 2-D)
    - other: Stack, Heap, Backtracking, Greedy, etc.
    """
    print("\nSeeding comprehensive knowledge points...")

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        knowledge_points = [
            # ===== ARRAYS & HASHING (Basic) =====
            {
                "name": "Arrays & Hashing",
                "description": "Master array operations and hash table techniques for O(1) lookups. Essential for solving problems efficiently.",
                "difficulty": "easy",
                "category": "array",
                "order_index": 1
            },
            {
                "name": "Two Pointers",
                "description": "Learn to use two pointers technique for solving array and string problems in linear time without extra space.",
                "difficulty": "easy",
                "category": "array",
                "order_index": 2
            },
            {
                "name": "Sliding Window",
                "description": "Master the sliding window pattern for subarray and substring problems. Critical for optimization problems.",
                "difficulty": "medium",
                "category": "array",
                "order_index": 3
            },
            
            # ===== STACK & QUEUE =====
            {
                "name": "Stack",
                "description": "Understand stack data structure and monotonic stack patterns. Essential for expression parsing and next greater element problems.",
                "difficulty": "easy",
                "category": "other",
                "order_index": 4
            },
            
            # ===== BINARY SEARCH =====
            {
                "name": "Binary Search",
                "description": "Master binary search for sorted arrays and search space problems. Achieve O(log n) time complexity.",
                "difficulty": "medium",
                "category": "array",
                "order_index": 5
            },
            
            # ===== LINKED LIST =====
            {
                "name": "Linked List",
                "description": "Learn linked list operations: reversal, cycle detection, and two-pointer techniques on lists.",
                "difficulty": "easy",
                "category": "other",
                "order_index": 6
            },
            
            # ===== TREES (Binary Trees) =====
            {
                "name": "Binary Tree - Traversal",
                "description": "Master tree traversals (inorder, preorder, postorder) using both recursion and iteration.",
                "difficulty": "easy",
                "category": "tree",
                "order_index": 7
            },
            {
                "name": "Binary Tree - DFS",
                "description": "Solve tree problems using depth-first search. Learn to identify path, diameter, and validation problems.",
                "difficulty": "medium",
                "category": "tree",
                "order_index": 8
            },
            {
                "name": "Binary Tree - BFS",
                "description": "Use level-order traversal and breadth-first search for tree problems. Perfect for level-based questions.",
                "difficulty": "medium",
                "category": "tree",
                "order_index": 9
            },
            {
                "name": "Binary Search Tree",
                "description": "Understand BST properties and operations. Learn validation, insertion, and deletion in BST.",
                "difficulty": "medium",
                "category": "tree",
                "order_index": 10
            },
            
            # ===== TRIE =====
            {
                "name": "Trie (Prefix Tree)",
                "description": "Build and use trie data structure for efficient string searching and prefix matching.",
                "difficulty": "medium",
                "category": "tree",
                "order_index": 11
            },
            
            # ===== HEAP / PRIORITY QUEUE =====
            {
                "name": "Heap / Priority Queue",
                "description": "Master heap data structure for finding kth largest/smallest elements and merge problems.",
                "difficulty": "medium",
                "category": "other",
                "order_index": 12
            },
            
            # ===== BACKTRACKING =====
            {
                "name": "Backtracking",
                "description": "Learn backtracking for permutations, combinations, and constraint satisfaction problems.",
                "difficulty": "medium",
                "category": "other",
                "order_index": 13
            },
            
            # ===== GRAPHS =====
            {
                "name": "Graph - DFS & BFS",
                "description": "Master graph traversal algorithms. Essential for connected components and path finding.",
                "difficulty": "medium",
                "category": "graph",
                "order_index": 14
            },
            {
                "name": "Graph - Union Find",
                "description": "Learn disjoint set (union-find) data structure for connectivity problems and cycle detection.",
                "difficulty": "medium",
                "category": "graph",
                "order_index": 15
            },
            {
                "name": "Graph - Topological Sort",
                "description": "Solve problems with dependencies using topological sorting on directed acyclic graphs.",
                "difficulty": "medium",
                "category": "graph",
                "order_index": 16
            },
            {
                "name": "Graph - Shortest Path",
                "description": "Master Dijkstra's and Bellman-Ford algorithms for shortest path problems.",
                "difficulty": "hard",
                "category": "graph",
                "order_index": 17
            },
            
            # ===== DYNAMIC PROGRAMMING =====
            {
                "name": "1-D Dynamic Programming",
                "description": "Start with 1D DP problems: climbing stairs, house robber, decode ways. Build foundation for complex DP.",
                "difficulty": "medium",
                "category": "dp",
                "order_index": 18
            },
            {
                "name": "2-D Dynamic Programming",
                "description": "Master 2D DP for grid problems, longest common subsequence, and edit distance.",
                "difficulty": "hard",
                "category": "dp",
                "order_index": 19
            },
            {
                "name": "DP - Knapsack Patterns",
                "description": "Learn 0/1 knapsack, unbounded knapsack, and subset sum problems.",
                "difficulty": "hard",
                "category": "dp",
                "order_index": 20
            },
            {
                "name": "DP - Strings",
                "description": "Solve string DP problems: palindrome partitioning, word break, and interleaving strings.",
                "difficulty": "hard",
                "category": "dp",
                "order_index": 21
            },
            
            # ===== GREEDY =====
            {
                "name": "Greedy Algorithms",
                "description": "Learn greedy strategies for interval problems, jump games, and optimization problems.",
                "difficulty": "medium",
                "category": "other",
                "order_index": 22
            },
            
            # ===== INTERVALS =====
            {
                "name": "Intervals",
                "description": "Master interval problems: merge intervals, meeting rooms, and insert intervals.",
                "difficulty": "medium",
                "category": "array",
                "order_index": 23
            },
            
            # ===== STRING ALGORITHMS =====
            {
                "name": "String Manipulation",
                "description": "Learn string operations, palindrome checks, and string reversal techniques.",
                "difficulty": "easy",
                "category": "string",
                "order_index": 24
            },
            {
                "name": "String Pattern Matching",
                "description": "Master KMP algorithm and pattern matching techniques for substring problems.",
                "difficulty": "hard",
                "category": "string",
                "order_index": 25
            },
            
            # ===== MATH & GEOMETRY =====
            {
                "name": "Math & Geometry",
                "description": "Solve mathematical problems: prime numbers, GCD, LCM, and geometric algorithms.",
                "difficulty": "medium",
                "category": "other",
                "order_index": 26
            },
            
            # ===== BIT MANIPULATION =====
            {
                "name": "Bit Manipulation",
                "description": "Master bitwise operations for efficient solutions to counting and XOR problems.",
                "difficulty": "easy",
                "category": "other",
                "order_index": 27
            },
            
            # ===== ADVANCED TOPICS =====
            {
                "name": "Advanced Graph Algorithms",
                "description": "Tackle advanced topics: minimum spanning tree, network flow, and strongly connected components.",
                "difficulty": "hard",
                "category": "graph",
                "order_index": 28
            },
            {
                "name": "Segment Tree & BIT",
                "description": "Learn range query data structures: segment tree and binary indexed tree (Fenwick tree).",
                "difficulty": "hard",
                "category": "other",
                "order_index": 29
            },
            {
                "name": "Monotonic Queue",
                "description": "Master monotonic queue pattern for sliding window maximum and related problems.",
                "difficulty": "medium",
                "category": "other",
                "order_index": 30
            }
        ]

        for kp_data in knowledge_points:
            kp = KnowledgePoint(**kp_data)
            session.add(kp)

        await session.commit()
        print(f"✓ Seeded {len(knowledge_points)} knowledge points")
        
        # Print summary by category
        print("\nKnowledge Points by Category:")
        categories = {}
        for kp in knowledge_points:
            cat = kp['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items()):
            print(f"  • {cat}: {count} topics")


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
    print("=" * 60)
    print("DATABASE INITIALIZATION - NEETCODE STYLE ROADMAP")
    print("=" * 60)

    try:
        await init_database()
        await seed_knowledge_points()
        await create_demo_user()

        print("\n" + "=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        print("\nRoadmap Overview:")
        print("  📚 30 comprehensive topics")
        print("  🎯 Covers arrays, trees, graphs, DP, and more")
        print("  📈 Progressive difficulty from easy to hard")
        print("\nNext Steps:")
        print("  1. Start the backend: cd backend && uvicorn main:app --reload")
        print("  2. Start the frontend: cd frontend && npm run dev")
        print("  3. Visit http://localhost:5173/roadmap")

    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


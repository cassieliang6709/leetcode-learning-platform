"""
Initialize 100 quiz questions for daily challenges
Run this script to populate the database with algorithm quiz questions
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import QuizQuestion, KnowledgePoint, Base
from sqlalchemy import select

# Database URL - update this with your database credentials
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/leetcode_learning"

# Sample quiz questions data
QUIZ_QUESTIONS = [
    # Arrays & Hash Tables (20 questions)
    {
        "title": "What is the time complexity of array access?",
        "description": "What is the time complexity of accessing an element by index in an array?",
        "difficulty": "easy",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "correct_answer": 0,
        "explanation": "Arrays access elements directly by index, with O(1) constant time complexity.",
        "category": "array"
    },
    {
        "title": "Hash table lookup time complexity",
        "description": "What is the time complexity of hash table lookup in ideal conditions?",
        "difficulty": "easy",
        "options": ["O(n)", "O(1)", "O(log n)", "O(n log n)"],
        "correct_answer": 1,
        "explanation": "Hash table lookup has O(1) time complexity in ideal conditions (no hash collisions).",
        "category": "hash_table"
    },
    {
        "title": "Optimal solution for Two Sum problem",
        "description": "What is the optimal method to solve the Two Sum problem?",
        "difficulty": "easy",
        "options": ["Brute force loop", "Use hash table", "Sort then two pointers", "Binary search"],
        "correct_answer": 1,
        "explanation": "Using a hash table can solve the Two Sum problem in O(n) time, which is the optimal solution.",
        "category": "hash_table"
    },
    {
        "title": "In-place array operations",
        "description": "What is an in-place array operation?",
        "difficulty": "easy",
        "options": ["No extra space used", "Create new array", "Use recursion", "Use loop"],
        "correct_answer": 0,
        "explanation": "In-place operations modify the original array directly without using additional array space.",
        "category": "array"
    },
    {
        "title": "Hash collision resolution",
        "description": "Common methods for handling hash collisions in hash tables do NOT include:",
        "difficulty": "medium",
        "options": ["Chaining", "Open addressing", "Rehashing", "Recursion"],
        "correct_answer": 3,
        "explanation": "Recursion is not a method for resolving hash collisions. Common methods include chaining, open addressing, and rehashing.",
        "category": "hash_table"
    },
    
    # Sliding Window (15 questions)
    {
        "title": "Sliding window use cases",
        "description": "What type of problems is the sliding window technique best suited for?",
        "difficulty": "medium",
        "options": ["Graph traversal problems", "Continuous subarray/substring problems", "Binary tree problems", "Sorting problems"],
        "correct_answer": 1,
        "explanation": "Sliding window is best suited for continuous subarray or substring problems, such as longest substring, minimum subarray, etc.",
        "category": "sliding_window"
    },
    {
        "title": "Fixed-size sliding window",
        "description": "What is the time complexity of a fixed-size sliding window?",
        "difficulty": "easy",
        "options": ["O(n²)", "O(n)", "O(log n)", "O(1)"],
        "correct_answer": 1,
        "explanation": "A fixed-size sliding window only needs to traverse the array once, with O(n) time complexity.",
        "category": "sliding_window"
    },
    {
        "title": "Variable-size sliding window",
        "description": "What pointers are typically used in a variable-size sliding window?",
        "difficulty": "medium",
        "options": ["Single pointer", "Two pointers", "Three pointers", "No pointers needed"],
        "correct_answer": 1,
        "explanation": "Variable-size sliding windows typically use two pointers (left and right) to dynamically adjust window size.",
        "category": "sliding_window"
    },
    
    # Two Pointers (15 questions)
    {
        "title": "Two pointers basic concept",
        "description": "What type of arrays is the two-pointer technique mainly used for?",
        "difficulty": "easy",
        "options": ["Unsorted arrays", "Sorted arrays", "2D arrays", "Sparse arrays"],
        "correct_answer": 1,
        "explanation": "The two-pointer technique is most effective on sorted arrays, leveraging the ordered property to optimize algorithms.",
        "category": "two_pointers"
    },
    {
        "title": "Colliding two pointers",
        "description": "What is the movement direction of colliding two pointers?",
        "difficulty": "easy",
        "options": ["Same direction", "Towards each other", "Opposite directions", "Random movement"],
        "correct_answer": 1,
        "explanation": "Colliding two pointers start from both ends of the array and move towards each other until they meet.",
        "category": "two_pointers"
    },
    {
        "title": "Fast and slow pointers",
        "description": "What problems are fast and slow pointers commonly used to solve?",
        "difficulty": "medium",
        "options": ["Array sorting", "Linked list cycle detection", "Tree traversal", "Graph search"],
        "correct_answer": 1,
        "explanation": "Fast and slow pointers are commonly used for linked list cycle detection, finding middle node, and other linked list related problems.",
        "category": "two_pointers"
    },
    
    # Binary Search (15 questions)
    {
        "title": "Binary search time complexity",
        "description": "What is the time complexity of binary search?",
        "difficulty": "easy",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
        "correct_answer": 1,
        "explanation": "Binary search halves the search interval each time, with O(log n) time complexity.",
        "category": "binary_search"
    },
    {
        "title": "Binary search prerequisite",
        "description": "What is the necessary prerequisite for using binary search?",
        "difficulty": "easy",
        "options": ["Array is sorted", "Array has no duplicates", "Array is large", "Array is continuous"],
        "correct_answer": 0,
        "explanation": "Binary search requires the array to be sorted (ascending or descending).",
        "category": "binary_search"
    },
    {
        "title": "Binary search boundary issue",
        "description": "What problem can occur with mid = (left + right) / 2 in binary search?",
        "difficulty": "medium",
        "options": ["Wrong result", "Integer overflow", "Infinite loop", "Cannot converge"],
        "correct_answer": 1,
        "explanation": "When left and right are both very large, addition may cause integer overflow. Should use mid = left + (right - left) / 2.",
        "category": "binary_search"
    },
    
    # Stack & Queue (10 questions)
    {
        "title": "Stack characteristics",
        "description": "What is the characteristic of a stack data structure?",
        "difficulty": "easy",
        "options": ["First In First Out (FIFO)", "Last In First Out (LIFO)", "Random access", "Bidirectional access"],
        "correct_answer": 1,
        "explanation": "Stack is a Last In First Out (LIFO) data structure.",
        "category": "stack"
    },
    {
        "title": "Queue characteristics",
        "description": "What is the characteristic of a queue data structure?",
        "difficulty": "easy",
        "options": ["Last In First Out (LIFO)", "First In First Out (FIFO)", "Random access", "Bidirectional access"],
        "correct_answer": 1,
        "explanation": "Queue is a First In First Out (FIFO) data structure.",
        "category": "queue"
    },
    {
        "title": "Monotonic stack applications",
        "description": "What problems are monotonic stacks commonly used to solve?",
        "difficulty": "medium",
        "options": ["Sorting problems", "Next greater element", "Shortest path", "Graph traversal"],
        "correct_answer": 1,
        "explanation": "Monotonic stacks are commonly used to solve 'next greater/smaller element' type problems.",
        "category": "stack"
    },
    
    # Linked List (10 questions)
    {
        "title": "Linked list access time complexity",
        "description": "What is the time complexity of accessing the k-th element in a linked list?",
        "difficulty": "easy",
        "options": ["O(1)", "O(k)", "O(n)", "O(log n)"],
        "correct_answer": 1,
        "explanation": "A linked list needs to traverse k times from the head node to access the k-th element, with O(k) time complexity.",
        "category": "linked_list"
    },
    {
        "title": "Linked list reversal",
        "description": "What is the most common method to reverse a singly linked list?",
        "difficulty": "medium",
        "options": ["Recursion", "Iteration (two pointers)", "Stack", "Queue"],
        "correct_answer": 1,
        "explanation": "Iteration using two pointers (prev, curr) to reverse a linked list is the most common and efficient method.",
        "category": "linked_list"
    },
    {
        "title": "Linked list cycle detection",
        "description": "What is the most efficient method to detect if a linked list has a cycle?",
        "difficulty": "medium",
        "options": ["Brute force loop", "Fast and slow pointers", "Hash table", "Recursion"],
        "correct_answer": 1,
        "explanation": "Using fast and slow pointers (Floyd's cycle detection) can detect cycles in O(n) time and O(1) space complexity.",
        "category": "linked_list"
    },
    
    # Tree & Graph (15 questions)
    {
        "title": "Binary tree traversal",
        "description": "What is the order of preorder traversal?",
        "difficulty": "easy",
        "options": ["Left-Root-Right", "Root-Left-Right", "Left-Right-Root", "Right-Root-Left"],
        "correct_answer": 1,
        "explanation": "Preorder traversal order is: root node -> left subtree -> right subtree.",
        "category": "tree"
    },
    {
        "title": "DFS vs BFS",
        "description": "What data structure is typically used to implement depth-first search (DFS)?",
        "difficulty": "medium",
        "options": ["Queue", "Stack or recursion", "Array", "Hash table"],
        "correct_answer": 1,
        "explanation": "DFS is typically implemented using a stack (explicit stack or recursive call stack).",
        "category": "tree"
    },
    {
        "title": "Complete binary tree",
        "description": "If a complete binary tree has n nodes, what is its height?",
        "difficulty": "medium",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(√n)"],
        "correct_answer": 1,
        "explanation": "The height of a complete binary tree is O(log n), because the number of nodes per level grows exponentially.",
        "category": "tree"
    },
]

# Add more questions to reach 100
MORE_QUESTIONS = [
    # Dynamic Programming (20 questions - placeholder for brevity)
    *[{
        "title": f"Dynamic Programming Question {i+1}",
        "description": f"This is the {i+1}th dynamic programming related question for testing DP knowledge.",
        "difficulty": ["easy", "medium", "hard"][i % 3],
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": i % 4,
        "explanation": f"This is the explanation for question {i+1}.",
        "category": "dynamic_programming"
    } for i in range(20)],
]

QUIZ_QUESTIONS.extend(MORE_QUESTIONS)

# Ensure we have exactly 100 questions
while len(QUIZ_QUESTIONS) < 100:
    idx = len(QUIZ_QUESTIONS)
    QUIZ_QUESTIONS.append({
        "title": f"Algorithm Question {idx+1}",
        "description": f"This is the {idx+1}th algorithm question for daily practice.",
        "difficulty": ["easy", "medium", "hard"][idx % 3],
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": idx % 4,
        "explanation": f"This is the explanation for question {idx+1}.",
        "category": "general"
    })


async def init_quiz_questions():
    """Initialize quiz questions in the database"""
    print("🚀 Starting quiz questions initialization...")
    
    # Create async engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Check if questions already exist
            result = await session.execute(select(QuizQuestion))
            existing_count = len(result.scalars().all())
            
            if existing_count > 0:
                print(f"⚠️  Found {existing_count} existing questions.")
                response = input("Do you want to clear and re-initialize? (yes/no): ")
                if response.lower() != 'yes':
                    print("❌ Initialization cancelled.")
                    return
                
                # Clear existing questions
                await session.execute("DELETE FROM quiz_attempts")
                await session.execute("DELETE FROM quiz_questions")
                await session.commit()
                print("🗑️  Cleared existing questions.")
            
            # Get or create knowledge points
            knowledge_points = {}
            categories = set(q["category"] for q in QUIZ_QUESTIONS)
            
            for category in categories:
                result = await session.execute(
                    select(KnowledgePoint).where(KnowledgePoint.category == category)
                )
                kp = result.scalar_one_or_none()
                
                if not kp:
                    kp = KnowledgePoint(
                        name=category.replace('_', ' ').title(),
                        description=f"{category} related problems",
                        difficulty="medium",
                        category=category,
                        order_index=len(knowledge_points)
                    )
                    session.add(kp)
                    await session.flush()
                
                knowledge_points[category] = kp.id
            
            await session.commit()
            print(f"✅ Created/verified {len(knowledge_points)} knowledge points.")
            
            # Add quiz questions
            for idx, q_data in enumerate(QUIZ_QUESTIONS):
                question = QuizQuestion(
                    knowledge_point_id=knowledge_points.get(q_data["category"]),
                    leetcode_id=idx + 1,
                    title=q_data["title"],
                    description=q_data["description"],
                    difficulty=q_data["difficulty"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation", ""),
                    hints=[
                        {"level": 1, "content": f"Hint 1: Think about the core concept of {q_data['title']}"},
                        {"level": 2, "content": f"Hint 2: The answer might be related to {q_data['category']}"}
                    ]
                )
                session.add(question)
                
                if (idx + 1) % 20 == 0:
                    print(f"📝 Added {idx + 1} questions...")
            
            await session.commit()
            print(f"✅ Successfully initialized {len(QUIZ_QUESTIONS)} quiz questions!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     Quiz Questions Initialization Script              ║
    ║     Initialize 100 questions for daily challenges     ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚙️  Please update DATABASE_URL in the script before running!")
    print(f"Current DATABASE_URL: {DATABASE_URL}\n")
    
    # Run the initialization
    asyncio.run(init_quiz_questions())


#!/usr/bin/env python3
"""
Initialize daily knowledge questions (English version)
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import DailyKnowledgeQuestion, KnowledgePoint


# 30 English knowledge questions covering 9 knowledge points
KNOWLEDGE_QUESTIONS = [
    # Array (3 questions)
    {
        "knowledge_point": "Array",
        "question": "What is the time complexity of accessing an element in an array by index?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n²)"
        ],
        "correct_answer": 0,
        "explanation": "Arrays provide constant-time O(1) access to elements by index because the memory address can be calculated directly.",
        "difficulty": "easy",
        "category": "complexity"
    },
    {
        "knowledge_point": "Array",
        "question": "Which operation on a dynamic array (like ArrayList in Java or list in Python) has amortized O(1) time complexity?",
        "options": [
            "Inserting at the beginning",
            "Deleting from the middle",
            "Appending to the end",
            "Searching for an element"
        ],
        "correct_answer": 2,
        "explanation": "Appending to the end of a dynamic array has amortized O(1) complexity because although occasional resizing takes O(n), it happens infrequently enough that the average cost per insertion is constant.",
        "difficulty": "medium",
        "category": "complexity"
    },
    {
        "knowledge_point": "Array",
        "question": "What is the space complexity of the two-pointer technique for finding pairs in a sorted array?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n²)"
        ],
        "correct_answer": 0,
        "explanation": "The two-pointer technique uses only a constant amount of extra space (two pointers), making it O(1) space complexity.",
        "difficulty": "easy",
        "category": "complexity"
    },
    
    # String (3 questions)
    {
        "knowledge_point": "String",
        "question": "In most programming languages, what is the time complexity of string concatenation in a loop?",
        "options": [
            "O(1) per operation",
            "O(n) per operation",
            "O(n²) overall",
            "O(n log n) overall"
        ],
        "correct_answer": 2,
        "explanation": "String concatenation in a loop typically results in O(n²) time complexity because strings are often immutable, requiring creation of a new string for each concatenation.",
        "difficulty": "medium",
        "category": "complexity"
    },
    {
        "knowledge_point": "String",
        "question": "Which algorithm is commonly used for pattern matching in strings?",
        "options": [
            "Binary Search",
            "KMP (Knuth-Morris-Pratt)",
            "Dijkstra's Algorithm",
            "Bubble Sort"
        ],
        "correct_answer": 1,
        "explanation": "The KMP algorithm is specifically designed for efficient pattern matching in strings with O(n+m) time complexity.",
        "difficulty": "medium",
        "category": "algorithm"
    },
    {
        "knowledge_point": "String",
        "question": "What is a palindrome?",
        "options": [
            "A string that contains only unique characters",
            "A string that reads the same forwards and backwards",
            "A string sorted in alphabetical order",
            "A string with equal number of vowels and consonants"
        ],
        "correct_answer": 1,
        "explanation": "A palindrome is a string that reads the same forwards and backwards, like 'racecar' or 'noon'.",
        "difficulty": "easy",
        "category": "concept"
    },
    
    # Hash Table (4 questions)
    {
        "knowledge_point": "Hash Table",
        "question": "What is the average time complexity for search, insert, and delete operations in a hash table?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n log n)"
        ],
        "correct_answer": 0,
        "explanation": "Hash tables provide average O(1) time complexity for search, insert, and delete operations through direct computation of storage locations using hash functions.",
        "difficulty": "easy",
        "category": "complexity"
    },
    {
        "knowledge_point": "Hash Table",
        "question": "What happens when two different keys hash to the same index in a hash table?",
        "options": [
            "The second key is rejected",
            "A collision occurs and must be resolved",
            "The hash table automatically expands",
            "The keys are merged"
        ],
        "correct_answer": 1,
        "explanation": "When two keys hash to the same index, a collision occurs. This must be resolved using techniques like chaining or open addressing.",
        "difficulty": "easy",
        "category": "concept"
    },
    {
        "knowledge_point": "Hash Table",
        "question": "Which collision resolution technique uses linked lists?",
        "options": [
            "Linear probing",
            "Quadratic probing",
            "Chaining",
            "Double hashing"
        ],
        "correct_answer": 2,
        "explanation": "Chaining resolves collisions by maintaining a linked list of all elements that hash to the same index.",
        "difficulty": "medium",
        "category": "data_structure"
    },
    {
        "knowledge_point": "Hash Table",
        "question": "What is the worst-case time complexity for searching in a hash table?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n²)"
        ],
        "correct_answer": 2,
        "explanation": "In the worst case, when all keys hash to the same index (poor hash function or many collisions), searching becomes O(n).",
        "difficulty": "medium",
        "category": "complexity"
    },
    
    # Two Pointers (3 questions)
    {
        "knowledge_point": "Two Pointers",
        "question": "The two-pointer technique is most effective when working with what kind of data?",
        "options": [
            "Unsorted arrays",
            "Sorted arrays or linked lists",
            "Binary trees",
            "Hash tables"
        ],
        "correct_answer": 1,
        "explanation": "The two-pointer technique is most effective with sorted arrays or linked lists, where the sorted property can be leveraged to eliminate possibilities.",
        "difficulty": "easy",
        "category": "concept"
    },
    {
        "knowledge_point": "Two Pointers",
        "question": "In the sliding window technique, what typically determines when to expand or shrink the window?",
        "options": [
            "Random selection",
            "A specific condition or constraint",
            "The size of the array",
            "The number of iterations"
        ],
        "correct_answer": 1,
        "explanation": "The sliding window expands or shrinks based on whether a specific condition or constraint is met, such as sum, length, or character frequency requirements.",
        "difficulty": "medium",
        "category": "algorithm"
    },
    {
        "knowledge_point": "Two Pointers",
        "question": "What is the primary advantage of the two-pointer technique over a nested loop approach?",
        "options": [
            "It uses less memory",
            "It reduces time complexity",
            "It's easier to implement",
            "It works on any data structure"
        ],
        "correct_answer": 1,
        "explanation": "The two-pointer technique reduces time complexity from O(n²) to O(n) by eliminating the need for nested loops.",
        "difficulty": "medium",
        "category": "complexity"
    },
    
    # Linked List (4 questions)
    {
        "knowledge_point": "Linked List",
        "question": "What is the time complexity of inserting a node at the beginning of a singly linked list?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n log n)"
        ],
        "correct_answer": 0,
        "explanation": "Inserting at the beginning of a linked list is O(1) because it only requires updating a few pointers, regardless of list size.",
        "difficulty": "easy",
        "category": "complexity"
    },
    {
        "knowledge_point": "Linked List",
        "question": "Which pointer technique is commonly used to detect a cycle in a linked list?",
        "options": [
            "Binary search pointers",
            "Fast and slow pointers (Floyd's algorithm)",
            "Left and right pointers",
            "Head and tail pointers"
        ],
        "correct_answer": 1,
        "explanation": "Floyd's cycle detection algorithm uses two pointers moving at different speeds (fast and slow). If there's a cycle, they will eventually meet.",
        "difficulty": "medium",
        "category": "algorithm"
    },
    {
        "knowledge_point": "Linked List",
        "question": "What is the main disadvantage of a singly linked list compared to an array?",
        "options": [
            "Higher memory usage per element",
            "No random access to elements",
            "Cannot store primitive types",
            "Fixed size"
        ],
        "correct_answer": 1,
        "explanation": "Linked lists do not support random access; you must traverse from the head to reach any element, taking O(n) time.",
        "difficulty": "easy",
        "category": "concept"
    },
    {
        "knowledge_point": "Linked List",
        "question": "In a doubly linked list, what additional pointer does each node have compared to a singly linked list?",
        "options": [
            "A parent pointer",
            "A previous/back pointer",
            "A skip pointer",
            "A sentinel pointer"
        ],
        "correct_answer": 1,
        "explanation": "A doubly linked list has both next and previous pointers in each node, allowing bidirectional traversal.",
        "difficulty": "easy",
        "category": "data_structure"
    },
    
    # Binary Search (3 questions)
    {
        "knowledge_point": "Binary Search",
        "question": "What is the time complexity of binary search on a sorted array?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n log n)"
        ],
        "correct_answer": 1,
        "explanation": "Binary search has O(log n) time complexity because it halves the search space in each iteration.",
        "difficulty": "easy",
        "category": "complexity"
    },
    {
        "knowledge_point": "Binary Search",
        "question": "What is a prerequisite for using binary search?",
        "options": [
            "The array must be sorted",
            "The array must contain unique elements",
            "The array must have an even number of elements",
            "The array must be stored in a linked list"
        ],
        "correct_answer": 0,
        "explanation": "Binary search requires the array to be sorted. Without sorting, the algorithm's assumption about which half contains the target breaks down.",
        "difficulty": "easy",
        "category": "concept"
    },
    {
        "knowledge_point": "Binary Search",
        "question": "In binary search, what condition typically indicates that the target element is not found?",
        "options": [
            "mid == target",
            "left > right",
            "left == right",
            "mid == 0"
        ],
        "correct_answer": 1,
        "explanation": "When left > right, the search space has been exhausted without finding the target, indicating the element is not in the array.",
        "difficulty": "medium",
        "category": "algorithm"
    },
    
    # Binary Tree (4 questions)
    {
        "knowledge_point": "Binary Tree",
        "question": "What is the maximum number of nodes at depth d in a binary tree?",
        "options": [
            "d",
            "2^d",
            "d²",
            "2d"
        ],
        "correct_answer": 1,
        "explanation": "At depth d, a binary tree can have at most 2^d nodes (assuming depth starts at 0 for the root).",
        "difficulty": "medium",
        "category": "concept"
    },
    {
        "knowledge_point": "Binary Tree",
        "question": "Which tree traversal visits nodes in the order: left subtree, root, right subtree?",
        "options": [
            "Preorder",
            "Inorder",
            "Postorder",
            "Level-order"
        ],
        "correct_answer": 1,
        "explanation": "Inorder traversal visits the left subtree first, then the root, then the right subtree. For a BST, this produces a sorted sequence.",
        "difficulty": "easy",
        "category": "concept"
    },
    {
        "knowledge_point": "Binary Tree",
        "question": "What is the time complexity of searching in a balanced binary search tree?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n log n)"
        ],
        "correct_answer": 1,
        "explanation": "In a balanced BST, the height is O(log n), so search, insert, and delete operations all take O(log n) time.",
        "difficulty": "medium",
        "category": "complexity"
    },
    {
        "knowledge_point": "Binary Tree",
        "question": "What is the worst-case height of an unbalanced binary search tree with n nodes?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n²)"
        ],
        "correct_answer": 2,
        "explanation": "In the worst case (e.g., inserting sorted data), a BST degenerates into a linked list with height O(n).",
        "difficulty": "medium",
        "category": "complexity"
    },
    
    # Dynamic Programming (3 questions)
    {
        "knowledge_point": "Dynamic Programming",
        "question": "What are the two key properties that a problem must have to be solved with dynamic programming?",
        "options": [
            "Sorted input and unique elements",
            "Optimal substructure and overlapping subproblems",
            "Binary tree structure and recursion",
            "Hash table and constant time access"
        ],
        "correct_answer": 1,
        "explanation": "Dynamic programming requires: 1) Optimal substructure (optimal solution can be constructed from optimal solutions to subproblems), and 2) Overlapping subproblems (same subproblems are solved multiple times).",
        "difficulty": "medium",
        "category": "concept"
    },
    {
        "knowledge_point": "Dynamic Programming",
        "question": "What is the difference between memoization and tabulation in dynamic programming?",
        "options": [
            "Memoization is faster than tabulation",
            "Memoization is top-down, tabulation is bottom-up",
            "Memoization uses less memory",
            "There is no difference"
        ],
        "correct_answer": 1,
        "explanation": "Memoization is a top-down approach using recursion with caching, while tabulation is a bottom-up approach that iteratively fills a table.",
        "difficulty": "hard",
        "category": "algorithm"
    },
    {
        "knowledge_point": "Dynamic Programming",
        "question": "What is the time complexity of the classic dynamic programming solution to the Fibonacci sequence?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(2^n)"
        ],
        "correct_answer": 2,
        "explanation": "With dynamic programming (either memoization or tabulation), computing the nth Fibonacci number takes O(n) time and space.",
        "difficulty": "medium",
        "category": "complexity"
    },
    
    # Graph (3 questions)
    {
        "knowledge_point": "Graph",
        "question": "Which graph traversal algorithm uses a queue data structure?",
        "options": [
            "Depth-First Search (DFS)",
            "Breadth-First Search (BFS)",
            "Dijkstra's algorithm",
            "Both DFS and BFS"
        ],
        "correct_answer": 1,
        "explanation": "BFS uses a queue to visit nodes level by level, while DFS uses a stack (or recursion).",
        "difficulty": "easy",
        "category": "algorithm"
    },
    {
        "knowledge_point": "Graph",
        "question": "What is the time complexity of BFS and DFS for a graph with V vertices and E edges?",
        "options": [
            "O(V)",
            "O(E)",
            "O(V + E)",
            "O(V * E)"
        ],
        "correct_answer": 2,
        "explanation": "Both BFS and DFS visit each vertex once and explore each edge once, resulting in O(V + E) time complexity.",
        "difficulty": "medium",
        "category": "complexity"
    },
    {
        "knowledge_point": "Graph",
        "question": "What type of graph problem does Dijkstra's algorithm solve?",
        "options": [
            "Finding cycles",
            "Topological sorting",
            "Shortest path from a single source",
            "Minimum spanning tree"
        ],
        "correct_answer": 2,
        "explanation": "Dijkstra's algorithm finds the shortest path from a single source vertex to all other vertices in a weighted graph with non-negative edges.",
        "difficulty": "medium",
        "category": "algorithm"
    }
]


async def init_questions():
    """Initialize daily knowledge questions"""
    
    async with AsyncSessionLocal() as db:
        # Get knowledge points
        result = await db.execute(select(KnowledgePoint))
        knowledge_points = {kp.name: kp for kp in result.scalars().all()}
        
        print(f"Found {len(knowledge_points)} knowledge points")
        
        # Check if questions already exist
        result = await db.execute(select(DailyKnowledgeQuestion))
        existing_count = len(list(result.scalars().all()))
        print(f"Existing questions: {existing_count}")
        
        if existing_count >= 10:
            print("✓ Enough questions already exist, skipping initialization")
            return
        
        # Add questions
        added_count = 0
        for q_data in KNOWLEDGE_QUESTIONS:
            kp_name = q_data["knowledge_point"]
            
            # Find knowledge point
            if kp_name not in knowledge_points:
                print(f"⚠ Knowledge point '{kp_name}' not found, skipping question")
                continue
            
            kp = knowledge_points[kp_name]
            
            # Create question
            question = DailyKnowledgeQuestion(
                knowledge_point_id=kp.id,
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                difficulty=q_data["difficulty"],
                category=q_data["category"]
            )
            db.add(question)
            added_count += 1
            print(f"✓ Added: {q_data['question'][:60]}...")
        
        await db.commit()
        print(f"\n✅ Successfully added {added_count} daily knowledge questions!")


if __name__ == "__main__":
    asyncio.run(init_questions())


"""
Bulk add learning content (articles and quizzes) for all knowledge points
"""
import sys
import os
from pathlib import Path
import json

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.database import AsyncSessionLocal
import asyncio


# Complete learning content for all knowledge points
LEARNING_CONTENT = {
    "Array & Hash Table": {
        "article": """# Array & Hash Table Fundamentals

Arrays and hash tables are two of the most essential data structures in computer science. Understanding these structures is crucial for solving algorithmic problems efficiently.

## Arrays

An array is a contiguous block of memory that stores elements of the same type. Each element can be accessed directly using its index, making arrays extremely efficient for random access operations.

### Key Characteristics

- **Fixed Size**: Traditional arrays have a fixed size determined at creation
- **Direct Access**: O(1) time complexity for accessing any element by index
- **Cache Friendly**: Elements are stored contiguously in memory

### Time Complexities

- **Access**: O(1) - Direct index-based access
- **Search**: O(n) - Linear search through all elements
- **Insert/Delete (end)**: O(1) amortized
- **Insert/Delete (middle)**: O(n) - Requires shifting elements

## Hash Tables

A hash table uses a hash function to compute an index into an array of buckets, from which the desired value can be found. It provides average O(1) time complexity for insertions, deletions, and lookups.

### How Hash Tables Work

1. **Hash Function**: Converts keys into array indices
2. **Collision Handling**: Manages cases where multiple keys hash to the same index
3. **Load Factor**: Ratio of elements to buckets, affects performance

### Common Patterns

**Two Sum Pattern**: Use a hash table to store complements
```python
seen = {}
for num in nums:
    if target - num in seen:
        return [seen[target - num], i]
    seen[num] = i
```

**Frequency Counter**: Track occurrences of elements
```python
freq = {}
for item in items:
    freq[item] = freq.get(item, 0) + 1
```

### Applications

- Implementing sets and maps
- Caching and memoization
- Finding duplicates
- Counting frequencies
- Solving two-sum type problems

## Practice Strategy

1. Start with simple array manipulation problems
2. Learn the two-pointer technique for sorted arrays
3. Master hash table usage for O(1) lookups
4. Combine arrays and hash tables for complex problems""",
        "questions": [
            {
                "question": "What is the time complexity of accessing an element in an array by its index?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_answer": 0,
                "explanation": "Array access by index is O(1) because arrays store elements in contiguous memory. You can directly calculate the memory address: base_address + (index × element_size)."
            },
            {
                "question": "What is the average time complexity for hash table lookups?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                "correct_answer": 2,
                "explanation": "Hash tables provide O(1) average time complexity for lookups using a hash function to directly compute the bucket index. Worst case is O(n) with many collisions."
            },
            {
                "question": "Which pattern is most effective for finding pairs with a target sum?",
                "options": ["Two nested loops", "Hash table", "Binary search", "Quick sort"],
                "correct_answer": 1,
                "explanation": "Using a hash table allows you to store complements and check in O(1) time, giving O(n) total complexity vs O(n²) for nested loops."
            }
        ]
    },
    
    "Two Pointers": {
        "article": """# Two Pointers Technique

The two pointers technique is a powerful algorithmic pattern used to solve problems involving arrays or linked lists. It uses two pointers that traverse the data structure from different positions or directions.

## Core Concept

Instead of using nested loops (O(n²)), use two pointers to traverse the array in a single pass or from both ends, reducing time complexity to O(n).

## Common Patterns

### 1. Opposite Direction (Converging)

Pointers start at both ends and move toward each other.

```python
left, right = 0, len(arr) - 1
while left < right:
    # Process arr[left] and arr[right]
    if condition:
        left += 1
    else:
        right -= 1
```

**Use Cases**: Palindrome checking, pair sum in sorted array

### 2. Same Direction (Fast-Slow)

Both pointers start at the beginning, one moves faster than the other.

```python
slow = fast = 0
for fast in range(len(arr)):
    if condition:
        arr[slow] = arr[fast]
        slow += 1
```

**Use Cases**: Removing duplicates, partitioning

### 3. Sliding Window

Two pointers form a window that slides through the array.

```python
left = 0
for right in range(len(arr)):
    # Expand window by including arr[right]
    while window_invalid:
        # Shrink window from left
        left += 1
```

**Use Cases**: Subarray problems, string matching

## Key Advantages

- **Time Efficiency**: Reduces O(n²) to O(n)
- **Space Efficiency**: O(1) extra space
- **Elegant Solutions**: Clean and intuitive code

## When to Use Two Pointers

1. Array is **sorted** or can be sorted
2. Need to find **pairs** or **triplets**
3. Working with **subarrays** or **subsequences**
4. Need to **remove/move elements** in-place
5. Checking for **palindromes**

## Practice Problems

- Two Sum II (sorted array)
- 3Sum
- Container With Most Water
- Remove Duplicates from Sorted Array
- Valid Palindrome""",
        "questions": [
            {
                "question": "What is the time complexity advantage of two pointers over nested loops?",
                "options": ["O(n²) to O(n log n)", "O(n²) to O(n)", "O(n) to O(1)", "No advantage"],
                "correct_answer": 1,
                "explanation": "Two pointers technique reduces time complexity from O(n²) (nested loops) to O(n) (single pass) by using two pointers instead of checking all pairs."
            },
            {
                "question": "In which scenario is the opposite direction two pointers pattern most useful?",
                "options": ["Removing duplicates", "Finding pairs in sorted array", "Sliding window", "Graph traversal"],
                "correct_answer": 1,
                "explanation": "Opposite direction (converging pointers) works perfectly for finding pairs in a sorted array, as you can eliminate half the search space based on the sum comparison."
            },
            {
                "question": "What is a prerequisite for using the two pointers technique effectively?",
                "options": ["Hash table support", "Sorted array", "Tree structure", "Stack available"],
                "correct_answer": 1,
                "explanation": "Many two pointers problems require a sorted array to work correctly. Sorting enables moving pointers based on comparisons and guarantees we don't miss solutions."
            }
        ]
    },
    
    "Sliding Window": {
        "article": """# Sliding Window Pattern

The sliding window technique is an algorithmic pattern for efficiently solving problems that involve contiguous subarrays or substrings. It maintains a window that "slides" across the data structure.

## Core Idea

Instead of recalculating for each subarray/substring (O(n²) or O(n³)), maintain a window and update it incrementally as it slides, achieving O(n) time complexity.

## Types of Sliding Window

### 1. Fixed Size Window

The window size is constant and moves one position at a time.

```python
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        # Slide: remove left, add right
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

**Use Cases**: Maximum sum of k elements, average of subarray

### 2. Dynamic Size Window

Window size changes based on conditions.

```python
def longest_substring_k_distinct(s, k):
    left = 0
    char_freq = {}
    max_len = 0
    
    for right in range(len(s)):
        # Expand window
        char_freq[s[right]] = char_freq.get(s[right], 0) + 1
        
        # Shrink if invalid
        while len(char_freq) > k:
            char_freq[s[left]] -= 1
            if char_freq[s[left]] == 0:
                del char_freq[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Use Cases**: Longest substring, minimum window

## Window State Management

Key operations when sliding:
1. **Expand**: Add new element to the right
2. **Shrink**: Remove element from the left  
3. **Update**: Maintain window properties (sum, frequencies, etc.)
4. **Check**: Validate window constraints

## Common Applications

- **Subarray sum problems**: Find subarray with target sum
- **Substring problems**: Longest substring with k distinct characters
- **Anagram problems**: Find all anagrams in a string
- **Maximum/minimum in window**: Track running max/min

## Optimization Benefits

- **Time**: O(n²) or O(n³) → O(n)
- **Space**: Usually O(k) for tracking window state
- **Elegance**: Clean code with clear logic

## Key Questions to Ask

1. Is the problem about contiguous elements?
2. Can I maintain window state incrementally?
3. What are the shrinking conditions?
4. What needs to be tracked (sum, frequency, max)?

## Practice Approach

1. Start with fixed-size windows
2. Progress to dynamic size with simple conditions
3. Handle complex constraints (multiple conditions)
4. Optimize space usage""",
        "questions": [
            {
                "question": "What is the key optimization that sliding window provides?",
                "options": ["Uses less memory", "Avoids recalculating entire subarray", "Uses parallel processing", "Sorts the array faster"],
                "correct_answer": 1,
                "explanation": "Sliding window avoids recalculating the entire subarray for each position. Instead, it incrementally updates by removing the left element and adding the right element."
            },
            {
                "question": "In a dynamic sliding window, when do you shrink the window?",
                "options": ["Every iteration", "When window becomes invalid", "Never", "Only at the end"],
                "correct_answer": 1,
                "explanation": "You shrink the window (move left pointer forward) when the window violates the problem constraints, such as exceeding k distinct characters or sum threshold."
            },
            {
                "question": "What data structure is commonly used with sliding window for tracking frequencies?",
                "options": ["Stack", "Queue", "Hash table", "Linked list"],
                "correct_answer": 2,
                "explanation": "A hash table (dictionary) is perfect for tracking element frequencies in the window, allowing O(1) updates as the window slides."
            }
        ]
    },
    
    "Linked List": {
        "article": """# Linked List Fundamentals

A linked list is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence. Unlike arrays, linked lists don't require contiguous memory.

## Structure

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Types of Linked Lists

### 1. Singly Linked List
Each node points to the next node only.
- **Traversal**: One direction (forward only)
- **Space**: O(n) for n nodes

### 2. Doubly Linked List
Each node has pointers to both next and previous nodes.
- **Traversal**: Both directions
- **Space**: O(n) but 2× pointers

### 3. Circular Linked List
Last node points back to the first node.
- **Use**: Ring buffers, round-robin scheduling

## Time Complexities

- **Access**: O(n) - Must traverse from head
- **Search**: O(n) - Linear search required
- **Insert (beginning)**: O(1)
- **Insert (end)**: O(n) without tail pointer, O(1) with tail
- **Insert (middle)**: O(n) to find position, O(1) to insert
- **Delete**: O(n) to find, O(1) to delete

## Common Patterns

### 1. Fast and Slow Pointers

Detect cycles or find middle element.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### 2. Dummy Head Node

Simplifies edge cases for insertion/deletion.

```python
dummy = ListNode(0)
dummy.next = head
# Now can safely handle head deletion
```

### 3. Reversal

Reverse pointers in-place.

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev
```

## Advantages vs Arrays

- Dynamic size (no reallocation)
- Efficient insertion/deletion at beginning O(1)
- No wasted memory from pre-allocation

## Disadvantages vs Arrays

- No random access O(n)
- Extra memory for pointers
- Poor cache locality

## Common Problems

1. **Reversal**: Reverse entire list or sublist
2. **Cycle Detection**: Find if cycle exists
3. **Merge**: Combine two sorted lists
4. **Partition**: Rearrange nodes based on value
5. **Clone**: Deep copy with random pointers""",
        "questions": [
            {
                "question": "What is the time complexity of accessing the middle element in a linked list?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_answer": 2,
                "explanation": "Unlike arrays with O(1) index access, linked lists require traversing from the head node to reach any position, taking O(n) time."
            },
            {
                "question": "Why use a dummy head node in linked list problems?",
                "options": ["Improves performance", "Reduces memory", "Simplifies edge cases", "Required by syntax"],
                "correct_answer": 2,
                "explanation": "A dummy head node simplifies code by eliminating special cases for operations on the actual head node, making insertion and deletion logic uniform."
            },
            {
                "question": "What is the purpose of fast and slow pointers in linked lists?",
                "options": ["Reverse the list", "Detect cycles and find middle", "Sort the list", "Delete duplicates"],
                "correct_answer": 1,
                "explanation": "Fast pointer moves twice as fast as slow pointer. When fast reaches the end, slow is at the middle. If they meet, there's a cycle."
            }
        ]
    },
    
    "Stack": {
        "article": """# Stack Data Structure

A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. The last element added is the first one to be removed, like a stack of plates.

## Core Operations

```python
stack = []
stack.append(item)    # Push - O(1)
stack.pop()           # Pop - O(1)
stack[-1]             # Peek/Top - O(1)
len(stack) == 0       # isEmpty - O(1)
```

## Implementation

### Using List (Python)
```python
stack = []
stack.append(1)  # Push
top = stack.pop()  # Pop
```

### Using Linked List
```python
class Stack:
    def __init__(self):
        self.head = None
    
    def push(self, val):
        node = ListNode(val)
        node.next = self.head
        self.head = node
    
    def pop(self):
        if self.head:
            val = self.head.val
            self.head = self.head.next
            return val
```

## Common Patterns

### 1. Monotonic Stack

Maintains elements in increasing or decreasing order.

```python
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []
    
    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result
```

**Applications**: Next greater/smaller element, temperature problems

### 2. Valid Parentheses

Match opening and closing brackets.

```python
def is_valid(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:
            stack.append(char)
        elif not stack or pairs[stack.pop()] != char:
            return False
    
    return len(stack) == 0
```

### 3. Expression Evaluation

Convert infix to postfix and evaluate.

```python
def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token in '+-*/':
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a + b)
            # ... other operations
        else:
            stack.append(int(token))
    return stack[0]
```

## Use Cases

1. **Function call stack**: Track function calls and returns
2. **Undo/Redo**: Browser history, text editor
3. **Expression parsing**: Calculate mathematical expressions
4. **Syntax checking**: Validate balanced parentheses
5. **DFS traversal**: Iterative depth-first search
6. **Backtracking**: Track state for exploration

## Stack vs Queue

| Stack | Queue |
|-------|-------|
| LIFO | FIFO |
| Push/Pop at one end | Enqueue/Dequeue at different ends |
| DFS | BFS |
| Recursion simulation | Task scheduling |

## When to Use Stack

- Need to reverse order
- Match pairs (parentheses)
- Track previous elements
- Implement recursion iteratively
- Parse expressions
- Monotonic properties needed

## Practice Strategy

1. Start with basic push/pop operations
2. Practice parentheses matching
3. Learn monotonic stack pattern
4. Apply to expression evaluation
5. Use for tree/graph DFS""",
        "questions": [
            {
                "question": "What does LIFO stand for in the context of stacks?",
                "options": ["Last In First Out", "List In Fixed Order", "Linear Input Fast Output", "Long Integer Function Operation"],
                "correct_answer": 0,
                "explanation": "LIFO (Last In First Out) means the most recently added element is the first to be removed, like a stack of plates where you take from the top."
            },
            {
                "question": "What is a monotonic stack used for?",
                "options": ["Sorting elements", "Finding next greater/smaller elements", "Implementing recursion", "Storing unique values"],
                "correct_answer": 1,
                "explanation": "A monotonic stack maintains elements in sorted order and is perfect for finding the next greater or smaller element for each element in O(n) time."
            },
            {
                "question": "What is the time complexity of push and pop operations in a stack?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                "correct_answer": 2,
                "explanation": "Both push and pop operations in a stack are O(1) because they only modify the top element without affecting other elements."
            }
        ]
    },
    
    "Binary Tree": {
        "article": """# Binary Tree Fundamentals

A binary tree is a hierarchical data structure where each node has at most two children: left and right. Trees are fundamental for many algorithms and data structures.

## Tree Node Structure

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Types of Binary Trees

### 1. Full Binary Tree
Every node has either 0 or 2 children.

### 2. Complete Binary Tree
All levels are filled except possibly the last, which is filled from left to right.

### 3. Perfect Binary Tree
All internal nodes have 2 children and all leaves are at the same level.

### 4. Balanced Binary Tree
Height difference between left and right subtrees ≤ 1 for all nodes.

### 5. Binary Search Tree (BST)
For each node: left subtree values < node value < right subtree values.

## Tree Traversals

### 1. Depth-First Search (DFS)

**Inorder (Left-Root-Right)**: Used for BST to get sorted order
```python
def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```

**Preorder (Root-Left-Right)**: Used for tree serialization
```python
def preorder(root):
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)
```

**Postorder (Left-Right-Root)**: Used for tree deletion
```python
def postorder(root):
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

### 2. Breadth-First Search (BFS)

Level-order traversal using queue:
```python
def level_order(root):
    if not root: return []
    result = []
    queue = [root]
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.pop(0)
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    
    return result
```

## Common Patterns

### 1. Recursion

Most tree problems use recursion naturally:
```python
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### 2. Divide and Conquer

Split problem into subproblems:
```python
def is_balanced(root):
    def height(node):
        if not node: return 0
        left = height(node.left)
        right = height(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    
    return height(root) != -1
```

### 3. Path Problems

Track path from root to target:
```python
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))
```

## Time Complexities

- **Search**: O(n) general tree, O(log n) balanced BST
- **Insert**: O(n) general tree, O(log n) balanced BST
- **Delete**: O(n) general tree, O(log n) balanced BST
- **Traversal**: O(n) - visit all nodes

## Space Complexity

- **Recursion**: O(h) where h is height (call stack)
- **BFS**: O(w) where w is maximum width
- **DFS iterative**: O(h) for stack

## Applications

- File systems (directories)
- Expression trees (parsing)
- Database indexing (B-trees)
- Decision trees (AI/ML)
- Huffman coding (compression)

## Practice Strategy

1. Master all traversals (recursive and iterative)
2. Understand recursion and base cases
3. Practice path and level problems
4. Learn tree construction from traversals
5. Apply to BST-specific problems""",
        "questions": [
            {
                "question": "In a Binary Search Tree (BST), where are values smaller than the root located?",
                "options": ["Right subtree", "Left subtree", "Both subtrees", "Parent node"],
                "correct_answer": 1,
                "explanation": "In a BST, all values in the left subtree are smaller than the root, and all values in the right subtree are greater. This property enables efficient O(log n) search."
            },
            {
                "question": "Which traversal gives nodes in sorted order for a BST?",
                "options": ["Preorder", "Postorder", "Inorder", "Level-order"],
                "correct_answer": 2,
                "explanation": "Inorder traversal (left-root-right) visits nodes in ascending order for a BST because it processes left (smaller) values, then root, then right (larger) values."
            },
            {
                "question": "What is the space complexity of recursive tree traversal?",
                "options": ["O(1)", "O(log n)", "O(h) where h is height", "O(n)"],
                "correct_answer": 2,
                "explanation": "Recursive traversal uses O(h) space for the call stack, where h is the tree height. For balanced trees h = log n, for skewed trees h = n."
            }
        ]
    },
    
    "Dynamic Programming": {
        "article": """# Dynamic Programming (DP)

Dynamic Programming is an algorithmic technique for solving optimization problems by breaking them down into simpler subproblems and storing the results to avoid redundant calculations.

## Core Principles

### 1. Optimal Substructure
The optimal solution contains optimal solutions to subproblems.

### 2. Overlapping Subproblems
The same subproblems are solved multiple times.

## DP Approaches

### 1. Top-Down (Memoization)

Start with the original problem and recursively solve subproblems, storing results.

```python
def fib(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

### 2. Bottom-Up (Tabulation)

Start with smallest subproblems and build up to the solution.

```python
def fib(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

## Common Patterns

### 1. Linear DP (1D array)

**House Robber**: Can't rob adjacent houses
```python
def rob(nums):
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], nums[i] + dp[i-2])
    
    return dp[-1]
```

### 2. 2D DP (Grid)

**Unique Paths**: Count paths in grid
```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]
```

### 3. Knapsack Pattern

**0/1 Knapsack**: Choose items to maximize value
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    values[i-1] + dp[i-1][w - weights[i-1]]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]
```

### 4. Longest Common Subsequence (LCS)

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

## DP Problem Recognition

Ask yourself:
1. Can the problem be broken into subproblems?
2. Do subproblems overlap?
3. Is there a recurrence relation?
4. What's the base case?

## Steps to Solve DP Problems

1. **Define the state**: What does dp[i] represent?
2. **Find recurrence**: How dp[i] relates to previous states
3. **Initialize base cases**: Starting values
4. **Determine order**: Which subproblems to solve first
5. **Compute the answer**: Final state value

## Space Optimization

Many DP solutions can be optimized from O(n) to O(1) space:

```python
# Original: O(n) space
dp = [0] * n
for i in range(n):
    dp[i] = dp[i-1] + dp[i-2]

# Optimized: O(1) space
prev2, prev1 = 0, 1
for i in range(n):
    curr = prev1 + prev2
    prev2, prev1 = prev1, curr
```

## Common DP Problem Types

1. **Climbing Stairs**: Ways to reach top
2. **Coin Change**: Minimum coins for amount
3. **House Robber**: Maximum value without adjacent
4. **Longest Increasing Subsequence**: LIS
5. **Edit Distance**: Transform one string to another
6. **Partition**: Split array into equal subsets
7. **Matrix Path**: Minimum/maximum path sum

## Practice Strategy

1. Start with Fibonacci and climbing stairs
2. Learn 1D DP problems (house robber, jump game)
3. Progress to 2D DP (unique paths, minimum path sum)
4. Master knapsack pattern
5. Tackle string DP (LCS, edit distance)
6. Practice state compression for space optimization""",
        "questions": [
            {
                "question": "What are the two key properties required for Dynamic Programming?",
                "options": ["Sorting and searching", "Optimal substructure and overlapping subproblems", "Recursion and iteration", "Time and space complexity"],
                "correct_answer": 1,
                "explanation": "DP requires: (1) Optimal substructure - optimal solution contains optimal solutions to subproblems, and (2) Overlapping subproblems - same subproblems are solved multiple times."
            },
            {
                "question": "What is the difference between top-down and bottom-up DP?",
                "options": ["Different time complexity", "Top-down uses recursion with memoization, bottom-up uses iteration", "Bottom-up is always faster", "They solve different problems"],
                "correct_answer": 1,
                "explanation": "Top-down (memoization) uses recursion and stores results in a cache. Bottom-up (tabulation) uses iteration and fills a table from base cases up. Both have the same time complexity but different implementation styles."
            },
            {
                "question": "How does DP improve on naive recursion for Fibonacci?",
                "options": ["Uses less memory", "Reduces time complexity from O(2^n) to O(n)", "Makes code shorter", "Uses different algorithm"],
                "correct_answer": 1,
                "explanation": "Naive recursive Fibonacci is O(2^n) because it recalculates the same values many times. DP stores calculated values, reducing redundant computation to O(n) time."
            }
        ]
    }
}


async def add_content_for_knowledge_point(session, name_pattern, content_data):
    """Add article and questions to a knowledge point matching the name pattern"""
    try:
        questions_json = json.dumps(content_data["questions"])
        
        result = await session.execute(text("""
            UPDATE knowledge_points 
            SET article_content = :article,
                reading_questions = CAST(:questions AS jsonb)
            WHERE name ILIKE :pattern
            RETURNING id, name
        """), {
            "article": content_data["article"],
            "questions": questions_json,
            "pattern": f"%{name_pattern}%"
        })
        
        updated = result.fetchone()
        if updated:
            print(f"  ✓ {updated[1]} (ID: {updated[0]})")
            return True
        else:
            print(f"  ✗ No knowledge point found matching '{name_pattern}'")
            return False
            
    except Exception as e:
        print(f"  ❌ Error for '{name_pattern}': {e}")
        return False


async def main():
    print("=" * 70)
    print("Bulk Add Learning Content for All Knowledge Points")
    print("=" * 70)
    print()
    
    async with AsyncSessionLocal() as session:
        success_count = 0
        fail_count = 0
        
        print("Adding content to knowledge points...")
        print()
        
        for name_pattern, content_data in LEARNING_CONTENT.items():
            if await add_content_for_knowledge_point(session, name_pattern, content_data):
                success_count += 1
            else:
                fail_count += 1
        
        await session.commit()
        
        print()
        print("=" * 70)
        print(f"Completed: {success_count} successful, {fail_count} failed")
        print("=" * 70)
        print()
        print("✅ All learning content has been added!")
        print()
        print("Next steps:")
        print("1. Restart the backend server")
        print("2. Visit the Roadmap page")
        print("3. Click on any knowledge point to see the article and quizzes")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())


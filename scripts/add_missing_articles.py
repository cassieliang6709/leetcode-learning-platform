"""
Add article content for the 6 missing knowledge points:
Binary Search, Graph, Greedy, Backtracking, Heap, Bit Manipulation
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


# Complete learning content for missing knowledge points
MISSING_CONTENT = {
    "Binary Search": {
        "article": """# Binary Search Algorithm

Binary search is one of the most efficient searching algorithms, reducing search space by half in each iteration. It's a fundamental divide-and-conquer technique used extensively in computer science.

## Core Concept

Binary search works on **sorted arrays** by repeatedly dividing the search interval in half. If the target value is less than the middle element, search the left half; otherwise, search the right half.

### Algorithm Steps

1. Start with two pointers: `left` at beginning, `right` at end
2. Calculate middle index: `mid = left + (right - left) // 2`
3. Compare target with `arr[mid]`:
   - If equal: Found! Return mid
   - If target < arr[mid]: Search left half (right = mid - 1)
   - If target > arr[mid]: Search right half (left = mid + 1)
4. Repeat until found or left > right

### Time Complexity

- **Time**: O(log n) - Divides search space by 2 each iteration
- **Space**: O(1) iterative, O(log n) recursive (call stack)

## Classic Implementation

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```

## Common Variations

### 1. Find First Occurrence
```python
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### 2. Find Last Occurrence
```python
def find_last(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### 3. Search in Rotated Array
```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # Left half sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

## Applications

- **Search in sorted arrays**: Finding elements efficiently
- **Finding boundaries**: First/last occurrence, insertion point
- **Peak finding**: Finding local maxima in arrays
- **Square root**: Computing integer square root
- **Search space reduction**: Optimizing brute force solutions

## Common Patterns

1. **Standard Binary Search**: Find exact match in sorted array
2. **Lower/Upper Bound**: Find insertion position
3. **Rotated Array Search**: Handle sorted but rotated arrays
4. **Binary Search on Answer**: Search for optimal value in range
5. **2D Matrix Search**: Apply binary search in matrices

## Practice Strategy

1. Master standard binary search implementation
2. Understand the loop invariants (left, right pointers)
3. Practice boundary cases (empty array, single element)
4. Learn variations (first/last occurrence)
5. Apply to advanced problems (rotated arrays, peak finding)""",
        "questions": [
            {
                "question": "What is the time complexity of binary search?",
                "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
                "correct_answer": 1,
                "explanation": "Binary search has O(log n) time complexity because it divides the search space in half with each iteration, leading to logarithmic growth."
            },
            {
                "question": "What is a prerequisite for binary search to work correctly?",
                "options": ["Array must be sorted", "Array must be large", "Array must have unique elements", "Array must be of even length"],
                "correct_answer": 0,
                "explanation": "Binary search requires the array to be sorted. It relies on the property that elements are in order to decide which half to search next."
            },
            {
                "question": "Why use 'mid = left + (right - left) // 2' instead of 'mid = (left + right) // 2'?",
                "options": ["It's faster", "To avoid integer overflow", "It's more readable", "No difference"],
                "correct_answer": 1,
                "explanation": "Using 'left + (right - left) // 2' prevents potential integer overflow when left and right are very large numbers. (left + right) could exceed the maximum integer value."
            }
        ]
    },
    "Graph": {
        "article": """# Graph Algorithms

Graphs are fundamental data structures representing relationships between objects. They consist of vertices (nodes) connected by edges and are used to model networks, relationships, and dependencies.

## Graph Basics

### Representations

**1. Adjacency List** (Most Common)
```python
# More space-efficient for sparse graphs
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}
```

**2. Adjacency Matrix**
```python
# Better for dense graphs, O(1) edge lookup
graph = [
    [0, 1, 1, 0],  # A connects to B, C
    [1, 0, 0, 1],  # B connects to A, D
    [1, 0, 0, 1],  # C connects to A, D
    [0, 1, 1, 0]   # D connects to B, C
]
```

### Graph Types

- **Directed vs Undirected**: Edges have direction or not
- **Weighted vs Unweighted**: Edges have weights or not
- **Cyclic vs Acyclic**: Contains cycles or not (DAG)
- **Connected vs Disconnected**: All nodes reachable or not

## Depth-First Search (DFS)

Explores as far as possible along each branch before backtracking.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited
```

**Applications**: Cycle detection, topological sort, path finding

## Breadth-First Search (BFS)

Explores all neighbors at current depth before moving to next level.

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
```

**Applications**: Shortest path (unweighted), level-order traversal

## Shortest Path Algorithms

### Dijkstra's Algorithm (Weighted, Non-negative)

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```

**Time Complexity**: O((V + E) log V) with min-heap

## Cycle Detection

### Undirected Graph
```python
def has_cycle(graph):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Found cycle
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False
```

### Directed Graph (DFS with colors)
```python
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    
    def dfs(node):
        if color[node] == GRAY:
            return True  # Back edge found
        if color[node] == BLACK:
            return False
        
        color[node] = GRAY
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

## Topological Sort

Order vertices in a directed acyclic graph (DAG) so that for every edge u→v, u comes before v.

```python
def topological_sort(graph):
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return stack[::-1]
```

## Common Graph Problems

1. **Number of Islands**: DFS/BFS on 2D grid
2. **Clone Graph**: Deep copy with DFS/BFS
3. **Course Schedule**: Cycle detection in directed graph
4. **Word Ladder**: BFS for shortest transformation
5. **Network Delay Time**: Dijkstra's shortest path
6. **Minimum Spanning Tree**: Kruskal's or Prim's algorithm

## Practice Strategy

1. Master DFS and BFS traversals
2. Understand graph representations
3. Practice cycle detection
4. Learn shortest path algorithms
5. Study topological sort for DAGs
6. Solve grid-based graph problems (islands, paths)""",
        "questions": [
            {
                "question": "What is the main difference between DFS and BFS?",
                "options": ["DFS uses queue, BFS uses stack", "DFS explores depth-first, BFS explores level-by-level", "BFS is always faster", "DFS only works on trees"],
                "correct_answer": 1,
                "explanation": "DFS explores as far as possible along each branch before backtracking (depth-first), while BFS explores all neighbors at the current depth before moving deeper (level-by-level)."
            },
            {
                "question": "Which algorithm finds the shortest path in an unweighted graph?",
                "options": ["DFS", "BFS", "Binary Search", "Quick Sort"],
                "correct_answer": 1,
                "explanation": "BFS finds the shortest path in unweighted graphs because it explores nodes level by level, guaranteeing the first time it reaches a node is via the shortest path."
            },
            {
                "question": "What is a DAG in graph theory?",
                "options": ["Directed Acyclic Graph", "Double Adjacent Graph", "Directed Array Graph", "Data Access Graph"],
                "correct_answer": 0,
                "explanation": "DAG stands for Directed Acyclic Graph - a directed graph with no cycles. It's fundamental for tasks like topological sorting and dependency resolution."
            }
        ]
    },
    "Greedy": {
        "article": """# Greedy Algorithms

Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum. They're efficient but don't always guarantee the best solution for all problems.

## Core Principle

**Greedy Choice Property**: A global optimum can be reached by selecting a local optimum at each step without reconsidering previous choices.

## Key Characteristics

1. **Make the best choice at each step**
2. **Never backtrack or reconsider**
3. **Hope local optimums lead to global optimum**
4. **Usually faster than dynamic programming**
5. **Doesn't always work - need to prove correctness**

## When Greedy Works

Greedy algorithms work when a problem has:
1. **Greedy Choice Property**: Local optimal leads to global optimal
2. **Optimal Substructure**: Optimal solution contains optimal subsolutions

## Classic Greedy Patterns

### 1. Activity Selection
**Problem**: Select maximum non-overlapping activities

```python
def activity_selection(activities):
    # Sort by end time
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return selected
```

**Why greedy works**: Choosing activity that ends earliest leaves most room for future activities.

### 2. Fractional Knapsack
**Problem**: Maximize value with weight limit (can take fractions)

```python
def fractional_knapsack(items, capacity):
    # Sort by value-to-weight ratio
    items.sort(key=lambda x: x[1]/x[0], reverse=True)
    
    total_value = 0
    for weight, value in items:
        if capacity >= weight:
            capacity -= weight
            total_value += value
        else:
            # Take fraction
            total_value += value * (capacity / weight)
            break
    
    return total_value
```

### 3. Huffman Coding
**Problem**: Optimal prefix-free binary code

```python
import heapq

def huffman_encoding(freq):
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p))
```

### 4. Minimum Spanning Tree (Kruskal's)
**Problem**: Connect all vertices with minimum total edge weight

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # Sort by weight
    uf = UnionFind(n)
    mst = []
    
    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
    
    return mst
```

## Common LeetCode Greedy Problems

### Jump Game
```python
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
```

### Gas Station
```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    
    return start
```

### Meeting Rooms II
```python
def min_meeting_rooms(intervals):
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = end_ptr = 0
    for start in starts:
        if start < ends[end_ptr]:
            rooms += 1
        else:
            end_ptr += 1
    
    return rooms
```

## Greedy vs Dynamic Programming

| Aspect | Greedy | Dynamic Programming |
|--------|--------|---------------------|
| **Decision** | Irrevocable | Can reconsider |
| **Speed** | Usually faster | Usually slower |
| **Optimality** | Not always optimal | Always optimal |
| **Examples** | Activity selection | 0/1 Knapsack |

## Common Greedy Strategies

1. **Sort first**: Often sorting helps identify greedy choice
2. **Two pointers**: Process from both ends
3. **Priority queue**: Always pick best available
4. **Exchange argument**: Prove swapping doesn't improve
5. **Stay ahead**: Greedy stays ahead or equal at each step

## Proving Greedy Correctness

1. **Greedy Choice**: Show local optimum leads to global optimum
2. **Optimal Substructure**: After greedy choice, problem reduces to smaller subproblem
3. **Exchange Argument**: Swapping greedy choice with any other doesn't improve solution

## Practice Strategy

1. Identify if problem has greedy choice property
2. Practice sorting-based greedy (intervals, scheduling)
3. Learn greedy with heaps (Huffman, merge intervals)
4. Study classic algorithms (Dijkstra, Kruskal)
5. Recognize when NOT to use greedy (0/1 knapsack needs DP)""",
        "questions": [
            {
                "question": "What is the greedy choice property?",
                "options": ["Choose the largest element always", "A locally optimal choice leads to globally optimal solution", "Always use sorting", "Make random choices"],
                "correct_answer": 1,
                "explanation": "The greedy choice property means making a locally optimal choice at each step will lead to a globally optimal solution. This must be proven for greedy to work correctly."
            },
            {
                "question": "Which problem CANNOT be solved optimally with greedy?",
                "options": ["Activity selection", "0/1 Knapsack", "Fractional knapsack", "Minimum spanning tree"],
                "correct_answer": 1,
                "explanation": "0/1 Knapsack cannot be solved optimally with greedy because you cannot take fractions. It requires dynamic programming. Fractional knapsack CAN use greedy."
            },
            {
                "question": "What's the key difference between greedy and dynamic programming?",
                "options": ["Greedy is always faster", "Greedy makes irrevocable choices, DP reconsiders choices", "DP uses more memory", "They solve different problems"],
                "correct_answer": 1,
                "explanation": "Greedy makes irrevocable decisions at each step without looking back, while DP considers all possibilities and can reconsider previous choices through memoization or tabulation."
            }
        ]
    },
    "Backtracking": {
        "article": """# Backtracking Algorithm

Backtracking is a systematic way to try all possible solutions by building candidates incrementally and abandoning candidates ("backtracking") as soon as it's determined they cannot lead to a valid solution.

## Core Concept

Think of backtracking as **exploring a decision tree**:
1. Make a choice
2. Recursively explore that choice
3. If it leads to success → return success
4. If it fails → undo the choice (backtrack) and try another

## Backtracking Template

```python
def backtrack(candidate):
    if is_solution(candidate):
        output(candidate)
        return
    
    for next_choice in get_choices(candidate):
        if is_valid(next_choice):
            make_choice(next_choice)
            backtrack(candidate)
            unmake_choice(next_choice)  # BACKTRACK
```

## Three Questions for Backtracking

1. **Choice**: What choices do I have at each step?
2. **Constraints**: What rules limit my choices?
3. **Goal**: When have I found a complete solution?

## Classic Problems

### 1. Permutations
**Problem**: Generate all permutations of array

```python
def permute(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])  # Found complete permutation
            return
        
        for i in range(len(remaining)):
            # Choice: Pick remaining[i]
            backtrack(path + [remaining[i]], 
                     remaining[:i] + remaining[i+1:])
    
    backtrack([], nums)
    return result
```

### 2. Combinations
**Problem**: Find all k-length combinations

```python
def combine(n, k):
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)  # Only use numbers after i
            path.pop()  # BACKTRACK
    
    backtrack(1, [])
    return result
```

### 3. Subsets
**Problem**: Generate all subsets (power set)

```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # Every path is valid
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # BACKTRACK
    
    backtrack(0, [])
    return result
```

### 4. N-Queens
**Problem**: Place N queens on N×N board (no attacks)

```python
def solve_n_queens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    
    def is_valid(row, col):
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check diagonal (upper-left)
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Check diagonal (upper-right)
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            if is_valid(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'  # BACKTRACK
    
    backtrack(0)
    return result
```

### 5. Sudoku Solver
**Problem**: Fill 9×9 grid following Sudoku rules

```python
def solve_sudoku(board):
    def is_valid(row, col, num):
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True
    
    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if is_valid(i, j, num):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = '.'  # BACKTRACK
                    return False
        return True
    
    backtrack()
```

### 6. Word Search
**Problem**: Find if word exists in board

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    
    def backtrack(r, c, index):
        if index == len(word):
            return True
        
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            board[r][c] != word[index]):
            return False
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore all 4 directions
        found = (backtrack(r+1, c, index+1) or
                backtrack(r-1, c, index+1) or
                backtrack(r, c+1, index+1) or
                backtrack(r, c-1, index+1))
        
        # BACKTRACK
        board[r][c] = temp
        return found
    
    for i in range(rows):
        for j in range(cols):
            if backtrack(i, j, 0):
                return True
    return False
```

## Optimization Techniques

### 1. Pruning
Cut branches that cannot lead to solution:
```python
if current_sum > target:
    return  # Prune this branch
```

### 2. Early Termination
```python
if found_solution:
    return True  # Stop searching
```

### 3. Sorting for Pruning
```python
candidates.sort()  # Sort to enable early pruning
for candidate in candidates:
    if candidate > remaining:
        break  # All remaining too large
```

## Time Complexity

Backtracking explores decision trees:
- **Permutations**: O(n! × n)
- **Combinations**: O(2^n × n)
- **Subsets**: O(2^n × n)
- **N-Queens**: O(n!)

Generally exponential - use for small inputs or with pruning.

## Backtracking vs Brute Force

- **Brute Force**: Try all possibilities, even invalid ones
- **Backtracking**: Abandon invalid paths early (pruning)

## Common Patterns

1. **Generate all combinations/permutations**
2. **Constraint satisfaction** (N-Queens, Sudoku)
3. **Path finding** (maze, word search)
4. **Subset selection** (partition, target sum)

## Practice Strategy

1. Master the backtracking template
2. Start with combinations and permutations
3. Practice with constraints (N-Queens)
4. Learn path-based backtracking (word search)
5. Optimize with pruning techniques
6. Recognize when backtracking is appropriate""",
        "questions": [
            {
                "question": "What is the key characteristic of backtracking?",
                "options": ["It always uses recursion", "It explores possibilities and undoes choices when they fail", "It's faster than greedy", "It only works on arrays"],
                "correct_answer": 1,
                "explanation": "Backtracking systematically explores all possibilities by making choices, exploring them recursively, and undoing (backtracking) choices that don't lead to solutions."
            },
            {
                "question": "What is pruning in backtracking?",
                "options": ["Removing elements from array", "Cutting branches that cannot lead to valid solutions", "Sorting the input", "Using less memory"],
                "correct_answer": 1,
                "explanation": "Pruning is the optimization technique of abandoning exploration of branches that cannot possibly lead to valid solutions, reducing the search space significantly."
            },
            {
                "question": "Which problem is typically solved with backtracking?",
                "options": ["Finding maximum in array", "Binary search", "N-Queens puzzle", "Sorting an array"],
                "correct_answer": 2,
                "explanation": "N-Queens is a classic backtracking problem where you try placing queens and backtrack when a placement violates constraints, exploring all valid configurations."
            }
        ]
    },
    "Heap": {
        "article": """# Heap Data Structure

A heap is a specialized tree-based data structure that satisfies the heap property. It's commonly implemented as a binary heap and used for efficient priority queue operations.

## Heap Properties

### Max Heap
- Parent ≥ Children
- Root is the maximum element
- Used for: Top K smallest, descending order

### Min Heap
- Parent ≤ Children
- Root is the minimum element
- Used for: Top K largest, ascending order, Dijkstra's algorithm

## Binary Heap Structure

A complete binary tree stored in an array:

```
Array: [10, 8, 6, 4, 5, 3, 2]

Tree representation (Max Heap):
        10
       /  \
      8    6
     / \  / \
    4  5 3   2
```

### Index Relationships
For element at index `i`:
- **Parent**: `(i - 1) // 2`
- **Left child**: `2 * i + 1`
- **Right child**: `2 * i + 2`

## Core Operations

### 1. Heapify (Bubble Down)
Maintain heap property by moving element down

```python
def heapify_down(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_down(arr, n, largest)
```

### 2. Bubble Up (Heapify Up)
Maintain heap property by moving element up

```python
def bubble_up(arr, i):
    parent = (i - 1) // 2
    
    if i > 0 and arr[i] > arr[parent]:
        arr[i], arr[parent] = arr[parent], arr[i]
        bubble_up(arr, parent)
```

### 3. Insert
**Time**: O(log n)

```python
def insert(heap, value):
    heap.append(value)  # Add at end
    bubble_up(heap, len(heap) - 1)
```

### 4. Extract Max/Min
**Time**: O(log n)

```python
def extract_max(heap):
    if not heap:
        return None
    
    max_val = heap[0]
    heap[0] = heap[-1]  # Move last to root
    heap.pop()
    
    if heap:
        heapify_down(heap, len(heap), 0)
    
    return max_val
```

### 5. Build Heap
**Time**: O(n) - Not O(n log n)!

```python
def build_heap(arr):
    n = len(arr)
    # Start from last internal node
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, n, i)
```

## Python's heapq Module

Python provides min-heap by default:

```python
import heapq

# Create heap
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)

# Extract min
min_val = heapq.heappop(heap)  # Returns 3

# Build heap from list
nums = [5, 7, 2, 1, 9]
heapq.heapify(nums)  # O(n)

# For max heap, negate values
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -7)
max_val = -heapq.heappop(max_heap)  # Returns 7
```

## Common Heap Patterns

### 1. Top K Elements
```python
def find_k_largest(nums, k):
    # Min heap of size k
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

### 2. K Closest Points
```python
def k_closest(points, k):
    # Max heap of size k (distances)
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [(x, y) for _, x, y in heap]
```

### 3. Merge K Sorted Lists
```python
def merge_k_lists(lists):
    heap = []
    result = []
    
    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result
```

### 4. Running Median
```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (left half)
        self.large = []  # Min heap (right half)
    
    def add_num(self, num):
        # Add to max heap (small)
        heapq.heappush(self.small, -num)
        
        # Balance: largest in small ≤ smallest in large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Maintain size property: |small| ≥ |large|
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

## Heap Sort

```python
def heap_sort(arr):
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Swap
        heapify_down(arr, i, 0)
```

**Time**: O(n log n), **Space**: O(1)

## Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(log n) | O(1) |
| Extract Min/Max | O(log n) | O(1) |
| Peek Min/Max | O(1) | O(1) |
| Build Heap | O(n) | O(1) |
| Heapify | O(log n) | O(1) |

## When to Use Heap

1. **Priority Queue**: Task scheduling, event simulation
2. **Top K problems**: K largest/smallest elements
3. **Median finding**: Running median, sliding window median
4. **Merge operations**: Merge K sorted lists/arrays
5. **Graph algorithms**: Dijkstra's, Prim's MST
6. **Stream processing**: Find median in data stream

## Practice Strategy

1. Master heapq operations in Python
2. Understand min heap vs max heap
3. Practice Top K problems
4. Learn two-heap pattern (running median)
5. Study heap-based graph algorithms
6. Solve merge problems with heaps""",
        "questions": [
            {
                "question": "What is the time complexity of building a heap from an array?",
                "options": ["O(n)", "O(n log n)", "O(log n)", "O(n²)"],
                "correct_answer": 0,
                "explanation": "Building a heap using bottom-up heapify is O(n), not O(n log n). This is because most elements are near the bottom and require few swaps."
            },
            {
                "question": "In a min heap, what is true about the root?",
                "options": ["It's the largest element", "It's the smallest element", "It's the median", "It's random"],
                "correct_answer": 1,
                "explanation": "In a min heap, the root is always the smallest element. Every parent is smaller than or equal to its children."
            },
            {
                "question": "What problem pattern commonly uses two heaps?",
                "options": ["Binary search", "Finding running median", "Sorting", "DFS traversal"],
                "correct_answer": 1,
                "explanation": "The two-heap pattern (max heap for smaller half, min heap for larger half) is commonly used to efficiently find the running median in a stream of numbers."
            }
        ]
    },
    "Bit Manipulation": {
        "article": """# Bit Manipulation

Bit manipulation involves directly working with binary digits (bits) using bitwise operators. It's essential for optimization, hardware programming, and certain algorithmic problems.

## Binary Number System

Numbers are stored as sequences of bits (0s and 1s):

```
Decimal: 5   →  Binary: 101
Decimal: 12  →  Binary: 1100
Decimal: -5  →  Binary: ...11111011 (Two's complement)
```

## Bitwise Operators

### 1. AND (&)
Both bits must be 1 to result in 1

```python
5 & 3 = 1
101 & 011 = 001
```

**Uses**: Check if bit is set, clear bits, get even/odd

### 2. OR (|)
At least one bit must be 1 to result in 1

```python
5 | 3 = 7
101 | 011 = 111
```

**Uses**: Set bits, combine flags

### 3. XOR (^)
Bits must be different to result in 1

```python
5 ^ 3 = 6
101 ^ 011 = 110
```

**Properties**:
- `a ^ a = 0` (same numbers cancel)
- `a ^ 0 = a` (identity)
- `a ^ b ^ a = b` (commutative, associative)

**Uses**: Find unique element, swap values, toggle bits

### 4. NOT (~)
Inverts all bits

```python
~5 = -6
~00000101 = 11111010
```

### 5. Left Shift (<<)
Shift bits left, fill with 0s

```python
5 << 1 = 10
101 << 1 = 1010
```

**Effect**: Multiply by 2^n (where n is shift amount)

### 6. Right Shift (>>)
Shift bits right, fill with sign bit

```python
5 >> 1 = 2
101 >> 1 = 10
```

**Effect**: Divide by 2^n (integer division)

## Common Bit Tricks

### Check if Power of 2
```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Examples:
# 8 = 1000, 7 = 0111 → 8 & 7 = 0 ✓
# 6 = 0110, 5 = 0101 → 6 & 5 = 4 ✗
```

### Count Set Bits (Hamming Weight)
```python
def count_bits(n):
    count = 0
    while n:
        count += n & 1  # Check last bit
        n >>= 1  # Shift right
    return count

# Brian Kernighan's Algorithm (faster)
def count_bits_fast(n):
    count = 0
    while n:
        n &= n - 1  # Remove rightmost 1
        count += 1
    return count
```

### Get Rightmost 1-bit
```python
def rightmost_one(n):
    return n & -n

# Example: 12 = 1100
# rightmost_one(12) = 4 = 0100
```

### Clear Rightmost 1-bit
```python
def clear_rightmost_one(n):
    return n & (n - 1)

# Example: 12 = 1100
# clear_rightmost_one(12) = 8 = 1000
```

### Toggle Bit at Position
```python
def toggle_bit(n, pos):
    return n ^ (1 << pos)

# Toggle 3rd bit: toggle_bit(5, 2) = 1
# 101 ^ 100 = 001
```

### Set Bit at Position
```python
def set_bit(n, pos):
    return n | (1 << pos)
```

### Clear Bit at Position
```python
def clear_bit(n, pos):
    return n & ~(1 << pos)
```

### Check Bit at Position
```python
def check_bit(n, pos):
    return (n & (1 << pos)) != 0
```

## Classic Problems

### 1. Single Number
**Problem**: Find unique element (all others appear twice)

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num  # XOR cancels duplicates
    return result

# [2, 3, 2, 4, 4] → 3
```

### 2. Missing Number
**Problem**: Find missing number in [0, n]

```python
def missing_number(nums):
    n = len(nums)
    xor = 0
    for i in range(n + 1):
        xor ^= i
    for num in nums:
        xor ^= num
    return xor
```

### 3. Reverse Bits
```python
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

### 4. Counting Bits (0 to n)
```python
def counting_bits(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

# i >> 1 removes last bit
# i & 1 checks if last bit is 1
```

### 5. Sum of Two Integers (Without + or -)
```python
def get_sum(a, b):
    mask = 0xFFFFFFFF
    
    while b != 0:
        carry = (a & b) << 1  # Carry bits
        a = (a ^ b) & mask    # Sum without carry
        b = carry & mask
    
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

### 6. Subsets (Using Bitmask)
```python
def subsets(nums):
    n = len(nums)
    result = []
    
    # Iterate through all possible subsets (2^n)
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result
```

## Bit Manipulation Patterns

### 1. XOR for Finding Unique
- Single number in array of duplicates
- Missing number
- Two unique numbers (all others twice)

### 2. AND for Checking/Clearing
- Check if bit is set
- Get even/odd (n & 1)
- Clear rightmost 1-bit (n & (n-1))

### 3. OR for Setting
- Set bit at position
- Combine flags/permissions

### 4. Shifts for Multiplication/Division
- Multiply by 2^k: n << k
- Divide by 2^k: n >> k

### 5. Bitmask for Subsets
- Generate all subsets
- Check subset membership
- Compress state in DP

## Advantages of Bit Manipulation

1. **Speed**: Direct hardware operations
2. **Space**: Compact representation
3. **Elegance**: Concise solutions
4. **Optimization**: Constant time operations

## Common Applications

- **Flags**: Store multiple boolean values
- **Permissions**: File/user permissions
- **Graphics**: Color manipulation (RGB)
- **Networking**: IP addresses, subnetting
- **Cryptography**: Bitwise operations in algorithms
- **Compression**: Huffman coding
- **State representation**: Game states, DP optimization

## Practice Strategy

1. Understand binary representation and two's complement
2. Master basic bitwise operators (AND, OR, XOR, NOT, shifts)
3. Learn common tricks (power of 2, count bits, etc.)
4. Practice XOR-based problems (single number, missing number)
5. Study bitmask techniques for subsets
6. Apply bit manipulation for optimization

## Tips

- Draw out binary representations for clarity
- Remember: `x & 1` checks odd/even
- XOR is your friend for finding unique elements
- Use bit manipulation for constant time/space improvements
- Test with small examples first""",
        "questions": [
            {
                "question": "What is the result of XOR operation: a ^ a?",
                "options": ["a", "2a", "0", "1"],
                "correct_answer": 2,
                "explanation": "XOR of a number with itself is always 0 because all corresponding bits are the same, resulting in 0. This property is used to find unique elements in arrays."
            },
            {
                "question": "How do you check if a number is a power of 2 using bit manipulation?",
                "options": ["n % 2 == 0", "n & (n-1) == 0", "n | n == 0", "n ^ 2 == 0"],
                "correct_answer": 1,
                "explanation": "A power of 2 has only one bit set (e.g., 8 = 1000). n-1 flips all bits after that bit (7 = 0111). Their AND gives 0: 1000 & 0111 = 0000."
            },
            {
                "question": "What does left shift by 1 (n << 1) do to a number?",
                "options": ["Divides by 2", "Multiplies by 2", "Adds 1", "Subtracts 1"],
                "correct_answer": 1,
                "explanation": "Left shift by 1 multiplies the number by 2. For example: 5 (101) << 1 = 10 (1010). Each left shift multiplies by 2^k where k is the shift amount."
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
            print(f"  ✅ {updated[1]} (ID: {updated[0]})")
            return True
        else:
            print(f"  ❌ No knowledge point found matching '{name_pattern}'")
            return False
            
    except Exception as e:
        print(f"  ❌ Error for '{name_pattern}': {e}")
        return False


async def main():
    print("\n" + "=" * 80)
    print("📝 ADD MISSING ARTICLE CONTENT")
    print("=" * 80)
    print("\nAdding articles for 6 missing knowledge points:\n")
    
    async with AsyncSessionLocal() as session:
        success_count = 0
        fail_count = 0
        
        for name_pattern, content_data in MISSING_CONTENT.items():
            print(f"Processing: {name_pattern}")
            if await add_content_for_knowledge_point(session, name_pattern, content_data):
                success_count += 1
            else:
                fail_count += 1
            print()
        
        await session.commit()
        
        print("=" * 80)
        print(f"📊 RESULTS:")
        print(f"   ✅ Successfully added: {success_count}")
        print(f"   ❌ Failed: {fail_count}")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


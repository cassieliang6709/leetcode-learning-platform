"""
Update AlgoMentor knowledge point articles with comprehensive, template-based content.

This script:
1. Deletes empty duplicate KnowledgePoints (IDs 23-48)
2. Rewrites all 13 core KP articles with Monster-style content:
   - Recognition checklist (when to use this pattern)
   - Core template code (Python, ready to copy)
   - Complexity table
   - Common patterns with examples
   - Common pitfalls
   - Recommended practice problems

Run: cd backend && python ../scripts/update_articles_v2.py
"""
import asyncio
import sys
from pathlib import Path

_root = Path(__file__).parent.parent
_backend = _root / "backend"
from dotenv import load_dotenv
load_dotenv(_backend / ".env")
sys.path.insert(0, str(_backend))

from sqlalchemy import select, delete, text, update
from app.database import AsyncSessionLocal
from app.models import KnowledgePoint, QuizQuestion

# ---------------------------------------------------------------------------
# Article content — 13 topics
# ---------------------------------------------------------------------------

ARTICLES = {
    "Array & Hash Table": """# Array & Hash Table

## 🎯 When to Use This Pattern
- Problem asks for a **pair, triplet, or subarray** that satisfies a condition
- You need **O(1) lookup** (e.g., "does X exist in the array?")
- Keywords: *two sum, count frequency, group by, find duplicate, index of complement*

## 🔍 Recognition Checklist
- [ ] Need to track what you've seen before
- [ ] Need to count occurrences of elements
- [ ] Need fast lookup (avoid O(n²) brute force)
- [ ] Grouping strings or numbers by a common property

---

## 🐍 Core Templates

### Template 1 — Two Sum (complement lookup)
```python
def twoSum(nums, target):
    seen = {}          # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
# Time: O(n)  Space: O(n)
```

### Template 2 — Frequency Count
```python
from collections import Counter

def solve(nums):
    freq = Counter(nums)          # {value: count}
    for val, count in freq.items():
        # process each unique value
        pass
# Time: O(n)  Space: O(n)
```

### Template 3 — Group by Key
```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))    # canonical form
        groups[key].append(s)
    return list(groups.values())
# Time: O(n·k·log k)  Space: O(n·k)
```

### Template 4 — Prefix Sum + Hash Map
```python
def subarraySum(nums, k):
    prefix_count = {0: 1}   # prefix_sum → how many times seen
    prefix = 0
    count = 0
    for num in nums:
        prefix += num
        count += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
    return count
# Time: O(n)  Space: O(n)
```

---

## 📊 Complexity Cheat Sheet
| Operation | Array | Hash Map |
|-----------|-------|----------|
| Access by index | O(1) | — |
| Search | O(n) | O(1) avg |
| Insert | O(n) amortized | O(1) avg |
| Delete | O(n) | O(1) avg |

---

## ⚠️ Common Pitfalls
1. **Hash collision**: Python dicts handle this, but understand the concept
2. **Modifying array while iterating** → iterate a copy or use indices
3. **Off-by-one in prefix sums** → always initialize `{0: 1}` for empty prefix
4. **Sorted vs unsorted matters** — hash map works on unsorted; two-pointer needs sorted

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Key Idea |
|---|---------|-----------|---------|
| 1 | Two Sum | Easy | complement map |
| 217 | Contains Duplicate | Easy | set |
| 242 | Valid Anagram | Easy | freq count |
| 49 | Group Anagrams | Medium | sorted key |
| 347 | Top K Frequent | Medium | Counter + heap |
| 238 | Product Except Self | Medium | prefix/suffix |
| 560 | Subarray Sum = K | Medium | prefix sum map |
| 128 | Longest Consecutive | Medium | set O(n) |
""",

    "Two Pointers": """# Two Pointers

## 🎯 When to Use This Pattern
- Array/string is **sorted** (or can be sorted) and you need pairs/triplets
- Need to shrink a window from both ends
- Keywords: *palindrome, pair sum, remove duplicates, reverse, partition*

## 🔍 Recognition Checklist
- [ ] Sorted array + find pair with target sum
- [ ] Need to check/compare elements from both ends
- [ ] "Merge two sorted arrays" style problems
- [ ] Remove elements in-place (fast/slow pointer)

---

## 🐍 Core Templates

### Template 1 — Opposite Ends (sorted array)
```python
def twoSumSorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
# Time: O(n)  Space: O(1)
```

### Template 2 — Fast / Slow Pointer (in-place remove)
```python
def removeElement(nums, val):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow   # new length
# Time: O(n)  Space: O(1)
```

### Template 3 — Three Sum (sort + two pointers)
```python
def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:   # skip duplicates
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif s < 0: left += 1
            else: right -= 1
    return result
# Time: O(n²)  Space: O(1) excluding output
```

### Template 4 — Palindrome Check
```python
def isPalindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1; right -= 1
    return True
```

---

## 📊 Complexity
| Approach | Time | Space | When |
|---------|------|-------|------|
| Opposite ends | O(n) | O(1) | Sorted, find pair |
| Fast/slow | O(n) | O(1) | Remove/partition in-place |
| Three Sum | O(n²) | O(1) | Sorted, find triplet |

---

## ⚠️ Common Pitfalls
1. **Forget to sort first** for opposite-ends two-pointer
2. **Duplicate skipping in 3Sum** — skip same value at outer AND inner loops
3. **`left < right` not `left <= right`** — with `<=` you'll check the same element twice

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Pattern |
|---|---------|-----------|---------|
| 125 | Valid Palindrome | Easy | opposite ends |
| 283 | Move Zeroes | Easy | fast/slow |
| 167 | Two Sum II | Medium | opposite ends |
| 15 | 3Sum | Medium | sort + two ptrs |
| 11 | Container With Most Water | Medium | greedy shrink |
| 42 | Trapping Rain Water | Hard | prefix max arrays |
""",

    "Sliding Window": """# Sliding Window

## 🎯 When to Use This Pattern
- Find the **longest/shortest subarray or substring** satisfying a condition
- All elements are positive (window can only grow/shrink meaningfully)
- Keywords: *longest substring, max sum subarray of size k, minimum window, at most k distinct*

## 🔍 Recognition Checklist
- [ ] Contiguous subarray / substring question
- [ ] "At most K" / "exactly K" distinct elements
- [ ] Fixed-size window (simpler) vs variable-size window
- [ ] Need to avoid O(n²) brute force over all subarrays

---

## 🐍 Core Templates

### Template 1 — Fixed Size Window
```python
def maxSumSubarrayK(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # slide
        best = max(best, window_sum)
    return best
# Time: O(n)  Space: O(1)
```

### Template 2 — Variable Window (shrink when invalid)
```python
def lengthOfLongestSubstring(s):
    char_count = {}
    left = 0
    best = 0
    for right in range(len(s)):
        # EXPAND: add s[right] to window
        char_count[s[right]] = char_count.get(s[right], 0) + 1

        # SHRINK: while window is invalid
        while char_count[s[right]] > 1:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        best = max(best, right - left + 1)
    return best
# Time: O(n)  Space: O(k) where k = alphabet size
```

### Template 3 — Minimum Window (find smallest valid window)
```python
def minWindow(s, t):
    need = Counter(t)
    missing = len(t)   # chars still needed
    best = ""
    left = 0
    for right, c in enumerate(s):
        if need.get(c, 0) > 0:
            missing -= 1
        need[c] = need.get(c, 0) - 1
        if missing == 0:                    # valid window
            # shrink from left
            while need.get(s[left], 0) < 0:
                need[s[left]] += 1
                left += 1
            window = s[left:right+1]
            if not best or len(window) < len(best):
                best = window
            need[s[left]] += 1             # remove left before next iteration
            missing += 1
            left += 1
    return best
# Time: O(n)  Space: O(k)
```

---

## 📊 Complexity
| Variant | Time | Space |
|---------|------|-------|
| Fixed window | O(n) | O(1) |
| Variable window | O(n) | O(k) |
| Minimum window | O(n) | O(k) |

---

## ⚠️ Common Pitfalls
1. **Two while loops** → Always outer `for right` + inner `while invalid: shrink`
2. **When to update best**: update AFTER shrinking (for min window), BEFORE shrinking (for max window)
3. **Deque for sliding max** → use `collections.deque` for O(1) max in fixed window

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 3 | Longest Substring No Repeat | Medium | variable window |
| 424 | Longest Repeating Char Replace | Medium | variable window |
| 567 | Permutation in String | Medium | fixed window |
| 76 | Minimum Window Substring | Hard | min window |
| 239 | Sliding Window Maximum | Hard | deque |
""",

    "Binary Search": """# Binary Search

## 🎯 When to Use This Pattern
- Array is **sorted** (or has a monotonic property)
- "Find minimum value that satisfies X" or "find insertion position"
- Need O(log n) instead of O(n) search
- Keywords: *sorted array, rotation, peak, kth smallest, search in O(log n)*

## 🔍 Recognition Checklist
- [ ] Input is sorted (or rotated sorted, or can be treated as monotonic)
- [ ] Answer space has a monotonic property (binary search on answer)
- [ ] "Find first/last position of target"
- [ ] Minimize/maximize with a condition that becomes easier above/below a threshold

---

## 🐍 Core Templates

### Template 1 — Classic Binary Search
```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:              # NOTE: <=
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
# Time: O(log n)  Space: O(1)
```

### Template 2 — Find First True (leftmost position)
```python
# Find first index where condition(i) is True
# Assumes: False False ... False True True ... True
def findFirst(arr, condition):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if condition(arr[mid]):
            result = mid          # candidate, but maybe not leftmost
            right = mid - 1      # try to find earlier
        else:
            left = mid + 1
    return result
```

### Template 3 — Binary Search on Answer
```python
# "Find minimum speed such that all packages arrive in time"
def solve(packages, H):
    def canFinish(speed):
        hours = sum((p + speed - 1) // speed for p in packages)
        return hours <= H

    left, right = 1, max(packages)
    while left < right:              # NOTE: < not <=
        mid = left + (right - left) // 2
        if canFinish(mid):
            right = mid              # valid, try lower
        else:
            left = mid + 1
    return left
# Time: O(n log(max)) Space: O(1)
```

### Template 4 — Rotated Sorted Array
```python
def searchRotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target: return mid
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

---

## 📊 Key Decision Points
| When | Use |
|------|-----|
| Find exact target | `left <= right`, return mid |
| Find leftmost | `left <= right`, save mid, shrink right |
| Find rightmost | `left <= right`, save mid, shrink left |
| Binary search on answer | `left < right`, shrink to converge |

---

## ⚠️ Common Pitfalls
1. **`mid = (left + right) // 2`** overflows in some languages → use `left + (right-left)//2`
2. **Infinite loop**: wrong update (`right = mid` without `left < right`) → carefully pick template
3. **Off-by-one**: `<=` vs `<` and `mid+1` vs `mid` — stick to one template per problem type

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 704 | Binary Search | Easy | classic |
| 35 | Search Insert Position | Easy | leftmost |
| 153 | Find Min in Rotated Array | Medium | rotated |
| 33 | Search in Rotated Array | Medium | rotated |
| 34 | First and Last Position | Medium | leftmost + rightmost |
| 875 | Koko Eating Bananas | Medium | search on answer |
| 4 | Median of Two Sorted Arrays | Hard | partition |
""",

    "Linked List": """# Linked List

## 🎯 When to Use This Pattern
- Problems involving linked list **traversal, reversal, cycle detection, merging**
- Need O(1) space operations on sequential data
- Keywords: *reverse, detect cycle, find middle, merge sorted lists, Nth from end*

## 🔍 Recognition Checklist
- [ ] Need to find middle of list (fast/slow)
- [ ] Detect or find start of cycle
- [ ] Reverse a list or sublists
- [ ] Merge or split lists
- [ ] Remove Nth node from end

---

## 🐍 Core Templates

### Template 1 — Fast / Slow (Find Middle)
```python
def findMiddle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow   # slow is at middle
# When list has even length, slow = second middle
```

### Template 2 — Cycle Detection (Floyd's)
```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def detectCycleStart(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next; fast = fast.next.next
        if slow == fast:
            slow = head          # reset one pointer to head
            while slow != fast:
                slow = slow.next; fast = fast.next
            return slow          # cycle start
    return None
```

### Template 3 — Reverse a Linked List
```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next  # save next
        curr.next = prev        # reverse link
        prev = curr             # advance prev
        curr = next_node        # advance curr
    return prev   # new head
# Time: O(n)  Space: O(1)
```

### Template 4 — Merge Two Sorted Lists
```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1; l1 = l1.next
        else:
            curr.next = l2; l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
# Time: O(m+n)  Space: O(1)
```

### Template 5 — Remove Nth from End
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):    # advance fast n+1 steps
        fast = fast.next
    while fast:
        fast = fast.next; slow = slow.next
    slow.next = slow.next.next
    return dummy.next
# Time: O(L)  Space: O(1)
```

---

## ⚠️ Common Pitfalls
1. **Always use a dummy node** when the head might be deleted
2. **Check `fast and fast.next`** before advancing in fast/slow (avoids null pointer)
3. **Save `next_node` before reversing** or you lose the rest of the list
4. **Off-by-one in Nth from end** — advance fast `n+1` steps (not n) to stop slow at the node BEFORE the one to delete

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 206 | Reverse Linked List | Easy | reverse |
| 21 | Merge Two Sorted Lists | Easy | merge |
| 141 | Linked List Cycle | Easy | fast/slow |
| 142 | Linked List Cycle II | Medium | Floyd's |
| 19 | Remove Nth From End | Medium | two pointers |
| 143 | Reorder List | Medium | middle + reverse + merge |
| 23 | Merge K Sorted Lists | Hard | heap / divide & conquer |
""",

    "Stack": """# Stack

## 🎯 When to Use This Pattern
- Problems with **matching pairs** (brackets, tags)
- Need to remember **previous states** while moving forward
- **Monotonic stack**: next greater/smaller element
- Keywords: *valid parentheses, next greater element, largest rectangle, decode string*

## 🔍 Recognition Checklist
- [ ] Matching/balancing brackets, tags, or symbols
- [ ] "Next greater/smaller element" to the left or right
- [ ] Evaluate expression left-to-right (calculator)
- [ ] Undo/redo or history tracking

---

## 🐍 Core Templates

### Template 1 — Balanced Parentheses
```python
def isValid(s):
    stack = []
    match = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in '({[':
            stack.append(c)
        elif not stack or stack[-1] != match[c]:
            return False
        else:
            stack.pop()
    return not stack
# Time: O(n)  Space: O(n)
```

### Template 2 — Monotonic Stack (Next Greater Element)
```python
def nextGreaterElement(nums):
    result = [-1] * len(nums)
    stack = []   # stores indices; stack is decreasing in value
    for i, num in enumerate(nums):
        # Pop elements smaller than current → current is their "next greater"
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
# Time: O(n)  Space: O(n)
```

### Template 3 — Monotonic Stack (Largest Rectangle in Histogram)
```python
def largestRectangleArea(heights):
    stack = []   # (index, height) — increasing stack
    max_area = 0
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
    return max_area
```

### Template 4 — Min Stack (O(1) min)
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []    # tracks minimums

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop(); self.min_stack.pop()

    def getMin(self): return self.min_stack[-1]
```

---

## ⚠️ Common Pitfalls
1. **Empty stack check before `stack[-1]`** — always guard before peeking
2. **Monotonic stack direction matters**: next GREATER → pop when `stack[-1] < current`; next SMALLER → pop when `stack[-1] > current`
3. **Process remaining stack after loop** — elements still in stack have no next greater element

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 20 | Valid Parentheses | Easy | balanced |
| 155 | Min Stack | Medium | min stack |
| 739 | Daily Temperatures | Medium | monotonic |
| 496 | Next Greater Element I | Easy | monotonic |
| 84 | Largest Rectangle in Histogram | Hard | monotonic |
| 42 | Trapping Rain Water | Hard | monotonic |
""",

    "Binary Tree": """# Binary Tree

## 🎯 When to Use This Pattern
- Any tree traversal (inorder, preorder, postorder, level-order)
- Tree path problems (root-to-leaf sum, longest path)
- Tree structure problems (is balanced, is symmetric, LCA)
- Keywords: *tree, binary search tree, depth, path sum, lowest common ancestor*

## 🔍 Recognition Checklist
- [ ] Need to visit every node → DFS or BFS traversal
- [ ] Find something about paths → DFS returning values up
- [ ] Level-by-level processing → BFS with a queue
- [ ] BST property: left < root < right (enables binary search)

---

## 🐍 Core Templates

### Template 1 — DFS Recursive (returns info from subtrees)
```python
def solve(root):
    if not root:
        return base_case_value      # e.g., 0, True, float('inf')

    left_val = solve(root.left)
    right_val = solve(root.right)

    # Combine and return
    return combine(root.val, left_val, right_val)

# Example: max depth
def maxDepth(root):
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Template 2 — BFS Level Order
```python
from collections import deque

def levelOrder(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):          # process one level at a time
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
# Time: O(n)  Space: O(w) where w = max width
```

### Template 3 — Path Problems (DFS with running state)
```python
def hasPathSum(root, target):
    def dfs(node, remaining):
        if not node: return False
        remaining -= node.val
        if not node.left and not node.right:   # leaf
            return remaining == 0
        return dfs(node.left, remaining) or dfs(node.right, remaining)
    return dfs(root, target)
```

### Template 4 — Lowest Common Ancestor
```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right: return root   # p and q on different sides
    return left or right              # both on one side
```

### Template 5 — BST Search / Insert
```python
def searchBST(root, val):
    if not root or root.val == val: return root
    return searchBST(root.left if val < root.val else root.right, val)

def insertIntoBST(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insertIntoBST(root.left, val)
    else:              root.right = insertIntoBST(root.right, val)
    return root
```

---

## 📊 Traversal Reference
| Order | Pattern | Use Case |
|-------|---------|---------|
| Preorder | root → left → right | Copy tree, serialize |
| Inorder | left → root → right | BST sorted order |
| Postorder | left → right → root | Delete tree, evaluate expression |
| Level order | BFS queue | Level-by-level, zigzag |

---

## ⚠️ Common Pitfalls
1. **Base case for null node** — always handle `if not root: return ...`
2. **DFS modifying global vs returning** — cleaner to return values and combine at each node
3. **BST inorder gives sorted array** — use this property to verify BST

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 104 | Max Depth of Binary Tree | Easy | DFS |
| 226 | Invert Binary Tree | Easy | DFS |
| 102 | Binary Tree Level Order | Medium | BFS |
| 112 | Path Sum | Easy | path DFS |
| 235 | LCA of BST | Easy | BST LCA |
| 236 | LCA of Binary Tree | Medium | general LCA |
| 124 | Binary Tree Max Path Sum | Hard | DFS return |
""",

    "Dynamic Programming": """# Dynamic Programming

## 🎯 When to Use This Pattern
- Problem has **overlapping subproblems** (same smaller problem solved many times)
- Problem has **optimal substructure** (optimal answer built from optimal sub-answers)
- Keywords: *minimum cost, maximum profit, number of ways, longest subsequence, can you reach*

## 🔍 Recognition Checklist
- [ ] "How many ways to..." → count DP
- [ ] "Minimum/maximum cost to..." → optimization DP
- [ ] "Can you achieve..." → boolean DP
- [ ] Choices at each step (take/skip, move right/down) → 2D DP or 1D DP
- [ ] String/sequence: longest common, edit distance → 2D DP

---

## 🐍 Core Templates

### Template 1 — 1D DP (Fibonacci-style)
```python
def climbStairs(n):
    if n <= 2: return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
    # Space optimize: use two variables instead of array
```

### Template 2 — 2D DP (grid / two sequences)
```python
def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
# Time: O(m*n)  Space: O(m*n) → optimize to O(n) with 1D array
```

### Template 3 — 0/1 Knapsack
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        # Iterate backwards to avoid using same item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
# This is the 0/1 knapsack (each item used at most once)
```

### Template 4 — LCS / Edit Distance
```python
def longestCommonSubsequence(text1, text2):
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

### Template 5 — Top-down Memoization
```python
from functools import lru_cache

def wordBreak(s, wordDict):
    word_set = set(wordDict)
    @lru_cache(maxsize=None)
    def dp(i):
        if i == len(s): return True
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in word_set and dp(j):
                return True
        return False
    return dp(0)
```

---

## 📊 DP Pattern Map
| Problem Type | Recurrence | Space |
|-------------|-----------|-------|
| Fibonacci | `dp[i] = dp[i-1] + dp[i-2]` | O(1) |
| Knapsack | `dp[w] = max(dp[w], dp[w-wi]+vi)` | O(W) |
| Grid paths | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` | O(n) |
| LCS | `dp[i][j] = dp[i-1][j-1]+1 or max(...)` | O(n) |

---

## ⚠️ Common Pitfalls
1. **Identify STATE clearly** — what changes at each step? (index, remaining capacity, etc.)
2. **Knapsack direction**: 0/1 knapsack iterate BACKWARDS; unbounded iterate FORWARDS
3. **Memoization vs tabulation**: start with memoization (`@lru_cache`) to verify logic, then convert to tabulation for space optimization

---

## 🏋️ Practice Problems (learn in this order!)
| # | Problem | Difficulty | Type |
|---|---------|-----------|------|
| 70 | Climbing Stairs | Easy | 1D DP |
| 198 | House Robber | Medium | 1D DP |
| 322 | Coin Change | Medium | unbounded knapsack |
| 300 | Longest Increasing Subsequence | Medium | subsequence |
| 1143 | Longest Common Subsequence | Medium | 2D DP |
| 416 | Partition Equal Subset Sum | Medium | 0/1 knapsack |
| 72 | Edit Distance | Hard | 2D DP |
""",

    "Graph": """# Graph

## 🎯 When to Use This Pattern
- Nodes with connections (social network, map, dependencies)
- "Is there a path from A to B?" / "How many connected components?"
- Keywords: *islands, connected, shortest path, cycle detection, topological order*

## 🔍 Recognition Checklist
- [ ] Grid with 0s/1s where you explore adjacent cells → implicit graph
- [ ] Explicit edges given as pairs `[u, v]`
- [ ] "Shortest path" → BFS (unweighted) or Dijkstra (weighted)
- [ ] "All possible paths" or "cycle detection" → DFS with visited set
- [ ] Task scheduling with dependencies → topological sort

---

## 🐍 Core Templates

### Template 1 — DFS (recursive)
```python
def numIslands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or (r, c) in visited or grid[r][c] == '0'):
            return
        visited.add((r, c))
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                count += 1
    return count
```

### Template 2 — BFS (shortest path in unweighted graph)
```python
from collections import deque

def shortestPath(graph, start, end):
    if start == end: return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph[node]:
            if neighbor == end: return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1   # no path
```

### Template 3 — Topological Sort (Kahn's BFS)
```python
from collections import deque

def canFinish(numCourses, prerequisites):
    indegree = [0] * numCourses
    adj = [[] for _ in range(numCourses)]
    for course, pre in prerequisites:
        adj[pre].append(course)
        indegree[course] += 1

    queue = deque(i for i in range(numCourses) if indegree[i] == 0)
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return count == numCourses   # False if cycle exists
```

### Template 4 — Union-Find (Disjoint Set)
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False   # already connected
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

---

## 📊 Algorithm Choice
| Goal | Algorithm | Time |
|------|-----------|------|
| Connectivity / islands | DFS or BFS | O(V+E) |
| Shortest path (unweighted) | BFS | O(V+E) |
| Shortest path (weighted) | Dijkstra | O(E log V) |
| Cycle detection / all paths | DFS + visited | O(V+E) |
| Dependency ordering | Topo Sort (Kahn) | O(V+E) |
| Connected components | Union-Find | O(α(n)) |

---

## ⚠️ Common Pitfalls
1. **Always mark visited before adding to queue** (BFS), not after popping
2. **Cycle detection**: track `visited` (all time) AND `in_path` (current DFS path) separately
3. **Grid neighbors**: use `[(0,1),(0,-1),(1,0),(-1,0)]` and bounds-check

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 200 | Number of Islands | Medium | DFS grid |
| 133 | Clone Graph | Medium | DFS/BFS |
| 207 | Course Schedule | Medium | topo sort |
| 323 | Connected Components | Medium | Union-Find |
| 743 | Network Delay Time | Medium | Dijkstra |
| 684 | Redundant Connection | Medium | Union-Find |
""",

    "Greedy": """# Greedy

## 🎯 When to Use This Pattern
- At each step, make the **locally optimal choice** and it leads to global optimum
- Usually proved by "exchange argument" (swapping any two choices doesn't improve)
- Keywords: *interval scheduling, jump game, meeting rooms, task assignment, min cost*

## 🔍 Recognition Checklist
- [ ] Interval problems (sort by start or end time)
- [ ] "Can you reach the end?" type problems
- [ ] Maximize/minimize something by making smart local choices
- [ ] Huffman coding, activity selection pattern

---

## 🐍 Core Templates

### Template 1 — Interval Scheduling (merge or count)
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])    # sort by start
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:         # overlaps
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

def minMeetingRooms(intervals):
    intervals.sort(key=lambda x: x[0])
    import heapq
    heap = []   # end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    return len(heap)
```

### Template 2 — Jump Game (farthest reach)
```python
def canJump(nums):
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest: return False    # can't reach this index
        farthest = max(farthest, i + jump)
    return True

def jump(nums):  # minimum jumps to reach end
    jumps = farthest = cur_end = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:           # must make a jump here
            jumps += 1
            cur_end = farthest
    return jumps
```

### Template 3 — Greedy with Sorting
```python
def leastInterval(tasks, n):
    from collections import Counter
    freq = sorted(Counter(tasks).values(), reverse=True)
    max_freq = freq[0]
    # Slots needed = (max_freq - 1) * (n + 1) + count of tasks with max_freq
    idle_slots = (max_freq - 1) * (n + 1) + freq.count(max_freq)
    return max(idle_slots, len(tasks))
```

---

## ⚠️ Common Pitfalls
1. **Greedy doesn't always work** — always prove correctness (exchange argument)
2. **Wrong sort key** — interval problems: sort by END for activity selection, by START for merging
3. **Greedy vs DP**: if optimal choice at each step affects future choices in complex ways → DP; if always take the obvious best → greedy

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Key Idea |
|---|---------|-----------|---------|
| 55 | Jump Game | Medium | farthest reach |
| 45 | Jump Game II | Medium | BFS levels |
| 56 | Merge Intervals | Medium | sort by start |
| 435 | Non-overlapping Intervals | Medium | sort by end |
| 134 | Gas Station | Medium | circular greedy |
| 621 | Task Scheduler | Medium | frequency slots |
""",

    "Backtracking": """# Backtracking

## 🎯 When to Use This Pattern
- Find **ALL** solutions (all subsets, all permutations, all valid paths)
- Constraint satisfaction (N-Queens, Sudoku)
- Keywords: *all subsets, all permutations, combinations, generate, valid arrangements*

## 🔍 Recognition Checklist
- [ ] "Generate all..." or "find all valid..."
- [ ] Build a solution step-by-step and undo if a constraint is violated
- [ ] State space is exponential but can be pruned early
- [ ] Subsets, permutations, combinations of a set

---

## 🐍 Core Templates

### Template 1 — Subsets (Power Set)
```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])           # add current subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)       # next element must be AFTER i
            path.pop()                   # UNDO
    backtrack(0, [])
    return result
```

### Template 2 — Combinations
```python
def combine(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            # Pruning: not enough numbers left to fill k spots
            if n - i + 1 < k - len(path): break
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return result
```

### Template 3 — Permutations
```python
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if used[i]: continue
            used[i] = True
            path.append(num)
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

### Template 4 — Permutations with Duplicates
```python
def permuteUnique(nums):
    nums.sort()     # SORT FIRST to handle duplicates
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            # Skip duplicate: if same value as previous AND previous not used
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

### Template 5 — Grid/String Backtracking (Word Search)
```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    def dfs(r, c, idx):
        if idx == len(word): return True
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or board[r][c] != word[idx]): return False
        temp = board[r][c]
        board[r][c] = '#'    # mark visited (in-place)
        found = any(dfs(r+dr, c+dc, idx+1) for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)])
        board[r][c] = temp   # UNDO
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

---

## ⚠️ Common Pitfalls
1. **`path.pop()` after every recursive call** — the undo step is non-negotiable
2. **Append a COPY `path[:]`**, not the list itself — lists are mutable
3. **Duplicate handling**: sort first, then skip `nums[i] == nums[i-1]` at same recursion depth
4. **Pruning matters**: add bounds checks early to avoid TLE

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 78 | Subsets | Medium | subset |
| 77 | Combinations | Medium | combination |
| 46 | Permutations | Medium | permutation |
| 47 | Permutations II | Medium | permutation + dedup |
| 39 | Combination Sum | Medium | subset (reuse allowed) |
| 79 | Word Search | Medium | grid DFS |
| 51 | N-Queens | Hard | constraint |
""",

    "Heap": """# Heap (Priority Queue)

## 🎯 When to Use This Pattern
- Repeatedly get the **min or max element** from a dynamic set
- **Top K** elements (largest, smallest, most frequent)
- **Merge K sorted** lists/arrays
- **Scheduling** by priority
- Keywords: *k largest, k closest, median stream, merge k sorted*

## 🔍 Recognition Checklist
- [ ] "Find top K..." or "kth largest/smallest"
- [ ] Process elements in sorted order but they arrive one by one
- [ ] Merge multiple sorted sequences
- [ ] Sliding window maximum/minimum

---

## 🐍 Core Templates

### Template 1 — Python Heap Basics
```python
import heapq

# Python only has min-heap
heap = []
heapq.heappush(heap, val)     # push
heapq.heappop(heap)           # pop min
heap[0]                        # peek min (no pop)

# MAX-HEAP: push negative values
heapq.heappush(heap, -val)
max_val = -heapq.heappop(heap)

# Build heap from list: O(n)
heapq.heapify(lst)
```

### Template 2 — Top K Largest Elements
```python
def topKLargest(nums, k):
    # Min-heap of size k: always discard smallest
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)    # remove smallest
    return list(heap)
# Time: O(n log k)  Space: O(k)

# Alternative: nlargest (less efficient but cleaner)
return heapq.nlargest(k, nums)
```

### Template 3 — K Closest Points to Origin
```python
def kClosest(points, k):
    # Max-heap (negative distance) of size k
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)    # negate for max-heap
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```

### Template 4 — Median of Data Stream
```python
class MedianFinder:
    def __init__(self):
        self.small = []   # max-heap (negate) — left half
        self.large = []   # min-heap — right half

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # Ensure max(small) <= min(large)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            heapq.heappush(self.large, -heapq.heappop(self.small))
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

### Template 5 — Merge K Sorted Lists
```python
def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = curr = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node; curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## ⚠️ Common Pitfalls
1. **Python only has min-heap** — negate values to simulate max-heap
2. **Heap of tuples**: `(priority, value)` — heapq uses first element for comparison
3. **`heapq.nlargest(k, iterable)`** is O(n log k), not O(n) — use for small n

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Template |
|---|---------|-----------|---------|
| 703 | Kth Largest in Stream | Easy | min-heap size k |
| 347 | Top K Frequent | Medium | min-heap |
| 973 | K Closest Points | Medium | max-heap |
| 215 | Kth Largest Element | Medium | min-heap or quickselect |
| 23 | Merge K Sorted Lists | Hard | min-heap |
| 295 | Find Median from Data Stream | Hard | two heaps |
""",

    "Bit Manipulation": """# Bit Manipulation

## 🎯 When to Use This Pattern
- Single number problems (XOR cancels duplicates)
- Power of 2 checks, subsets via bitmask
- Optimize space with bit flags
- Keywords: *XOR, single number, missing number, power of 2, subset*

## 🔍 Recognition Checklist
- [ ] "Find the element that appears once while others appear twice" → XOR
- [ ] "Power of 2?" → `n & (n-1) == 0`
- [ ] Enumerate all subsets of a set → bitmask `0` to `1<<n`
- [ ] Count set bits → `bin(n).count('1')` or Brian Kernighan's

---

## 🐍 Core Templates

### Template 1 — Bit Operations Cheat Sheet
```python
# Get bit at position i
(n >> i) & 1

# Set bit at position i
n | (1 << i)

# Clear bit at position i
n & ~(1 << i)

# Toggle bit at position i
n ^ (1 << i)

# Check if n is a power of 2
n > 0 and (n & (n - 1)) == 0

# Remove lowest set bit (Brian Kernighan)
n & (n - 1)        # removes rightmost set bit

# Get lowest set bit
n & (-n)            # isolates rightmost set bit

# Count set bits
bin(n).count('1')   # O(k) where k = number of bits
```

### Template 2 — XOR: Single Number
```python
def singleNumber(nums):
    result = 0
    for n in nums:
        result ^= n    # XOR cancels pairs: a ^ a = 0, a ^ 0 = a
    return result
# Time: O(n)  Space: O(1)
```

### Template 3 — Missing Number
```python
def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
    # Or XOR version: XOR all indices with all values
```

### Template 4 — Enumerate All Subsets (Bitmask)
```python
def allSubsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):        # 0 to 2^n - 1
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
# Time: O(2^n * n)  — only use for n <= 20
```

### Template 5 — Reverse Bits
```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

---

## 📊 XOR Properties (memorize these!)
| Property | Example |
|---------|---------|
| `a ^ a = 0` | cancels duplicates |
| `a ^ 0 = a` | identity |
| XOR is commutative & associative | order doesn't matter |
| `a ^ b ^ a = b` | "decrypt" — reveals the different element |

---

## ⚠️ Common Pitfalls
1. **Python integers are arbitrary precision** — no overflow, but may need to mask: `n & 0xFFFFFFFF` for 32-bit
2. **Operator precedence**: `a & b == 0` → actually `a & (b == 0)` — use parentheses: `(a & b) == 0`
3. **Bitmask DP state explosion**: only use bitmask DP for n ≤ 20

---

## 🏋️ Practice Problems
| # | Problem | Difficulty | Key Idea |
|---|---------|-----------|---------|
| 136 | Single Number | Easy | XOR |
| 338 | Counting Bits | Easy | `n & (n-1)` |
| 191 | Number of 1 Bits | Easy | Brian Kernighan |
| 268 | Missing Number | Easy | XOR or math |
| 190 | Reverse Bits | Easy | shift |
| 137 | Single Number II | Medium | bit count mod 3 |
| 260 | Single Number III | Medium | XOR mask |
""",
}


async def main():
    async with AsyncSessionLocal() as db:
        # ------------------------------------------------------------------
        # Step 1: Delete empty duplicate KnowledgePoints (23-48)
        # First remap any quiz_questions that reference them
        # ------------------------------------------------------------------
        print("Step 1: Cleaning duplicate KnowledgePoints (IDs 23-48)...")

        # Find which KP IDs have content (the real ones)
        real_kps_result = await db.execute(
            select(KnowledgePoint).where(
                KnowledgePoint.id.in_(range(10, 23))
            )
        )
        real_kps = {kp.name: kp for kp in real_kps_result.scalars().all()}
        print(f"  Real KPs: {list(real_kps.keys())}")

        # Get empty duplicate KPs
        dup_kps_result = await db.execute(
            select(KnowledgePoint).where(
                KnowledgePoint.id.in_(range(23, 49))
            )
        )
        dup_kps = dup_kps_result.scalars().all()

        # Remap quiz_questions from duplicates to real KPs
        remapped = 0
        for dup in dup_kps:
            real = real_kps.get(dup.name)
            if real:
                await db.execute(
                    update(QuizQuestion)
                    .where(QuizQuestion.knowledge_point_id == dup.id)
                    .values(knowledge_point_id=real.id)
                )
                remapped += 1

        # Now delete the duplicate KPs
        dup_ids = [kp.id for kp in dup_kps]
        if dup_ids:
            await db.execute(
                delete(KnowledgePoint).where(KnowledgePoint.id.in_(dup_ids))
            )
        print(f"  Deleted {len(dup_ids)} empty duplicate KPs, remapped {remapped} question groups")

        # ------------------------------------------------------------------
        # Step 2: Update articles for the 13 real KnowledgePoints
        # ------------------------------------------------------------------
        print("\nStep 2: Writing comprehensive articles...")

        all_kps_result = await db.execute(
            select(KnowledgePoint).where(
                KnowledgePoint.id.in_(range(10, 23))
            )
        )
        all_kps = all_kps_result.scalars().all()

        updated = 0
        for kp in all_kps:
            article = ARTICLES.get(kp.name)
            if not article:
                print(f"  SKIP: No article for {kp.name!r}")
                continue

            kp.article_content = article

            # Ensure proper tags/category are set
            category_map = {
                "Array & Hash Table": "array",
                "Two Pointers": "two_pointers",
                "Sliding Window": "sliding_window",
                "Binary Search": "binary_search",
                "Linked List": "linked_list",
                "Stack": "stack",
                "Binary Tree": "tree",
                "Dynamic Programming": "dynamic_programming",
                "Graph": "graph",
                "Greedy": "greedy",
                "Backtracking": "backtracking",
                "Heap": "heap",
                "Bit Manipulation": "bit",
            }
            kp.category = category_map.get(kp.name, kp.category)
            updated += 1
            print(f"  ✓ {kp.name} ({len(article)} chars)")

        await db.commit()
        print(f"\nDone! Updated {updated} articles.")
        print("Run POST /api/rag/index/all to rebuild the vector index.")


if __name__ == "__main__":
    asyncio.run(main())

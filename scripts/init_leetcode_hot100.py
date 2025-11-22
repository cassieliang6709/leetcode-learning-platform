"""
Initialize LeetCode Hot 100 problems with 3-level hints
This script populates the database with curated problems and pre-generated hints
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import AsyncSessionLocal, init_db
from backend.app.models import KnowledgePoint, QuizQuestion


# LeetCode Hot 100 problems organized by knowledge points
LEETCODE_HOT_100 = [
    # ===== ARRAY & HASHING =====
    {
        "knowledge_point": "Array & Hash Table",
        "category": "array",
        "difficulty": "easy",
        "description": "Master array manipulation and hash table techniques",
        "problems": [
            {
                "leetcode_id": 1,
                "title": "Two Sum",
                "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use a hash map to store numbers you've seen so far. For each number, check if its complement (target - current) exists in the map. This allows you to solve the problem in a single pass with O(n) time complexity."
                    },
                    {
                        "type": "code",
                        "content": """def twoSum(nums, target):
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []"""
                    },
                    {
                        "type": "video",
                        "content": "Watch NeetCode's detailed explanation"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=KLlXCFG5TnA",
                "test_cases": [
                    {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
                    {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]}
                ]
            },
            {
                "leetcode_id": 49,
                "title": "Group Anagrams",
                "description": """Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase.

Example:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use a hash map where the key represents the character frequency pattern. You can either sort each string as the key, or use a character count array/tuple. Words with the same sorted string or character count are anagrams."
                    },
                    {
                        "type": "code",
                        "content": """from collections import defaultdict

def groupAnagrams(strs):
    anagram_map = defaultdict(list)
    for word in strs:
        # Use sorted string as key
        key = ''.join(sorted(word))
        anagram_map[key].append(word)
    return list(anagram_map.values())"""
                    },
                    {
                        "type": "video",
                        "content": "Watch comprehensive walkthrough"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=vzdNOK2oB2E",
                "test_cases": [
                    {"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, 
                     "output": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]}
                ]
            },
            {
                "leetcode_id": 217,
                "title": "Contains Duplicate",
                "description": """Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example:
Input: nums = [1,2,3,1]
Output: true""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use a hash set to track numbers you've seen. If you encounter a number already in the set, return true. If you finish iterating without finding duplicates, return false. This gives O(n) time and O(n) space."
                    },
                    {
                        "type": "code",
                        "content": """def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False"""
                    },
                    {
                        "type": "video",
                        "content": "Watch solution explanation"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=3OamzN90kPg",
                "test_cases": [
                    {"input": {"nums": [1, 2, 3, 1]}, "output": True},
                    {"input": {"nums": [1, 2, 3, 4]}, "output": False}
                ]
            }
        ]
    },
    
    # ===== TWO POINTERS =====
    {
        "knowledge_point": "Two Pointers",
        "category": "two_pointers",
        "difficulty": "easy",
        "description": "Learn to use two pointers technique for array and string problems",
        "problems": [
            {
                "leetcode_id": 125,
                "title": "Valid Palindrome",
                "description": """A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string s, return true if it is a palindrome, or false otherwise.

Example:
Input: s = "A man, a plan, a canal: Panama"
Output: true""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use two pointers starting from both ends of the string. Skip non-alphanumeric characters and compare characters case-insensitively. Move pointers toward each other until they meet. If all comparisons match, it's a palindrome."
                    },
                    {
                        "type": "code",
                        "content": """def isPalindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True"""
                    },
                    {
                        "type": "video",
                        "content": "Watch two pointers technique explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=jJXJ16kPFWg",
                "test_cases": [
                    {"input": {"s": "A man, a plan, a canal: Panama"}, "output": True},
                    {"input": {"s": "race a car"}, "output": False}
                ]
            },
            {
                "leetcode_id": 15,
                "title": "3Sum",
                "description": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Sort the array first. Fix one number and use two pointers for the remaining array to find pairs that sum to the negative of the fixed number. Skip duplicates to avoid duplicate triplets. Time complexity: O(n²)."
                    },
                    {
                        "type": "code",
                        "content": """def threeSum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first number
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result"""
                    },
                    {
                        "type": "video",
                        "content": "Watch 3Sum solution walkthrough"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=jzZsG8n2R9A",
                "test_cases": [
                    {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "output": [[-1, -1, 2], [-1, 0, 1]]}
                ]
            }
        ]
    },
    
    # ===== SLIDING WINDOW =====
    {
        "knowledge_point": "Sliding Window",
        "category": "sliding_window",
        "difficulty": "medium",
        "description": "Master the sliding window technique for substring and subarray problems",
        "problems": [
            {
                "leetcode_id": 3,
                "title": "Longest Substring Without Repeating Characters",
                "description": """Given a string s, find the length of the longest substring without repeating characters.

Example:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use a sliding window with two pointers and a hash set. Expand the window by moving the right pointer and add characters to the set. When you encounter a duplicate, shrink the window from the left until the duplicate is removed. Track the maximum window size."
                    },
                    {
                        "type": "code",
                        "content": """def lengthOfLongestSubstring(s):
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Shrink window if duplicate found
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length"""
                    },
                    {
                        "type": "video",
                        "content": "Watch sliding window technique explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=wiGpQwVHdE0",
                "test_cases": [
                    {"input": {"s": "abcabcbb"}, "output": 3},
                    {"input": {"s": "bbbbb"}, "output": 1},
                    {"input": {"s": "pwwkew"}, "output": 3}
                ]
            },
            {
                "leetcode_id": 424,
                "title": "Longest Repeating Character Replacement",
                "description": """You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.

Example:
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use sliding window with a frequency map. The key insight: for a valid window, (window_length - most_frequent_char_count) <= k. Track the maximum frequency in the current window and expand/shrink accordingly."
                    },
                    {
                        "type": "code",
                        "content": """from collections import defaultdict

def characterReplacement(s, k):
    count = defaultdict(int)
    left = 0
    max_freq = 0
    max_length = 0
    
    for right in range(len(s)):
        count[s[right]] += 1
        max_freq = max(max_freq, count[s[right]])
        
        # Check if current window is valid
        window_size = right - left + 1
        if window_size - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length"""
                    },
                    {
                        "type": "video",
                        "content": "Watch detailed solution walkthrough"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=gqXU1UyA8pk",
                "test_cases": [
                    {"input": {"s": "ABAB", "k": 2}, "output": 4},
                    {"input": {"s": "AABABBA", "k": 1}, "output": 4}
                ]
            }
        ]
    },
    
    # ===== BINARY SEARCH =====
    {
        "knowledge_point": "Binary Search",
        "category": "binary_search",
        "difficulty": "medium",
        "description": "Learn binary search and its variations",
        "problems": [
            {
                "leetcode_id": 153,
                "title": "Find Minimum in Rotated Sorted Array",
                "description": """Suppose an array of length n sorted in ascending order is rotated between 1 and n times. Given the sorted rotated array nums of unique elements, return the minimum element of this array.

Example:
Input: nums = [3,4,5,1,2]
Output: 1""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use binary search. Compare the middle element with the rightmost element. If mid > right, the minimum is in the right half. Otherwise, it's in the left half (including mid). This works because one half is always sorted and contains the minimum."
                    },
                    {
                        "type": "code",
                        "content": """def findMin(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        # Minimum is in right half
        if nums[mid] > nums[right]:
            left = mid + 1
        # Minimum is in left half (including mid)
        else:
            right = mid
    
    return nums[left]"""
                    },
                    {
                        "type": "video",
                        "content": "Watch binary search in rotated array"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=nIVW4P8b1VA",
                "test_cases": [
                    {"input": {"nums": [3, 4, 5, 1, 2]}, "output": 1},
                    {"input": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "output": 0}
                ]
            },
            {
                "leetcode_id": 33,
                "title": "Search in Rotated Sorted Array",
                "description": """There is an integer array nums sorted in ascending order (with distinct values). Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

Example:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use modified binary search. First identify which half is sorted by comparing nums[left] with nums[mid]. Then check if the target lies in the sorted half's range. If yes, search that half; otherwise, search the other half. Time: O(log n)."
                    },
                    {
                        "type": "code",
                        "content": """def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1"""
                    },
                    {
                        "type": "video",
                        "content": "Watch comprehensive explanation"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=U8XENwh8Oy8",
                "test_cases": [
                    {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, "output": 4},
                    {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, "output": -1}
                ]
            }
        ]
    },
    
    # ===== LINKED LIST =====
    {
        "knowledge_point": "Linked List",
        "category": "linked_list",
        "difficulty": "easy",
        "description": "Master linked list manipulation and traversal techniques",
        "problems": [
            {
                "leetcode_id": 206,
                "title": "Reverse Linked List",
                "description": """Given the head of a singly linked list, reverse the list, and return the reversed list.

Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use three pointers: prev (initially None), current (head), and next. Iterate through the list, reversing the next pointer of each node to point to prev. Move all three pointers one step forward. Return prev as the new head."
                    },
                    {
                        "type": "code",
                        "content": """def reverseList(head):
    prev = None
    current = head
    
    while current:
        # Save next node
        next_node = current.next
        # Reverse pointer
        current.next = prev
        # Move pointers forward
        prev = current
        current = next_node
    
    return prev"""
                    },
                    {
                        "type": "video",
                        "content": "Watch linked list reversal explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=G0_I-ZF0S38",
                "test_cases": [
                    {"input": {"head": [1, 2, 3, 4, 5]}, "output": [5, 4, 3, 2, 1]}
                ]
            },
            {
                "leetcode_id": 141,
                "title": "Linked List Cycle",
                "description": """Given head, the head of a linked list, determine if the linked list has a cycle in it.

Example:
Input: head = [3,2,0,-4], pos = 1
Output: true""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use Floyd's Cycle Detection (fast and slow pointers). Move slow pointer one step and fast pointer two steps. If they meet, there's a cycle. If fast reaches null, there's no cycle. Time: O(n), Space: O(1)."
                    },
                    {
                        "type": "code",
                        "content": """def hasCycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True"""
                    },
                    {
                        "type": "video",
                        "content": "Watch Floyd's algorithm explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=gBTe7lFR3vc",
                "test_cases": [
                    {"input": {"head": [3, 2, 0, -4], "pos": 1}, "output": True}
                ]
            }
        ]
    },
    
    # ===== STACK =====
    {
        "knowledge_point": "Stack",
        "category": "stack",
        "difficulty": "easy",
        "description": "Learn to use stack data structure for various problems",
        "problems": [
            {
                "leetcode_id": 20,
                "title": "Valid Parentheses",
                "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

Example:
Input: s = "()[]{}"
Output: true""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use a stack. Push opening brackets onto the stack. When you encounter a closing bracket, check if it matches the top of the stack. If yes, pop; if no or stack is empty, return false. After processing all characters, the stack should be empty."
                    },
                    {
                        "type": "code",
                        "content": """def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # Closing bracket
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            # Opening bracket
            stack.append(char)
    
    return len(stack) == 0"""
                    },
                    {
                        "type": "video",
                        "content": "Watch stack-based solution"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=WTzjTskDFMg",
                "test_cases": [
                    {"input": {"s": "()[]{}"}, "output": True},
                    {"input": {"s": "(]"}, "output": False}
                ]
            },
            {
                "leetcode_id": 155,
                "title": "Min Stack",
                "description": """Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use two stacks: one for actual values and one for tracking minimums. When pushing, also push the current minimum onto the min stack. When popping, pop from both stacks. getMin() simply returns the top of the min stack. All operations are O(1)."
                    },
                    {
                        "type": "code",
                        "content": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        # Push current minimum
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)
    
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def getMin(self):
        return self.min_stack[-1]"""
                    },
                    {
                        "type": "video",
                        "content": "Watch Min Stack design explanation"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=qkLl7nAwDPo",
                "test_cases": []
            }
        ]
    },
    
    # ===== DYNAMIC PROGRAMMING =====
    {
        "knowledge_point": "Dynamic Programming",
        "category": "dynamic_programming",
        "difficulty": "medium",
        "description": "Master dynamic programming for optimization problems",
        "problems": [
            {
                "leetcode_id": 70,
                "title": "Climbing Stairs",
                "description": """You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "This is a Fibonacci problem. To reach step n, you can come from step n-1 (take 1 step) or step n-2 (take 2 steps). So dp[n] = dp[n-1] + dp[n-2]. Base cases: dp[1] = 1, dp[2] = 2. Can optimize space to O(1)."
                    },
                    {
                        "type": "code",
                        "content": """def climbStairs(n):
    if n <= 2:
        return n
    
    # Space-optimized approach
    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1"""
                    },
                    {
                        "type": "video",
                        "content": "Watch DP solution explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=Y0lT9Fck7qI",
                "test_cases": [
                    {"input": {"n": 2}, "output": 2},
                    {"input": {"n": 3}, "output": 3}
                ]
            },
            {
                "leetcode_id": 198,
                "title": "House Robber",
                "description": """You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

Example:
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "At each house, you have two choices: rob it (add its value to max from 2 houses ago) or skip it (take max from previous house). Use DP: dp[i] = max(dp[i-1], nums[i] + dp[i-2]). Can optimize to O(1) space using two variables."
                    },
                    {
                        "type": "code",
                        "content": """def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    # Space-optimized approach
    prev2 = 0  # max money 2 houses ago
    prev1 = 0  # max money 1 house ago
    
    for money in nums:
        current = max(prev1, money + prev2)
        prev2 = prev1
        prev1 = current
    
    return prev1"""
                    },
                    {
                        "type": "video",
                        "content": "Watch House Robber solution"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=xlvhyfcoQa4",
                "test_cases": [
                    {"input": {"nums": [1, 2, 3, 1]}, "output": 4},
                    {"input": {"nums": [2, 7, 9, 3, 1]}, "output": 12}
                ]
            },
            {
                "leetcode_id": 322,
                "title": "Coin Change",
                "description": """You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

Example:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use bottom-up DP. Create array dp where dp[i] represents minimum coins needed for amount i. For each amount, try using each coin and take minimum: dp[i] = min(dp[i], dp[i-coin] + 1). Initialize dp[0] = 0 and others to infinity. Time: O(amount * coins)."
                    },
                    {
                        "type": "code",
                        "content": """def coinChange(coins, amount):
    # Initialize DP array
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Build up from 1 to amount
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1"""
                    },
                    {
                        "type": "video",
                        "content": "Watch coin change DP solution"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=H9bfqozjoqs",
                "test_cases": [
                    {"input": {"coins": [1, 2, 5], "amount": 11}, "output": 3},
                    {"input": {"coins": [2], "amount": 3}, "output": -1}
                ]
            }
        ]
    },
    
    # ===== TREE =====
    {
        "knowledge_point": "Binary Tree",
        "category": "tree",
        "difficulty": "easy",
        "description": "Learn binary tree traversal and manipulation",
        "problems": [
            {
                "leetcode_id": 104,
                "title": "Maximum Depth of Binary Tree",
                "description": """Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example:
Input: root = [3,9,20,null,null,15,7]
Output: 3""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use recursion. The maximum depth is 1 + max(left subtree depth, right subtree depth). Base case: if node is null, return 0. This is a classic post-order traversal problem. Time: O(n), Space: O(h) where h is height."
                    },
                    {
                        "type": "code",
                        "content": """def maxDepth(root):
    # Base case
    if not root:
        return 0
    
    # Recursive case
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    return 1 + max(left_depth, right_depth)"""
                    },
                    {
                        "type": "video",
                        "content": "Watch tree depth calculation"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=hTM3phVI6YQ",
                "test_cases": [
                    {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": 3}
                ]
            },
            {
                "leetcode_id": 226,
                "title": "Invert Binary Tree",
                "description": """Given the root of a binary tree, invert the tree, and return its root.

Example:
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]""",
                "difficulty": "easy",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use recursion or iteration. For each node, swap its left and right children, then recursively invert the left and right subtrees. Base case: if node is null, return null. Can also use BFS/DFS with a queue/stack."
                    },
                    {
                        "type": "code",
                        "content": """def invertTree(root):
    # Base case
    if not root:
        return None
    
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invertTree(root.left)
    invertTree(root.right)
    
    return root"""
                    },
                    {
                        "type": "video",
                        "content": "Watch tree inversion explained"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=OnSn2XEQ4MY",
                "test_cases": [
                    {"input": {"root": [4, 2, 7, 1, 3, 6, 9]}, "output": [4, 7, 2, 9, 6, 3, 1]}
                ]
            },
            {
                "leetcode_id": 102,
                "title": "Binary Tree Level Order Traversal",
                "description": """Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

Example:
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]""",
                "difficulty": "medium",
                "hints": [
                    {
                        "type": "strategy",
                        "content": "Use BFS with a queue. Add root to queue. For each level, process all nodes in the queue (use queue size to know how many), add their values to current level list, and add their children to queue for next level. Repeat until queue is empty."
                    },
                    {
                        "type": "code",
                        "content": """from collections import deque

def levelOrder(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for i in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result"""
                    },
                    {
                        "type": "video",
                        "content": "Watch BFS level order traversal"
                    }
                ],
                "video_link": "https://www.youtube.com/watch?v=6ZnyEApgFYg",
                "test_cases": [
                    {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": [[3], [9, 20], [15, 7]]}
                ]
            }
        ]
    }
]


async def init_leetcode_data():
    """Initialize LeetCode Hot 100 problems with hints"""
    print("🚀 Initializing LeetCode Hot 100 data...")
    
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            # Create knowledge points and problems
            for kp_data in LEETCODE_HOT_100:
                print(f"\n📚 Creating knowledge point: {kp_data['knowledge_point']}")
                
                # Create knowledge point
                knowledge_point = KnowledgePoint(
                    name=kp_data["knowledge_point"],
                    description=kp_data["description"],
                    difficulty=kp_data["difficulty"],
                    category=kp_data["category"]
                )
                db.add(knowledge_point)
                await db.flush()
                
                # Create problems for this knowledge point
                for prob_data in kp_data["problems"]:
                    print(f"  ✅ Adding: #{prob_data['leetcode_id']} - {prob_data['title']}")
                    
                    problem = QuizQuestion(
                        knowledge_point_id=knowledge_point.id,
                        leetcode_id=prob_data["leetcode_id"],
                        title=prob_data["title"],
                        description=prob_data["description"],
                        difficulty=prob_data["difficulty"],
                        hints=prob_data["hints"],
                        video_link=prob_data["video_link"],
                        test_cases=prob_data.get("test_cases", []),
                        solution=None,
                        starter_code=None
                    )
                    db.add(problem)
            
            await db.commit()
            print("\n✨ Successfully initialized LeetCode Hot 100 data!")
            print(f"📊 Total knowledge points: {len(LEETCODE_HOT_100)}")
            total_problems = sum(len(kp["problems"]) for kp in LEETCODE_HOT_100)
            print(f"📝 Total problems: {total_problems}")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error initializing data: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(init_leetcode_data())


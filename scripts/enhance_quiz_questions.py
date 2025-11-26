"""
Enhanced Quiz Questions Data
Add comprehensive test cases, hints, and starter code for LeetCode Hot 100
"""
import asyncio
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import AsyncSessionLocal
from app.models import QuizQuestion
from sqlalchemy import select


# Enhanced data with test cases, better hints, and starter code
ENHANCED_QUESTIONS = {
    # Two Sum - LeetCode 1
    1: {
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "expected": "[0,1]"},
            {"input": "[3,2,4]\n6", "expected": "[1,2]"},
            {"input": "[3,3]\n6", "expected": "[0,1]"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Brute Force (O(n²)): Check every pair - inefficient\n2. Better Approach: Use a hash map to store numbers you've seen\n3. Key Insight: For each number x, look for (target - x) in the hash map\n4. Time Complexity: Can you do it in O(n)?\n\nThink: What should you store in the hash map?"
            },
            {
                "type": "code",
                "content": "# Two Sum - Core Implementation Pattern\n\ndef twoSum(nums, target):\n    # Step 1: Create a hash map\n    seen = {}  # {value: index}\n    \n    # Step 2: Iterate through array\n    for i, num in enumerate(nums):\n        complement = target - num\n        \n        # Step 3: Check if complement exists\n        if complement in seen:\n            return [seen[complement], i]\n        \n        # Step 4: Store current number\n        seen[num] = i\n    \n    return []  # No solution found"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=KLlXCFG5TnA\n\nNeetCode provides step-by-step walkthrough with visualization."
            }
        ],
        "starter_code": {
            "python": "def twoSum(nums: List[int], target: int) -> List[int]:\n    # Write your solution here\n    pass",
            "javascript": "function twoSum(nums, target) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}",
            "cpp": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};"
        }
    },
    
    # Contains Duplicate - LeetCode 217
    217: {
        "test_cases": [
            {"input": "[1,2,3,1]", "expected": "true"},
            {"input": "[1,2,3,4]", "expected": "false"},
            {"input": "[1,1,1,3,3,4,3,2,4,2]", "expected": "true"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Problem: Detect if any value appears twice\n2. Approaches:\n   - Sorting: Sort array, check adjacent elements - O(n log n)\n   - Hash Set: Use set to track seen numbers - O(n)\n3. Key Insight: Set only stores unique values\n4. Optimal: Hash set approach is O(n) time, O(n) space\n\nWhich data structure is perfect for checking duplicates?"
            },
            {
                "type": "code",
                "content": "# Contains Duplicate - Implementation Pattern\n\ndef containsDuplicate(nums):\n    # Method 1: Using Set (Most Pythonic)\n    return len(nums) != len(set(nums))\n    \n    # Method 2: Hash Set with iteration (More explicit)\n    seen = set()\n    for num in nums:\n        if num in seen:\n            return True\n        seen.add(num)\n    return False"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=3OamzN90kPg\n\nLearn multiple approaches and optimization techniques."
            }
        ],
        "starter_code": {
            "python": "def containsDuplicate(nums: List[int]) -> bool:\n    # Write your solution here\n    pass",
            "javascript": "function containsDuplicate(nums) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public boolean containsDuplicate(int[] nums) {\n        // Write your solution here\n        return false;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool containsDuplicate(vector<int>& nums) {\n        // Write your solution here\n        return false;\n    }\n};"
        }
    },
    
    # Valid Anagram - LeetCode 242
    242: {
        "test_cases": [
            {"input": "anagram\nnagaram", "expected": "true"},
            {"input": "rat\ncar", "expected": "false"},
            {"input": "listen\nsilent", "expected": "true"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Definition: Anagram = same letters, different order\n2. Approaches:\n   - Sorting: Sort both strings and compare - O(n log n)\n   - Hash Map: Count character frequencies - O(n)\n   - Array: Use fixed-size array for 26 letters - O(n)\n3. Edge Cases: Different lengths? Empty strings?\n4. Optimal: Hash map or character count array\n\nHow can you efficiently compare character frequencies?"
            },
            {
                "type": "code",
                "content": "# Valid Anagram - Implementation Patterns\n\ndef isAnagram(s, t):\n    # Method 1: Sorting (Simple)\n    return sorted(s) == sorted(t)\n    \n    # Method 2: Hash Map (Optimal)\n    if len(s) != len(t):\n        return False\n    \n    count = {}\n    for char in s:\n        count[char] = count.get(char, 0) + 1\n    \n    for char in t:\n        if char not in count:\n            return False\n        count[char] -= 1\n        if count[char] < 0:\n            return False\n    \n    return True"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=9UtInBqnCgA\n\nLearn different approaches and optimization techniques."
            }
        ],
        "starter_code": {
            "python": "def isAnagram(s: str, t: str) -> bool:\n    # Write your solution here\n    pass",
            "javascript": "function isAnagram(s, t) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public boolean isAnagram(String s, String t) {\n        // Write your solution here\n        return false;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write your solution here\n        return false;\n    }\n};"
        }
    },
    
    # Group Anagrams - LeetCode 49
    49: {
        "test_cases": [
            {"input": "[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "expected": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]"},
            {"input": "[\"\"]", "expected": "[[\"\"]]"},
            {"input": "[\"a\"]", "expected": "[[\"a\"]]"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Goal: Group strings that are anagrams together\n2. Key Insight: Anagrams have the same sorted characters\n3. Approach: Use sorted string as hash key\n4. Data Structure: HashMap with sorted string → list of words\n5. Time Complexity: O(n * k log k) where n=words, k=avg length\n\nWhat makes a good hash key for grouping anagrams?"
            },
            {
                "type": "code",
                "content": "# Group Anagrams - Implementation Pattern\n\nfrom collections import defaultdict\n\ndef groupAnagrams(strs):\n    # Use sorted tuple as key\n    groups = defaultdict(list)\n    \n    for word in strs:\n        # Sort characters to create key\n        key = tuple(sorted(word))\n        groups[key].append(word)\n    \n    # Return all groups\n    return list(groups.values())\n\n# Alternative: Use character count as key\ndef groupAnagrams_v2(strs):\n    groups = defaultdict(list)\n    \n    for word in strs:\n        # Create count array [a-z]\n        count = [0] * 26\n        for char in word:\n            count[ord(char) - ord('a')] += 1\n        \n        key = tuple(count)\n        groups[key].append(word)\n    \n    return list(groups.values())"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=vzdNOK2oB2E\n\nLearn how to use hash maps effectively for grouping."
            }
        ],
        "starter_code": {
            "python": "def groupAnagrams(strs: List[str]) -> List[List[str]]:\n    # Write your solution here\n    pass",
            "javascript": "function groupAnagrams(strs) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public List<List<String>> groupAnagrams(String[] strs) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}",
            "cpp": "class Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        // Write your solution here\n        return {};\n    }\n};"
        }
    },
    
    # Top K Frequent Elements - LeetCode 347
    347: {
        "test_cases": [
            {"input": "[1,1,1,2,2,3]\n2", "expected": "[1,2]"},
            {"input": "[1]\n1", "expected": "[1]"},
            {"input": "[1,2]\n2", "expected": "[1,2]"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Goal: Find k most frequent elements\n2. Approaches:\n   - Sorting: Count frequencies, sort - O(n log n)\n   - Heap: Use min-heap of size k - O(n log k)\n   - Bucket Sort: Group by frequency - O(n)\n3. Key Insight: Frequency range is [1, n]\n4. Optimal: Bucket sort approach is O(n)\n\nCan you use the frequency range constraint?"
            },
            {
                "type": "code",
                "content": "# Top K Frequent Elements - Implementation Patterns\n\nfrom collections import Counter\nimport heapq\n\ndef topKFrequent(nums, k):\n    # Method 1: Using Counter + Heap\n    count = Counter(nums)\n    return [num for num, freq in count.most_common(k)]\n    \n    # Method 2: Bucket Sort (O(n))\n    count = Counter(nums)\n    # Create buckets: index = frequency\n    buckets = [[] for _ in range(len(nums) + 1)]\n    \n    for num, freq in count.items():\n        buckets[freq].append(num)\n    \n    # Collect from high frequency to low\n    result = []\n    for freq in range(len(buckets) - 1, -1, -1):\n        result.extend(buckets[freq])\n        if len(result) >= k:\n            return result[:k]\n    \n    return result"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=YPTqKIgVk-k\n\nLearn bucket sort technique for optimal O(n) solution."
            }
        ],
        "starter_code": {
            "python": "def topKFrequent(nums: List[int], k: int) -> List[int]:\n    # Write your solution here\n    pass",
            "javascript": "function topKFrequent(nums, k) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public int[] topKFrequent(int[] nums, int k) {\n        // Write your solution here\n        return new int[]{};\n    }\n}",
            "cpp": "class Solution {\npublic:\n    vector<int> topKFrequent(vector<int>& nums, int k) {\n        // Write your solution here\n        return {};\n    }\n};"
        }
    },
    
    # Valid Palindrome - LeetCode 125
    125: {
        "test_cases": [
            {"input": "A man, a plan, a canal: Panama", "expected": "true"},
            {"input": "race a car", "expected": "false"},
            {"input": " ", "expected": "true"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Definition: Read same forwards and backwards\n2. Key: Only consider alphanumeric characters, ignore case\n3. Approaches:\n   - Two pointers: Start from both ends - O(n), O(1)\n   - Clean string: Remove non-alphanumeric, compare - O(n), O(n)\n4. Edge Cases: Empty string? All spaces? Mixed case?\n5. Optimal: Two pointers from both ends\n\nHow can you skip non-alphanumeric characters efficiently?"
            },
            {
                "type": "code",
                "content": "# Valid Palindrome - Implementation Pattern\n\ndef isPalindrome(s):\n    # Two pointers approach\n    left, right = 0, len(s) - 1\n    \n    while left < right:\n        # Skip non-alphanumeric from left\n        while left < right and not s[left].isalnum():\n            left += 1\n        \n        # Skip non-alphanumeric from right\n        while left < right and not s[right].isalnum():\n            right -= 1\n        \n        # Compare characters (case-insensitive)\n        if s[left].lower() != s[right].lower():\n            return False\n        \n        left += 1\n        right -= 1\n    \n    return True\n\n# Alternative: Clean string first\ndef isPalindrome_v2(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=jJXJ16kPFWg\n\nLearn two-pointer technique and string manipulation."
            }
        ],
        "starter_code": {
            "python": "def isPalindrome(s: str) -> bool:\n    # Write your solution here\n    pass",
            "javascript": "function isPalindrome(s) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public boolean isPalindrome(String s) {\n        // Write your solution here\n        return false;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Write your solution here\n        return false;\n    }\n};"
        }
    },
    
    # Longest Substring Without Repeating Characters - LeetCode 3
    3: {
        "test_cases": [
            {"input": "abcabcbb", "expected": "3"},
            {"input": "bbbbb", "expected": "1"},
            {"input": "pwwkew", "expected": "3"},
            {"input": "", "expected": "0"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Goal: Find longest substring without repeating chars\n2. Technique: Sliding Window with hash set/map\n3. Key Insight: Expand window until duplicate, then shrink\n4. Data Structure: Set to track characters in current window\n5. Time Complexity: O(n) with sliding window\n\nWhen do you need to shrink the window?"
            },
            {
                "type": "code",
                "content": "# Longest Substring Without Repeating - Pattern\n\ndef lengthOfLongestSubstring(s):\n    char_set = set()\n    left = 0\n    max_length = 0\n    \n    for right in range(len(s)):\n        # Shrink window while duplicate exists\n        while s[right] in char_set:\n            char_set.remove(s[left])\n            left += 1\n        \n        # Add current character\n        char_set.add(s[right])\n        max_length = max(max_length, right - left + 1)\n    \n    return max_length\n\n# Alternative: Using hash map with index\ndef lengthOfLongestSubstring_v2(s):\n    char_index = {}  # {char: last_seen_index}\n    left = 0\n    max_length = 0\n    \n    for right, char in enumerate(s):\n        if char in char_index and char_index[char] >= left:\n            left = char_index[char] + 1\n        \n        char_index[char] = right\n        max_length = max(max_length, right - left + 1)\n    \n    return max_length"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=wiGpQwVHdE0\n\nMaster sliding window technique with visualization."
            }
        ],
        "starter_code": {
            "python": "def lengthOfLongestSubstring(s: str) -> int:\n    # Write your solution here\n    pass",
            "javascript": "function lengthOfLongestSubstring(s) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public int lengthOfLongestSubstring(String s) {\n        // Write your solution here\n        return 0;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Write your solution here\n        return 0;\n    }\n};"
        }
    },
    
    # Binary Search - LeetCode 704
    704: {
        "test_cases": [
            {"input": "[-1,0,3,5,9,12]\n9", "expected": "4"},
            {"input": "[-1,0,3,5,9,12]\n2", "expected": "-1"},
            {"input": "[5]\n5", "expected": "0"},
        ],
        "hints": [
            {
                "type": "strategy",
                "content": "💡 Strategy Hint:\n\n1. Requirement: Array is sorted - binary search applicable\n2. Idea: Divide search space in half each iteration\n3. Template: left=0, right=len-1, compare mid with target\n4. Edge Cases: Empty array? Target not found?\n5. Time Complexity: O(log n) - very efficient!\n\nBe careful with mid calculation to avoid overflow!"
            },
            {
                "type": "code",
                "content": "# Binary Search - Classic Template\n\ndef search(nums, target):\n    left, right = 0, len(nums) - 1\n    \n    while left <= right:\n        # Calculate mid (avoid overflow)\n        mid = left + (right - left) // 2\n        \n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1  # Search right half\n        else:\n            right = mid - 1  # Search left half\n    \n    return -1  # Target not found\n\n# Remember:\n# - Use 'left <= right' for inclusive bounds\n# - Update left = mid + 1 or right = mid - 1\n# - Return -1 if not found"
            },
            {
                "type": "video",
                "content": "🎥 Watch detailed explanation:\nhttps://www.youtube.com/watch?v=s4DPM8ct1pI\n\nLearn binary search fundamentals and common pitfalls."
            }
        ],
        "starter_code": {
            "python": "def search(nums: List[int], target: int) -> int:\n    # Write your solution here\n    pass",
            "javascript": "function search(nums, target) {\n    // Write your solution here\n}",
            "java": "class Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};"
        }
    },
}


async def enhance_questions():
    """Update quiz questions with enhanced data"""
    async with AsyncSessionLocal() as db:
        print("🚀 Starting quiz questions enhancement...")
        print()
        
        updated_count = 0
        skipped_count = 0
        
        for leetcode_id, enhanced_data in ENHANCED_QUESTIONS.items():
            # Find question by leetcode_id
            result = await db.execute(
                select(QuizQuestion).where(QuizQuestion.leetcode_id == leetcode_id)
            )
            question = result.scalar_one_or_none()
            
            if not question:
                print(f"⚠️  LeetCode #{leetcode_id} not found in database")
                skipped_count += 1
                continue
            
            # Update test cases
            question.test_cases = enhanced_data.get("test_cases", [])
            
            # Update hints
            question.hints = enhanced_data.get("hints", [])
            
            # Update starter code
            question.starter_code = enhanced_data.get("starter_code", {})
            
            updated_count += 1
            print(f"✅ Updated #{leetcode_id}: {question.title}")
            print(f"   - Test cases: {len(question.test_cases)}")
            print(f"   - Hints: {len(question.hints)} levels")
            print(f"   - Languages: {len(question.starter_code)} (Python, JS, Java, C++)")
            print()
        
        # Commit changes
        await db.commit()
        
        print("=" * 60)
        print(f"✨ Enhancement complete!")
        print(f"   Updated: {updated_count} questions")
        print(f"   Skipped: {skipped_count} questions")
        print()
        print("📊 Next Steps:")
        print("   1. Test the code execution feature")
        print("   2. Try the hint system in Code Check page")
        print("   3. Submit code to see AI suggestions")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(enhance_questions())


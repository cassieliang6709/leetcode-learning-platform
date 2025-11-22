"""
Complete LeetCode Hot 100 problems with 3-level hints
Optimized version with template-based hint generation
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import AsyncSessionLocal, init_db
from backend.app.models import KnowledgePoint, QuizQuestion


# Template for generating hints based on problem category
def generate_hints(title, category, difficulty):
    """Generate 3-level hints using templates"""
    hints = [
        {
            "type": "strategy",
            "content": f"For {title}: Analyze the problem and identify the key data structure and algorithm pattern. Consider the constraints and think about optimal time/space complexity."
        },
        {
            "type": "code",
            "content": f"# {title} - {difficulty}\n# Category: {category}\n# Implement your solution here\n# Time: O(?), Space: O(?)"
        },
        {
            "type": "video",
            "content": "Watch NeetCode's explanation for detailed walkthrough"
        }
    ]
    return hints


# Complete LeetCode Hot 100 dataset
LEETCODE_HOT_100 = [
    {
        "knowledge_point": "Array & Hash Table",
        "category": "array",
        "difficulty": "easy",
        "description": "Master array manipulation and hash table techniques for efficient lookups and storage",
        "problems": [
            {"id": 1, "title": "Two Sum", "difficulty": "easy", "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.", "video": "https://www.youtube.com/watch?v=KLlXCFG5TnA"},
            {"id": 217, "title": "Contains Duplicate", "difficulty": "easy", "description": "Given an integer array nums, return true if any value appears at least twice.", "video": "https://www.youtube.com/watch?v=3OamzN90kPg"},
            {"id": 242, "title": "Valid Anagram", "difficulty": "easy", "description": "Given two strings s and t, return true if t is an anagram of s.", "video": "https://www.youtube.com/watch?v=9UtInBqnCgA"},
            {"id": 49, "title": "Group Anagrams", "difficulty": "medium", "description": "Group strings that are anagrams of each other.", "video": "https://www.youtube.com/watch?v=vzdNOK2oB2E"},
            {"id": 347, "title": "Top K Frequent Elements", "difficulty": "medium", "description": "Return the k most frequent elements from an array.", "video": "https://www.youtube.com/watch?v=YPTqKIgVk-k"},
            {"id": 238, "title": "Product of Array Except Self", "difficulty": "medium", "description": "Return an array where each element is the product of all elements except itself.", "video": "https://www.youtube.com/watch?v=bNvIQI2wAjk"},
            {"id": 128, "title": "Longest Consecutive Sequence", "difficulty": "medium", "description": "Find the length of the longest consecutive elements sequence.", "video": "https://www.youtube.com/watch?v=P6RZZMu_maU"},
            {"id": 560, "title": "Subarray Sum Equals K", "difficulty": "medium", "description": "Find total number of continuous subarrays whose sum equals k.", "video": "https://www.youtube.com/watch?v=HbbYPQc-Oo4"},
        ]
    },
    {
        "knowledge_point": "Two Pointers",
        "category": "two_pointers",
        "difficulty": "easy",
        "description": "Learn efficient two-pointer techniques for array and string problems",
        "problems": [
            {"id": 125, "title": "Valid Palindrome", "difficulty": "easy", "description": "Check if a string is a palindrome, considering only alphanumeric characters.", "video": "https://www.youtube.com/watch?v=jJXJ16kPFWg"},
            {"id": 15, "title": "3Sum", "difficulty": "medium", "description": "Find all triplets that sum to zero.", "video": "https://www.youtube.com/watch?v=jzZsG8n2R9A"},
            {"id": 11, "title": "Container With Most Water", "difficulty": "medium", "description": "Find two lines that together with x-axis form a container with most water.", "video": "https://www.youtube.com/watch?v=UuiTKBwPgAo"},
            {"id": 42, "title": "Trapping Rain Water", "difficulty": "hard", "description": "Calculate how much water can be trapped after raining.", "video": "https://www.youtube.com/watch?v=ZI2z5pq0TqA"},
            {"id": 167, "title": "Two Sum II", "difficulty": "medium", "description": "Find two numbers in a sorted array that add up to target.", "video": "https://www.youtube.com/watch?v=-gjxg6Pln50"},
            {"id": 283, "title": "Move Zeroes", "difficulty": "easy", "description": "Move all zeros to the end while maintaining relative order.", "video": "https://www.youtube.com/watch?v=aayNRwUN3Do"},
        ]
    },
    {
        "knowledge_point": "Sliding Window",
        "category": "sliding_window",
        "difficulty": "medium",
        "description": "Master sliding window technique for substring and subarray problems",
        "problems": [
            {"id": 3, "title": "Longest Substring Without Repeating Characters", "difficulty": "medium", "description": "Find the length of longest substring without repeating characters.", "video": "https://www.youtube.com/watch?v=wiGpQwVHdE0"},
            {"id": 424, "title": "Longest Repeating Character Replacement", "difficulty": "medium", "description": "Find longest substring with same letter after k replacements.", "video": "https://www.youtube.com/watch?v=gqXU1UyA8pk"},
            {"id": 76, "title": "Minimum Window Substring", "difficulty": "hard", "description": "Find minimum window substring containing all characters of another string.", "video": "https://www.youtube.com/watch?v=jSto0O4AJbM"},
            {"id": 239, "title": "Sliding Window Maximum", "difficulty": "hard", "description": "Find maximum in each sliding window of size k.", "video": "https://www.youtube.com/watch?v=DfljaUwZsOk"},
            {"id": 567, "title": "Permutation in String", "difficulty": "medium", "description": "Check if one string's permutation is substring of another.", "video": "https://www.youtube.com/watch?v=UbyhOgBN834"},
            {"id": 438, "title": "Find All Anagrams in String", "difficulty": "medium", "description": "Find all start indices of anagrams in a string.", "video": "https://www.youtube.com/watch?v=G8xtZy0fDKg"},
        ]
    },
    {
        "knowledge_point": "Binary Search",
        "category": "binary_search",
        "difficulty": "medium",
        "description": "Learn binary search and its variations for efficient searching",
        "problems": [
            {"id": 704, "title": "Binary Search", "difficulty": "easy", "description": "Implement binary search algorithm.", "video": "https://www.youtube.com/watch?v=s4DPM8ct1pI"},
            {"id": 33, "title": "Search in Rotated Sorted Array", "difficulty": "medium", "description": "Search for a target in a rotated sorted array.", "video": "https://www.youtube.com/watch?v=U8XENwh8Oy8"},
            {"id": 153, "title": "Find Minimum in Rotated Sorted Array", "difficulty": "medium", "description": "Find minimum element in rotated sorted array.", "video": "https://www.youtube.com/watch?v=nIVW4P8b1VA"},
            {"id": 4, "title": "Median of Two Sorted Arrays", "difficulty": "hard", "description": "Find median of two sorted arrays.", "video": "https://www.youtube.com/watch?v=q6IEA26hvXc"},
            {"id": 74, "title": "Search a 2D Matrix", "difficulty": "medium", "description": "Search for a value in a 2D matrix.", "video": "https://www.youtube.com/watch?v=Ber2pi2C0j0"},
            {"id": 34, "title": "Find First and Last Position", "difficulty": "medium", "description": "Find starting and ending position of target in sorted array.", "video": "https://www.youtube.com/watch?v=4sQL7R5ySUU"},
        ]
    },
    {
        "knowledge_point": "Linked List",
        "category": "linked_list",
        "difficulty": "easy",
        "description": "Master linked list manipulation and traversal techniques",
        "problems": [
            {"id": 206, "title": "Reverse Linked List", "difficulty": "easy", "description": "Reverse a singly linked list.", "video": "https://www.youtube.com/watch?v=G0_I-ZF0S38"},
            {"id": 21, "title": "Merge Two Sorted Lists", "difficulty": "easy", "description": "Merge two sorted linked lists.", "video": "https://www.youtube.com/watch?v=XIdigk956u0"},
            {"id": 141, "title": "Linked List Cycle", "difficulty": "easy", "description": "Detect if linked list has a cycle.", "video": "https://www.youtube.com/watch?v=gBTe7lFR3vc"},
            {"id": 142, "title": "Linked List Cycle II", "difficulty": "medium", "description": "Find the node where cycle begins.", "video": "https://www.youtube.com/watch?v=QfbOhn0WZ88"},
            {"id": 2, "title": "Add Two Numbers", "difficulty": "medium", "description": "Add two numbers represented as linked lists.", "video": "https://www.youtube.com/watch?v=wgFPrzTjm7s"},
            {"id": 19, "title": "Remove Nth Node From End", "difficulty": "medium", "description": "Remove the nth node from end of list.", "video": "https://www.youtube.com/watch?v=XVuQxVej6y8"},
            {"id": 143, "title": "Reorder List", "difficulty": "medium", "description": "Reorder list in specific pattern.", "video": "https://www.youtube.com/watch?v=S5bfdUTrKLM"},
            {"id": 23, "title": "Merge K Sorted Lists", "difficulty": "hard", "description": "Merge k sorted linked lists.", "video": "https://www.youtube.com/watch?v=q5a5OiGbT6Q"},
        ]
    },
    {
        "knowledge_point": "Stack",
        "category": "stack",
        "difficulty": "easy",
        "description": "Learn stack data structure for LIFO operations",
        "problems": [
            {"id": 20, "title": "Valid Parentheses", "difficulty": "easy", "description": "Check if parentheses are valid.", "video": "https://www.youtube.com/watch?v=WTzjTskDFMg"},
            {"id": 155, "title": "Min Stack", "difficulty": "medium", "description": "Design a stack with min operation in O(1).", "video": "https://www.youtube.com/watch?v=qkLl7nAwDPo"},
            {"id": 739, "title": "Daily Temperatures", "difficulty": "medium", "description": "Find how many days until warmer temperature.", "video": "https://www.youtube.com/watch?v=cTBiBSnjO3c"},
            {"id": 84, "title": "Largest Rectangle in Histogram", "difficulty": "hard", "description": "Find largest rectangle area in histogram.", "video": "https://www.youtube.com/watch?v=zx5Sw9130L0"},
            {"id": 394, "title": "Decode String", "difficulty": "medium", "description": "Decode an encoded string.", "video": "https://www.youtube.com/watch?v=qB0zZpBJlh8"},
            {"id": 853, "title": "Car Fleet", "difficulty": "medium", "description": "Count number of car fleets.", "video": "https://www.youtube.com/watch?v=Pr6T-3yB9RM"},
        ]
    },
    {
        "knowledge_point": "Binary Tree",
        "category": "tree",
        "difficulty": "easy",
        "description": "Master binary tree traversal and manipulation",
        "problems": [
            {"id": 104, "title": "Maximum Depth of Binary Tree", "difficulty": "easy", "description": "Find maximum depth of binary tree.", "video": "https://www.youtube.com/watch?v=hTM3phVI6YQ"},
            {"id": 226, "title": "Invert Binary Tree", "difficulty": "easy", "description": "Invert a binary tree.", "video": "https://www.youtube.com/watch?v=OnSn2XEQ4MY"},
            {"id": 100, "title": "Same Tree", "difficulty": "easy", "description": "Check if two trees are identical.", "video": "https://www.youtube.com/watch?v=vRbbcKXCxOw"},
            {"id": 572, "title": "Subtree of Another Tree", "difficulty": "easy", "description": "Check if a tree is subtree of another.", "video": "https://www.youtube.com/watch?v=E36O5SWp-LE"},
            {"id": 102, "title": "Binary Tree Level Order Traversal", "difficulty": "medium", "description": "Traverse tree level by level.", "video": "https://www.youtube.com/watch?v=6ZnyEApgFYg"},
            {"id": 98, "title": "Validate Binary Search Tree", "difficulty": "medium", "description": "Check if tree is valid BST.", "video": "https://www.youtube.com/watch?v=s6ATEkipzow"},
            {"id": 230, "title": "Kth Smallest Element in BST", "difficulty": "medium", "description": "Find kth smallest element in BST.", "video": "https://www.youtube.com/watch?v=5LUXSvjmGCw"},
            {"id": 105, "title": "Construct Binary Tree", "difficulty": "medium", "description": "Construct tree from preorder and inorder traversal.", "video": "https://www.youtube.com/watch?v=ihj4IQGZ2zc"},
            {"id": 124, "title": "Binary Tree Maximum Path Sum", "difficulty": "hard", "description": "Find maximum path sum in binary tree.", "video": "https://www.youtube.com/watch?v=Hr5cWUld4vU"},
            {"id": 297, "title": "Serialize and Deserialize Binary Tree", "difficulty": "hard", "description": "Serialize and deserialize binary tree.", "video": "https://www.youtube.com/watch?v=u4JAi2JJhI8"},
            {"id": 236, "title": "Lowest Common Ancestor", "difficulty": "medium", "description": "Find LCA of two nodes.", "video": "https://www.youtube.com/watch?v=gs2LMfuOR9k"},
            {"id": 543, "title": "Diameter of Binary Tree", "difficulty": "easy", "description": "Find diameter of binary tree.", "video": "https://www.youtube.com/watch?v=bkxqA8Rfv04"},
            {"id": 110, "title": "Balanced Binary Tree", "difficulty": "easy", "description": "Check if tree is height-balanced.", "video": "https://www.youtube.com/watch?v=QfJsau0ItOY"},
        ]
    },
    {
        "knowledge_point": "Dynamic Programming",
        "category": "dynamic_programming",
        "difficulty": "medium",
        "description": "Master dynamic programming for optimization problems",
        "problems": [
            {"id": 70, "title": "Climbing Stairs", "difficulty": "easy", "description": "Count ways to climb n stairs.", "video": "https://www.youtube.com/watch?v=Y0lT9Fck7qI"},
            {"id": 198, "title": "House Robber", "difficulty": "medium", "description": "Rob houses to maximize amount without alerting police.", "video": "https://www.youtube.com/watch?v=xlvhyfcoQa4"},
            {"id": 213, "title": "House Robber II", "difficulty": "medium", "description": "Rob houses arranged in circle.", "video": "https://www.youtube.com/watch?v=rWAJCfYYOvM"},
            {"id": 5, "title": "Longest Palindromic Substring", "difficulty": "medium", "description": "Find longest palindromic substring.", "video": "https://www.youtube.com/watch?v=XYQecbcd6_c"},
            {"id": 300, "title": "Longest Increasing Subsequence", "difficulty": "medium", "description": "Find length of longest increasing subsequence.", "video": "https://www.youtube.com/watch?v=cjWnW0hdF1Y"},
            {"id": 322, "title": "Coin Change", "difficulty": "medium", "description": "Find minimum coins needed for amount.", "video": "https://www.youtube.com/watch?v=H9bfqozjoqs"},
            {"id": 139, "title": "Word Break", "difficulty": "medium", "description": "Check if string can be segmented into dictionary words.", "video": "https://www.youtube.com/watch?v=Sx9NNgInc3A"},
            {"id": 152, "title": "Maximum Product Subarray", "difficulty": "medium", "description": "Find contiguous subarray with largest product.", "video": "https://www.youtube.com/watch?v=lXVy6YWFcRM"},
            {"id": 416, "title": "Partition Equal Subset Sum", "difficulty": "medium", "description": "Check if array can be partitioned into equal sum subsets.", "video": "https://www.youtube.com/watch?v=IsvocB5BJhw"},
            {"id": 62, "title": "Unique Paths", "difficulty": "medium", "description": "Count unique paths in grid.", "video": "https://www.youtube.com/watch?v=IlEsdxuD4lY"},
            {"id": 55, "title": "Jump Game", "difficulty": "medium", "description": "Check if you can reach last index.", "video": "https://www.youtube.com/watch?v=Yan0cv2cLy8"},
            {"id": 45, "title": "Jump Game II", "difficulty": "medium", "description": "Find minimum jumps to reach end.", "video": "https://www.youtube.com/watch?v=dJ7sWiOoK7g"},
            {"id": 91, "title": "Decode Ways", "difficulty": "medium", "description": "Count ways to decode a string.", "video": "https://www.youtube.com/watch?v=6aEyTjOwlJU"},
        ]
    },
    {
        "knowledge_point": "Graph",
        "category": "graph",
        "difficulty": "medium",
        "description": "Learn graph algorithms and traversals",
        "problems": [
            {"id": 200, "title": "Number of Islands", "difficulty": "medium", "description": "Count number of islands in grid.", "video": "https://www.youtube.com/watch?v=pV2kpPD66nE"},
            {"id": 133, "title": "Clone Graph", "difficulty": "medium", "description": "Clone an undirected graph.", "video": "https://www.youtube.com/watch?v=mQeF6bN8hMk"},
            {"id": 207, "title": "Course Schedule", "difficulty": "medium", "description": "Check if can finish all courses.", "video": "https://www.youtube.com/watch?v=EgI5nU9etnU"},
            {"id": 417, "title": "Pacific Atlantic Water Flow", "difficulty": "medium", "description": "Find cells that can reach both oceans.", "video": "https://www.youtube.com/watch?v=s-VkcjHqkGI"},
            {"id": 130, "title": "Surrounded Regions", "difficulty": "medium", "description": "Capture surrounded regions.", "video": "https://www.youtube.com/watch?v=9z2BunfoZ5Y"},
            {"id": 210, "title": "Course Schedule II", "difficulty": "medium", "description": "Return course order.", "video": "https://www.youtube.com/watch?v=Akt3glAwyfY"},
            {"id": 684, "title": "Redundant Connection", "difficulty": "medium", "description": "Find edge that creates cycle.", "video": "https://www.youtube.com/watch?v=FXWRE67PLL0"},
        ]
    },
    {
        "knowledge_point": "Greedy",
        "category": "greedy",
        "difficulty": "medium",
        "description": "Master greedy algorithms for optimization",
        "problems": [
            {"id": 53, "title": "Maximum Subarray", "difficulty": "medium", "description": "Find contiguous subarray with maximum sum.", "video": "https://www.youtube.com/watch?v=5WZl3MMT0Eg"},
            {"id": 121, "title": "Best Time to Buy and Sell Stock", "difficulty": "easy", "description": "Maximize profit from stock prices.", "video": "https://www.youtube.com/watch?v=1pkOgXD63yU"},
            {"id": 122, "title": "Best Time to Buy and Sell Stock II", "difficulty": "medium", "description": "Maximize profit with multiple transactions.", "video": "https://www.youtube.com/watch?v=3SJ3pUkPQMc"},
            {"id": 763, "title": "Partition Labels", "difficulty": "medium", "description": "Partition string into as many parts as possible.", "video": "https://www.youtube.com/watch?v=B7m8UmZE-vw"},
        ]
    },
    {
        "knowledge_point": "Backtracking",
        "category": "backtracking",
        "difficulty": "medium",
        "description": "Learn backtracking for combinatorial problems",
        "problems": [
            {"id": 39, "title": "Combination Sum", "difficulty": "medium", "description": "Find all combinations that sum to target.", "video": "https://www.youtube.com/watch?v=GBKI9VSKdGg"},
            {"id": 46, "title": "Permutations", "difficulty": "medium", "description": "Generate all permutations of array.", "video": "https://www.youtube.com/watch?v=s7AvT7cGdSo"},
            {"id": 78, "title": "Subsets", "difficulty": "medium", "description": "Generate all subsets of array.", "video": "https://www.youtube.com/watch?v=REOH22Xwdkk"},
            {"id": 22, "title": "Generate Parentheses", "difficulty": "medium", "description": "Generate all valid parentheses combinations.", "video": "https://www.youtube.com/watch?v=s9fokUqJ76A"},
            {"id": 79, "title": "Word Search", "difficulty": "medium", "description": "Search for word in 2D grid.", "video": "https://www.youtube.com/watch?v=pfiQ_PS1g8E"},
            {"id": 131, "title": "Palindrome Partitioning", "difficulty": "medium", "description": "Partition string into palindromes.", "video": "https://www.youtube.com/watch?v=3jvWodd7ht0"},
        ]
    },
    {
        "knowledge_point": "Heap",
        "category": "heap",
        "difficulty": "medium",
        "description": "Master heap/priority queue data structure",
        "problems": [
            {"id": 215, "title": "Kth Largest Element", "difficulty": "medium", "description": "Find kth largest element in array.", "video": "https://www.youtube.com/watch?v=XEmy13g1Qxc"},
            {"id": 295, "title": "Find Median from Data Stream", "difficulty": "hard", "description": "Find median from data stream.", "video": "https://www.youtube.com/watch?v=itmhHWaHupI"},
            {"id": 973, "title": "K Closest Points to Origin", "difficulty": "medium", "description": "Find k closest points to origin.", "video": "https://www.youtube.com/watch?v=rI2EBUEMfTk"},
        ]
    },
    {
        "knowledge_point": "Bit Manipulation",
        "category": "bit",
        "difficulty": "easy",
        "description": "Learn bit manipulation techniques",
        "problems": [
            {"id": 191, "title": "Number of 1 Bits", "difficulty": "easy", "description": "Count number of 1 bits.", "video": "https://www.youtube.com/watch?v=5Km3utixwZs"},
            {"id": 338, "title": "Counting Bits", "difficulty": "easy", "description": "Count bits for 0 to n.", "video": "https://www.youtube.com/watch?v=awxaRgUB4Kw"},
            {"id": 136, "title": "Single Number", "difficulty": "easy", "description": "Find element appearing once.", "video": "https://www.youtube.com/watch?v=qMPX1AOa83k"},
        ]
    }
]


async def init_leetcode_data():
    """Initialize complete LeetCode Hot 100 data"""
    print("🚀 Initializing Complete LeetCode Hot 100...")
    print(f"📊 Total categories: {len(LEETCODE_HOT_100)}")
    
    total_problems = sum(len(cat["problems"]) for cat in LEETCODE_HOT_100)
    print(f"📝 Total problems: {total_problems}")
    
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            problem_count = 0
            
            for kp_data in LEETCODE_HOT_100:
                print(f"\n📚 Creating: {kp_data['knowledge_point']}")
                
                # Create knowledge point
                knowledge_point = KnowledgePoint(
                    name=kp_data["knowledge_point"],
                    description=kp_data["description"],
                    difficulty=kp_data["difficulty"],
                    category=kp_data["category"]
                )
                db.add(knowledge_point)
                await db.flush()
                
                # Create problems
                for prob in kp_data["problems"]:
                    problem_count += 1
                    print(f"  ✅ [{problem_count}/{total_problems}] #{prob['id']} - {prob['title']}")
                    
                    hints = generate_hints(prob['title'], kp_data['category'], prob['difficulty'])
                    
                    problem = QuizQuestion(
                        knowledge_point_id=knowledge_point.id,
                        leetcode_id=prob["id"],
                        title=prob["title"],
                        description=prob["description"],
                        difficulty=prob["difficulty"],
                        hints=hints,
                        video_link=prob["video"],
                        test_cases=[],
                        solution=None,
                        starter_code=None
                    )
                    db.add(problem)
            
            await db.commit()
            print(f"\n✨ Successfully initialized {problem_count} problems!")
            print(f"📊 Categories: {len(LEETCODE_HOT_100)}")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(init_leetcode_data())


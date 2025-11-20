"""
Add sample questions with test cases for code execution
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import engine
from app.models import QuizQuestion, KnowledgePoint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


async def add_sample_questions():
    """Add sample questions with executable test cases"""
    print("\n📝 Adding sample questions with test cases...")

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        # Get Arrays & Hashing knowledge point
        result = await session.execute(
            select(KnowledgePoint).where(KnowledgePoint.name == "Arrays & Hashing")
        )
        arrays_kp = result.scalar_one_or_none()
        
        if not arrays_kp:
            print("❌ Arrays & Hashing knowledge point not found. Run init_db_with_roadmap.py first.")
            return

        # Sample Question 1: Two Sum
        two_sum = QuizQuestion(
            knowledge_point_id=arrays_kp.id,
            leetcode_id=1,
            title="Two Sum",
            description="""Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
```

**Constraints:**
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.""",
            difficulty="easy",
            solution="""# Hash Map Approach - O(n) time, O(n) space

def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            hints={
                "level1": "Think about using a hash map to store numbers you've seen.",
                "level2": "For each number, check if (target - number) exists in your hash map.",
                "level3": "Store the index as the value in your hash map for quick lookup."
            },
            test_cases=[
                {
                    "input": "[2,7,11,15]\n9",
                    "expected": "[0, 1]"
                },
                {
                    "input": "[3,2,4]\n6",
                    "expected": "[1, 2]"
                },
                {
                    "input": "[3,3]\n6",
                    "expected": "[0, 1]"
                },
                {
                    "input": "[1,5,3,7,9]\n12",
                    "expected": "[2, 4]"
                }
            ],
            starter_code={
                "python": """def twoSum(nums, target):
    # Write your code here
    pass

# Read input
nums = eval(input())
target = int(input())

# Call function and print result
result = twoSum(nums, target)
print(result)""",
                "javascript": """function twoSum(nums, target) {
    // Write your code here
}

// Read input (for testing)
const input = require('fs').readFileSync(0, 'utf-8').trim().split('\\n');
const nums = JSON.parse(input[0]);
const target = parseInt(input[1]);

// Call function and print result
console.log(JSON.stringify(twoSum(nums, target)));""",
                "java": """import java.util.*;

class Solution {
    public static int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[]{};
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // Read nums array
        String numsStr = sc.nextLine();
        String[] parts = numsStr.replace("[", "").replace("]", "").split(",");
        int[] nums = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            nums[i] = Integer.parseInt(parts[i].trim());
        }
        // Read target
        int target = Integer.parseInt(sc.nextLine());
        
        // Call function and print result
        int[] result = twoSum(nums, target);
        System.out.println(Arrays.toString(result));
    }
}"""
            }
        )
        session.add(two_sum)

        # Sample Question 2: Valid Palindrome
        valid_palindrome = QuizQuestion(
            knowledge_point_id=arrays_kp.id,
            leetcode_id=125,
            title="Valid Palindrome",
            description="""A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

**Example 1:**
```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

**Example 2:**
```
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

**Example 3:**
```
Input: s = " "
Output: true
Explanation: Empty string is considered a palindrome.
```

**Constraints:**
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.""",
            difficulty="easy",
            solution="""# Two Pointers Approach - O(n) time, O(1) space

def isPalindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True""",
            hints={
                "level1": "Use two pointers starting from both ends.",
                "level2": "Skip non-alphanumeric characters and compare characters in lowercase.",
                "level3": "Move pointers inward until they meet or find a mismatch."
            },
            test_cases=[
                {
                    "input": "A man, a plan, a canal: Panama",
                    "expected": "true"
                },
                {
                    "input": "race a car",
                    "expected": "false"
                },
                {
                    "input": " ",
                    "expected": "true"
                },
                {
                    "input": "Was it a car or a cat I saw?",
                    "expected": "true"
                }
            ],
            starter_code={
                "python": """def isPalindrome(s):
    # Write your code here
    pass

# Read input
s = input()

# Call function and print result
result = isPalindrome(s)
print(str(result).lower())""",
                "javascript": """function isPalindrome(s) {
    // Write your code here
}

// Read input
const input = require('fs').readFileSync(0, 'utf-8').trim();

// Call function and print result
console.log(isPalindrome(input).toString());"""
            }
        )
        session.add(valid_palindrome)

        await session.commit()
        print("✅ Added 2 sample questions with test cases:")
        print("  1. Two Sum (Easy)")
        print("  2. Valid Palindrome (Easy)")
        print("\nThese questions can now be tested with real code execution!")


async def main():
    """Run the script"""
    print("=" * 60)
    print("ADDING SAMPLE QUESTIONS WITH TEST CASES")
    print("=" * 60)

    try:
        await add_sample_questions()
        
        print("\n" + "=" * 60)
        print("✅ Sample questions added successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Start backend: cd backend && uvicorn main:app --reload")
        print("  2. Test code execution at: http://localhost:8000/docs")
        print("  3. Try submitting code for these questions!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


import asyncio
import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update
from app.models import KnowledgePoint
from app.database import DATABASE_URL

# Markdown article content for testing
MARKDOWN_ARTICLE = """
# Two Pointers Technique

## Introduction

The **Two Pointers** technique is a common algorithmic pattern that uses two pointers (or indices) to iterate through a data structure, typically an array or linked list. This technique is particularly useful for solving problems that require:

- Searching for pairs in a sorted array
- Removing duplicates
- Finding subarrays that meet certain conditions
- Reversing or rearranging elements

## Core Concepts

### 1. Opposite Direction Pointers

In this pattern, one pointer starts from the beginning and another from the end, moving toward each other.

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []
```

### 2. Same Direction Pointers

Both pointers move in the same direction, often with one pointer moving faster than the other.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1
```

## When to Use Two Pointers

✓ The array is **sorted** or can be sorted  
✓ You need to find **pairs** or **triplets** with specific properties  
✓ You need to **partition** or **rearrange** elements  
✓ You want to achieve **O(n)** time complexity instead of O(n²)

## Common Patterns

### Pattern 1: Sum Problems

Finding pairs in a sorted array that sum to a target value.

**Example:** Two Sum II (Sorted Array)

### Pattern 2: Sliding Window

Using two pointers to maintain a window of elements.

**Example:** Longest Substring Without Repeating Characters

### Pattern 3: Fast and Slow Pointers

One pointer moves twice as fast as the other.

**Example:** Detecting cycles in linked lists

## Time Complexity

Most two-pointer solutions run in **O(n)** time complexity with **O(1)** space complexity, making them very efficient.

## Practice Tips

1. **Identify the pattern**: Look for sorted arrays or linked lists
2. **Define pointer behavior**: Decide whether pointers move in same or opposite directions
3. **Handle edge cases**: Empty arrays, single elements, duplicates
4. **Test with examples**: Walk through your solution with sample inputs

> 💡 **Pro Tip**: When stuck on an O(n²) solution, consider if two pointers could reduce it to O(n)!

---

## Common Mistakes to Avoid

- Forgetting to check array bounds
- Not handling the case when pointers meet
- Incorrectly updating pointer positions
- Assuming the array is sorted when it's not

Ready to practice? Let's solve some problems!
"""


async def update_article_content():
    """Update article content for Two Pointers knowledge point"""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Find the Two Pointers knowledge point (assuming it's ID 16 based on the terminal logs)
        result = await session.execute(
            select(KnowledgePoint).where(KnowledgePoint.name.like('%Two Pointer%'))
        )
        knowledge_point = result.scalar_one_or_none()
        
        if knowledge_point:
            print(f"Found knowledge point: {knowledge_point.name} (ID: {knowledge_point.id})")
            
            # Update with markdown article content
            await session.execute(
                update(KnowledgePoint)
                .where(KnowledgePoint.id == knowledge_point.id)
                .values(article_content=MARKDOWN_ARTICLE)
            )
            
            await session.commit()
            print(f"✅ Successfully updated article content with Markdown formatting!")
        else:
            print("❌ Two Pointers knowledge point not found")
            
            # List all knowledge points
            result = await session.execute(select(KnowledgePoint))
            points = result.scalars().all()
            print("\nAvailable knowledge points:")
            for point in points:
                print(f"  - {point.id}: {point.name}")


if __name__ == "__main__":
    asyncio.run(update_article_content())


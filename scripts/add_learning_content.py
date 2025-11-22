"""
Migration script to add article_content and reading_questions fields to knowledge_points table
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.database import engine, AsyncSessionLocal
import asyncio


async def add_learning_content_fields():
    """Add article_content and reading_questions columns to knowledge_points table"""
    async with engine.begin() as conn:
        try:
            # Check if columns already exist
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='knowledge_points' 
                AND column_name IN ('article_content', 'reading_questions')
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            
            # Add article_content if it doesn't exist
            if 'article_content' not in existing_columns:
                await conn.execute(text("""
                    ALTER TABLE knowledge_points 
                    ADD COLUMN article_content TEXT
                """))
                print("✓ Added article_content column")
            else:
                print("→ article_content column already exists")
            
            # Add reading_questions if it doesn't exist
            if 'reading_questions' not in existing_columns:
                await conn.execute(text("""
                    ALTER TABLE knowledge_points 
                    ADD COLUMN reading_questions JSON
                """))
                print("✓ Added reading_questions column")
            else:
                print("→ reading_questions column already exists")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise


async def add_sample_content():
    """Add sample learning content to existing knowledge points"""
    import json
    
    async with AsyncSessionLocal() as session:
        try:
            # Sample article for "Two Sum" or first knowledge point
            sample_article = """# Understanding Array Basics

Arrays are one of the most fundamental data structures in computer science. They provide a way to store multiple values of the same type in a contiguous block of memory.

## What is an Array?

An array is a collection of elements identified by index or key. Each element in an array can be accessed directly using its index, making arrays extremely efficient for random access operations.

## Time Complexity

- **Access**: O(1) - Direct access to any element
- **Search**: O(n) - Linear search through all elements
- **Insert/Delete**: O(n) - May require shifting elements

## Common Patterns

When working with array problems, you'll often encounter these patterns:

1. **Two Pointer Technique**: Using two pointers to traverse the array from different positions
2. **Sliding Window**: Maintaining a window of elements that satisfies certain conditions
3. **Hash Table**: Using additional space to store information for O(1) lookups

## Practice Strategy

Start with simple array manipulation problems, then progress to more complex two-pointer and sliding window problems. Understanding these fundamentals will help you solve more advanced algorithmic challenges."""

            sample_questions = [
                {
                    "question": "What is the time complexity of accessing an element in an array by its index?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    "correct_answer": 0,
                    "explanation": "Array access by index is O(1) because arrays store elements in contiguous memory locations. You can directly calculate the memory address of any element using its index."
                },
                {
                    "question": "Which pattern is most useful for finding pairs in an array?",
                    "options": ["Binary Search", "Two Pointer", "Dynamic Programming", "Divide and Conquer"],
                    "correct_answer": 1,
                    "explanation": "The Two Pointer technique is particularly effective for finding pairs in arrays, especially when the array is sorted. It allows you to efficiently explore combinations without nested loops."
                },
                {
                    "question": "What is the space complexity of the hash table approach for finding elements?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                    "correct_answer": 2,
                    "explanation": "Using a hash table requires O(n) extra space because you might need to store all n elements in the worst case. This trades space for improved time complexity."
                }
            ]

            # Convert to JSON string for PostgreSQL
            questions_json = json.dumps(sample_questions)

            # Update first knowledge point with sample content
            result = await session.execute(text("""
                UPDATE knowledge_points 
                SET article_content = :article,
                    reading_questions = CAST(:questions AS jsonb)
                WHERE id = (SELECT MIN(id) FROM knowledge_points)
                RETURNING id, name
            """), {"article": sample_article, "questions": questions_json})
            
            updated = result.fetchone()
            if updated:
                print(f"\n✓ Added sample content to knowledge point: {updated[1]} (ID: {updated[0]})")
            
            await session.commit()
            print("✅ Sample content added successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Failed to add sample content: {e}")
            raise


async def main():
    import sys
    
    print("=" * 60)
    print("Knowledge Points Learning Content Migration")
    print("=" * 60)
    print()
    
    # Add columns
    print("Step 1: Adding new columns to database...")
    await add_learning_content_fields()
    
    # Add sample content
    print("\nStep 2: Adding sample learning content...")
    
    # Check for command line argument or interactive mode
    add_sample = 'n'
    if len(sys.argv) > 1:
        add_sample = sys.argv[1].lower()
    else:
        try:
            add_sample = input("\nDo you want to add sample content to the first knowledge point? (y/n): ")
        except (EOFError, KeyboardInterrupt):
            print("\nRunning in non-interactive mode. Skipping sample content.")
            add_sample = 'n'
    
    if add_sample == 'y':
        await add_sample_content()
    else:
        print("Skipped adding sample content.")
    
    print("\n" + "=" * 60)
    print("Migration completed! Next steps:")
    print("1. Run the backend server: cd backend && python main.py")
    print("2. Check the Roadmap page and click on a knowledge point")
    print("3. Add more article content and questions to other knowledge points")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


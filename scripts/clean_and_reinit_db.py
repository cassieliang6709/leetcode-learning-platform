"""
Clean database and prepare for fresh LeetCode Hot 100 data
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from backend.app.database import AsyncSessionLocal, init_db
from backend.app.models import QuizQuestion, KnowledgePoint, QuizAttempt, CodeSubmission


async def clean_database():
    """Clean all quiz-related data from database"""
    print("🧹 Cleaning database...")
    
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            # Delete in correct order to respect foreign keys
            print("  Deleting quiz attempts...")
            await db.execute(text("DELETE FROM quiz_attempts"))
            
            print("  Deleting code submissions...")
            await db.execute(text("DELETE FROM code_submissions"))
            
            print("  Deleting quiz questions...")
            await db.execute(text("DELETE FROM quiz_questions"))
            
            print("  Deleting knowledge points...")
            await db.execute(text("DELETE FROM knowledge_points"))
            
            # Reset sequences
            print("  Resetting ID sequences...")
            await db.execute(text("ALTER SEQUENCE quiz_questions_id_seq RESTART WITH 1"))
            await db.execute(text("ALTER SEQUENCE knowledge_points_id_seq RESTART WITH 1"))
            
            await db.commit()
            print("✅ Database cleaned successfully!")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error cleaning database: {str(e)}")
            raise


if __name__ == "__main__":
    asyncio.run(clean_database())


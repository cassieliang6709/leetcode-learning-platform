#!/usr/bin/env python3
"""
Create daily_knowledge_questions and daily_knowledge_attempts tables
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import text
from app.database import engine


async def migrate():
    """Create new tables for daily knowledge questions"""
    
    async with engine.begin() as conn:
        print("Creating daily_knowledge_questions table...")
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS daily_knowledge_questions (
                    id SERIAL PRIMARY KEY,
                    knowledge_point_id INTEGER REFERENCES knowledge_points(id),
                    question TEXT NOT NULL,
                    options JSON NOT NULL,
                    correct_answer INTEGER NOT NULL,
                    explanation TEXT,
                    difficulty VARCHAR(20) DEFAULT 'medium',
                    category VARCHAR(50),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("✓ Created daily_knowledge_questions table")
        except Exception as e:
            print(f"✗ Error creating daily_knowledge_questions: {e}")
            raise
        
        print("Creating daily_knowledge_attempts table...")
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS daily_knowledge_attempts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    question_id INTEGER NOT NULL REFERENCES daily_knowledge_questions(id),
                    is_correct BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("✓ Created daily_knowledge_attempts table")
        except Exception as e:
            print(f"✗ Error creating daily_knowledge_attempts: {e}")
            raise
        
        print("Creating indexes...")
        try:
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_daily_knowledge_kp 
                ON daily_knowledge_questions(knowledge_point_id)
            """))
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_daily_attempts_user 
                ON daily_knowledge_attempts(user_id)
            """))
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_daily_attempts_date 
                ON daily_knowledge_attempts(completed_at)
            """))
            print("✓ Created indexes")
        except Exception as e:
            print(f"✗ Error creating indexes: {e}")
    
    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(migrate())


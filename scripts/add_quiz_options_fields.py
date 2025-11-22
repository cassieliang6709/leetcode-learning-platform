#!/usr/bin/env python3
"""
Add options, correct_answer, and explanation fields to quiz_questions table
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import text
from app.database import engine


async def migrate():
    """Add new fields to quiz_questions table"""
    
    async with engine.begin() as conn:
        print("Adding options field...")
        try:
            await conn.execute(text(
                "ALTER TABLE quiz_questions ADD COLUMN IF NOT EXISTS options JSON"
            ))
            print("✓ Added options field")
        except Exception as e:
            print(f"✗ Error adding options: {e}")
        
        print("Adding correct_answer field...")
        try:
            await conn.execute(text(
                "ALTER TABLE quiz_questions ADD COLUMN IF NOT EXISTS correct_answer INTEGER"
            ))
            print("✓ Added correct_answer field")
        except Exception as e:
            print(f"✗ Error adding correct_answer: {e}")
        
        print("Adding explanation field...")
        try:
            await conn.execute(text(
                "ALTER TABLE quiz_questions ADD COLUMN IF NOT EXISTS explanation TEXT"
            ))
            print("✓ Added explanation field")
        except Exception as e:
            print(f"✗ Error adding explanation: {e}")
    
    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(migrate())


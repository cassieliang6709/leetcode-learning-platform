#!/usr/bin/env python3
"""
Migration Script: Add code execution columns to quiz_questions table
- test_cases: JSON column for test case data
- starter_code: JSON column for starter code templates
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text
from app.database import engine

async def migrate():
    print("=" * 60)
    print("DATABASE MIGRATION: Add Code Execution Columns")
    print("=" * 60)
    print()
    
    async with engine.begin() as conn:
        # Check if columns already exist
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'quiz_questions' 
            AND column_name IN ('test_cases', 'starter_code')
        """)
        
        result = await conn.execute(check_query)
        existing_columns = [row[0] for row in result.fetchall()]
        
        if 'test_cases' in existing_columns and 'starter_code' in existing_columns:
            print("✓ Columns already exist! No migration needed.")
            return
        
        print("📝 Adding columns to quiz_questions table...")
        
        # Add test_cases column
        if 'test_cases' not in existing_columns:
            await conn.execute(text("""
                ALTER TABLE quiz_questions 
                ADD COLUMN test_cases JSON
            """))
            print("✓ Added 'test_cases' column")
        else:
            print("⚠️  'test_cases' column already exists")
        
        # Add starter_code column
        if 'starter_code' not in existing_columns:
            await conn.execute(text("""
                ALTER TABLE quiz_questions 
                ADD COLUMN starter_code JSON
            """))
            print("✓ Added 'starter_code' column")
        else:
            print("⚠️  'starter_code' column already exists")
        
        print()
        print("=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Run: python3 scripts/add_sample_questions.py")
        print("  2. Start backend: cd backend && uvicorn main:app --reload")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(migrate())
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)



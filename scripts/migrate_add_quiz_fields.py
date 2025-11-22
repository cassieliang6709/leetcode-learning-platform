"""
Database migration to add new fields to quiz_questions table
Adds: options (JSON), correct_answer (Integer), explanation (Text)
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Database URL - update this with your database credentials
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/leetcode_learning"


async def migrate_database():
    """Add new columns to quiz_questions table"""
    print("🔄 Starting database migration...")
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        try:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'quiz_questions' 
                AND column_name IN ('options', 'correct_answer', 'explanation');
            """)
            result = await conn.execute(check_query)
            existing_columns = [row[0] for row in result.fetchall()]
            
            if len(existing_columns) == 3:
                print("✅ All columns already exist. Migration not needed.")
                return
            
            # Add options column (JSON)
            if 'options' not in existing_columns:
                await conn.execute(text("""
                    ALTER TABLE quiz_questions 
                    ADD COLUMN IF NOT EXISTS options JSON;
                """))
                print("✅ Added 'options' column")
            
            # Add correct_answer column (Integer)
            if 'correct_answer' not in existing_columns:
                await conn.execute(text("""
                    ALTER TABLE quiz_questions 
                    ADD COLUMN IF NOT EXISTS correct_answer INTEGER;
                """))
                print("✅ Added 'correct_answer' column")
            
            # Add explanation column (Text)
            if 'explanation' not in existing_columns:
                await conn.execute(text("""
                    ALTER TABLE quiz_questions 
                    ADD COLUMN IF NOT EXISTS explanation TEXT;
                """))
                print("✅ Added 'explanation' column")
            
            print("\n🎉 Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         Database Migration Script                     ║
    ║    Add quiz fields: options, correct_answer, explanation║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚙️  Please update DATABASE_URL in the script before running!")
    print(f"Current DATABASE_URL: {DATABASE_URL}\n")
    
    asyncio.run(migrate_database())


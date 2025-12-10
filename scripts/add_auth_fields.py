#!/usr/bin/env python3
"""
Add authentication fields to users table
"""
import asyncio
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text
from app.database import engine
from app.services.auth_service import hash_password


async def migrate_users():
    """Add hashed_password field to existing users"""
    async with engine.begin() as conn:
        # Check if column already exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='hashed_password'
        """))
        
        if result.scalar_one_or_none():
            print("✓ hashed_password column already exists")
        else:
            print("Adding hashed_password column...")
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN hashed_password VARCHAR(255)
            """))
            print("✓ Added hashed_password column")
        
        # Set default password for existing users
        result = await conn.execute(text("""
            SELECT COUNT(*) FROM users WHERE hashed_password IS NULL
        """))
        count = result.scalar()
        
        if count > 0:
            print(f"Setting default password for {count} existing users...")
            default_password = hash_password("password123")
            await conn.execute(text(f"""
                UPDATE users 
                SET hashed_password = '{default_password}'
                WHERE hashed_password IS NULL
            """))
            print("✓ Updated existing users with default password: 'password123'")
        
        # Make column NOT NULL
        await conn.execute(text("""
            ALTER TABLE users 
            ALTER COLUMN hashed_password SET NOT NULL
        """))
        print("✓ Set hashed_password as NOT NULL")
        
        # Add indexes for better performance
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)
        """))
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
        """))
        print("✓ Added indexes on username and email")
    
    print("\n✅ Migration completed successfully!")
    print("\nℹ️  Existing users can now login with password: 'password123'")


if __name__ == "__main__":
    asyncio.run(migrate_users())














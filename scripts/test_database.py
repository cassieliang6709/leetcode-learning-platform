#!/usr/bin/env python3
"""
数据库连接测试脚本
Test database connection and verify setup
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import engine, DATABASE_URL
from sqlalchemy import text


async def test_connection():
    """Test database connection and query data"""
    print("=" * 50)
    print("数据库连接测试 Database Connection Test")
    print("=" * 50)
    print()
    
    print(f"📊 连接串: {DATABASE_URL}")
    print()
    
    try:
        # Test connection
        async with engine.connect() as conn:
            print("✓ 数据库连接成功")
            
            # Test query - count tables
            result = await conn.execute(text("""
                SELECT COUNT(*) as table_count 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.scalar()
            print(f"✓ 数据表数量: {table_count}")
            
            # Test query - count knowledge points
            result = await conn.execute(text("SELECT COUNT(*) FROM knowledge_points"))
            kp_count = result.scalar()
            print(f"✓ 知识点数量: {kp_count}")
            
            # Test query - count users
            result = await conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            print(f"✓ 用户数量: {user_count}")
            
            # Get sample knowledge points
            result = await conn.execute(text("""
                SELECT name, difficulty, category 
                FROM knowledge_points 
                ORDER BY order_index 
                LIMIT 3
            """))
            
            print("\n📚 示例知识点:")
            for row in result:
                print(f"  - {row.name} ({row.difficulty}) - {row.category}")
            
            print("\n" + "=" * 50)
            print("✅ 数据库测试通过！")
            print("=" * 50)
            print()
            print("🚀 可以启动服务了:")
            print("  cd backend && uvicorn main:app --reload")
            print()
            
    except Exception as e:
        print(f"\n❌ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_connection())


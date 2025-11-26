"""
Check which knowledge points have article content
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import KnowledgePoint
import asyncio


async def check_article_status():
    """Check article content status for all knowledge points"""
    async with AsyncSessionLocal() as db:
        try:
            # Get all knowledge points
            result = await db.execute(
                select(KnowledgePoint).order_by(KnowledgePoint.order_index)
            )
            knowledge_points = result.scalars().all()
            
            print("\n" + "="*80)
            print("📚 KNOWLEDGE POINTS ARTICLE STATUS")
            print("="*80 + "\n")
            
            has_article = 0
            no_article = 0
            
            for kp in knowledge_points:
                article_status = "✅ HAS ARTICLE" if kp.article_content else "❌ NO ARTICLE"
                article_length = len(kp.article_content) if kp.article_content else 0
                
                if kp.article_content:
                    has_article += 1
                else:
                    no_article += 1
                
                print(f"{kp.id}. {kp.name}")
                print(f"   Category: {kp.category}")
                print(f"   Difficulty: {kp.difficulty}")
                print(f"   Status: {article_status}")
                if article_length > 0:
                    print(f"   Article Length: {article_length} characters")
                print()
            
            print("="*80)
            print(f"📊 SUMMARY")
            print(f"   Total Knowledge Points: {len(knowledge_points)}")
            print(f"   ✅ With Articles: {has_article}")
            print(f"   ❌ Without Articles: {no_article}")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"❌ Error checking article status: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(check_article_status())


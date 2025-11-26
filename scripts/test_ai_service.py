"""
Test AI service connection
"""
import sys
import os
from pathlib import Path
import asyncio

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(backend_path / '.env')

from app.services.siliconflow_ai import get_ai_service


async def test_ai_service():
    """Test basic AI service functionality"""
    print("\n" + "="*60)
    print("🤖 Testing AI Service Connection")
    print("="*60 + "\n")
    
    ai_service = get_ai_service()
    
    # Test 1: Simple message
    print("Test 1: Simple greeting...")
    try:
        result = await ai_service._make_request(
            messages=[{"role": "user", "content": "Hello, respond with just 'Hi!'"}],
            max_tokens=50,
            temperature=0.5
        )
        
        if result["success"]:
            print("✅ Success!")
            print(f"   Response: {result['content'][:100]}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    
    # Test 2: Code chat
    print("Test 2: Code explanation...")
    try:
        chat_result = await ai_service.chat_about_code(
            user_message="Explain this in one sentence",
            code="def hello(): return 'world'",
            language="python",
            problem_description="Test problem"
        )
        
        if chat_result["success"]:
            print("✅ Success!")
            print(f"   Response: {chat_result['response'][:150]}...")
        else:
            print(f"❌ Failed: {chat_result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\n" + "="*60)
    
    # Close client
    await ai_service.close()


if __name__ == "__main__":
    asyncio.run(test_ai_service())


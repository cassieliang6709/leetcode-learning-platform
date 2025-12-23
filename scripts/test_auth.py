#!/usr/bin/env python3
"""
Test authentication functionality
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api"


async def test_auth():
    """Test authentication endpoints"""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Authentication Functionality\n")
        
        # Test 1: Register new user
        print("1️⃣ Testing user registration...")
        register_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/auth/register", json=register_data)
            if response.status_code == 201:
                data = response.json()
                print(f"   ✅ Registration successful!")
                print(f"   - User: {data['user']['username']}")
                print(f"   - Email: {data['user']['email']}")
                print(f"   - Token: {data['access_token'][:20]}...")
                token = data['access_token']
            else:
                print(f"   ⚠️  Registration failed: {response.json()}")
                # Try to login instead
                print("\n   Attempting to login with existing user...")
                login_data = {
                    "username": register_data["username"],
                    "password": register_data["password"]
                }
                response = await client.post(f"{BASE_URL}/auth/login", json=login_data)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Login successful!")
                    token = data['access_token']
                else:
                    print(f"   ❌ Login failed: {response.json()}")
                    return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        print()
        
        # Test 2: Get current user info
        print("2️⃣ Testing get current user info...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"   ✅ Retrieved user info:")
                print(f"   - ID: {user['id']}")
                print(f"   - Username: {user['username']}")
                print(f"   - Email: {user['email']}")
            else:
                print(f"   ❌ Failed: {response.json()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        
        # Test 3: Login with existing user
        print("3️⃣ Testing login with existing user...")
        login_data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        try:
            response = await client.post(f"{BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Login successful!")
                print(f"   - Username: {data['user']['username']}")
                print(f"   - Token received: Yes")
            else:
                print(f"   ❌ Failed: {response.json()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        
        # Test 4: Test protected endpoint with token
        print("4️⃣ Testing protected endpoint...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{BASE_URL}/knowledge/points", headers=headers)
            if response.status_code == 200:
                print(f"   ✅ Protected endpoint accessible with token")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        
        # Test 5: Test protected endpoint without token
        print("5️⃣ Testing protected endpoint without token...")
        try:
            response = await client.get(f"{BASE_URL}/knowledge/points")
            if response.status_code == 401:
                print(f"   ✅ Correctly rejected unauthorized request")
            elif response.status_code == 200:
                print(f"   ⚠️  Endpoint is not protected (might be intentional)")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        print("✅ Authentication testing completed!")


if __name__ == "__main__":
    asyncio.run(test_auth())

















"""
Integration tests for authentication routes
"""
import pytest
from httpx import AsyncClient


class TestRegisterRoute:
    """Test user registration endpoint"""
    
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "newuser@example.com"
        assert "id" in data["user"]
    
    async def test_register_duplicate_username(self, client: AsyncClient, test_user):
        """Test registration with duplicate username"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "testuser",  # Already exists
                "email": "different@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with duplicate email"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "differentuser",
                "email": "test@example.com",  # Already exists
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    async def test_register_missing_fields(self, client: AsyncClient):
        """Test registration with missing fields"""
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "newuser"
            }
        )
        
        assert response.status_code == 422


class TestLoginRoute:
    """Test user login endpoint"""
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login"""
        response = await client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "testuser"
    
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password"""
        response = await client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with nonexistent user"""
        response = await client.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
    
    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields"""
        response = await client.post(
            "/api/auth/login",
            json={
                "username": "testuser"
            }
        )
        
        assert response.status_code == 422


class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    async def test_get_current_user_success(self, authenticated_client: AsyncClient):
        """Test getting current user info with valid token"""
        response = await authenticated_client.get("/api/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert data["username"] == "testuser"
    
    async def test_get_current_user_no_token(self, client: AsyncClient):
        """Test getting current user without token"""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token"""
        client.headers["Authorization"] = "Bearer invalid.token.here"
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401


class TestAuthenticationFlow:
    """Test complete authentication flow"""
    
    async def test_register_then_login(self, client: AsyncClient):
        """Test registering a user and then logging in"""
        # Register
        register_response = await client.post(
            "/api/auth/register",
            json={
                "username": "flowuser",
                "email": "flow@example.com",
                "password": "password123"
            }
        )
        assert register_response.status_code == 201
        register_token = register_response.json()["access_token"]
        
        # Login with same credentials
        login_response = await client.post(
            "/api/auth/login",
            json={
                "username": "flowuser",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        login_token = login_response.json()["access_token"]
        
        # Both tokens should be valid (though different)
        assert register_token != login_token
    
    async def test_full_authentication_flow(self, client: AsyncClient):
        """Test complete flow: register -> login -> get user info"""
        # Register
        register_response = await client.post(
            "/api/auth/register",
            json={
                "username": "fullflowuser",
                "email": "fullflow@example.com",
                "password": "password123"
            }
        )
        assert register_response.status_code == 201
        
        # Login
        login_response = await client.post(
            "/api/auth/login",
            json={
                "username": "fullflowuser",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Get user info with token
        client.headers["Authorization"] = f"Bearer {token}"
        me_response = await client.get("/api/auth/me")
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "fullflowuser"




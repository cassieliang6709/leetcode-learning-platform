"""
Unit tests for authentication service
"""
import pytest
from datetime import timedelta
from jose import jwt

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_hash_password_different_results(self):
        """Test that same password produces different hashes (salt)"""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self):
        """Test password verification with empty password"""
        hashed = hash_password("test_password_123")
        
        assert verify_password("", hashed) is False


class TestJWTTokens:
    """Test JWT token creation and validation"""
    
    def test_create_access_token(self):
        """Test creating access token"""
        data = {"sub": 123}
        token = create_access_token(data)
        
        assert token is not None
        assert len(token) > 0
    
    def test_create_access_token_with_expiry(self):
        """Test creating token with custom expiry"""
        data = {"sub": "123"}  # sub must be string
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        assert token is not None
        
        # Decode and verify expiry
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload
    
    def test_token_contains_user_id(self):
        """Test that token contains user ID"""
        user_id = "123"  # sub must be string
        data = {"sub": user_id}
        token = create_access_token(data)
        
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == user_id
    
    def test_token_different_users(self):
        """Test that different users get different tokens"""
        token1 = create_access_token({"sub": "1"})
        token2 = create_access_token({"sub": "2"})
        
        assert token1 != token2
    
    def test_token_decode_valid(self):
        """Test decoding valid token"""
        user_id = "123"  # sub must be string
        token = create_access_token({"sub": user_id})
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_token_decode_invalid_signature(self):
        """Test decoding token with invalid signature"""
        from jose import JWTError
        
        token = create_access_token({"sub": "123"})
        
        with pytest.raises(JWTError):
            jwt.decode(token, "wrong-secret", algorithms=[ALGORITHM])
    
    def test_token_additional_data(self):
        """Test token with additional data"""
        data = {"sub": "123", "email": "test@example.com", "role": "admin"}  # sub must be string
        token = create_access_token(data)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"


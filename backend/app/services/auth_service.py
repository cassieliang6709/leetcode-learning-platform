"""
Authentication service for user authentication and authorization.

This module provides password hashing, JWT token creation and validation,
and user authentication functions for the LeetCode Learning Platform.

It uses bcrypt for password hashing and JWT (JSON Web Tokens) for
session management. All authentication functions include proper error
handling and security best practices.

Author: Yue Liang
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.database import get_db

# Configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your-secret-key-change-this-in-production-use-env-variable"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", auto_error=False
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash.

    Returns:
        Hashed password string.

    Raises:
        ValueError: If password is empty or invalid.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    
    # bcrypt has a 72-byte limit, truncate if necessary
    # Encode to bytes to check length accurately
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify.
        hashed_password: Previously hashed password to compare against.

    Returns:
        True if passwords match, False otherwise.

    Raises:
        ValueError: If either password is empty or invalid.
    """
    if not plain_password or not isinstance(plain_password, str):
        return False
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token for user authentication.

    The token includes expiration time and user identification data.
    Backend uses this token to identify the current user.

    Args:
        data: Dictionary containing user data (typically includes "sub" key
            with user ID).
        expires_delta: Optional custom expiration time. If not provided,
            uses default ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT token string.

    Raises:
        ValueError: If data is empty or invalid.
        Exception: If JWT encoding fails.
    """
    if not data or not isinstance(data, dict):
        raise ValueError("Token data must be a non-empty dictionary")

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise Exception(f"Failed to create access token: {e}") from e

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.

    This function allows optional authentication - returns None if no token
    is provided, allowing routes to work for both authenticated and
    unauthenticated users.

    Args:
        token: Optional JWT token from request headers.
        db: Database session dependency.

    Returns:
        User object if token is valid, None if no token provided.

    Raises:
        HTTPException: If token is invalid, expired, or user not found.
    """
    if not token:
        return None
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)  # Ensure user_id is an integer
    except (JWTError, ValueError, TypeError) as e:
        raise credentials_exception from e
    
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching user: {e}"
        ) from e
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_required(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Require authenticated user for protected routes.

    This function ensures that only authenticated users can access
    the route. Raises 401 error if user is not authenticated.

    Args:
        current_user: Optional user from get_current_user dependency.

    Returns:
        User object if authenticated.

    Raises:
        HTTPException: If user is not authenticated (401 Unauthorized).
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


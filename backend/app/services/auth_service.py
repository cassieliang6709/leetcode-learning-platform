"""
Authentication service for user authentication and authorization.

Uses bcrypt for password hashing and JWT for session management.
Tokens are delivered as httpOnly cookies (with Authorization header fallback).

Author: Yue Liang
"""

import hashlib
import logging
import os
import secrets
import warnings
import bcrypt as _bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from jose.exceptions import JWTEncodeError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models import User, RefreshToken
from app.database import get_db

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your-secret-key-change-this-in-production-use-env-variable"
)
_PLACEHOLDER_KEY = "your-secret-key-change-this-in-production-use-env-variable"
if SECRET_KEY == _PLACEHOLDER_KEY:
    warnings.warn(
        "SECRET_KEY is the insecure placeholder default. "
        "Set a strong SECRET_KEY environment variable before deploying to production.",
        RuntimeWarning,
        stacklevel=1,
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15           # short-lived; refresh token extends sessions
REFRESH_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", auto_error=False
)


def _to_bcrypt_bytes(password: str) -> bytes:
    """Encode password to UTF-8 bytes, truncated to bcrypt's 72-byte limit."""
    b = password.encode("utf-8")
    return b[:72] if len(b) > 72 else b


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    return _bcrypt.hashpw(_to_bcrypt_bytes(password), _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against its bcrypt hash."""
    if not plain_password or not isinstance(plain_password, str):
        return False
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    try:
        return _bcrypt.checkpw(
            _to_bcrypt_bytes(plain_password),
            hashed_password.encode("utf-8")
        )
    except (_bcrypt.exceptions.InvalidHashError, ValueError):
        return False


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a signed JWT access token."""
    if not data or not isinstance(data, dict):
        raise ValueError("Token data must be a non-empty dictionary")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTEncodeError as e:
        raise ValueError(f"Failed to create access token: {e}") from e


async def create_refresh_token(user_id: int, db: AsyncSession) -> str:
    """Generate a cryptographically random refresh token, store its hash, and return the raw value."""
    raw = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db.add(RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
    await db.commit()
    return raw


async def rotate_refresh_token(raw_token: str, db: AsyncSession) -> tuple[str, int]:
    """
    Validate a refresh token, revoke it, and issue a fresh one.

    Returns (new_raw_token, user_id).
    Raises HTTPException 401 if the token is missing, expired, or revoked.
    """
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    try:
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        stored = result.scalar_one_or_none()
    except SQLAlchemyError:
        logger.exception("DB error looking up refresh token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    now = datetime.now(timezone.utc)
    if not stored or stored.revoked or stored.expires_at.replace(tzinfo=timezone.utc) < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    stored.revoked = True
    await db.flush()
    new_raw = await create_refresh_token(stored.user_id, db)
    return new_raw, stored.user_id


async def revoke_all_refresh_tokens(user_id: int, db: AsyncSession) -> None:
    """Revoke all active refresh tokens for a user (called on logout)."""
    try:
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
        )
        for token in result.scalars().all():
            token.revoked = True
        await db.commit()
    except SQLAlchemyError:
        logger.exception("DB error revoking refresh tokens for user %s", user_id)


def _resolve_token(request: Request, header_token: Optional[str]) -> Optional[str]:
    """Return token from Authorization header, or fall back to httpOnly cookie."""
    if header_token:
        return header_token
    return request.cookies.get("access_token")


async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get current authenticated user from JWT token (header or httpOnly cookie).

    Returns None for unauthenticated requests so that routes can handle
    both authenticated and guest users.
    """
    resolved_token = _resolve_token(request, token)
    if not resolved_token:
        return None

    try:
        payload = jwt.decode(resolved_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        user_id = int(user_id)
    except (JWTError, ValueError, TypeError):
        return None

    try:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError:
        logger.exception("DB error resolving user %s from token", user_id)
        return None


async def get_current_user_required(
    current_user: Optional[User] = Depends(get_current_user),
) -> User:
    """Require an authenticated user; raise 401 if not authenticated."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

"""
Authentication routes: register, login, logout, and current user.

Tokens are issued as httpOnly cookies (SameSite=Lax) and also returned
in the JSON body for clients that prefer header-based auth.

Author: Yue Liang
"""

import logging
import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

# True in any environment that isn't local development
_SECURE_COOKIES = os.getenv("ENVIRONMENT", "development").lower() not in ("development", "local", "dev")

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    rotate_refresh_token,
    revoke_all_refresh_tokens,
    get_current_user_required,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

_ACCESS_COOKIE_MAX_AGE  = ACCESS_TOKEN_EXPIRE_MINUTES * 60
_REFRESH_COOKIE_MAX_AGE = REFRESH_TOKEN_EXPIRE_DAYS * 86_400


def _auth_response(
    access_token: str,
    refresh_token: str,
    user: User,
    status_code: int = 200,
) -> JSONResponse:
    """Return JSON with access token + set both tokens as httpOnly cookies."""
    user_data = UserResponse.model_validate(user)
    resp = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data.model_dump(mode="json"),
        },
        status_code=status_code,
    )
    resp.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=_SECURE_COOKIES,
        max_age=_ACCESS_COOKIE_MAX_AGE,
        path="/",
    )
    resp.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=_SECURE_COOKIES,
        max_age=_REFRESH_COOKIE_MAX_AGE,
        path="/api/auth",  # only sent to auth endpoints
    )
    return resp


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Register a new user account.

    Returns a JWT token (in body and httpOnly cookie) on success.
    Raises 400 if username or email is already taken.
    Rate limited to 5 requests per minute per IP.
    """
    try:
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already in use",
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        ) from e

    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = await create_refresh_token(new_user.id, db)
    return _auth_response(access_token, refresh_token, new_user, status_code=201)


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Authenticate user and issue a JWT token.

    Returns the token in both the JSON body and an httpOnly cookie.
    Rate limited to 10 requests per minute per IP.
    """
    try:
        result = await db.execute(
            select(User).where(User.username == credentials.username)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user.last_login_at = datetime.now(timezone.utc)
        await db.commit()

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = await create_refresh_token(user.id, db)
        return _auth_response(access_token, refresh_token, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        ) from e


@router.post("/refresh")
async def refresh(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Issue a new access token using the refresh token cookie.

    Rotates the refresh token on every call (single-use).
    Returns 401 if the refresh token is missing, expired, or revoked.
    """
    raw = request.cookies.get("refresh_token")
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    new_refresh_raw, user_id = await rotate_refresh_token(raw, db)
    access_token = create_access_token(data={"sub": str(user_id)})

    resp = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    resp.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=_SECURE_COOKIES,
        max_age=_ACCESS_COOKIE_MAX_AGE,
        path="/",
    )
    resp.set_cookie(
        key="refresh_token",
        value=new_refresh_raw,
        httponly=True,
        samesite="lax",
        secure=_SECURE_COOKIES,
        max_age=_REFRESH_COOKIE_MAX_AGE,
        path="/api/auth",
    )
    return resp


@router.post("/logout")
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """Revoke refresh token and clear both auth cookies."""
    raw = request.cookies.get("refresh_token")
    if raw:
        token_hash = __import__("hashlib").sha256(raw.encode()).hexdigest()
        from sqlalchemy import select as _select
        from app.models import RefreshToken
        try:
            result = await db.execute(
                _select(RefreshToken).where(RefreshToken.token_hash == token_hash)
            )
            stored = result.scalar_one_or_none()
            if stored:
                stored.revoked = True
                await db.commit()
        except SQLAlchemyError:
            logger.exception("DB error revoking refresh token on logout")

    resp = JSONResponse(content={"message": "Logged out"})
    resp.delete_cookie(key="access_token", path="/")
    resp.delete_cookie(key="refresh_token", path="/api/auth")
    return resp


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_required),
) -> UserResponse:
    """Return the authenticated user's profile."""
    return UserResponse.model_validate(current_user)

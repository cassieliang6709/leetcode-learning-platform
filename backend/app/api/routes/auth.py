"""
Authentication routes: register, login, logout, and current user.

Tokens are issued as httpOnly cookies (SameSite=Lax) and also returned
in the JSON body for clients that prefer header-based auth.

Author: Yue Liang
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_required,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

_COOKIE_MAX_AGE = ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds


def _auth_response(access_token: str, user: User, status_code: int = 200) -> JSONResponse:
    """Return JSON with token + set the same token as an httpOnly cookie."""
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
        secure=False,  # Set True in production (HTTPS required)
        max_age=_COOKIE_MAX_AGE,
        path="/",
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
    return _auth_response(access_token, new_user, status_code=201)


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

        access_token = create_access_token(data={"sub": str(user.id)})
        return _auth_response(access_token, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        ) from e


@router.post("/logout")
async def logout() -> JSONResponse:
    """Clear the authentication cookie."""
    resp = JSONResponse(content={"message": "Logged out"})
    resp.delete_cookie(key="access_token", path="/")
    return resp


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_required),
) -> UserResponse:
    """Return the authenticated user's profile."""
    return UserResponse.model_validate(current_user)

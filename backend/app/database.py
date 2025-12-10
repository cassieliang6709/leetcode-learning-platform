"""
Database configuration and session management.

This module provides database connection setup, session management,
and initialization functions for the LeetCode Learning Platform.

It uses SQLAlchemy with async support for PostgreSQL database operations.
All database sessions are properly managed with error handling and
automatic rollback on exceptions.

Author: Yue Liang
"""

import os
import getpass
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Get current user for default database URL
CURRENT_USER = getpass.getuser()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{CURRENT_USER}@localhost:5432/leetcode_learning"
)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for FastAPI routes.

    Provides an async database session that automatically commits
    on success and rolls back on exceptions. The session is properly
    closed in the finally block.

    Yields:
        AsyncSession: Database session for use in route handlers.

    Raises:
        Exception: Any database exception that occurs during
            the session lifecycle will be raised after rollback.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.

    Creates all database tables defined in the models using
    SQLAlchemy metadata. This function should be called once
    during application startup.

    Raises:
        Exception: If table creation fails.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        raise Exception(f"Failed to initialize database: {e}") from e



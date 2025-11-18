import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Get current user for default database URL
import getpass
CURRENT_USER = getpass.getuser()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{CURRENT_USER}@localhost:5432/leetcode_learning"
)

engine = create_async_engine(
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


async def get_db():
    """Database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



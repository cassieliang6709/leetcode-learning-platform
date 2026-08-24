"""
FastAPI application entry point for AlgoMentor.

This module initializes the FastAPI application, configures CORS,
registers all API routes, and handles application lifecycle events
including database initialization.

Author: Yue Liang
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load environment variables
load_dotenv()

from app.api.routes import (
    knowledge, quiz, code_check, code_execution, ai_assistant, auth, rag
)
from app.database import init_db

# Rate limiter: keyed by client IP, uses in-memory storage by default
# Set REDIS_URL env var to use Redis for distributed rate limiting
import os
redis_url = os.getenv("REDIS_URL")
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url or "memory://"
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events. Initializes database
    tables on application startup.

    Args:
        app: FastAPI application instance.

    Yields:
        None: Application is ready to serve requests.
    """
    try:
        await init_db()
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
    yield


app = FastAPI(
    title="AlgoMentor",
    description="AI-powered algorithm learning platform",
    version="1.0.0",
    lifespan=lifespan
)

# Attach rate limiter and its 429 error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware configuration
_extra_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        *_extra_origins,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(
    knowledge.router, prefix="/api/knowledge", tags=["knowledge"]
)
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(code_check.router, prefix="/api/code", tags=["code"])
app.include_router(
    code_execution.router, prefix="/api/execution", tags=["execution"]
)
app.include_router(
    ai_assistant.router, prefix="/api/ai", tags=["ai-assistant"]
)
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])


@app.get("/")
async def root() -> dict:
    """
    Root endpoint.

    Returns basic API information and status.

    Returns:
        Dictionary with API name and status.
    """
    return {"message": "AlgoMentor API", "status": "running"}


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Used for monitoring and load balancer health checks.

    Returns:
        Dictionary with health status.
    """
    return {"status": "healthy"}


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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

from app.api.routes import (
    knowledge, quiz, code_check, code_execution, ai_assistant, auth
)
from app.database import init_db


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

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",  # Allow all Vercel subdomains
        "*"  # Temporary allow all, change to specific domain after deployment
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


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.api.routes import knowledge, quiz, code_check, code_execution, ai_assistant, auth
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    yield


app = FastAPI(
    title="LeetCode Learning Platform",
    description="AI-powered algorithm learning platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
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

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(code_check.router, prefix="/api/code", tags=["code"])
app.include_router(code_execution.router, prefix="/api/execution", tags=["execution"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["ai-assistant"])


@app.get("/")
async def root():
    return {"message": "LeetCode Learning Platform API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


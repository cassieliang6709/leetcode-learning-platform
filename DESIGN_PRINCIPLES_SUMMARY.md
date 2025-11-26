# Design Principles Quick Reference

## Overview
This is a concise summary of the design principles and best practices demonstrated in the LeetCode Learning Platform. For detailed explanations and code examples, see [DESIGN_PRINCIPLES_AND_PRACTICES.md](./DESIGN_PRINCIPLES_AND_PRACTICES.md).

---

## Core Architecture Patterns

### 1. **Layered Architecture** ✅
```
Routes (HTTP) → Services (Logic) → Database (Data)
         ↓
    Schemas (Validation)
         ↓
     Models (Entities)
```

### 2. **Key Design Patterns**
- **Repository Pattern**: Data access abstraction via SQLAlchemy ORM
- **Strategy Pattern**: Multiple code analysis strategies (AI + fallback)
- **Dependency Injection**: Database sessions, contexts
- **Factory Pattern**: Consistent model instantiation
- **Context Pattern**: React state management

### 3. **SOLID Principles**
- ✅ **Single Responsibility**: Each module has one job
- ✅ **Open/Closed**: Extensible without modification (JSON fields, new routes)
- ✅ **Liskov Substitution**: Pydantic models can be substituted
- ✅ **Interface Segregation**: Focused API endpoints
- ✅ **Dependency Inversion**: Depends on abstractions (FastAPI Dependencies)

---

## Code Quality Highlights

### Type Safety
```python
# Pydantic validation
class QuizAnswerSubmit(BaseModel):
    question_id: int
    selected_option: int

# Type hints everywhere
async def analyze_code(code: str, language: str) -> Dict[str, Any]:
```

### Error Handling
```python
try:
    # Primary path
    return await ai_analysis()
except Exception:
    # Graceful degradation
    return await simple_analysis()
```

### Resource Management
```python
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()  # Automatic
        finally:
            await session.close()     # Guaranteed
```

---

## Modular File Organization

### Backend (Each < 500 lines)
```
app/
├── api/routes/         # Feature-based routes
│   ├── quiz.py        # Quiz endpoints
│   ├── code_check.py  # Code review endpoints
│   └── ai_assistant.py # AI endpoints
├── services/          # Business logic layer
│   ├── ai_service.py
│   └── code_executor.py
├── models.py          # Database entities (155 lines)
├── schemas.py         # API contracts (129 lines)
└── database.py        # DB setup (49 lines)
```

### Frontend
```
src/
├── pages/            # Feature pages
├── contexts/         # Global state
├── services/         # API layer
└── styles/           # Shared styles
```

---

## Testability Features

### 1. Dependency Injection
```python
# Easy to mock in tests
@router.get("/{id}")
async def handler(db: AsyncSession = Depends(get_db)):
    # Can inject TestSessionLocal in tests
```

### 2. Pure Functions
```python
async def _simple_code_analysis(code: str, language: str) -> Dict:
    # No side effects
    # Deterministic output
    # Easy to test
```

### 3. Clear Interfaces
```javascript
// Frontend never touches axios directly
const data = await api.getDailyQuiz(userId)
// Can mock entire API layer
```

---

## Database Design

### Normalized Schema
```python
class User:
    quiz_attempts = relationship("QuizAttempt")
    code_submissions = relationship("CodeSubmission")

class QuizQuestion:
    attempts = relationship("QuizAttempt")
    knowledge_point = relationship("KnowledgePoint")
```

### Flexible JSON Fields
```python
test_cases = Column(JSON)      # Variable test cases
starter_code = Column(JSON)    # Multi-language support
hints = Column(JSON)           # Flexible hint structure
```

### Audit Fields
```python
created_at = Column(DateTime(timezone=True), server_default=func.now())
updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

---

## API Design

### RESTful Structure
```python
GET    /api/quiz/daily/{user_id}
POST   /api/quiz/answer/{user_id}
GET    /api/quiz/{question_id}
GET    /api/quiz/{question_id}/hint/{level}
```

### Consistent Responses
```python
@router.get("/daily/{user_id}", response_model=DailyProgressResponse)
async def get_daily_quiz(...) -> DailyProgressResponse:
    return DailyProgressResponse(...)  # Type-safe
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
)
```

---

## Scalability & Performance

### Async/Await
```python
# All I/O operations are non-blocking
async def get_quiz_detail(question_id: int):
    result = await db.execute(...)
    return result
```

### Connection Pooling
```python
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Configurable
)
```

### Efficient Queries
```python
# Avoid N+1 queries
result = await db.execute(
    select(QuizQuestion)
    .options(selectinload(QuizQuestion.knowledge_point))
)
```

---

## Security Best Practices

### Environment Variables
```python
api_key = os.getenv("SILICONFLOW_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Input Validation
```python
# Pydantic automatically validates
class CodeSubmissionCreate(BaseModel):
    question_id: int          # Must be int
    code: str                 # Required
    language: str = "python"  # Default value
```

### SQL Injection Prevention
```python
# Using ORM, not raw SQL
result = await db.execute(
    select(QuizQuestion).where(QuizQuestion.id == question_id)
)
```

---

## Documentation Standards

### Docstrings
```python
async def get_daily_quiz(user_id: int):
    """Get daily knowledge challenge questions (3 random excluding answered)"""
```

### Self-Documenting Code
```python
# Clear variable names
answered_today_ids = [row[0] for row in result.fetchall()]
correct_count = sum(1 for a in attempts if a.is_correct)

# Clear function names
async def submit_answer(...)
async def get_daily_progress(...)
```

### Type Hints
```python
async def generate_plan(data: Dict, score: int) -> Dict[str, Any]:
```

---

## DevOps Ready

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Lifecycle Management
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Startup
    yield
    # Cleanup here

app = FastAPI(lifespan=lifespan)
```

### Deployment Scripts
```
scripts/
├── start_backend.sh
├── start_frontend.sh
├── start_all.sh
├── stop_all.sh
└── init_db.py
```

---

## Extensibility Examples

### Adding New Language Support
```python
# Just update JSON, no schema change
starter_code = {
    "python": "def solution(): pass",
    "javascript": "function solution() {}",
    "rust": "fn solution() {}"  # ← Add here
}
```

### Adding New Route
```python
# 1. Add to routes/new_feature.py
@router.get("/new-endpoint")
async def new_handler():
    pass

# 2. Register in main.py
app.include_router(new_feature.router, prefix="/api/new")

# No existing code modified (Open/Closed Principle)
```

### Adding New Model
```python
# 1. Add to models.py
class NewFeature(Base):
    __tablename__ = "new_features"
    # ...

# 2. Add to schemas.py
class NewFeatureResponse(BaseModel):
    # ...

# 3. Database migration handled by init_db()
```

---

## Code Metrics

| Metric | Status |
|--------|--------|
| **File Size** | ✅ All < 500 lines |
| **Function Size** | ✅ Mostly < 50 lines |
| **Cyclomatic Complexity** | ✅ Low (simple control flow) |
| **Code Duplication** | ✅ Minimal (DRY principle) |
| **Type Coverage** | ✅ High (type hints + Pydantic) |
| **Documentation** | ✅ Good (docstrings + comments) |
| **Modularity** | ✅ High (clear module boundaries) |
| **Testability** | ✅ High (DI + pure functions) |

---

## Key Takeaways

1. **Small, Focused Modules**: No files > 500 lines, each module has one responsibility
2. **Type Safety**: Pydantic validation + type hints prevent runtime errors
3. **Layered Architecture**: Clear separation between HTTP/Business/Data layers
4. **Error Resilience**: Graceful degradation, transaction management
5. **DRY Principle**: Centralized API client, shared database sessions
6. **Testable Code**: Dependency injection, pure functions, clear interfaces
7. **Production Ready**: Health checks, lifecycle management, deployment scripts
8. **Extensible Design**: Easy to add features without modifying existing code
9. **Security First**: Environment variables, input validation, ORM protection
10. **Documentation**: Docstrings, type hints, self-documenting code

---

## Further Reading

For detailed code examples and in-depth explanations of each principle:

📖 **[Full Design Principles Document](./DESIGN_PRINCIPLES_AND_PRACTICES.md)** (32KB)

For project structure and development workflow:

📖 **[Development Guidelines](./docs/DEVELOPMENT_GUIDELINES.md)** (if exists)
📖 **[README](./readme.md)**

---

**Last Updated**: 2025-11-25


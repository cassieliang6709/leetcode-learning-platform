# Testing Guide

## Overview

AlgoMentor has comprehensive test coverage including unit tests and integration tests.

## Quick Start

```bash
# From backend directory
cd backend

# Run all tests
./scripts/run_tests.sh

# Or manually
pytest
```

## Test Structure

- **Unit Tests** (`tests/unit/`): Test individual components
  - Auth service (password hashing, JWT tokens)
  - AI service (learning plan generation)
  - Database models
  - Pydantic schemas

- **Integration Tests** (`tests/integration/`): Test API endpoints
  - Authentication routes (register, login)
  - Quiz routes (daily quizzes, submissions)
  - Knowledge routes (roadmap, learning plans)
  - Code execution routes

## Test Coverage

```bash
# Run with coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html
```

## Writing Tests

### Example Unit Test

```python
import pytest
from app.services.auth_service import hash_password, verify_password

def test_password_hashing():
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
```

### Example Integration Test

```python
import pytest
from httpx import AsyncClient

async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert "access_token" in response.json()
```

## Requirements

- Python 3.8+
- PostgreSQL (test database)
- Dependencies: pytest, pytest-asyncio, pytest-cov, faker

## See Also

- [tests/README.md](tests/README.md) - Detailed testing documentation
- [pytest.ini](pytest.ini) - Pytest configuration




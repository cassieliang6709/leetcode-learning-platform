# Testing Documentation

This directory contains comprehensive unit and integration tests for the AlgoMentor backend API.

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_auth_service.py    # Auth service tests
│   ├── test_ai_service.py      # AI service tests
│   ├── test_models.py          # Database model tests
│   └── test_schemas.py         # Pydantic schema tests
└── integration/             # Integration tests
    ├── test_auth_routes.py          # Auth API endpoints
    ├── test_quiz_routes.py          # Quiz API endpoints
    ├── test_knowledge_routes.py     # Knowledge API endpoints
    └── test_code_execution_routes.py # Code execution endpoints
```

## 🚀 Running Tests

### Quick Start

```bash
# From backend directory
cd backend

# Make test script executable
chmod +x scripts/run_tests.sh

# Run all tests
./scripts/run_tests.sh
```

### Manual Test Execution

```bash
# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov faker

# Create test database (one time)
createdb leetcode_learning_test

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run specific test class
pytest tests/unit/test_auth_service.py::TestPasswordHashing

# Run specific test
pytest tests/unit/test_auth_service.py::TestPasswordHashing::test_hash_password

# Run with coverage report
pytest --cov=app --cov-report=html

# Run tests in parallel (faster)
pytest -n auto
```

## 📊 Test Coverage

After running tests with coverage, view the report:

```bash
# Open HTML coverage report
open htmlcov/index.html

# View terminal coverage summary
pytest --cov=app --cov-report=term-missing
```

## 🧪 Test Categories

### Unit Tests

Unit tests focus on individual components in isolation:

- **`test_auth_service.py`**: Password hashing, JWT token generation/validation
- **`test_ai_service.py`**: Learning plan generation, AI recommendations
- **`test_models.py`**: Database models, relationships, validation
- **`test_schemas.py`**: Pydantic schema validation

### Integration Tests

Integration tests verify API endpoints and full request/response cycles:

- **`test_auth_routes.py`**: User registration, login, authentication flow
- **`test_quiz_routes.py`**: Daily quizzes, question fetching, answer submission
- **`test_knowledge_routes.py`**: Knowledge points, learning plans, roadmap
- **`test_code_execution_routes.py`**: Code submission, execution (requires Piston API)

## 🔧 Test Configuration

### Environment Variables

Tests use a separate test database. Configure in `.env` or set directly:

```bash
export TEST_DATABASE_URL="postgresql+asyncpg://localhost:5432/leetcode_learning_test"
```

### Pytest Configuration

See `pytest.ini` for test configuration:
- Automatic async test handling
- Coverage reporting
- Test discovery patterns

## 🏗️ Test Fixtures

Common fixtures available in `conftest.py`:

- `db_session`: Fresh database session for each test
- `client`: HTTP test client
- `test_user`: Pre-created test user
- `test_user_token`: Authentication token
- `authenticated_client`: Client with auth token
- `test_knowledge_point`: Sample knowledge point
- `test_quiz_question`: Sample quiz question
- `test_daily_question`: Sample daily question

### Using Fixtures

```python
async def test_something(client: AsyncClient, test_user):
    """Test using fixtures"""
    response = await client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
```

## ✅ Best Practices

### 1. Test Naming
```python
# Good
async def test_login_with_valid_credentials(client):
    pass

# Bad
async def test1(client):
    pass
```

### 2. Test Structure (AAA Pattern)
```python
async def test_something(client):
    # Arrange - setup test data
    user_data = {"username": "test", "password": "pass"}
    
    # Act - execute the action
    response = await client.post("/api/auth/login", json=user_data)
    
    # Assert - verify results
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### 3. Test Independence
Each test should be independent and not rely on other tests:

```python
# Good - creates own data
async def test_delete_user(client, db_session):
    user = User(username="temp")
    db_session.add(user)
    await db_session.commit()
    # ... test logic
```

### 4. Use Appropriate Assertions
```python
# Good - specific assertions
assert response.status_code == 200
assert "email" in data
assert data["is_active"] is True

# Bad - generic assertions
assert response
assert data
```

## 🐛 Debugging Tests

### Run with print statements
```bash
pytest -v -s  # -s shows print output
```

### Run with debugger
```bash
pytest --pdb  # Drop into debugger on failure
```

### Increase verbosity
```bash
pytest -vv  # Extra verbose
```

### Show test duration
```bash
pytest --durations=10  # Show 10 slowest tests
```

## 📈 Test Metrics

Current test coverage targets:
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Cover all API endpoints
- **Overall**: 70%+ code coverage

## 🔄 Continuous Integration

Tests run automatically on:
- Pre-commit hooks (optional)
- Pull requests
- Main branch pushes

## ⚠️ Known Limitations

1. **Code Execution Tests**: Some tests require Piston API to be running. These tests gracefully handle API unavailability.

2. **External Dependencies**: AI service tests use mock implementations. For full AI testing, configure actual AI API keys.

3. **Database**: Tests use a separate test database that is recreated for each test run.

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)

## 🆘 Troubleshooting

### Test database connection errors
```bash
# Ensure PostgreSQL is running
pg_ctl status

# Recreate test database
dropdb leetcode_learning_test
createdb leetcode_learning_test
```

### Import errors
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow tests
```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto
```

## 📝 Adding New Tests

When adding new features:

1. **Write tests first** (TDD approach)
2. Add unit tests for new services/utilities
3. Add integration tests for new API endpoints
4. Update this README if adding new test categories
5. Ensure tests pass before committing:
   ```bash
   ./scripts/run_tests.sh
   ```




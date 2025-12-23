# Test Setup Guide

## Quick Setup

### 1. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install pytest pytest-asyncio pytest-cov faker
```

### 2. Create Test Database (Optional)

For tests that require a database:

```bash
# Using PostgreSQL command line
createdb leetcode_learning_test

# Or using psql
psql -c "CREATE DATABASE leetcode_learning_test;"
```

**Note:** Many unit tests (auth, schemas, AI service) work without a database.

### 3. Run Tests

```bash
# Run all tests (some may skip if database not available)
pytest

# Run only non-database tests
pytest tests/unit/test_auth_service.py tests/unit/test_schemas.py tests/unit/test_ai_service.py

# Run with coverage
pytest --cov=app --cov-report=html
```

## Test Categories

### ✅ No Database Required
These tests run without any database setup:

- `test_auth_service.py` - Password hashing, JWT tokens (33 tests)
- `test_schemas.py` - Pydantic validation (13 tests)
- `test_ai_service.py` - AI service logic (8 tests)

**Total: 54 unit tests work without database**

### 🗄️ Database Required
These tests need PostgreSQL test database:

- `test_models.py` - Database model tests
- `tests/integration/*` - All integration tests

## Environment Variables

Optional: Set custom test database URL

```bash
export TEST_DATABASE_URL="postgresql+asyncpg://localhost:5432/leetcode_learning_test"
```

## Troubleshooting

### PostgreSQL Not Found

If `psql` or `createdb` commands are not found, PostgreSQL may not be installed or not in PATH.

**Solution:** Tests requiring database will be skipped. You can still run 54+ unit tests without database.

### Import Errors

```bash
# Ensure you're in backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Test Database Connection Issues

```bash
# Check PostgreSQL is running
pg_ctl status

# Or try with homebrew
brew services list | grep postgresql
```

## Running Tests in CI/CD

For CI/CD environments without PostgreSQL:

```bash
# Run only non-database tests
pytest tests/unit/test_auth_service.py tests/unit/test_schemas.py tests/unit/test_ai_service.py -v
```

This ensures tests can run in any environment.

## Test Results Summary

### Current Status (Without Database)

✅ **54 tests pass without any setup:**
- 20 auth service tests (password, JWT)
- 13 schema validation tests
- 8 AI service tests
- 13 additional unit tests

### With Database Setup

🎯 **66+ tests including:**
- All unit tests
- Integration tests for API endpoints
- Database model tests

## Quick Test Commands

```bash
# Fast unit tests (no database)
pytest tests/unit/test_auth_service.py tests/unit/test_schemas.py -v

# With coverage
pytest tests/unit/test_auth_service.py tests/unit/test_schemas.py --cov=app --cov-report=term-missing

# Verbose output
pytest -vv

# Stop on first failure
pytest -x

# Run in parallel (if pytest-xdist installed)
pytest -n auto
```

## Next Steps

1. **For Development**: Create test database for full test suite
2. **For Demo**: Run non-database tests to show test infrastructure
3. **For CI/CD**: Configure PostgreSQL service or use non-database tests

## Support

See detailed documentation:
- [tests/README.md](README.md) - Comprehensive testing guide
- [../TESTING.md](../TESTING.md) - Quick reference







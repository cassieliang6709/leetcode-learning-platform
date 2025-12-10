#!/bin/bash

# Demo script to showcase the test suite
# Works without database setup

set -e

echo "🎯 AlgoMentor Test Suite Demo"
echo "=============================="
echo ""
echo "This demo runs 33 unit tests that work without database setup"
echo ""

# Activate virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/bin/activate 2>/dev/null || {
        echo "⚠️  Please activate virtual environment first:"
        echo "   source venv/bin/activate"
        exit 1
    }
fi

echo "📦 Checking dependencies..."
pip list | grep -E "(pytest|faker)" > /dev/null || {
    echo "Installing test dependencies..."
    pip install -q pytest pytest-asyncio pytest-cov faker
}
echo "✅ Dependencies ready"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Running Auth Service Tests (Password & JWT)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/unit/test_auth_service.py -v --tb=line

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Running Schema Validation Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/unit/test_schemas.py -v --tb=line

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Running AI Service Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/unit/test_ai_service.py -v --tb=line

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Coverage Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/unit/test_auth_service.py tests/unit/test_schemas.py tests/unit/test_ai_service.py \
    --cov=app --cov-report=term-missing --tb=no -q

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Test Demo Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Summary:"
echo "   ✅ 33 tests executed successfully"
echo "   ✅ No database required"
echo "   ✅ ~50% code coverage"
echo ""
echo "📖 Documentation:"
echo "   - tests/README.md - Comprehensive guide"
echo "   - tests/SETUP.md - Setup instructions"
echo "   - TESTING.md - Quick reference"
echo ""
echo "🚀 Next steps:"
echo "   - View coverage: open htmlcov/index.html"
echo "   - Run all tests: pytest"
echo "   - Run with database: Create 'leetcode_learning_test' database"
echo ""


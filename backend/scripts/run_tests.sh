#!/bin/bash

# Test runner script for AlgoMentor backend

set -e  # Exit on error

echo "🧪 AlgoMentor Test Suite"
echo "========================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "Activating virtual environment..."
    source venv/bin/activate || {
        echo "❌ Failed to activate virtual environment"
        echo "Please create it first: python3 -m venv venv"
        exit 1
    }
fi

# Check if test database exists
echo "📊 Checking test database..."
TEST_DB="leetcode_learning_test"
if psql -lqt | cut -d \| -f 1 | grep -qw "$TEST_DB"; then
    echo "✅ Test database exists"
else
    echo "⚠️  Test database not found. Creating..."
    createdb "$TEST_DB" || {
        echo "❌ Failed to create test database"
        echo "You may need to create it manually: createdb leetcode_learning_test"
        exit 1
    }
    echo "✅ Test database created"
fi

echo ""
echo "🔧 Installing/updating test dependencies..."
pip install -q pytest pytest-asyncio pytest-cov faker httpx

echo ""
echo "🧹 Cleaning previous test artifacts..."
rm -rf htmlcov .coverage .pytest_cache

echo ""
echo "🚀 Running tests..."
echo ""

# Run tests with coverage
pytest "$@"

# Check if tests passed
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "📊 Coverage report generated in: htmlcov/index.html"
    echo "   Open with: open htmlcov/index.html"
else
    echo "❌ Some tests failed (exit code: $TEST_EXIT_CODE)"
    exit $TEST_EXIT_CODE
fi







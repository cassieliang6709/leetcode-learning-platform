#!/bin/bash

# Start Demo Script for LeetCode Learning Platform

echo "======================================"
echo "LeetCode Learning Platform - Demo"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL found${NC}"
else
    echo -e "${RED}✗ PostgreSQL not found${NC}"
    echo "Please install PostgreSQL first"
    exit 1
fi

# Check if database exists
if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw leetcode_learning; then
    echo -e "${GREEN}✓ Database 'leetcode_learning' exists${NC}"
else
    echo -e "${YELLOW}! Database not found, creating...${NC}"
    cd "$(dirname "$0")"
    ./create_db.sh
fi

echo ""
echo "======================================"
echo "Starting Backend..."
echo "======================================"

# Start backend in background
cd "$(dirname "$0")/../backend"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and start backend
source venv/bin/activate
pip install -q -r requirements.txt

echo -e "${GREEN}Starting FastAPI server on http://localhost:8000${NC}"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo ""
echo "======================================"
echo "Starting Frontend..."
echo "======================================"

# Start frontend
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi

echo -e "${GREEN}Starting Vite dev server on http://localhost:5173${NC}"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo -e "${GREEN}✓ Demo is running!${NC}"
echo "======================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓ Services stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait



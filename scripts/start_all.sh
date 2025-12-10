#!/bin/bash
# Start both frontend and backend services

set -e

echo "🚀 Starting LeetCode Learning Platform..."

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check PostgreSQL
echo -e "${BLUE}📊 Checking PostgreSQL service...${NC}"
if ! pg_isready -q; then
    echo -e "${RED}❌ PostgreSQL is not running${NC}"
    echo "Start PostgreSQL: brew services start postgresql@14"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL is running${NC}"

# Check if database exists
DB_EXISTS=$(psql -lqt | cut -d \| -f 1 | grep -w leetcode_learning | wc -l)
if [ "$DB_EXISTS" -eq 0 ]; then
    echo -e "${BLUE}📊 Creating database...${NC}"
    psql -d postgres -c "CREATE DATABASE leetcode_learning;"
    echo -e "${GREEN}✅ Database created successfully${NC}"
fi

# Start backend
echo -e "${BLUE}🔧 Starting backend service...${NC}"
cd "$PROJECT_ROOT/backend"

# Check virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3.12 -m venv venv || python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Start backend (background)
uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started successfully (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
echo -e "${BLUE}⏳ Waiting for backend to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ Backend is ready${NC}"
        break
    fi
    sleep 1
done

# Start frontend
echo -e "${BLUE}🎨 Starting frontend service...${NC}"
cd "$PROJECT_ROOT/frontend"

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    npm install
fi

# Start frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started successfully (PID: $FRONTEND_PID)${NC}"

# Save PIDs
echo "$BACKEND_PID" > /tmp/leetcode_backend.pid
echo "$FRONTEND_PID" > /tmp/leetcode_frontend.pid

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Startup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "📱 Frontend: ${BLUE}http://localhost:5173${NC}"
echo -e "🔧 Backend: ${BLUE}http://localhost:8000${NC}"
echo -e "📚 API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "Stop services: ${BLUE}./scripts/stop_all.sh${NC}"
echo ""

# Wait for user interrupt
wait


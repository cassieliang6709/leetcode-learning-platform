#!/bin/bash
# Stop all services

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🛑 Stopping AlgoMentor..."

# Stop backend
if [ -f /tmp/leetcode_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/leetcode_backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✅ Backend stopped${NC}"
    fi
    rm /tmp/leetcode_backend.pid
fi

# Stop frontend
if [ -f /tmp/leetcode_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/leetcode_frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
    rm /tmp/leetcode_frontend.pid
fi

# Fallback: kill processes by port
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo -e "${GREEN}✅ All services stopped${NC}"


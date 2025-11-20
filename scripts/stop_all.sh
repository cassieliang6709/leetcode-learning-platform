#!/bin/bash
# 停止所有服务

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🛑 停止 LeetCode Learning Platform..."

# 停止后端
if [ -f /tmp/leetcode_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/leetcode_backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✅ 后端已停止${NC}"
    fi
    rm /tmp/leetcode_backend.pid
fi

# 停止前端
if [ -f /tmp/leetcode_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/leetcode_frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✅ 前端已停止${NC}"
    fi
    rm /tmp/leetcode_frontend.pid
fi

# 备用方案：通过端口杀死进程
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo -e "${GREEN}✅ 所有服务已停止${NC}"


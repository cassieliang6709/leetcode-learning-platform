#!/bin/bash
# 一键启动前后端服务

set -e

echo "🚀 启动 LeetCode Learning Platform..."

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 PostgreSQL
echo -e "${BLUE}📊 检查 PostgreSQL 服务...${NC}"
if ! pg_isready -q; then
    echo -e "${RED}❌ PostgreSQL 未运行${NC}"
    echo "启动 PostgreSQL: brew services start postgresql@14"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL 运行中${NC}"

# 检查数据库是否存在
DB_EXISTS=$(psql -lqt | cut -d \| -f 1 | grep -w leetcode_learning | wc -l)
if [ "$DB_EXISTS" -eq 0 ]; then
    echo -e "${BLUE}📊 创建数据库...${NC}"
    psql -d postgres -c "CREATE DATABASE leetcode_learning;"
    echo -e "${GREEN}✅ 数据库创建成功${NC}"
fi

# 启动后端
echo -e "${BLUE}🔧 启动后端服务...${NC}"
cd "$PROJECT_ROOT/backend"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 创建虚拟环境...${NC}"
    python3.12 -m venv venv || python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# 启动后端（后台运行）
uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ 后端启动成功 (PID: $BACKEND_PID)${NC}"

# 等待后端启动
echo -e "${BLUE}⏳ 等待后端就绪...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ 后端就绪${NC}"
        break
    fi
    sleep 1
done

# 启动前端
echo -e "${BLUE}🎨 启动前端服务...${NC}"
cd "$PROJECT_ROOT/frontend"

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 安装前端依赖...${NC}"
    npm install
fi

# 启动前端
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ 前端启动成功 (PID: $FRONTEND_PID)${NC}"

# 保存 PID
echo "$BACKEND_PID" > /tmp/leetcode_backend.pid
echo "$FRONTEND_PID" > /tmp/leetcode_frontend.pid

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 启动完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "📱 前端地址: ${BLUE}http://localhost:5173${NC}"
echo -e "🔧 后端地址: ${BLUE}http://localhost:8000${NC}"
echo -e "📚 API 文档: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "停止服务: ${BLUE}./scripts/stop_all.sh${NC}"
echo ""

# 等待用户中断
wait


#!/bin/bash
# 检查前后端连接状态

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/backend/.env"
DEFAULT_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/algomentor"

if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

DATABASE_URL="${DATABASE_URL:-$DEFAULT_DATABASE_URL}"
DB_NAME="${DATABASE_URL##*/}"
DB_NAME="${DB_NAME%%\?*}"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔍 检查服务连接状态..."
echo ""

# 检查后端
echo -e "${BLUE}检查后端 (http://localhost:8000)...${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ 后端运行正常${NC}"
    echo -e "   API: http://localhost:8000"
    echo -e "   文档: http://localhost:8000/docs"
else
    echo -e "${RED}❌ 后端未运行${NC}"
    echo -e "   启动: ./scripts/start_backend.sh"
fi

echo ""

# 检查前端
echo -e "${BLUE}检查前端 (http://localhost:5173)...${NC}"
if curl -s http://localhost:5173 > /dev/null; then
    echo -e "${GREEN}✅ 前端运行正常${NC}"
    echo -e "   访问: http://localhost:5173"
else
    echo -e "${RED}❌ 前端未运行${NC}"
    echo -e "   启动: ./scripts/start_frontend.sh"
fi

echo ""

# 检查数据库
echo -e "${BLUE}检查数据库 (PostgreSQL)...${NC}"
if pg_isready -q; then
    echo -e "${GREEN}✅ PostgreSQL 运行正常${NC}"
    
    # 检查数据库是否存在
    DB_EXISTS=$(psql -lqt | cut -d \| -f 1 | grep -w "$DB_NAME" | wc -l)
    if [ "$DB_EXISTS" -gt 0 ]; then
        echo -e "${GREEN}✅ 数据库 '$DB_NAME' 存在${NC}"
    else
        echo -e "${RED}❌ 数据库 '$DB_NAME' 不存在${NC}"
        echo -e "   创建: psql -d postgres -c \"CREATE DATABASE $DB_NAME;\""
    fi
else
    echo -e "${RED}❌ PostgreSQL 未运行${NC}"
    echo -e "   启动: brew services start postgresql@14"
fi

echo ""
echo "================================"
echo -e "${BLUE}快速启动命令:${NC}"
echo "  一键启动: ./scripts/start_all.sh"
echo "  停止服务: ./scripts/stop_all.sh"
echo "  初始化DB: python3 scripts/init_db.py"
echo "================================"

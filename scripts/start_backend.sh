#!/bin/bash
# 单独启动后端服务

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 启动后端服务...${NC}"

cd "$PROJECT_ROOT/backend"

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 创建虚拟环境...${NC}"
    python3.12 -m venv venv || python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 启动服务
echo -e "${GREEN}✅ 后端服务启动中...${NC}"
echo -e "${BLUE}🔧 API 地址: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API 文档: http://localhost:8000/docs${NC}"

uvicorn main:app --reload --port 8000


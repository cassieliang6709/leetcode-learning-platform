#!/bin/bash
# 单独启动前端服务

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎨 启动前端服务...${NC}"

cd "$PROJECT_ROOT/frontend"

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 安装依赖...${NC}"
    npm install
fi

# 启动服务
echo -e "${GREEN}✅ 前端服务启动中...${NC}"
echo -e "${BLUE}📱 访问地址: http://localhost:5173${NC}"

npm run dev


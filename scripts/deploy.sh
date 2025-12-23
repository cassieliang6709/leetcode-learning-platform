#!/bin/bash
# 部署辅助脚本 - 帮助准备部署所需文件

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 部署准备脚本${NC}"
echo ""

# 检查前端构建
echo -e "${BLUE}📦 检查前端构建...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  正在安装前端依赖...${NC}"
    npm install
fi

echo -e "${BLUE}🔨 构建前端...${NC}"
npm run build
echo -e "${GREEN}✅ 前端构建成功${NC}"
cd ..

# 检查后端配置
echo ""
echo -e "${BLUE}🔧 检查后端配置...${NC}"
if [ ! -f "backend/Procfile" ]; then
    echo -e "${YELLOW}⚠️  未找到 Procfile${NC}"
else
    echo -e "${GREEN}✅ Procfile 存在${NC}"
fi

# 检查 Vercel 配置
echo ""
echo -e "${BLUE}📄 检查 Vercel 配置...${NC}"
if [ ! -f "frontend/vercel.json" ]; then
    echo -e "${YELLOW}⚠️  未找到 vercel.json${NC}"
else
    echo -e "${GREEN}✅ vercel.json 存在${NC}"
fi

# 提示创建 .env.production
echo ""
echo -e "${YELLOW}📝 重要提示：${NC}"
echo -e "${YELLOW}   部署前端到 Vercel 前，需要：${NC}"
echo -e "${YELLOW}   1. 在 Vercel 项目设置中添加环境变量：${NC}"
echo -e "${YELLOW}      VITE_API_URL=https://你的后端URL/api${NC}"
echo -e "${YELLOW}   2. 或者创建 frontend/.env.production 文件（不提交到 git）${NC}"

echo ""
echo -e "${GREEN}✅ 部署准备完成！${NC}"
echo ""
echo -e "${BLUE}📚 详细部署步骤请查看：${NC}"
echo -e "   - DEPLOYMENT_GUIDE.md (完整指南)"
echo -e "   - DEPLOYMENT_CHECKLIST.md (快速清单)"

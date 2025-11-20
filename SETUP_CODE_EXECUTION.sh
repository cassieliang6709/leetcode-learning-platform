#!/bin/bash

# 代码执行功能设置脚本
# 一键安装依赖、添加题目、启动服务

echo "=================================================="
echo "🚀 代码执行功能 - 一键设置"
echo "=================================================="
echo ""

cd /Users/liangyue/Documents/school/cs5001_project

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: 停止旧服务器
echo "${BLUE}Step 1/4: 检查并停止旧服务器...${NC}"
OLD_PID=$(lsof -ti:8000)
if [ ! -z "$OLD_PID" ]; then
    echo "${YELLOW}发现运行中的服务器 (PID: $OLD_PID)，正在停止...${NC}"
    kill $OLD_PID 2>/dev/null
    sleep 1
    echo "${GREEN}✓ 旧服务器已停止${NC}"
else
    echo "${GREEN}✓ 端口 8000 可用${NC}"
fi
echo ""

# Step 2: 激活虚拟环境并安装依赖
echo "${BLUE}Step 2/4: 安装后端依赖...${NC}"
cd backend

# 检查虚拟环境
if [ ! -d "../.venv" ]; then
    echo "${YELLOW}创建虚拟环境...${NC}"
    cd ..
    python3 -m venv .venv
    cd backend
fi

# 激活虚拟环境并安装
source ../.venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "${GREEN}✓ 依赖安装成功${NC}"
else
    echo "${RED}✗ 依赖安装失败，请手动运行: cd backend && pip install -r requirements.txt${NC}"
    exit 1
fi
echo ""

# Step 3: 添加示例题目
echo "${BLUE}Step 3/4: 添加示例题目...${NC}"
cd ..
python3 scripts/add_sample_questions.py

if [ $? -eq 0 ]; then
    echo "${GREEN}✓ 题目添加成功${NC}"
else
    echo "${YELLOW}⚠ 题目可能已存在或数据库未初始化${NC}"
    echo "${YELLOW}如果是首次运行，请先执行: python3 scripts/init_db_with_roadmap.py${NC}"
fi
echo ""

# Step 4: 提示启动命令
echo "${BLUE}Step 4/4: 准备启动服务器...${NC}"
echo ""
echo "=================================================="
echo "${GREEN}✓ 设置完成！${NC}"
echo "=================================================="
echo ""
echo "${BLUE}现在可以启动服务器：${NC}"
echo ""
echo "  ${YELLOW}cd backend && source ../.venv/bin/activate && uvicorn main:app --reload${NC}"
echo ""
echo "或者运行："
echo ""
echo "  ${YELLOW}cd backend${NC}"
echo "  ${YELLOW}uvicorn main:app --reload${NC}"
echo ""
echo "${BLUE}然后访问：${NC}"
echo "  • API 文档: ${YELLOW}http://localhost:8000/docs${NC}"
echo "  • 测试端点: ${YELLOW}POST /api/execute/run${NC}"
echo ""
echo "=================================================="



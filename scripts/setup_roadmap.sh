#!/bin/bash

# Roadmap Setup Script
# 一键设置完整的学习路线图数据

echo "=================================================="
echo "🗺️  ROADMAP SETUP - NEETCODE STYLE"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "${BLUE}📍 Project Root: ${PROJECT_ROOT}${NC}"
echo ""

# Step 1: Initialize Database
echo "${BLUE}Step 1/3: Initializing database with 30 knowledge points...${NC}"
cd "$PROJECT_ROOT"

if python3 scripts/init_db_with_roadmap.py; then
    echo "${GREEN}✓ Database initialized successfully!${NC}"
    echo ""
else
    echo "${RED}✗ Database initialization failed!${NC}"
    echo "${YELLOW}Please check your database connection and try again.${NC}"
    exit 1
fi

# Step 2: Backend Setup Check
echo "${BLUE}Step 2/3: Checking backend setup...${NC}"

if [ -d "$PROJECT_ROOT/backend/venv" ]; then
    echo "${GREEN}✓ Backend virtual environment found${NC}"
else
    echo "${YELLOW}⚠ Backend venv not found. Creating...${NC}"
    cd "$PROJECT_ROOT/backend"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "${GREEN}✓ Backend dependencies installed${NC}"
fi
echo ""

# Step 3: Frontend Setup Check
echo "${BLUE}Step 3/3: Checking frontend setup...${NC}"

if [ -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo "${GREEN}✓ Frontend dependencies found${NC}"
else
    echo "${YELLOW}⚠ Frontend node_modules not found. Installing...${NC}"
    cd "$PROJECT_ROOT/frontend"
    npm install
    echo "${GREEN}✓ Frontend dependencies installed${NC}"
fi
echo ""

# Success Summary
echo "=================================================="
echo "${GREEN}✓ ROADMAP SETUP COMPLETE!${NC}"
echo "=================================================="
echo ""
echo "${BLUE}📊 What's Ready:${NC}"
echo "  • 30 knowledge points loaded"
echo "  • 6 categories configured"
echo "  • Progressive difficulty (Easy → Hard)"
echo "  • Demo user created"
echo ""
echo "${BLUE}🚀 Next Steps:${NC}"
echo ""
echo "  ${YELLOW}1. Start Backend:${NC}"
echo "     cd backend"
echo "     uvicorn main:app --reload"
echo ""
echo "  ${YELLOW}2. Start Frontend (in new terminal):${NC}"
echo "     cd frontend"
echo "     npm run dev"
echo ""
echo "  ${YELLOW}3. Open Browser:${NC}"
echo "     http://localhost:5173/roadmap"
echo ""
echo "${BLUE}📚 Documentation:${NC}"
echo "  • Setup Guide: QUICK_ROADMAP_SETUP.md"
echo "  • Data Details: ROADMAP_DATA.md"
echo "  • Design Docs: NEETCODE_REDESIGN.md"
echo ""
echo "=================================================="
echo "${GREEN}Happy Learning! 🎉${NC}"
echo "=================================================="


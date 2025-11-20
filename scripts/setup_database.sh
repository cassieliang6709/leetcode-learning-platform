#!/bin/bash

# Database Setup Script - 数据库自动配置脚本
# This script will automatically configure the PostgreSQL database

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DB_NAME="leetcode_learning"
CURRENT_USER=$(whoami)

echo ""
echo "======================================"
echo "  数据库自动配置 Database Setup"
echo "======================================"
echo ""

# Step 1: Check if PostgreSQL is installed
echo -e "${BLUE}[1/6] 检查 PostgreSQL 安装状态...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${RED}✗ PostgreSQL 未安装${NC}"
    echo ""
    echo "请先安装 PostgreSQL:"
    echo "  macOS:  brew install postgresql@14"
    echo "  Linux:  sudo apt-get install postgresql postgresql-contrib"
    echo ""
    exit 1
fi
PG_VERSION=$(psql --version | awk '{print $3}')
echo -e "${GREEN}✓ PostgreSQL 已安装 (版本: $PG_VERSION)${NC}"
echo ""

# Step 2: Check if PostgreSQL is running
echo -e "${BLUE}[2/6] 检查 PostgreSQL 运行状态...${NC}"
if pg_isready -q; then
    echo -e "${GREEN}✓ PostgreSQL 正在运行${NC}"
else
    echo -e "${YELLOW}⚠ PostgreSQL 未运行，尝试启动...${NC}"
    
    # Try to start PostgreSQL based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew services start postgresql@14 2>/dev/null || brew services start postgresql 2>/dev/null || {
                echo -e "${RED}✗ 无法启动 PostgreSQL${NC}"
                echo "请手动启动: brew services start postgresql"
                exit 1
            }
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo systemctl start postgresql 2>/dev/null || {
            echo -e "${RED}✗ 无法启动 PostgreSQL${NC}"
            echo "请手动启动: sudo systemctl start postgresql"
            exit 1
        }
    fi
    
    # Wait and check again
    sleep 2
    if pg_isready -q; then
        echo -e "${GREEN}✓ PostgreSQL 已启动${NC}"
    else
        echo -e "${RED}✗ PostgreSQL 启动失败${NC}"
        exit 1
    fi
fi
echo ""

# Step 3: Create database
echo -e "${BLUE}[3/6] 创建数据库...${NC}"
echo "数据库名称: $DB_NAME"
echo "用户: $CURRENT_USER"

# Drop existing database if exists
psql -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true

# Create new database
if psql -d postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null; then
    echo -e "${GREEN}✓ 数据库创建成功${NC}"
else
    echo -e "${YELLOW}⚠ 尝试使用其他方法创建数据库...${NC}"
    createdb $DB_NAME 2>/dev/null || {
        echo -e "${RED}✗ 数据库创建失败${NC}"
        echo "请手动创建: createdb $DB_NAME"
        exit 1
    }
    echo -e "${GREEN}✓ 数据库创建成功${NC}"
fi
echo ""

# Step 4: Create .env file
echo -e "${BLUE}[4/6] 创建环境配置文件...${NC}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/backend/.env"

DATABASE_URL="postgresql+asyncpg://$CURRENT_USER@localhost:5432/$DB_NAME"

cat > "$ENV_FILE" << EOF
# Database Configuration
DATABASE_URL=$DATABASE_URL

# Application Settings
DEBUG=True
ENVIRONMENT=development

# API Keys (add your keys here if needed)
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
EOF

echo -e "${GREEN}✓ 环境配置文件已创建: backend/.env${NC}"
echo ""

# Step 5: Initialize database tables
echo -e "${BLUE}[5/6] 初始化数据表和种子数据...${NC}"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/backend/venv" ]; then
    source "$PROJECT_ROOT/backend/venv/bin/activate"
    echo "使用虚拟环境: backend/venv"
else
    echo -e "${YELLOW}⚠ 未找到虚拟环境，使用系统 Python${NC}"
fi

# Run initialization script
cd "$PROJECT_ROOT"
if python3 scripts/init_db.py; then
    echo -e "${GREEN}✓ 数据库初始化成功${NC}"
else
    echo -e "${RED}✗ 数据库初始化失败${NC}"
    echo "请检查 Python 依赖是否安装完整"
    exit 1
fi
echo ""

# Step 6: Verify connection
echo -e "${BLUE}[6/6] 验证数据库连接...${NC}"
if psql -d $DB_NAME -c "SELECT COUNT(*) FROM knowledge_points;" > /dev/null 2>&1; then
    KP_COUNT=$(psql -d $DB_NAME -t -c "SELECT COUNT(*) FROM knowledge_points;" 2>/dev/null | xargs)
    echo -e "${GREEN}✓ 数据库连接成功${NC}"
    echo "  - 知识点数量: $KP_COUNT"
    
    USER_COUNT=$(psql -d $DB_NAME -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | xargs)
    echo "  - 用户数量: $USER_COUNT"
else
    echo -e "${RED}✗ 数据库连接验证失败${NC}"
    exit 1
fi
echo ""

# Success summary
echo "======================================"
echo -e "${GREEN}✓ 数据库配置完成！${NC}"
echo "======================================"
echo ""
echo "📊 配置信息:"
echo "  数据库名: $DB_NAME"
echo "  用户名: $CURRENT_USER"
echo "  主机: localhost:5432"
echo "  连接串: $DATABASE_URL"
echo ""
echo "📝 环境文件: backend/.env"
echo ""
echo "🚀 下一步:"
echo "  1. 启动后端服务:"
echo "     cd backend && uvicorn main:app --reload"
echo ""
echo "  2. 启动前端服务:"
echo "     cd frontend && npm run dev"
echo ""
echo "  3. 或使用启动脚本:"
echo "     cd scripts && ./start_demo.sh"
echo ""


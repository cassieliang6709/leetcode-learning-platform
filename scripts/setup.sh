#!/bin/bash

# Setup script for LeetCode Learning Platform

echo "======================================"
echo "Setup: LeetCode Learning Platform"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(dirname "$0")/.."

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found${NC}"
    exit 1
fi

# Check PostgreSQL
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    PG_VERSION=$(psql --version)
    echo -e "${GREEN}✓ $PG_VERSION${NC}"
else
    echo -e "${RED}✗ PostgreSQL not found${NC}"
    echo "Please install PostgreSQL:"
    echo "  macOS: brew install postgresql"
    echo "  Linux: sudo apt-get install postgresql"
    exit 1
fi

echo ""
echo "======================================"
echo "Step 1: Database Setup"
echo "======================================"

# Create database
cd "$PROJECT_ROOT/scripts"
chmod +x create_db.sh
./create_db.sh

echo ""
echo "======================================"
echo "Step 2: Backend Setup"
echo "======================================"

cd "$PROJECT_ROOT/backend"

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "Step 3: Initialize Database"
echo "======================================"

cd "$PROJECT_ROOT"
python scripts/init_db.py

echo ""
echo "======================================"
echo "Step 4: Frontend Setup"
echo "======================================"

cd "$PROJECT_ROOT"
cd frontend

# Install npm packages
echo "Installing npm dependencies..."
npm install

echo ""
echo "======================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "======================================"
echo ""
echo "To start the demo, run:"
echo "  cd scripts"
echo "  ./start_demo.sh"
echo ""
echo "Or manually:"
echo "  Terminal 1: cd backend && uvicorn main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""



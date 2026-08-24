#!/bin/bash
# Start backend service only

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR=".venv"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Starting backend service...${NC}"

cd "$PROJECT_ROOT/backend"

# Activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3.12 -m venv "$VENV_DIR" || python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -r requirements.txt
else
    source "$VENV_DIR/bin/activate"
fi

# Start service
echo -e "${GREEN}✅ Backend service starting...${NC}"
echo -e "${BLUE}🔧 API URL: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"

uvicorn main:app --reload --host localhost --port 8000

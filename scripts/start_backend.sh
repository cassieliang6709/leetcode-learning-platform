#!/bin/bash
# Start backend service only

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Starting backend service...${NC}"

cd "$PROJECT_ROOT/backend"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3.12 -m venv venv || python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start service
echo -e "${GREEN}✅ Backend service starting...${NC}"
echo -e "${BLUE}🔧 API URL: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"

uvicorn main:app --reload --port 8000


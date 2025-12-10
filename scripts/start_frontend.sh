#!/bin/bash
# Start frontend service only

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎨 Starting frontend service...${NC}"

cd "$PROJECT_ROOT/frontend"

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    npm install
fi

# Start service
echo -e "${GREEN}✅ Frontend service starting...${NC}"
echo -e "${BLUE}📱 Access URL: http://localhost:5173${NC}"

npm run dev


#!/bin/bash

# Setup Production Environment Configuration Script
# This script helps you create the .env.production file for frontend deployment

echo "🚀 LeetCode Learning Platform - Production Environment Setup"
echo "==========================================================="
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📝 Please provide your production API URL"
echo "   (Your Render backend URL, e.g., https://leetcode-backend.onrender.com)"
echo ""
read -p "Enter your backend URL: " BACKEND_URL

# Remove trailing slash if present
BACKEND_URL=${BACKEND_URL%/}

# Create .env.production file
cat > frontend/.env.production << EOF
# Production API URL
# Generated on $(date)
VITE_API_URL=${BACKEND_URL}/api
EOF

echo ""
echo "✅ Created frontend/.env.production with:"
echo "   VITE_API_URL=${BACKEND_URL}/api"
echo ""
echo "📋 Next steps:"
echo "   1. Commit and push this file: git add frontend/.env.production"
echo "   2. Deploy to Vercel with this environment variable"
echo "   3. Update backend/main.py CORS settings with your Vercel URL"
echo ""
echo "🎉 Setup complete!"


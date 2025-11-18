#!/bin/bash

# Quick GitHub Setup Script
# This script helps you quickly push your project to GitHub

echo "🚀 GitHub Repository Quick Setup"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run 'git init' first."
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

# Get repository name
read -p "Enter repository name (default: leetcode-learning-platform): " REPO_NAME
REPO_NAME=${REPO_NAME:-leetcode-learning-platform}

echo ""
echo "📋 Summary:"
echo "   Username: $GITHUB_USERNAME"
echo "   Repository: $REPO_NAME"
echo "   URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

read -p "Is this correct? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ Cancelled"
    exit 1
fi

echo ""
echo "🔧 Setting up remote..."

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Add remote
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git remote add origin "$REPO_URL"

echo "✅ Remote added: $REPO_URL"
echo ""

# Update README with username
if [ -f "README.md" ]; then
    echo "📝 Updating README.md..."
    # This is a simple replacement - you may want to review it manually
    echo "   (You should manually update README.md with your GitHub username)"
fi

echo ""
echo "📤 Ready to push to GitHub!"
echo ""
echo "Next steps:"
echo "   1. Create repository on GitHub: https://github.com/new"
echo "      - Name: $REPO_NAME"
echo "      - Description: AI-powered algorithm learning platform"
echo "      - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "   2. Then run these commands:"
echo "      git push -u origin main"
echo ""
echo "   Or run this script again with --push flag to push automatically:"
echo "      ./GITHUB_QUICK_SETUP.sh --push"
echo ""

# If --push flag is provided, push automatically
if [ "$1" == "--push" ]; then
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo "🌐 View your repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        echo ""
        echo "❌ Push failed. Make sure:"
        echo "   1. Repository exists on GitHub"
        echo "   2. You have push permissions"
        echo "   3. You're logged in (git credential helper)"
    fi
fi

echo ""
echo "📚 For detailed setup instructions, see: GITHUB_SETUP.md"


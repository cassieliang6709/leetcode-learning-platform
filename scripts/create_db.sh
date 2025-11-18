#!/bin/bash

# Script to create PostgreSQL database for the project

DB_NAME="leetcode_learning"

echo "Creating PostgreSQL database: $DB_NAME"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Error: PostgreSQL is not installed"
    echo "Please install PostgreSQL first:"
    echo "  macOS: brew install postgresql@14"
    echo "  Linux: sudo apt-get install postgresql"
    exit 1
fi

# Get current user
CURRENT_USER=$(whoami)

echo "Using current user: $CURRENT_USER"

# Create database with current user
psql -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true
psql -d postgres -c "CREATE DATABASE $DB_NAME;"

if [ $? -eq 0 ]; then
    echo "✓ Database created successfully"
    echo ""
    echo "Connection details:"
    echo "  Database: $DB_NAME"
    echo "  User: $CURRENT_USER"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo ""
    echo "Connection string:"
    echo "  postgresql+asyncpg://$CURRENT_USER@localhost:5432/$DB_NAME"
    echo ""
    echo "⚠️  IMPORTANT: Update backend/.env with your connection string"
else
    echo "✗ Failed to create database"
    echo "Try manually: psql -d postgres -c \"CREATE DATABASE $DB_NAME;\""
    exit 1
fi


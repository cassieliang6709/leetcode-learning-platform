-- AlgoMentor database initialization
-- This script runs automatically when the PostgreSQL container starts for the first time.

-- Enable pgvector extension for semantic search (RAG pipeline)
CREATE EXTENSION IF NOT EXISTS vector;

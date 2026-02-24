<div align="center">

# AlgoMentor

**AI-Powered Coding Interview Prep Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL+pgvector-15-336791?logo=postgresql)](https://github.com/pgvector/pgvector)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Features](#features) · [Architecture](#architecture) · [Quick Start](#quick-start) · [API](#api-reference) · [Deploy](#deployment)

</div>

---

AlgoMentor is a full-stack LeetCode-style practice platform with a **RAG pipeline** that retrieves relevant algorithm articles from pgvector and injects them into Gemini 2.5 Flash — so every AI hint, chat response, and suggestion is grounded in the actual course curriculum, not hallucinated generics.

**89 LeetCode problems · 13 algorithm topics · Dynamic AI hints · Isolated code execution · Semantic search**

---

## Features

### 🧭 Structured Learning Roadmap
13 algorithm topics with comprehensive articles: pattern recognition checklists, Python templates (2–5 per topic), complexity tables, common pitfalls, and practice problem lists. Topics: Array/Hash, Two Pointers, Sliding Window, Binary Search, Linked List, Stack, Trees, DP, Graphs, Greedy, Backtracking, Heap, Bit Manipulation.

### 💻 Code Practice (89 LeetCode Hot 100)
- **Monaco Editor** (VS Code engine) — Python, JavaScript, Java, C++
- Language-specific starter code with stdin/stdout scaffolding for Piston
- **Run Code** (test feedback) and **Submit** (full evaluation + AI analysis)
- **Isolated execution**: Docker sandbox, 3s timeout, 128MB memory limit, no network access

### 🤖 RAG-Augmented AI Tutor
Every AI response retrieves relevant article chunks from pgvector before calling the LLM:

- **Chat**: multi-turn conversation about your code, grounded in course material
- **Failure analysis**: auto-triggered on test fail — identifies the specific bug
- **Optimization**: auto-triggered on all-pass — suggests complexity improvements
- **Source badges**: shows which article the AI referenced (📚 Sliding Window)

### 💡 Dynamic AI Hints (3 levels)
Hints are generated from your **current code** + **failing test cases** — not static text:

| Level | Style | What you get |
|-------|-------|-------------|
| 🤔 1 — Socratic | Question | ONE guiding question, no algorithm name, no spoilers |
| 🧭 2 — Direction | Approach | Pattern name + bullet-point strategy, zero code |
| 📝 3 — Pseudocode | Scaffold | Full pseudocode with `TODO` stubs + complexity note |

Levels are gated — unlock 1 before 2, unlock 2 before 3.

### 🔍 Semantic Problem Search
"sliding window substring" → LeetCode 3, 76, 424. In-memory cosine similarity over all 89 problem embeddings. Debounced 400ms with live results in the drawer.

### 📊 Personalized Context (RAG B)
AI automatically injects your last 3 submission outcomes per problem: *"You passed 2/3 test cases last time — edge case handling is likely the issue."*

### 📜 Submission History
All submissions with status, language, timestamp. Click any past entry to reload the problem.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              React SPA (Vite + Monaco)               │
│  Roadmap │ Learning │ CodeCheck │ Quiz │ Auth        │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS REST
┌──────────────────────▼──────────────────────────────┐
│           FastAPI (async Python 3.11)                │
│  /auth  /knowledge  /quiz  /code  /execution         │
│  /ai (chat · hint · suggest)  /rag (index · search)  │
│                                                      │
│  ┌──────────────┐  ┌─────────────────────────────┐  │
│  │ code_executor│  │ gemini_ai.py                 │  │
│  │ Piston HTTP  │  │ chat_about_code  (RAG+B+D)   │  │
│  └──────┬───────┘  │ get_dynamic_hint (NEW)        │  │
│         │          │ get_failure_suggestion         │  │
│  ┌──────┴───────┐  └──────────────┬───────────────┘  │
│  │  SlowAPI     │  ┌──────────────▼───────────────┐  │
│  │  Rate limit  │  │ rag_service.py                │  │
│  │  Redis/mem   │  │ chunk → embed → pgvector      │  │
│  └──────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
            │                         │
  ┌─────────▼──────┐       ┌──────────▼──────────┐
  │  Piston Docker │       │  PostgreSQL + pgvec  │
  │  3s timeout    │       │  users               │
  │  128MB mem     │       │  knowledge_points    │
  │  net isolated  │       │  knowledge_embeddings│
  └────────────────┘       │  quiz_questions      │
                           │  code_submissions    │
                           └─────────────────────┘
```

**RAG Pipeline:**
```
13 articles → 500-char chunks (50-char overlap)
           → all-MiniLM-L6-v2 (384-dim, local)
           → pgvector cosine similarity (threshold 0.4)
           → top-3 chunks → Gemini 2.5 Flash system prompt
```

---

## Quick Start

### Prerequisites
- Python 3.11+ · Node.js 18+ · Docker + Docker Compose
- [Google Gemini API key](https://ai.google.dev/) (free tier)

### Option A — Docker (recommended)

```bash
git clone https://github.com/cassieliang6709/leetcode-learning-platform.git
cd leetcode-learning-platform

cp backend/.env.example backend/.env
# Edit backend/.env → set GEMINI_API_KEY and SECRET_KEY

docker-compose up -d

# Install Piston language runtimes (one-time, ~2 min)
bash scripts/setup_piston.sh

# Seed database
docker-compose exec backend python scripts/init_db.py
docker-compose exec backend python scripts/update_articles_v2.py

# Build RAG vector index
curl -X POST http://localhost:8000/api/rag/index/all
```

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

### Option B — Local Dev

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api" > .env.local
npm run dev
```

> **Code execution without Docker:** Get a free Piston API key from [discord.gg/engineerman](https://discord.gg/engineerman) (`#api-key` channel) and set `PISTON_API_KEY=your-key` in `backend/.env`.

---

## Environment Variables

```env
# backend/.env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/algomentor
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-random-32-char-secret      # openssl rand -hex 32
PISTON_URL=http://localhost:2000/api/v2    # self-hosted Docker; omit for public API
PISTON_API_KEY=                            # needed only for public emkc.org API
REDIS_URL=redis://localhost:6379           # optional; falls back to in-memory
SQL_ECHO=false
```

---

## Project Structure

```
algo-mentor/
├── backend/
│   ├── main.py                       # App entry, CORS, routes, rate limiter
│   ├── app/
│   │   ├── models.py                 # SQLAlchemy: User, QuizQuestion, CodeSubmission, KnowledgeEmbedding
│   │   ├── database.py               # Async SQLAlchemy session factory
│   │   ├── api/routes/
│   │   │   ├── auth.py
│   │   │   ├── knowledge.py          # Roadmap articles + learning plan
│   │   │   ├── quiz.py               # MCQ quizzes with hints
│   │   │   ├── code_check.py         # Problem list (deduplicated), AI analysis
│   │   │   ├── code_execution.py     # Piston submit, starter code, submission history
│   │   │   ├── ai_assistant.py       # Chat (RAG+B+D), dynamic hints, failure/opt suggest
│   │   │   └── rag.py                # Index all, chunk search, semantic problem search
│   │   └── services/
│   │       ├── gemini_ai.py          # Gemini 2.5 Flash: chat, dynamic hints, analysis
│   │       ├── rag_service.py        # Chunking, embedding, pgvector retrieval
│   │       ├── code_executor.py      # Piston API wrapper (PISTON_URL env var)
│   │       └── auth_service.py       # JWT creation/validation + bcrypt
│   └── scripts/
│       ├── init_db.py                # Create tables + seed 89 problems
│       └── update_articles_v2.py     # Clean duplicate KPs + write 13 articles
├── frontend/src/
│   ├── pages/
│   │   ├── CodeCheckPage.jsx         # Main IDE: editor, dynamic hints, AI chat, submissions
│   │   ├── LearningPage.jsx          # Article reader with markdown
│   │   ├── RoadmapPage.jsx           # Topic grid with dynamic category filter
│   │   └── QuizPage.jsx
│   └── services/api.js               # All API calls (Axios + JWT interceptor)
├── docker-compose.yml                # postgres/pgvector + redis + piston + backend
├── backend/Dockerfile                # Pre-downloads sentence-transformers model
└── scripts/
    ├── init_db.sql                   # CREATE EXTENSION vector (auto on postgres start)
    └── setup_piston.sh               # Install py/js/java/cpp runtimes into Piston
```

---

## API Reference

| Method | Endpoint | Rate | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register` | — | Create account |
| `POST` | `/api/auth/login` | — | Login → JWT |
| `GET` | `/api/code/problems` | — | 89 problems (deduplicated by leetcode_id) |
| `GET` | `/api/execution/question/{id}/starter-code` | — | Language starter code |
| `POST` | `/api/execution/submit/{id}` | 10/min | Run code against test cases |
| `GET` | `/api/execution/submissions/me/recent` | — | Last N submissions (JWT) |
| `POST` | `/api/ai/hint` | 20/min | Dynamic 3-level AI hint (RAG-augmented) |
| `POST` | `/api/ai/chat` | 20/min | Multi-turn AI chat (RAG + user history) |
| `POST` | `/api/ai/suggestion/failure` | — | Auto failure analysis |
| `POST` | `/api/ai/suggestion/optimization` | — | Complexity suggestions |
| `GET` | `/api/rag/problems/search?q=...` | — | Semantic problem search |
| `POST` | `/api/rag/index/all` | — | Rebuild pgvector index (admin) |

Full interactive docs: `http://localhost:8000/docs`

---

## Deployment

**Recommended stack: Railway + Vercel + Supabase ($5/month)**

```bash
# 1. Supabase — create project, run in SQL Editor:
CREATE EXTENSION IF NOT EXISTS vector;

# 2. Railway — deploy backend
brew install railway
cd backend && railway login && railway init && railway up
# Set env vars in Railway Dashboard

# 3. Initialize DB
DATABASE_URL="your-supabase-url" python scripts/init_db.py
DATABASE_URL="your-supabase-url" python scripts/update_articles_v2.py
curl -X POST https://your-app.railway.app/api/rag/index/all

# 4. Vercel — deploy frontend
cd frontend && npx vercel deploy --prod
# Set VITE_API_URL=https://your-app.railway.app/api
```

See [`interview-prep/MASTER.md`](interview-prep/MASTER.md) for full deployment guide and interview Q&A.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Monaco Editor, React Markdown, Axios |
| Backend | FastAPI, SQLAlchemy 2.0 async, Pydantic v2, python-jose, bcrypt |
| Database | PostgreSQL 15 + pgvector |
| AI / LLM | Google Gemini 2.5 Flash |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` (384-dim, local inference) |
| Code Execution | Piston (Docker sandbox or public API) |
| Rate Limiting | SlowAPI + Redis (in-memory fallback) |
| Deployment | Railway · Vercel · Supabase |

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
Built by <a href="https://github.com/cassieliang6709">Yue Liang</a>
</div>

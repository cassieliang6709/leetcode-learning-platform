# AlgoMentor — Interview Master Reference

> Updated: 2026-02-24 | Supersedes all prior interview-prep docs

---

## Table of Contents
1. [One-Sentence Pitch](#pitch)
2. [Architecture Overview](#architecture)
3. [Full API Surface](#api)
4. [Technical Q&A — System Design](#qa-system)
5. [Technical Q&A — RAG & AI Pipeline](#qa-rag)
6. [Technical Q&A — Dynamic Hint System](#qa-hints)
7. [Technical Q&A — Frontend & Code Execution](#qa-frontend)
8. [Technical Q&A — Scaling & Trade-offs](#qa-scaling)
9. [Resume Bullets by Role](#resume)
10. [Deployment Guide — Railway + Vercel + Supabase](#deploy)
11. [Next Improvements](#next)

---

## 1. One-Sentence Pitch {#pitch}

> "I built **AlgoMentor**, a full-stack AI-powered coding tutor with a RAG pipeline that chunks 13 algorithm articles, embeds them with sentence-transformers, stores in pgvector, and injects retrieved context into Gemini 2.5 Flash — so users get hints and answers grounded in the actual curriculum. The platform covers 89 LeetCode problems in a Monaco editor with Docker-based isolated code execution, a 3-level dynamic AI hint system (Socratic → Direction → Pseudocode), personalized context from submission history, and semantic problem search. Stack: FastAPI + React + PostgreSQL/pgvector + Gemini 2.5 Flash."

---

## 2. Architecture Overview {#architecture}

```
┌─────────────────────────────────────────────────────────────────┐
│                        React SPA (Vite)                          │
│  HomePage │ RoadmapPage │ LearningPage │ CodeCheckPage           │
│  Monaco Editor │ AI Chat │ Dynamic Hints │ Submissions Tab       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS REST
┌──────────────────────────▼──────────────────────────────────────┐
│                   FastAPI (async, Python 3.11)                   │
│                                                                  │
│  /api/auth        /api/knowledge    /api/quiz                   │
│  /api/code        /api/execution    /api/ai         /api/rag    │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ auth_service│  │ code_executor│  │      gemini_ai.py        │ │
│  │ JWT + bcrypt│  │ Piston REST  │  │  get_failure_suggestion  │ │
│  └─────────────┘  └──────┬───────┘  │  chat_about_code (RAG)  │ │
│                          │          │  get_dynamic_hint (NEW)  │ │
│  ┌─────────────┐         │          │  get_optimization        │ │
│  │  rag_service│         │          └────────────┬────────────┘ │
│  │ chunk+embed │         │                       │              │
│  │ pgvector    │         │          ┌────────────▼────────────┐ │
│  └──────┬──────┘         │          │  sentence-transformers   │ │
│         │                │          │  all-MiniLM-L6-v2 384d  │ │
└─────────┼────────────────┼──────────┴────────────────────────-─┘
          │                │
┌─────────▼──────┐  ┌──────▼────────────────┐
│  PostgreSQL    │  │  Piston (Docker)        │
│  + pgvector    │  │  run_timeout: 3000ms    │
│  users         │  │  memory_limit: 128MB    │
│  knowledge_pts │  │  network isolated       │
│  embeddings    │  └────────────────────────┘
│  quiz_qs       │
│  submissions   │  ┌────────────────────────┐
└────────────────┘  │  Redis (optional)       │
                    │  SlowAPI rate limiting   │
                    │  (in-memory fallback)    │
                    └────────────────────────┘
```

### Key Technology Choices

| Component | Choice | Why |
|-----------|--------|-----|
| Backend | FastAPI + asyncpg | Native async/await — handles concurrent AI calls + DB queries without blocking |
| Database | PostgreSQL + pgvector | Vector search + relational data in one DB; no Pinecone dependency; same ACID transactions |
| Embedding | all-MiniLM-L6-v2 (384-dim) | 90MB, local inference ~50ms, strong semantic similarity benchmark |
| LLM | Gemini 2.5 Flash | Low latency Flash design, generous free tier, excellent code reasoning |
| Code execution | Piston (Docker) | Open-source, Docker-isolated containers, 12 languages, 3s timeout, 128MB limit |
| Frontend | React + Monaco Editor | VS Code engine; dynamic syntax highlighting; starter code injection |
| Auth | JWT (python-jose) + bcrypt | Stateless, no session store needed; bcrypt for password hashing |
| Rate limiting | SlowAPI + Redis | Per-IP counters; Redis for multi-instance consistency; memory fallback |

---

## 3. Full API Surface {#api}

```
AUTH
  POST  /api/auth/register
  POST  /api/auth/login
  GET   /api/auth/me

KNOWLEDGE (Learning Roadmap)
  GET   /api/knowledge/points
  GET   /api/knowledge/points/{id}
  GET   /api/knowledge/points/{id}/questions
  POST  /api/knowledge/test/{user_id}
  GET   /api/knowledge/plan/{user_id}

QUIZ
  GET   /api/quiz/daily/{user_id}
  POST  /api/quiz/answer/{user_id}
  GET   /api/quiz/by-knowledge/{kp_id}
  GET   /api/quiz/{id}/hint/{level}

CODE CHECK (AI static analysis)
  POST  /api/code/check
  GET   /api/code/problems
  GET   /api/code/problem/{id}
  GET   /api/code/hint/{id}/{level}         ← static hints (legacy)
  GET   /api/code/submissions/{user_id}

CODE EXECUTION (Piston)
  POST  /api/execution/submit/{question_id}     ← 10 req/min rate limit
  GET   /api/execution/question/{id}/starter-code
  GET   /api/execution/supported-languages
  GET   /api/execution/submissions/me/recent    ← JWT auth, optional

AI ASSISTANT
  POST  /api/ai/suggestion/failure              ← auto-called on test fail
  POST  /api/ai/chat                            ← 20 req/min, RAG B+D
  POST  /api/ai/suggestion/optimization
  POST  /api/ai/hint                            ← NEW: dynamic 3-level AI hint

RAG
  POST  /api/rag/index/all                      ← admin: rebuild vector index
  GET   /api/rag/search                         ← article chunk search
  GET   /api/rag/problems/search?q=...          ← RAG C: semantic problem search
```

---

## 4. Technical Q&A — System Design {#qa-system}

**Q: Walk me through the overall architecture.**

The frontend is a React SPA with Monaco Editor for code editing. It talks to a FastAPI async backend over REST. The backend has six route groups: auth, knowledge, quiz, code (static analysis), execution (Piston), and AI/RAG. Data is stored in PostgreSQL with pgvector extension for vector search. Code execution is delegated to Piston — a Docker-based sandbox we call via HTTP. AI responses come from Gemini 2.5 Flash, always augmented by RAG context retrieved from pgvector.

---

**Q: Why FastAPI over Django/Flask?**

Three reasons: (1) native async/await for non-blocking DB + AI API calls in one thread, (2) Pydantic models give automatic request validation and OpenAPI docs for free, (3) startup latency is much lower than Django which matters for Railway cold starts.

---

**Q: How is your DB schema designed?**

Core tables:
- `users` — id, username, email, hashed_password
- `knowledge_points` — name, category, difficulty, article_content (TEXT), description
- `knowledge_embeddings` — knowledge_point_id (FK), chunk_text, embedding (vector(384)), chunk_index
- `quiz_questions` — title, description, category, difficulty, hints (JSONB array), test_cases (JSONB array), starter_code (JSONB per-language), leetcode_id
- `code_submissions` — user_id, question_id, code, language, passed (bool), ai_feedback (JSONB with test summary)

The JSONB columns for `test_cases` and `starter_code` let me store structured data without extra join tables, keeping queries simple.

---

**Q: How do you handle the duplicate problem records in the DB?**

We have 267 DB rows but only 89 unique LeetCode problems (three init scripts ran historically). Rather than touching the DB, I added deduplication at the API layer in `get_problems()`: group by `leetcode_id`, prefer the record with non-empty `test_cases`. For `get_problem_detail()` and `get_starter_code()`, there's a fallback: if the primary record is empty, query siblings with the same `leetcode_id` until we find one with data.

---

**Q: How does JWT auth work?**

`python-jose` generates HS256-signed JWTs containing `user_id` and `exp` (7-day TTL). Passwords are hashed with bcrypt (direct calls — we removed passlib because it's incompatible with bcrypt 4.x). The React frontend stores the token in localStorage and an Axios request interceptor automatically injects `Authorization: Bearer <token>` on every request. A response interceptor catches 401s and redirects to `/login`, with a whitelist for endpoints that are optional-auth (like recent submissions).

---

**Q: How do you prevent API abuse?**

SlowAPI rate limiter keyed on client IP:
- `/api/execution/submit` — 10 req/min (Piston is expensive)
- `/api/ai/chat` and `/api/ai/hint` — 20 req/min (Gemini API cost)
- Redis backend for multi-instance consistency; falls back to in-memory for single-instance dev

---

## 5. Technical Q&A — RAG & AI Pipeline {#qa-rag}

**Q: Explain your RAG pipeline end-to-end.**

```
Article text (13 KPs)
  → split into 500-char chunks with 50-char overlap
  → encode with sentence-transformers all-MiniLM-L6-v2 → 384-dim vector
  → store in knowledge_embeddings (pgvector)

User asks a question
  → encode query with same model
  → SELECT chunk_text, (1 - embedding <=> query_vec) AS score
    FROM knowledge_embeddings
    WHERE score > 0.4
    ORDER BY score DESC LIMIT 3
  → format top-3 chunks into RAG context string
  → inject into Gemini system prompt
  → AI answers grounded in actual curriculum material
```

---

**Q: What's RAG B — personalized context?**

When a logged-in user sends a chat message or requests a hint, the backend queries their last 3 `CodeSubmission` records for the current problem. It formats them as: *"Your last 3 attempts: Python, 2/3 passed (most recent)"*. This context is prepended to the RAG context before calling Gemini. Result: the AI can say "You've been passing 2/3 test cases — your edge case handling for empty arrays is likely the issue."

---

**Q: What's RAG C — semantic problem search?**

`GET /api/rag/problems/search?q=sliding+window` runs in-memory cosine similarity between the query embedding and embeddings of all 89 problem titles+descriptions (computed on-the-fly with numpy). Returns top-8 problems with similarity score > 0.25. This lets users find problems by concept rather than exact title. E.g. "two pointer string" → Longest Substring Without Repeating, Valid Palindrome, 3Sum.

---

**Q: What's RAG D — source attribution?**

The `/api/ai/chat` and `/api/ai/hint` endpoints return a `rag_sources` array: `[{id: 3, name: "Sliding Window"}]`. The frontend renders these as small badges under each AI message: "📚 Sliding Window". This increases user trust (they can verify what the AI based its answer on) and demonstrates the RAG is actually doing something useful, not just hallucinating.

---

**Q: Why the 0.4 similarity threshold?**

Empirically tuned: below 0.2 introduces noisy irrelevant chunks; above 0.6 returns nothing for most queries. 0.4 gives clean relevant results for domain-specific questions like "sliding window template" while filtering out unrelated chunks.

---

**Q: pgvector vs Pinecone/Weaviate?**

For this scale (~103 chunks across 13 articles), pgvector is strictly better: zero extra infra, vector queries and relational filters run in one SQL statement, ACID consistency between article updates and embedding updates. Pinecone only beats pgvector at billions of vectors with very high QPS.

---

**Q: Can you swap the embedding model?**

Yes. The model is loaded via `get_embedding_model()` singleton in `rag_service.py`. Swapping to `text-embedding-3-small` (OpenAI, 1536-dim) requires changing that one function and re-running `POST /api/rag/index/all`. The pgvector column would need to be resized, which is a one-time ALTER TABLE.

---

## 6. Technical Q&A — Dynamic Hint System {#qa-hints}

**Q: How does the new Dynamic AI Hint system work?**

`POST /api/ai/hint` accepts `question_id`, `code`, `language`, `hint_level` (1–3), and optional `test_results`. The backend:
1. Fetches the problem description from DB
2. Runs RAG retrieval (top-2 article chunks relevant to the problem)
3. Optionally injects user's failing test cases as context
4. Calls `GeminiAI.get_dynamic_hint()` with a level-specific prompt instruction
5. Returns the hint markdown + `rag_sources` for attribution

The hint is **tailored to the user's current code** — not a static lookup. If the user's code has a specific bug, the Level 1 hint will ask a question that points exactly at it.

---

**Q: What are the three hint levels?**

| Level | Name | Behavior | Constraint |
|-------|------|----------|------------|
| 1 | Socratic Question | Asks ONE guiding question to make the student discover the issue themselves | No algorithm name, no approach, max 2 sentences |
| 2 | Direction Hint | Names the algorithm pattern + 2–3 bullet-point approach | No code whatsoever |
| 3 | Pseudocode | Full pseudocode with TODO comments marking steps to implement | Complexity note at end |

Level 2 and 3 are gated: you must unlock Level 1 first (progressive disclosure reduces shortcutting).

---

**Q: Why tie hints to user's code instead of static hints?**

Static hints (Level 1: "Think about using a hash map") are useless when the user already has a hash map in their code and the actual bug is an off-by-one error. Dynamic hints look at what the user wrote and at the failing test cases, then ask *exactly* the right Socratic question. This is the pedagogical core of the system.

---

**Q: How do the failing test cases improve the hint?**

The frontend passes the current `testResults.test_results` array to the hint endpoint. The backend formats the first 2 failing cases as: `"Input: [1,2,3] | Expected: 6 | Got: 5"` and injects them into the prompt. The AI then references the specific failure rather than giving generic advice.

---

## 7. Technical Q&A — Frontend & Code Execution {#qa-frontend}

**Q: How does the code editor work?**

Monaco Editor (the VS Code engine) loaded via `@monaco-editor/react`. On problem select, the frontend calls `GET /api/execution/question/{id}/starter-code?language=python`. The backend returns language-specific starter code that includes the stdin/stdout parsing framework Piston needs. The editor supports Python, JavaScript, Java, C++ with syntax highlighting.

---

**Q: Why does starter code include stdin parsing?**

Piston communicates via stdin/stdout. The test harness sends JSON-encoded test inputs through stdin; the code must parse them, call the Solution method, and print the result to stdout. The starter code template handles all this boilerplate so users only implement the algorithm.

---

**Q: What were the hardest bugs to fix?**

Three significant ones:
1. **Piston 400 errors**: Self-hosted Piston limits `run_timeout` to max 3000ms. We were sending 5000ms. Fixed by capping both compile and run timeouts at 3000ms.
2. **267 duplicate problems**: Three init scripts each ran once, creating 3× the data. Fixed with API-layer deduplication: `get_problems()` groups by `leetcode_id`, prefers the record with populated `test_cases`.
3. **Unauthenticated users redirected to login**: `loadRecentSubmissions()` was called in `useEffect` unconditionally. The 401 response triggered the Axios interceptor's redirect. Fixed: (a) only fetch submissions on tab click, (b) whitelist that endpoint in the interceptor's `isOptionalAuth` check.

---

**Q: How does the semantic problem search work on the frontend?**

The search bar in the problem list drawer debounces input by 400ms, then calls `GET /api/rag/problems/search?q=<query>`. Results are sorted by cosine similarity score and displayed above the full problem list. Selecting a result loads that problem into the editor and closes the drawer.

---

## 8. Technical Q&A — Scaling & Trade-offs {#qa-scaling}

**Q: Where are the bottlenecks at 1000 QPS?**

1. `sentence-transformers` embedding is CPU-bound. At 1000 QPS we'd need either a GPU or a batching queue for embedding requests — or swap to an API-based embedding service (OpenAI, Cohere).
2. Gemini API has its own rate limits. Solution: semantic caching — cache `(question_id, query_hash) → response`.
3. Piston container startup latency (~200–500ms). Solution: container pool pre-warming, or move to a long-running sandbox with process isolation instead of container-per-execution.

---

**Q: How would you scale code execution?**

Horizontal: spin up multiple Piston instances behind a load balancer, add a submission queue (Redis/SQS) to smooth traffic spikes. Stateless API layer can scale horizontally without coordination. The submission queue also enables async result polling — users don't hold a request open during execution.

---

**Q: What would you change about the RAG pipeline?**

Add a cross-encoder reranker as a second pass: after vector retrieval gives top-10 candidates, the reranker rescores them with a bidirectional attention model for much higher precision. Also collect user thumbs-up/down on AI answers to create a fine-tuning dataset. Current pipeline has no feedback loop.

---

**Q: JWT stateless — what about token revocation?**

Current system has no revocation (pure stateless JWT). If a token is stolen, it's valid until the 7-day expiry. Production hardening: shorten access token TTL to 15 minutes, add a refresh token flow, and maintain a Redis blacklist for explicit logouts. The trade-off is one extra Redis lookup per request vs the security improvement.

---

## 9. Resume Bullets by Role {#resume}

### SDE / Software Engineer

```
AlgoMentor — AI-Powered Coding Interview Platform                [github.com/...]
• Built full-stack coding practice platform: React + FastAPI + PostgreSQL (pgvector),
  with Monaco Editor, JWT auth, rate-limited REST API, and Docker-isolated code
  execution via Piston (3s timeout, 128MB memory limit, network isolation)
• Designed RAG pipeline: chunked 13 algorithm articles → sentence-transformers
  (all-MiniLM-L6-v2, 384-dim) → pgvector cosine search → Gemini 2.5 Flash context
  injection; grounds AI responses in curriculum material to reduce hallucinations
• Built 3-level Dynamic AI Hint system: Socratic question → Direction hint →
  Pseudocode; hints are tailored to user's current code and failing test cases via
  RAG context injection, not static lookups
• Implemented API-layer deduplication for 267 DB records → 89 unique problems;
  fallback chain for starter-code and test-case retrieval when records are sparse
```

### ML / AI Engineer

```
AlgoMentor — RAG-Enhanced Adaptive AI Coding Tutor               [github.com/...]
• Designed end-to-end RAG pipeline: overlapping-chunk text splitting (500-char/50-
  overlap) → local embedding with all-MiniLM-L6-v2 (384-dim) → pgvector cosine
  similarity retrieval (threshold 0.4) → context-augmented generation with Gemini 2.5 Flash
• Built 3-tier adaptive hint engine (POST /api/ai/hint): Level 1 = Socratic question,
  Level 2 = pattern + direction, Level 3 = pseudocode with TODO stubs; prompt
  includes user's failing test cases for targeted, code-aware feedback
• Implemented personalized tutoring context (RAG B): injected user's last 3 submission
  outcomes (pass rate, language, timestamp) into LLM system prompt for adaptive hints
• Built semantic problem search (RAG C): in-memory cosine similarity across 89 problem
  embeddings via numpy; returns relevance-ranked results with 0.6+ scores on
  domain-specific queries ("sliding window substring" → LeetCode 3, 76, 424)
• Added RAG source attribution (RAG D): returns knowledge point names alongside AI
  responses; frontend renders "📚 Sliding Window" badges to ground user trust
```

### Product Manager

```
AlgoMentor — AI Coding Interview Prep Platform (Solo-Built)     [github.com/...]
• Identified gap in interview prep tools lacking personalized AI feedback; designed
  and shipped end-to-end platform in 3 weeks: 89 LeetCode problems, 13 topics,
  AI tutoring, code execution, and learning roadmap
• Designed 3-level progressive hint system (Socratic → Direction → Pseudocode)
  with friction gates; hints use user's current code and failing test cases for
  personalized guidance — not generic static text
• Shipped RAG-powered AI tutor grounding hints in course materials; added source
  attribution badges so users know which article the AI referenced
• Built semantic problem search so users find problems by concept ("two pointer
  on sorted array") rather than exact titles; debounced 400ms UX with live results
• Defined measurable progress tracking: test case pass rate per submission,
  per-topic assessments, personalized learning plan from weak area detection
```

### Data Engineering / Backend-Focused

```
AlgoMentor — Knowledge Base, Vector Search & Async API          [github.com/...]
• Built async FastAPI backend with PostgreSQL + pgvector; designed normalized schema
  with JSONB columns for test_cases and starter_code (per-language map), avoiding
  N+1 join tables while keeping queries clean
• Implemented batch embedding pipeline: 13 knowledge articles → 103 chunks →
  384-dim vectors in pgvector; re-indexed via admin endpoint POST /api/rag/index/all
• Built in-memory semantic search with numpy cosine similarity across 89 problem
  embeddings; deduplicates by leetcode_id at API layer (267 DB rows → 89 unique)
• Designed rate-limiting backed by Redis with in-memory fallback (SlowAPI);
  stateless service + external session store for horizontal scaling readiness
• Added personalized submission history injection for AI context: last 3 CodeSubmission
  rows per user/problem queried async and formatted into LLM system prompt
```

---

## 10. Deployment Guide — Railway + Vercel + Supabase {#deploy}

**Cost:** $5/month (Railway Hobby) + free (Vercel + Supabase)

### Step 1 — Supabase (5 min)
```bash
# 1. Sign up at supabase.com → New Project
# 2. Settings → Database → URI  (change protocol to postgresql+asyncpg, port 5432)
# 3. SQL Editor → run:
CREATE EXTENSION IF NOT EXISTS vector;
```

### Step 2 — Railway Backend (10 min)
```bash
brew install railway
cd algo-mentor/backend
railway login
railway init    # select "Empty Project"
railway up
```

Railway Dashboard → Variables → add:
```env
DATABASE_URL=postgresql+asyncpg://[supabase-connection-string]
GEMINI_API_KEY=your-gemini-key
SECRET_KEY=<openssl rand -hex 32>
PISTON_API_KEY=             # optional — see Step 5
SQL_ECHO=false
```

### Step 3 — Initialize Database
```bash
# Run locally, pointing at Supabase
cd backend
DATABASE_URL="postgresql+asyncpg://..." python scripts/init_db.py
DATABASE_URL="postgresql+asyncpg://..." python scripts/update_articles_v2.py

# After Railway deploy — rebuild RAG index
curl -X POST https://your-app.railway.app/api/rag/index/all
```

### Step 4 — Vercel Frontend (3 min)
```bash
cd algo-mentor/frontend
npx vercel deploy --prod
```
Vercel Dashboard → Settings → Environment Variables:
```env
VITE_API_URL=https://your-app.railway.app/api
```

### Step 5 — Piston API Key (optional, for code execution)
```
1. Join Discord: https://discord.gg/engineerman
2. Request free API key in #api-key channel
3. Add to Railway: PISTON_API_KEY=your-key
```
> Without a Piston key: code execution is disabled, but AI tutoring, RAG chat, dynamic hints, roadmap, and quiz all work — fully sufficient for demos.

### Multi-project Cost Estimate

| Projects | Plan | Monthly |
|----------|------|---------|
| 1–2 | Railway Hobby + Supabase free | **$5** |
| 3–5 | Railway Hobby + Neon free × N | **$5** |
| 5+ | Railway Team + Neon | **$20** |

---

## 11. Next Improvements {#next}

### High Priority (Interview Demo Value)

| Feature | Effort | Demo Impact |
|---------|--------|-------------|
| Hint quality feedback (👍/👎) | 2h | Shows data collection mindset |
| Submission streak / heatmap | 3h | Gamification, retention signal |
| Cross-encoder reranker for RAG | 4h | Shows ML depth |

### Medium Priority

| Feature | Effort | Notes |
|---------|--------|-------|
| Refresh token + short JWT TTL | 3h | Production security hardening |
| Async submission queue (Redis) | 4h | Handles Piston latency spikes |
| Problem difficulty progression | 3h | Spaced repetition recommendation |

### Architectural Evolution

If traffic grows:
1. **Embedding bottleneck** → GPU server or batch queue in front of `sentence-transformers`
2. **Gemini rate limit** → Semantic cache: `(question_id + query_hash) → response` in Redis
3. **Piston latency** → Pre-warmed container pool; or migrate to Firecracker microVMs
4. **pgvector at scale** → Switch index from IVFFlat to HNSW (`CREATE INDEX ... USING hnsw`) — O(log n) query vs O(n)

---

*AlgoMentor — built by Yue Liang | Last updated 2026-02-24*

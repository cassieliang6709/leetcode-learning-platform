# AlgoMentor — 部署方案 & 面试准备

> 生成日期：2026-02-23

---

## 一、最终部署方案（多项目通用）

### 推荐组合：Vercel + Railway + Supabase

```
前端  → Vercel      免费，GitHub push 自动部署
后端  → Railway     $5/月 Hobby（所有项目共享一个 Plan）
数据库 → Supabase   免费（最多 2 个项目）或 Neon（无限免费）
```

### 为什么选这套

| 需求 | 答案 |
|------|------|
| 自动 CI/CD | GitHub 连接后，push 即部署 |
| pgvector 支持 | Supabase / Neon 原生支持 |
| Python 后端 | Railway NIXPACKS 自动检测 Python |
| 多项目管理 | Railway 一个账号开多个 Service |
| 零运维 | 全托管 PaaS，无需管 server |

### 多项目费用估算

| 项目数 | 方案 | 月费 |
|--------|------|------|
| 1-2 个 | Railway Hobby + Supabase 免费 | **$5/月** |
| 3-5 个 | Railway Hobby + Neon 免费 x N | **$5/月** |
| 5+ 个 | Railway Team + Neon | **$20/月** |

---

## 二、AlgoMentor 部署 Step-by-Step

### Step 1 — Supabase 数据库（5分钟）

```bash
# 1. 注册 supabase.com，创建免费项目
# 2. Settings → Database → Connection string → URI
#    把协议改成 postgresql+asyncpg，端口改成 5432
# 3. SQL Editor 里运行：
CREATE EXTENSION IF NOT EXISTS vector;
```

### Step 2 — Railway 后端（10分钟）

```bash
# 安装 Railway CLI
brew install railway       # macOS

cd algo-mentor/backend
railway login
railway init               # 选 "Empty Project"
railway up                 # 部署
```

在 Railway Dashboard → Variables 添加：

```env
DATABASE_URL=postgresql+asyncpg://[supabase-connection-string]
GEMINI_API_KEY=你的Gemini Key
SECRET_KEY=随机32字符字符串（openssl rand -hex 16）
PISTON_API_KEY=            # 可选，见下方
SQL_ECHO=false
```

### Step 3 — 初始化数据库

```bash
# 本地连 Supabase DB 运行初始化脚本
cd backend
DATABASE_URL="你的supabase-url" python scripts/init_db.py
DATABASE_URL="你的supabase-url" python scripts/update_articles_v2.py

# 部署完成后，调用 RAG 索引接口
curl -X POST https://your-railway-url.railway.app/api/rag/index/all
```

### Step 4 — Vercel 前端（3分钟）

```bash
cd algo-mentor/frontend
npx vercel deploy --prod

# 设置环境变量（Vercel Dashboard → Settings → Environment Variables）
VITE_API_URL=https://your-app.railway.app/api
```

### Step 5 — Piston 代码执行（可选）

```
1. 加入 Discord: https://discord.gg/engineerman
2. 在 #api-key 频道申请免费 API Key
3. Railway 变量添加 PISTON_API_KEY=你的key
```

> 没有 Piston Key：代码执行功能不可用，但 AI 辅导、学习路线、题库全部正常，足够 demo。

---

## 三、面试技术问题 Q&A

### 系统设计 / 架构

| 问题 | 回答要点 |
|------|---------|
| 整体架构是什么？ | React SPA → FastAPI async REST → PostgreSQL(pgvector) + Redis(可选)。Piston 作为隔离代码执行沙箱（Docker容器，网络隔离，3秒超时，128MB内存限制） |
| 为什么选 FastAPI 而不是 Django/Flask？ | 原生 async/await 支持高并发；Pydantic 自动数据验证；自动生成 OpenAPI 文档；startup latency 低于 Django |
| 数据库 schema 怎么设计的？ | `QuizQuestion`（starter_code JSONB per-language, test_cases JSONB array）；`KnowledgePoint`（article_content 文章）；`KnowledgeEmbedding`（pgvector 384维向量）；`CodeSubmission`（提交历史，ai_feedback JSON） |
| 如何防止 API 滥用？ | SlowAPI rate limiter：代码执行 10次/分钟，AI 聊天 20次/分钟；Piston 本身有内存+时间沙箱 |
| 如何保证代码执行安全？ | Piston 每次在独立 Docker 容器运行，禁止网络访问，3秒超时强制终止，128MB 内存上限，进程隔离 |
| JWT 认证怎么实现的？ | python-jose 生成 JWT，bcrypt 哈希密码，前端 axios 拦截器自动注入 Authorization header，401 自动跳转登录页 |

### RAG & AI Pipeline

| 问题 | 回答要点 |
|------|---------|
| RAG pipeline 怎么实现的？ | 文章按 500char/50overlap 分块 → `all-MiniLM-L6-v2`（384维）本地 embedding → pgvector 存储 → 用户提问时 cosine similarity 检索 top-3 chunks（score > 0.4）→ 注入 Gemini prompt |
| 为什么选 all-MiniLM-L6-v2？ | 90MB、推理快（~50ms）、384维够用、语义相似度 benchmark 优秀；相比 large model 减少 latency 和内存消耗 |
| 语义搜索如何实现？ | 对 query embed，与 pgvector 中所有 chunk 做 `1 - cosine_distance`，过滤 score < 0.4，返回 top-3；题目语义搜索则是 in-memory 对 89 道题描述做相似度 |
| 个性化上下文是怎么做的？ | 检索用户在当前题目的最近 3 次 CodeSubmission，格式化 "你之前 X/Y test cases 通过" 注入 system prompt，让 AI 基于用户历史调整建议 |
| 为什么 Gemini 2.5 Flash 而不是 GPT-4？ | 更快（Flash 低延迟设计）、免费额度更高、代码任务表现优异、API 简洁 |
| min_score=0.4 怎么定的？ | 实验调参：< 0.2 引入噪音，> 0.6 大部分查询无结果；0.4 在实际问题上平衡准确率和召回率 |
| pgvector vs Pinecone/Weaviate？ | pgvector 避免额外服务依赖，向量和业务数据在同一 PostgreSQL 事务中保持一致，< 1M chunks 性能完全够用；Pinecone 在 billion 级向量才有优势 |
| RAG 如何提升 AI 回答质量？ | 没有 RAG 时 AI 会给通用答案；有 RAG 后 AI 能说"根据我们 Sliding Window 文章中的 Template 3..."，答案锚定在课程内容，减少幻觉 |

### 前端 / 代码执行

| 问题 | 回答要点 |
|------|---------|
| 代码编辑器怎么做的？ | Monaco Editor（VS Code 同款引擎），动态加载题目 starter code，支持 Python/JS/Java/C++ 语法高亮 |
| starter code 为什么包含 stdin 框架？ | Piston 通过 stdin/stdout 通信，需要把 JSON 格式的 test input 解析成函数参数，调用 Solution 方法，输出结果到 stdout 与 expected 比对 |
| 遇到的最大技术问题？ | 三个：① Piston timeout 配置（自建实例限制 3秒，发 5000ms 返回 400）；② 数据库重复数据（3套 init scripts 各跑一次），API 层去重解决；③ pgvector JSON operator 类型不匹配导致 SQL 错误 |

### Scaling & Trade-offs

| 问题 | 回答要点 |
|------|---------|
| 如何 scale？ | 代码执行：横向扩展 Piston 节点 + 请求队列；AI：缓存相同题目的 RAG context；DB：读写分离，向量索引用 HNSW（O(log n) query）|
| 如果 QPS 到 1000，bottleneck 在哪？ | ① sentence-transformers embedding 是 CPU bound，需要 GPU 或批处理；② Gemini API rate limit；③ Piston Docker 启动时间（可用容器池预热）|
| embedding 模型能换成更好的吗？ | 可以，接口抽象好了，换 `text-embedding-3-small`（OpenAI，1536维）只需改 `get_embedding_model()`，但要重新 index；需要权衡 latency vs 质量 |

---

## 四、简历 Bullets（按职位类型）

### SDE / Software Engineer

```
AlgoMentor — AI-Powered Coding Interview Platform                [github.com/...]
• Built full-stack coding practice platform: React + FastAPI + PostgreSQL (pgvector),
  with Monaco Editor, JWT auth, and isolated code execution via Piston Docker sandbox
• Designed RAG pipeline: chunked 13 algorithm articles → sentence-transformers
  (all-MiniLM-L6-v2, 384-dim) → pgvector cosine search → Gemini 2.5 Flash prompt
  injection; grounds AI responses in curriculum material to reduce hallucinations
• Implemented semantic problem search using in-memory embedding similarity across
  89 LeetCode problems; returns relevance-ranked results in < 200ms
• Built rate-limited REST API (SlowAPI: 10 req/min execution, 20 req/min AI chat)
  with personalized context injection from user submission history
```

### ML / AI Engineer

```
AlgoMentor — RAG-Enhanced AI Coding Tutor                        [github.com/...]
• Designed end-to-end RAG pipeline: overlapping-chunk text splitting (500-char/50-
  overlap) → local embedding with all-MiniLM-L6-v2 (384-dim) → pgvector cosine
  similarity retrieval → context-augmented generation with Gemini 2.5 Flash
• Built personalized tutoring context: injected user's historical submission outcomes
  (pass rate, language, timestamps) into LLM prompts for adaptive, user-aware hints
• Implemented semantic problem recommendation via embedding cosine similarity across
  89 problem descriptions; achieved 0.6+ relevance scores on domain-specific queries
  (e.g., "sliding window substring" → LeetCode 3, 76, 424)
• Integrated multi-turn AI chat with RAG source attribution (shows which knowledge
  article was referenced) and failure-mode analysis triggered by test case outcomes
```

### Product Manager

```
AlgoMentor — AI Coding Interview Prep Platform (Solo-Built)      [github.com/...]
• Identified gap in interview prep tools lacking personalized AI feedback; designed
  and shipped full platform in 3 weeks covering 89 LeetCode problems across 13 topics
• Shipped RAG-powered AI tutor grounding hints in course materials (patterns,
  templates) instead of generic responses; added source attribution for transparency
• Defined 3-tier hint system (Strategy → Code → Video) to scaffold learning without
  spoiling solutions; tracked submission history to personalize subsequent hints
• Built measurable progress tracking: test case pass rate per submission, per-topic
  assessments, personalized learning plan generation based on weak area detection
```

### Data Engineering / Backend-focused

```
AlgoMentor — Knowledge Base & Semantic Search System             [github.com/...]
• Built async FastAPI backend with PostgreSQL + pgvector; designed normalized schema
  for quiz questions (test_cases JSONB), vector embeddings, and submission history
• Implemented batch embedding pipeline: 13 knowledge articles → 103 chunks →
  384-dim vectors in pgvector; re-indexed via admin endpoint POST /api/rag/index/all
• Resolved production data quality: 267 DB rows deduped to 89 unique problems via
  API-layer deduplication (prefer record with populated test_cases JSONB array)
• Deployed rate-limiting backed by Redis with in-memory fallback; designed for
  horizontal scaling via stateless service + external session store pattern
```

---

## 五、一句话 Pitch（面试开场用）

> "I built **AlgoMentor**, a full-stack AI coding tutor. The core technical contribution is a RAG pipeline — I chunk algorithm articles, embed them with sentence-transformers, store in pgvector, and retrieve relevant context to ground Gemini's responses in the actual curriculum. Users can solve 89 LeetCode problems in a Monaco editor with isolated Docker-based code execution, get personalized AI hints based on their submission history, and find problems via semantic search. Stack: FastAPI + React + PostgreSQL + pgvector + Gemini 2.5 Flash."

---

## 六、Hint 系统改进方向（下一步规划）

### 现状问题
- 静态预设 hint，不知道用户卡在哪里
- 3 级跳跃太大（strategy → 完整代码，没有中间过渡）
- 完全不利用已有的 AI + RAG 能力

### 改进方案

#### 方案 A：AI Dynamic Hints（高优先级）
```
POST /api/ai/hint
{
  "question_id": 6,
  "code": "用户当前代码",
  "test_results": [...],   // 哪些 case 失败了
  "hint_level": 1          // 1=苏格拉底提问 2=方向提示 3=伪代码
}
```
- Level 1：只问一个引导性问题（苏格拉底式）
- Level 2：指出问题方向，不给代码
- Level 3：伪代码框架，有 TODO 注释

#### 方案 B：5 级渐进式揭示

| Level | 名称 | 内容 | 摩擦感 |
|-------|------|------|--------|
| 1 | Nudge | 一句引导问题 | 无 |
| 2 | Pattern | 指出算法模式名称 | 无 |
| 3 | Approach | 伪代码步骤 | 需点击确认 |
| 4 | Scaffold | 有 TODO 的代码框架 | 高摩擦 |
| 5 | Solution | 完整代码 | "提交不计分" 警告 |

#### 方案 C：RAG 增强 Hint
- Hint 生成时检索相关 knowledge article
- AI 能说"这道题用 Sliding Window 模式，你看过我们的 Sliding Window 文章里 Template 3 吗？"

---

*生成时间：2026-02-23 | AlgoMentor Project*

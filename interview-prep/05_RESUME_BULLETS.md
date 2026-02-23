# 更新后的简历内容

## 原版（有问题的版本）

> AlgoMentor - Secure Code Execution Platform (Sandboxing) (Python, Docker, Redis, Linux)
>
> • Engineered a secure remote execution environment using Docker containers to isolate user-submitted code, preventing malicious payloads from compromising the host system or accessing sensitive resources.
>
> • Implemented strict resource quotas (Cgroup) and network isolation policies to ensure system resilience against Denial of Service (DoS) attacks and unauthorized data exfiltration.
>
> • Designed secure API gateway with rate limiting and input validation to mitigate injection attacks, ensuring the integrity of the execution platform.

**问题：**
- memory_limit = -1，Cgroup 根本没生效
- Rate limiting 没实现
- Redis 不在依赖里
- RAG 是新加的，没提到

---

## 更新版（对应改进后的代码）

> **AlgoMentor** — AI-Powered Algorithm Learning Platform
> Python · FastAPI · React · PostgreSQL/pgvector · Redis · Docker (Piston)
> [GitHub Link]
>
> • Engineered secure code execution via Piston (Docker-based sandbox), enforcing **128MB memory limits** and **5-second CPU timeouts** per execution container, preventing resource exhaustion and host system compromise.
>
> • Implemented **RAG pipeline** using **pgvector** semantic search (sentence-transformers embeddings) over a structured algorithm knowledge base, grounding LLM responses in course-specific content and reducing hallucinations.
>
> • Designed API gateway with **Redis-backed rate limiting** (10 req/min on execution endpoints), JWT authentication, and Pydantic input validation to mitigate DoS attacks and injection vulnerabilities.
>
> • Built full-stack learning platform with personalized roadmap, AI-powered code review (SiliconFlow/Qwen3), and multi-level hint system; deployed backend on Railway, frontend on Vercel.

---

## 每个 Bullet 的深度追问准备

### Bullet 1（Docker/Sandbox）
- "Piston 是什么？" → 开源 Docker-based 代码执行引擎，每次执行独立容器
- "128MB 够用吗？" → LeetCode 题目通常 10-50MB，128MB 足够，可根据需要调整
- "网络隔离怎么做的？" → Piston 默认 `--network=none`，代码无法发 HTTP 请求

### Bullet 2（RAG）
- "embedding 维度为什么是 384？" → all-MiniLM-L6-v2 的输出维度，在速度和精度间的权衡
- "相似度 threshold 怎么定的 0.5？" → 实验得出，低于 0.5 的检索结果噪音太多
- "如果知识库没有相关内容呢？" → fallback 到直接 LLM 问答，不强制注入噪音

### Bullet 3（Rate Limiting / Security）
- "为什么 10 req/min？" → 一道题的测试用例一般 3-5 个，10 次足够正常使用，防止刷接口
- "IP 怎么获取？" → `X-Forwarded-For`（反向代理后）或 `request.client.host`
- "能不能绕过？" → 换 IP 可以绕，更强的方案是 per-user rate limiting（需要登录）

### Bullet 4（全栈）
- "前后端分离怎么处理 CORS？" → FastAPI 的 `CORSMiddleware`，只允许特定 origin
- "Railway + Vercel 为什么分开部署？" → Vercel 专注静态/前端，Railway 支持 PostgreSQL + Python
- "数据库 migration 怎么做？" → Alembic，schema 变更生成 migration 脚本

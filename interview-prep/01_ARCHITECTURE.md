# AlgoMentor 系统架构

## 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  HomePage │ RoadmapPage │ LearningPage │ CodeCheckPage   │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend                          │
│                                                           │
│  /api/auth     /api/knowledge  /api/quiz                 │
│  /api/execute  /api/ai         /api/rag  (NEW)           │
│                                                           │
│  ┌──────────┐ ┌────────────┐ ┌─────────────────────┐    │
│  │   Auth   │ │    Code    │ │     AI Service       │    │
│  │ Service  │ │  Executor  │ │  SiliconFlow LLM     │    │
│  │JWT+bcrypt│ │Piston API  │ │+ RAG retrieval (NEW) │    │
│  └──────────┘ └─────┬──────┘ └──────────┬──────────┘    │
└────────────────────────────────────────────────────────-─┘
               │                          │
    ┌──────────▼──────┐       ┌──────────▼──────────────┐
    │  Piston API     │       │   PostgreSQL + pgvector  │
    │(Docker-based    │       │  - users                 │
    │ sandbox, ext.)  │       │  - knowledge_points      │
    └─────────────────┘       │  - knowledge_embeddings  │
                              │  - quiz_questions        │
    ┌─────────────────┐       │  - code_submissions      │
    │  Redis (NEW)    │       └──────────────────────────┘
    │  Rate limiting  │
    └─────────────────┘
```

## 关键技术选型理由

### FastAPI (Python)
- 原生 async/await，适合 IO 密集型任务（DB 查询 + 外部 API 调用）
- Pydantic 自动做 request validation，防 injection
- OpenAPI docs 自动生成

### PostgreSQL + pgvector（而不是独立 vector DB）
- 不需要额外维护 Pinecone/Weaviate 等服务
- 向量搜索和关系查询可以在同一个事务里完成
- 余弦相似度查询：`embedding <=> query_embedding ORDER BY LIMIT 3`

### Piston API（代码执行）
- 开源项目（github.com/engineer-man/piston），本身基于 Docker
- 每次执行在独立容器里，执行完销毁
- 支持 compile_timeout / run_timeout / memory_limit 参数
- 生产部署：self-hosted Piston 实例，不依赖公共 API

### sentence-transformers（Embedding 模型）
- `all-MiniLM-L6-v2`：384 维，本地运行，速度快
- 不需要调用外部 embedding API（省钱，无延迟）
- 适合语义相似度搜索

### Redis（Rate Limiting）
- SlowAPI（FastAPI 的 rate limiting 库）用 Redis 存计数器
- key = IP 地址，TTL = 60秒
- 没有 Redis 时自动降级到内存存储

---

## 数据流：用户提问 AI（RAG 流程）

```
用户发送聊天消息
        │
        ▼
1. 将用户问题用 sentence-transformers 转成 embedding
        │
        ▼
2. pgvector 余弦相似度搜索 knowledge_embeddings 表
   SELECT chunk_text, 1-(embedding<=>query) AS score
   WHERE knowledge_point_id = ? ORDER BY score LIMIT 3
        │
        ▼
3. 将检索到的 top-3 文章片段拼成 context
        │
        ▼
4. 构造 prompt：
   system: "基于以下课程资料回答..."
   context: [检索到的文章片段]
   user: 原始问题
        │
        ▼
5. 调用 SiliconFlow API（Qwen3-30B）
        │
        ▼
6. 返回 AI 回答 + sources（来自哪个知识点）
```

---

## 数据流：代码执行（安全执行）

```
用户提交代码
        │
        ▼
1. FastAPI 做输入验证（code 非空，language 在白名单内）
        │
        ▼
2. Rate limiter 检查（10次/分钟/IP，Redis 计数）
        │
        ▼
3. 发送到 Piston API：
   - run_timeout: 5000ms（5秒）
   - compile_timeout: 10000ms
   - run_memory_limit: 128MB
        │
        ▼
4. Piston 在 Docker 容器内执行，网络隔离
        │
        ▼
5. 解析结果，对比 expected output
        │
        ▼
6. 保存 submission（如果用户已登录）
        │
        ▼
7. 如果失败，自动调用 AI 分析失败原因
```

---

## 安全设计

| 威胁 | 防护措施 |
|------|---------|
| 恶意代码执行 | Piston Docker 沙箱，网络隔离，5秒超时 |
| DoS / 资源耗尽 | 128MB 内存限制，5秒 CPU 限制，Rate limiting |
| SQL 注入 | SQLAlchemy ORM 参数化查询 |
| JWT 伪造 | HS256 签名，SECRET_KEY 从环境变量读取 |
| 用户数据泄露 | 需要认证才能访问提交历史（修复后） |
| 密码泄露 | bcrypt hash，72字节截断处理 |

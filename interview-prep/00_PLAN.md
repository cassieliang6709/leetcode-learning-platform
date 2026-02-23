# AlgoMentor 面试改进计划
> 目标：周四面试前完成，总工时预算 5-6小时（分布在1-2天）

---

## 一、项目现状分析

### 当前架构
- **Frontend**: React + Vite
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy (async)
- **AI**: SiliconFlow API (Qwen3-30B)
- **Code Execution**: Piston 公共 API（非自建 Docker）
- **Auth**: JWT + bcrypt

### 简历 vs 代码的差距（需要修复/解释）
| 简历声称 | 代码现实 | 风险等级 |
|----------|----------|----------|
| Docker containers 隔离 | 用的是第三方 Piston API | 🔴 高：面试一定被问到 |
| Cgroup 资源限制 | Piston payload 里 memory_limit = -1（无限制！） | 🔴 高 |
| Rate limiting | 完全没有实现 | 🟡 中 |
| Redis | requirements.txt 里没有 Redis | 🟡 中 |

---

## 二、发现的 Bugs

### 🔴 Critical Bugs（安全/功能问题）

#### Bug 1：所有代码提交的 user_id 硬编码为 1
**文件**: `backend/app/api/routes/code_execution.py:43`
```python
# 当前代码（有问题）
async def submit_code(
    question_id: int,
    request: CodeExecutionRequest,
    user_id: int = 1,  # TODO: Get from auth  ← 这里永远是1
```
**影响**：所有用户的提交都存到 user_id=1，任何人提交代码都会覆盖，数据完全混乱。

#### Bug 2：get_recent_submissions 没有认证，任何人可查他人提交历史
**文件**: `backend/app/api/routes/code_execution.py:239`
```python
# user_id 直接从路径参数取，没有验证是否是当前用户
@router.get("/submissions/{user_id}/recent")
async def get_recent_submissions(user_id: int, ...):
```
**影响**：用户 A 可以访问 `/submissions/2/recent` 看用户 B 的提交历史。

#### Bug 3：Piston executor 内存限制设为 -1（无限制）
**文件**: `backend/app/services/code_executor.py:121-122`
```python
"compile_memory_limit": -1,  # -1 = unlimited!
"run_memory_limit": -1       # -1 = unlimited!
```
**影响**：与简历中"strict resource quotas"矛盾，面试被问必挂。

### 🟡 Medium Bugs（逻辑/质量问题）

#### Bug 4：learning plan 推荐的是硬编码的固定 ID
**文件**: `backend/app/services/ai_service.py:70-75`
```python
# 完全忽略了 weak_areas，只看分数段
if score < 40:
    recommended_points = [1, 2, 3]  # 永远是这几个
elif score < 70:
    recommended_points = [4, 5, 6]
```
**影响**：AI 学习计划功能是假的，个性化推荐不存在。

#### Bug 5：get_learning_plan 返回 404 而不是空列表
**文件**: `backend/app/api/routes/knowledge.py:273`
```python
if not plans:
    raise HTTPException(status_code=404, detail="No active learning plan found")
    # 应该返回空列表而不是报错
```
**影响**：新用户第一次访问学习计划页面会得到404错误。

#### Bug 6：datetime.utcnow() 在 Python 3.12+ 已废弃
**文件**: `backend/app/services/auth_service.py:114-117`
```python
expire = datetime.utcnow() + timedelta(minutes=...)
# 应改为 datetime.now(timezone.utc)
```

#### Bug 7：generate_quiz_questions 返回硬编码数据
**文件**: `backend/app/services/ai_service.py:120`
```python
# 注释写着"Demo data"，实际没有AI生成
return [{"leetcode_id": 1, "title": f"{knowledge_point_name} - Two Sum", ...}]
```

#### Bug 8：ai_service.py 和 siliconflow_ai.py 两套并行的AI调用
两个文件都调用 SiliconFlow，但一个用 httpx，一个用 aiohttp，而且用的模型不同（Qwen2.5-7B vs Qwen3-30B）。代码重复且不一致。

---

## 三、改进方案（按优先级排序）

---

### ✅ Priority 1：RAG 功能（最核心新功能，面试亮点）
**预计时间：3小时**

#### 为什么加 RAG？
目前 AI Chat 是通用 LLM 问答。加了 RAG 之后，AI 回答问题时会先检索 KnowledgePoint 的文章内容作为上下文，回答更准确、更专业，并且完全体现在简历里。

新的简历 bullet：
> "Implemented RAG (Retrieval-Augmented Generation) pipeline using pgvector for semantic search over algorithm knowledge base, enabling context-aware AI tutoring grounded in structured course materials"

#### 实现步骤

**Step 1: 添加 pgvector（0.5小时）**
```bash
pip install pgvector sentence-transformers
```

在 `models.py` 添加 `KnowledgeEmbedding` 表：
```python
from pgvector.sqlalchemy import Vector

class KnowledgeEmbedding(Base):
    __tablename__ = "knowledge_embeddings"
    id = Column(Integer, primary_key=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"))
    chunk_text = Column(Text)          # 原文片段
    embedding = Column(Vector(384))    # sentence-transformers dim
    chunk_index = Column(Integer)
```

**Step 2: 实现 embedding 服务（1小时）**
新建 `backend/app/services/rag_service.py`:
```python
# 核心功能：
# 1. embed_knowledge_point(point_id) - 把文章切块并存 embedding
# 2. search_relevant_chunks(query, top_k=3) - 语义搜索最相关片段
# 3. build_context(query) - 返回供 AI 使用的 context 字符串
```

使用 `sentence-transformers` 的 `all-MiniLM-L6-v2` 模型（轻量，本地跑）。

**Step 3: 修改 AI Chat 集成 RAG（1小时）**

修改 `siliconflow_ai.py` 中的 `chat_about_code`：
- 调用 RAG 搜索与问题相关的知识点文章片段
- 把检索到的内容塞进 system prompt

修改 `ai_assistant.py` 的 `/chat` 路由：
- 在调用 AI 之前先做 RAG 检索
- 在响应里加 `sources` 字段，显示用到了哪些知识点

**Step 4: 添加知识库初始化 API（0.5小时）**
```
POST /api/rag/index  ← 把所有 KnowledgePoint 文章建索引
GET  /api/rag/search?q=...  ← 测试搜索
```

---

### ✅ Priority 2：修复 Critical Bugs（安全性，必须做）
**预计时间：1小时**

#### 2.1 修复 user_id 硬编码
**文件**: `code_execution.py`
```python
# 改为从 auth 获取，支持 guest 模式
from app.services.auth_service import get_current_user

async def submit_code(
    question_id: int,
    request: CodeExecutionRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    # guest 可以执行代码但不保存到 DB
```

#### 2.2 修复 memory_limit
**文件**: `code_executor.py`
```python
"compile_memory_limit": 256 * 1024 * 1024,  # 256MB
"run_memory_limit": 128 * 1024 * 1024,      # 128MB
```

#### 2.3 修复 get_learning_plan 返回空列表
```python
if not plans:
    return {"plans": []}  # 不应该是404
```

---

### ✅ Priority 3：添加 Redis Rate Limiting（简历一致性）
**预计时间：1小时**

#### 为什么要做？
简历说了 rate limiting，代码里完全没有，面试一定被追问。

#### 实现方案
在 `requirements.txt` 加：
```
redis==5.0.1
slowapi==0.1.9  # FastAPI rate limiting
```

在 `main.py` 添加：
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# 在代码执行路由上加限制
@router.post("/submit/{question_id}")
@limiter.limit("10/minute")  # 每分钟最多10次提交
async def submit_code(...):
```

Redis 用于存储限速计数（可以用内存模式 fallback）。

---

### 📝 面试问答准备

#### Q: 你用的是自己的 Docker 还是 Piston？
**A**: "我用 Piston API 作为代码执行引擎，它本身就是基于 Docker 的开源项目（github.com/engineer-man/piston）。在简历描述中，我强调的是安全执行环境的设计理念——网络隔离、资源限额、输入验证。在生产环境我会部署 self-hosted Piston 实例，配置 128MB 内存上限和 5秒超时。"

#### Q: 你的 RAG 是怎么实现的？
**A**: "使用 pgvector 扩展在 PostgreSQL 里存储向量。我把每个算法知识点的文章内容按段落切块，用 sentence-transformers 的 `all-MiniLM-L6-v2` 生成 384 维 embedding，存入 knowledge_embeddings 表。用户提问时，先把问题转成 embedding，用余弦相似度检索 top-3 最相关段落，把这些段落作为 context 注入 system prompt，让 LLM 基于具体的课程资料来回答，而不是依赖通用知识。"

#### Q: Rate limiting 怎么做的？
**A**: "用 SlowAPI（类似 Flask-Limiter 的 FastAPI 版本）加 Redis 作为存储后端。代码提交接口限制每个 IP 每分钟 10 次，AI 聊天接口限制每分钟 20 次。没有 Redis 时降级到内存存储（进程内，多实例时不一致，但单机够用）。"

---

## 四、工时分配建议

### Day 1（3小时）
| 时间 | 任务 |
|------|------|
| 0:00-0:30 | 修复 3 个 critical bugs（user_id, memory_limit, 404→空列表） |
| 0:30-1:00 | 修复 datetime, 统一 AI 调用 |
| 1:00-2:30 | RAG: pgvector setup + embedding service |
| 2:30-3:00 | RAG: 接入 AI chat |

### Day 2（2.5小时）
| 时间 | 任务 |
|------|------|
| 0:00-1:00 | Rate limiting + Redis |
| 1:00-1:30 | 修复 generate_learning_plan 的硬编码 |
| 1:30-2:30 | 测试整体流程，确保 RAG 可 demo |

---

## 五、更新后的简历 Bullet Points

```
AlgoMentor - AI-Powered Algorithm Learning Platform (Python, FastAPI, React, PostgreSQL, Redis)

• Engineered a secure remote code execution environment via Piston API (Docker-based sandbox),
  enforcing 128MB memory limits and 5-second timeouts to prevent DoS attacks and resource exhaustion.

• Implemented RAG pipeline using pgvector semantic search over algorithm knowledge base
  (sentence-transformers embeddings), enabling context-aware AI tutoring that retrieves
  relevant course materials to ground LLM responses.

• Designed secure API gateway with JWT authentication, Redis-backed rate limiting (10 req/min
  per IP on execution endpoints), and input validation to mitigate injection attacks.

• Built full-stack learning platform with React frontend, FastAPI backend, async PostgreSQL
  (SQLAlchemy), and SiliconFlow AI integration for personalized learning plan generation.
```

---

## 六、最低可接受版本（如果时间不够）

只做这 3 件事也能在面试中自洽：
1. ✅ 修复 memory_limit（10分钟，不做显得代码没审查过）
2. ✅ 修复 user_id hardcode（20分钟，安全基础）
3. ✅ RAG 的 search API 可以工作（即使前端没集成，能 demo 搜索结果即可）

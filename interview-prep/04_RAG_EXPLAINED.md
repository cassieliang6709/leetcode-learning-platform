# RAG 功能详解

## 什么是 RAG？
RAG = Retrieval-Augmented Generation（检索增强生成）

**没有 RAG 的 AI Chat（原来）：**
```
用户："二叉树的 BFS 怎么实现？"
     ↓
LLM 凭借训练数据里的通用知识回答
     ↓
回答：通用的、可能和课程内容无关的解释
```

**有 RAG 的 AI Chat（现在）：**
```
用户："二叉树的 BFS 怎么实现？"
     ↓
1. 把问题转成 embedding 向量
     ↓
2. 在 knowledge_embeddings 表里用余弦相似度搜索
   找到最相关的 3 个课程文章片段（比如 BFS 那一节）
     ↓
3. 把这 3 个片段作为 context 传给 LLM：
   "基于以下课程资料回答：[BFS 文章内容...]"
     ↓
回答：基于课程内容、和学习路径一致的精准解释
     + 附上"参考资料：树的层序遍历 第2节"
```

---

## 数据库 Schema

```sql
-- pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 知识点文章的向量存储
CREATE TABLE knowledge_embeddings (
    id              SERIAL PRIMARY KEY,
    knowledge_point_id INTEGER REFERENCES knowledge_points(id),
    chunk_text      TEXT NOT NULL,       -- 原文片段（500字符）
    embedding       VECTOR(384),         -- all-MiniLM-L6-v2 的维度
    chunk_index     INTEGER NOT NULL,    -- 第几个片段
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 向量搜索索引（HNSW 算法，近似最近邻）
CREATE INDEX ON knowledge_embeddings
USING hnsw (embedding vector_cosine_ops);
```

---

## 核心代码逻辑

### 1. 文章切块（Chunking）
```python
def chunk_text(text: str, chunk_size=500, overlap=50) -> List[str]:
    """
    把长文章切成小块，相邻块有 overlap 防止边界信息丢失

    例：文章 1500 字
    → chunk 1: 字符 0-500
    → chunk 2: 字符 450-950   (overlap=50，从450开始)
    → chunk 3: 字符 900-1400
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

### 2. 生成并存储 Embedding
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

async def index_knowledge_point(point_id: int, db: AsyncSession):
    # 取文章内容
    point = await db.get(KnowledgePoint, point_id)

    # 切块
    chunks = chunk_text(point.article_content)

    # 批量生成 embedding（本地推理，不需要 API key）
    embeddings = model.encode(chunks)  # shape: (n_chunks, 384)

    # 存入数据库
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        db.add(KnowledgeEmbedding(
            knowledge_point_id=point_id,
            chunk_text=chunk,
            embedding=emb.tolist(),
            chunk_index=i
        ))
    await db.commit()
```

### 3. 语义搜索
```python
async def search_relevant_chunks(
    query: str,
    db: AsyncSession,
    knowledge_point_id: Optional[int] = None,
    top_k: int = 3
) -> List[Dict]:
    # 把查询转成 embedding
    query_embedding = model.encode([query])[0]

    # pgvector 余弦相似度搜索
    # <=> 是余弦距离（越小越相似），1-距离 = 相似度
    stmt = (
        select(
            KnowledgeEmbedding.chunk_text,
            KnowledgeEmbedding.knowledge_point_id,
            (1 - KnowledgeEmbedding.embedding.cosine_distance(query_embedding)).label("score")
        )
        .order_by(text("score DESC"))
        .limit(top_k)
    )
    if knowledge_point_id:
        stmt = stmt.where(KnowledgeEmbedding.knowledge_point_id == knowledge_point_id)

    results = await db.execute(stmt)
    return [
        {"text": r.chunk_text, "score": float(r.score), "point_id": r.knowledge_point_id}
        for r in results
        if r.score > 0.5  # 低相似度的过滤掉
    ]
```

### 4. 集成到 AI Chat
```python
async def chat_about_code(self, user_message, code, language, ...):
    # 1. RAG 检索
    relevant_chunks = await search_relevant_chunks(user_message, db)

    # 2. 构建 RAG context
    rag_context = ""
    if relevant_chunks:
        rag_context = "\n\n**Relevant Course Materials:**\n"
        for chunk in relevant_chunks:
            rag_context += f"---\n{chunk['text']}\n"

    # 3. 构建 messages（带 RAG context）
    messages = [
        {
            "role": "system",
            "content": f"""You are a programming tutor for AlgoMentor.

{rag_context}

Use the course materials above to ground your answer when relevant."""
        },
        {"role": "user", "content": user_message}
    ]

    # 4. 调用 LLM
    result = await self._make_request(messages)

    return {
        "response": result["content"],
        "sources": [c["point_id"] for c in relevant_chunks]  # 告诉前端引用了哪些知识点
    }
```

---

## API 端点

### 建立索引
```
POST /api/rag/index
Body: {"knowledge_point_id": 1}  # 单个知识点
POST /api/rag/index/all           # 全部重建
```

### 搜索测试
```
GET /api/rag/search?q=二叉树BFS&top_k=3
Response:
{
  "results": [
    {"text": "BFS 使用队列...", "score": 0.87, "knowledge_point": "树的遍历"},
    {"text": "层序遍历的时间复杂度...", "score": 0.76, "knowledge_point": "树的遍历"},
    {"text": "BFS vs DFS 的对比...", "score": 0.71, "knowledge_point": "图的搜索"}
  ]
}
```

---

## 面试中如何 Demo

1. 打开 Code Check 页面，选一道树的题目
2. 点击 AI Chat，输入"这道题该怎么思考？"
3. AI 返回的答案会引用课程里关于该算法的文章片段
4. 响应里有 `sources` 字段显示引用了哪个知识点
5. 对比：去掉 RAG 后 AI 给出的是通用回答，加了 RAG 后回答里有课程的具体例子

# AlgoMentor - 快速启动（面试演示）

## 前置条件
- Docker Desktop 运行中
- `SILICONFLOW_API_KEY` 已配置（否则 AI 进入 fallback 模式）

---

## 一键启动（推荐）

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 SILICONFLOW_API_KEY

# 2. 启动所有服务（首次需要 build，约 3-5 分钟）
docker compose up --build

# 3. 等待所有服务 healthy 后，安装 Piston 语言运行时（只需一次）
bash scripts/setup_piston.sh

# 4. 打开浏览器
# Frontend: http://localhost:5173  (需要单独 npm run dev)
# Backend API: http://localhost:8000/docs
```

---

## 服务状态确认

```bash
docker compose ps
# 所有服务应该显示 "healthy" 或 "running"

# 测试代码执行
curl http://localhost:2000/api/v2/runtimes | python3 -m json.tool

# 测试后端 API
curl http://localhost:8000/health

# 测试 RAG 搜索（先要有数据）
curl "http://localhost:8000/api/rag/search?q=binary+search"
```

---

## 各服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| PostgreSQL | 5432 | pgvector 数据库 |
| Redis | 6379 | Rate limiting 存储 |
| Piston | 2000 | Docker 代码执行沙箱 |
| Backend | 8000 | FastAPI (`/docs` 有 swagger UI) |
| Frontend | 5173 | React (需要单独 `npm run dev`) |

---

## 仅本地开发（不用 Docker）

```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # 编辑 .env
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

本地开发模式下代码执行使用公共 Piston API（不需要 Docker）。

---

## 面试演示脚本

1. `docker compose ps` → 展示所有服务 healthy
2. 打开 `/docs` → 展示 API 文档自动生成
3. 演示注册/登录
4. 演示代码执行 → "这里用 self-hosted Piston，运行在独立 Docker 容器里"
5. 演示 AI Chat → "用了 RAG，先从知识库检索相关文章段落再调 LLM"
6. `GET /api/rag/search?q=two+sum` → 展示向量搜索结果
7. `docker stats` → 展示容器资源使用

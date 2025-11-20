# 🚀 快速启动指南

## 前提条件

确保已安装：
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

## 一键启动（推荐）

```bash
# 1. 启动所有服务
./scripts/start_all.sh

# 2. 访问应用
# 前端: http://localhost:5173
# 后端: http://localhost:8000
# API文档: http://localhost:8000/docs

# 3. 停止所有服务
./scripts/stop_all.sh
```

## 分步启动

### 1. 准备数据库

```bash
# 确保 PostgreSQL 运行中
brew services start postgresql@14

# 创建数据库
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 初始化数据库
python3 scripts/init_db.py
```

### 2. 启动后端

```bash
# 方式1: 使用脚本（推荐）
./scripts/start_backend.sh

# 方式2: 手动启动
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. 启动前端

```bash
# 方式1: 使用脚本（推荐）
./scripts/start_frontend.sh

# 方式2: 手动启动
cd frontend
npm install
npm run dev
```

## 检查连接状态

```bash
./scripts/check_connection.sh
```

## 环境变量配置（可选）

```bash
# 复制环境变量模板
cp backend/env.template backend/.env

# 编辑配置
vi backend/.env
```

## 常见问题

### 端口被占用

```bash
# 查看并杀死占用端口的进程
lsof -ti:8000 | xargs kill -9  # 后端
lsof -ti:5173 | xargs kill -9  # 前端
```

### PostgreSQL 未运行

```bash
# 启动 PostgreSQL
brew services start postgresql@14

# 检查状态
brew services list
```

### Python 版本问题

```bash
# 使用 Python 3.12
brew install python@3.12
python3.12 -m venv venv
```

## 测试 API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取知识点列表
curl http://localhost:8000/api/knowledge/points

# 查看 API 文档
open http://localhost:8000/docs
```

## 项目结构

```
cs5001_project/
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/routes/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── main.py
├── frontend/         # React 前端
│   ├── src/
│   │   ├── pages/
│   │   └── services/api.js
│   └── package.json
└── scripts/          # 工具脚本
    ├── start_all.sh
    ├── start_backend.sh
    ├── start_frontend.sh
    ├── stop_all.sh
    ├── init_db.py
    └── check_connection.sh
```

## 下一步

1. 访问前端: http://localhost:5173
2. 完成知识测试
3. 获取个性化学习计划
4. 开始刷题！


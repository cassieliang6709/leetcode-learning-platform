# 🔗 前后端连接完整指南

## ✅ 连接状态总结

| 组件 | 地址 | 状态 | 说明 |
|------|------|------|------|
| 后端 API | http://localhost:8000 | ✅ 运行中 | FastAPI 服务 |
| API 文档 | http://localhost:8000/docs | ✅ 可访问 | Swagger UI |
| 前端应用 | http://localhost:5173 | 待启动 | React + Vite |
| 数据库 | localhost:5432 | ✅ 运行中 | PostgreSQL |

## 📋 已完成的配置

### 1. 后端配置 ✅

**CORS 设置** (`backend/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**API 路由**:
- ✅ `/api/knowledge/*` - 知识点管理
- ✅ `/api/quiz/*` - 题目和测试
- ✅ `/api/code/*` - 代码检查
- ✅ `/api/execute/*` - 代码执行

### 2. 前端配置 ✅

**API 客户端** (`frontend/src/services/api.js`):
```javascript
const API_BASE_URL = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

**已配置的 API 方法**:
- ✅ `getKnowledgePoints()` - 获取知识点
- ✅ `getQuizzesByKnowledge()` - 获取题目
- ✅ `checkCode()` - 代码检查
- ✅ `requestCodeHint()` - 获取提示

### 3. 数据库配置 ✅

**连接字符串** (`backend/app/database.py`):
```python
DATABASE_URL = postgresql+asyncpg://USER@localhost:5432/leetcode_learning
```

## 🚀 启动服务

### 方式 1: 一键启动（推荐）

```bash
./scripts/start_all.sh
```

### 方式 2: 分别启动

**终端 1 - 后端:**
```bash
./scripts/start_backend.sh
# 或手动: cd backend && source venv/bin/activate && uvicorn main:app --reload
```

**终端 2 - 前端:**
```bash
./scripts/start_frontend.sh
# 或手动: cd frontend && npm run dev
```

## 🧪 测试连接

### 方法 1: 使用测试脚本

```bash
./scripts/check_connection.sh
```

### 方法 2: 使用浏览器测试页面

```bash
# 在浏览器打开
open scripts/test_connection.html
```

### 方法 3: 手动测试 API

```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 获取知识点列表
curl http://localhost:8000/api/knowledge/points

# 3. 测试 CORS
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/knowledge/points -v
```

## 📊 API 端点列表

### Knowledge API (`/api/knowledge`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/points` | 获取所有知识点 |
| POST | `/test/{userId}` | 提交知识测试 |
| GET | `/plan/{userId}` | 获取学习计划 |

### Quiz API (`/api/quiz`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/by-knowledge/{knowledgePointId}` | 按知识点获取题目 |
| GET | `/{questionId}` | 获取题目详情 |
| POST | `/{questionId}/attempt/{userId}` | 提交答题记录 |
| GET | `/{questionId}/hint/{level}` | 获取提示 |

### Code API (`/api/code`)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/check/{userId}` | 检查代码 |
| POST | `/hint/{questionId}/{userId}` | 获取代码提示 |
| GET | `/submissions/{userId}` | 获取提交历史 |

### Execution API (`/api/execute`)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/run` | 运行代码 |

## 🔧 故障排查

### 问题 1: 前端无法访问后端

**症状**: 浏览器控制台显示 CORS 错误或网络错误

**解决方案**:
```bash
# 1. 确认后端运行
curl http://localhost:8000/health

# 2. 检查 CORS 配置
# 确保 backend/main.py 中包含前端地址

# 3. 重启后端
./scripts/stop_all.sh
./scripts/start_backend.sh
```

### 问题 2: 数据库连接失败

**症状**: 后端启动时报错 "database connection failed"

**解决方案**:
```bash
# 1. 检查 PostgreSQL 状态
brew services list

# 2. 启动 PostgreSQL
brew services start postgresql@14

# 3. 确认数据库存在
psql -l | grep leetcode_learning

# 4. 创建数据库（如果不存在）
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 5. 初始化数据库
python3 scripts/init_db.py
```

### 问题 3: 端口被占用

**症状**: "Address already in use" 错误

**解决方案**:
```bash
# 查找并杀死占用端口的进程
lsof -ti:8000 | xargs kill -9  # 后端
lsof -ti:5173 | xargs kill -9  # 前端
```

### 问题 4: Python 版本不兼容

**症状**: "asyncpg" 安装失败或运行错误

**解决方案**:
```bash
# 使用 Python 3.12
brew install python@3.12
cd backend
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📦 依赖检查

### 后端依赖
```bash
cd backend
source venv/bin/activate
pip list | grep -E "fastapi|uvicorn|sqlalchemy|asyncpg"
```

### 前端依赖
```bash
cd frontend
npm list | grep -E "react|axios|vite"
```

## 🎯 验证连接成功

当一切正常时，你应该能够：

1. ✅ 访问 http://localhost:8000/docs 查看 API 文档
2. ✅ 访问 http://localhost:5173 看到前端界面
3. ✅ 在前端点击 "Roadmap" 能够加载知识点列表
4. ✅ 浏览器控制台无 CORS 错误
5. ✅ 后端日志显示来自前端的请求

## 📞 获取帮助

如果以上步骤都无法解决问题:

1. 查看后端日志: 检查终端输出
2. 查看前端日志: 打开浏览器控制台 (F12)
3. 检查网络请求: 浏览器开发者工具 -> Network
4. 运行完整检查: `./scripts/check_connection.sh`

## 🎉 下一步

连接成功后，你可以：

1. 访问首页完成知识测试
2. 查看个性化学习路径
3. 在 Roadmap 中浏览知识点
4. 在 Code Check 页面提交代码
5. 使用 API 文档测试所有端点

---

**创建时间**: 2025-11-20  
**项目**: LeetCode Learning Platform  
**状态**: ✅ 后端运行中 | ⏳ 前端待启动


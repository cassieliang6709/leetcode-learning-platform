# 📜 Scripts 目录说明

这个目录包含了所有用于启动、测试和管理 LeetCode Learning Platform 的脚本。

## 📁 文件列表

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `start_all.sh` | Shell | 🚀 一键启动前后端 |
| `start_backend.sh` | Shell | 🔧 启动后端服务 |
| `start_frontend.sh` | Shell | 🎨 启动前端服务 |
| `stop_all.sh` | Shell | 🛑 停止所有服务 |
| `check_connection.sh` | Shell | 🔍 检查连接状态 |
| `init_db.py` | Python | 📊 初始化数据库 |
| `test_connection.html` | HTML | 🧪 浏览器连接测试 |

## 🚀 快速开始

### 一键启动（推荐）

```bash
./scripts/start_all.sh
```

这个命令会：
1. 检查 PostgreSQL 状态
2. 确认数据库存在
3. 启动后端服务 (localhost:8000)
4. 启动前端服务 (localhost:5173)

### 单独启动

**只启动后端**:
```bash
./scripts/start_backend.sh
```

**只启动前端**:
```bash
./scripts/start_frontend.sh
```

## 🔍 检查和测试

### 检查服务状态

```bash
./scripts/check_connection.sh
```

输出示例:
```
✅ 后端运行正常
✅ 前端运行正常
✅ PostgreSQL 运行正常
✅ 数据库 'leetcode_learning' 存在
```

### 浏览器测试

```bash
# macOS
open scripts/test_connection.html

# Linux
xdg-open scripts/test_connection.html
```

## 🛑 停止服务

```bash
./scripts/stop_all.sh
```

或手动停止:
```bash
# 杀死端口占用
lsof -ti:8000 | xargs kill -9  # 后端
lsof -ti:5173 | xargs kill -9  # 前端
```

## 📊 数据库管理

### 初始化数据库

```bash
python3 scripts/init_db.py
```

这个脚本会：
1. 创建所有数据库表
2. 插入 9 个知识点
3. 创建示例题目

### 创建数据库

```bash
psql -d postgres -c "CREATE DATABASE leetcode_learning;"
```

## 🔧 脚本详情

### start_all.sh

**功能**:
- 检查 PostgreSQL 服务
- 创建数据库（如不存在）
- 启动后端（后台运行）
- 等待后端就绪
- 启动前端

**输出**:
```
🚀 启动 LeetCode Learning Platform...
📊 检查 PostgreSQL 服务...
✅ PostgreSQL 运行中
🔧 启动后端服务...
✅ 后端启动成功 (PID: 12345)
⏳ 等待后端就绪...
✅ 后端就绪
🎨 启动前端服务...
✅ 前端启动成功 (PID: 12346)

========================================
🎉 启动完成！
========================================

📱 前端地址: http://localhost:5173
🔧 后端地址: http://localhost:8000
📚 API 文档: http://localhost:8000/docs

停止服务: ./scripts/stop_all.sh
```

### start_backend.sh

**功能**:
- 检查/创建虚拟环境
- 安装 Python 依赖
- 启动 FastAPI 服务

**端口**: 8000

### start_frontend.sh

**功能**:
- 检查/安装 Node.js 依赖
- 启动 Vite 开发服务器

**端口**: 5173

### stop_all.sh

**功能**:
- 读取保存的进程 PID
- 优雅地停止后端和前端
- 清理 PID 文件
- 备用: 强制杀死端口占用进程

### check_connection.sh

**功能**:
- 检查后端健康状态
- 检查前端是否响应
- 检查 PostgreSQL 服务
- 验证数据库存在
- 显示快速启动命令

### init_db.py

**功能**:
- 创建所有数据库表
- 插入基础数据:
  - 9 个知识点（Array、Hash Table、Two Pointers 等）
  - 示例题目（Two Sum、Valid Anagram）
- 跳过已存在的数据

**使用**:
```bash
python3 scripts/init_db.py
```

### test_connection.html

**功能**:
- 浏览器内连接测试
- 后端健康检查
- API 数据获取测试
- CORS 跨域验证
- 实时显示测试结果

**使用**:
```bash
open scripts/test_connection.html
```

## 🎯 常见使用场景

### 场景 1: 首次设置

```bash
# 1. 创建数据库
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 2. 初始化数据
python3 scripts/init_db.py

# 3. 启动服务
./scripts/start_all.sh
```

### 场景 2: 日常开发

```bash
# 启动
./scripts/start_all.sh

# 开发中...

# 停止
./scripts/stop_all.sh
```

### 场景 3: 调试后端

```bash
# 只启动后端，查看详细日志
./scripts/start_backend.sh
```

### 场景 4: 测试前端

```bash
# 确保后端运行
curl http://localhost:8000/health

# 启动前端
./scripts/start_frontend.sh
```

### 场景 5: 验证连接

```bash
# 命令行检查
./scripts/check_connection.sh

# 或浏览器测试
open scripts/test_connection.html
```

## ⚠️ 注意事项

1. **执行权限**: 所有 `.sh` 文件都有执行权限 (`chmod +x`)
2. **Python 版本**: 推荐使用 Python 3.12
3. **Node.js 版本**: 推荐使用 Node.js 18+
4. **PostgreSQL**: 必须运行在 localhost:5432
5. **端口占用**: 确保 8000 和 5173 端口未被占用

## 🔧 自定义配置

### 修改端口

**后端端口** (编辑 `start_backend.sh`):
```bash
uvicorn main:app --reload --port 8000  # 改为其他端口
```

**前端端口** (编辑 `frontend/vite.config.js`):
```javascript
server: {
  port: 5173  // 改为其他端口
}
```

### 修改数据库

编辑 `backend/.env`:
```
DATABASE_URL=postgresql+asyncpg://USER@localhost:5432/YOUR_DATABASE
```

## 📞 故障排查

### 问题: 脚本无法执行

```bash
# 添加执行权限
chmod +x scripts/*.sh
```

### 问题: Python 找不到模块

```bash
# 确保在虚拟环境中
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 问题: 端口被占用

```bash
# 查看端口占用
lsof -i :8000
lsof -i :5173

# 杀死进程
./scripts/stop_all.sh
```

## 📚 相关文档

- [QUICKSTART.md](../QUICKSTART.md) - 快速启动指南
- [CONNECTION_GUIDE.md](../CONNECTION_GUIDE.md) - 连接详细说明
- [readme.md](../readme.md) - 项目总览

---

**维护**: 定期更新脚本以适应项目变化  
**贡献**: 欢迎提交改进建议


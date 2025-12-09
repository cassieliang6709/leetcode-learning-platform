# 🚀 从这里开始

欢迎使用 **AlgoMentor**！

## ⚡ 最快启动方式（推荐）

```bash
# 一键启动所有服务
./scripts/start_all.sh
```

然后访问:
- 📱 前端: http://localhost:5173
- 🔧 后端: http://localhost:8000
- 📚 API 文档: http://localhost:8000/docs

## ✅ 快速检查清单

### 1. 前置要求

- [ ] Python 3.12+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] PostgreSQL 14+ 已安装并运行

```bash
# 检查版本
python3 --version
node --version
psql --version

# 启动 PostgreSQL（如未运行）
brew services start postgresql@14
```

### 2. 数据库设置（首次）

```bash
# 创建数据库
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 初始化数据
python3 scripts/init_db.py
```

### 3. 启动应用

```bash
# 一键启动
./scripts/start_all.sh
```

### 4. 验证连接

```bash
# 方式 1: 命令行
./scripts/check_connection.sh

# 方式 2: 浏览器
open scripts/test_connection.html
```

## 📋 详细文档

如果遇到问题，查看这些文档：

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 详细启动步骤 |
| [CONNECTION_GUIDE.md](CONNECTION_GUIDE.md) | 连接配置详解 |
| [FRONTEND_BACKEND_CONNECTION_COMPLETE.md](FRONTEND_BACKEND_CONNECTION_COMPLETE.md) | 连接验证报告 |
| [scripts/README.md](scripts/README.md) | 脚本使用说明 |

## 🎯 功能快览

1. **知识测试** - 评估你的算法基础
2. **学习路径** - AI 生成个性化计划
3. **题目练习** - 9 大类算法题目
4. **多级提示** - 策略 → 代码 → 视频
5. **代码检查** - AI 代码审查反馈

## 🔧 常用命令

```bash
# 启动所有服务
./scripts/start_all.sh

# 只启动后端
./scripts/start_backend.sh

# 只启动前端
./scripts/start_frontend.sh

# 停止所有服务
./scripts/stop_all.sh

# 检查连接状态
./scripts/check_connection.sh

# 初始化数据库
python3 scripts/init_db.py
```

## ⚠️ 常见问题

### 端口被占用

```bash
# 清理端口
lsof -ti:8000 | xargs kill -9  # 后端
lsof -ti:5173 | xargs kill -9  # 前端

# 或使用停止脚本
./scripts/stop_all.sh
```

### 数据库连接失败

```bash
# 检查 PostgreSQL
brew services list

# 启动 PostgreSQL
brew services start postgresql@14

# 确认数据库存在
psql -l | grep leetcode_learning
```

### Python 环境问题

```bash
# 使用 Python 3.12
cd backend
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎉 就这么简单！

启动后，访问 http://localhost:5173 开始你的算法学习之旅！

---

**需要帮助？** 查看 [CONNECTION_GUIDE.md](CONNECTION_GUIDE.md) 获取详细故障排查步骤。


# 快速开始指南

## 🚀 5 分钟快速启动

### 方法一：一键启动（推荐）

```bash
# 1. 首次设置（只需运行一次）
cd scripts
chmod +x setup.sh start_demo.sh
./setup.sh

# 2. 启动 demo
./start_demo.sh
```

然后访问 http://localhost:5173

### 方法二：手动启动

#### 终端 1 - 后端

```bash
cd backend

# 创建虚拟环境（首次）
python3 -m venv venv
source venv/bin/activate

# 安装依赖（首次）
pip install -r requirements.txt

# 启动后端
uvicorn main:app --reload --port 8000
```

#### 终端 2 - 初始化数据库（首次）

```bash
# 创建数据库（首次）
psql -U postgres -c "CREATE DATABASE leetcode_learning;"

# 初始化表和数据（首次）
python scripts/init_db.py
```

#### 终端 3 - 前端

```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动前端
npm run dev
```

## 🎯 使用演示

1. **首页测试** (http://localhost:5173)
   - 点击 "Start Assessment" 开始知识测试
   - 回答 3 个问题
   - 查看 AI 生成的学习计划

2. **查看 Roadmap**
   - 点击导航栏的 "Roadmap"
   - 浏览 9 个知识点
   - 点击任意卡片查看练习题

3. **练习题页面**
   - 阅读题目描述
   - 点击 "Strategy Hint" 获取算法提示
   - 点击 "Code Example" 查看代码示例
   - 点击 "Video Explanation" 获取视频链接

4. **代码检查**
   - 点击导航栏的 "Code Check"
   - 粘贴你的代码
   - 点击 "Check Code" 获取 AI 反馈

## 📊 Demo 账户

- User ID: 1
- Username: demo_user
- Email: demo@example.com

## 🔍 API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档

## ❓ 遇到问题？

### 后端无法启动
```bash
# 检查 Python 版本（需要 3.9+）
python3 --version

# 检查端口占用
lsof -i :8000
```

### 前端无法启动
```bash
# 检查 Node 版本（需要 16+）
node --version

# 清除缓存
rm -rf node_modules package-lock.json
npm install
```

### 数据库连接失败
```bash
# 检查 PostgreSQL 状态
# macOS:
brew services list
brew services start postgresql

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql
```

## 📖 详细文档

查看 [README_DEMO.md](./README_DEMO.md) 了解：
- 完整的技术架构
- 详细的 API 说明
- 数据库设计
- 功能特性

## 🎉 开始使用

现在你可以开始体验这个 AI 驱动的 LeetCode 学习平台了！



# 快速修复指南 🚀

## 立即可用的解决方案

### 第一步：使用正确的 Python 版本

```bash
# 安装 Python 3.12（如果还没有）
brew install python@3.12

# 验证安装
python3.12 --version
```

### 第二步：完全清理并重新设置

```bash
cd /Users/liangyue/Documents/school/cs5001_project

# 清理旧环境
rm -rf backend/venv
rm -rf frontend/node_modules

# 创建数据库（使用当前用户）
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 设置后端
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库
cd ..
python scripts/init_db.py

# 设置前端
cd frontend
npm install
```

### 第三步：启动服务

**终端 1 - 后端：**
```bash
cd /Users/liangyue/Documents/school/cs5001_project/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**终端 2 - 前端：**
```bash
cd /Users/liangyue/Documents/school/cs5001_project/frontend
npm run dev
```

### 第四步：访问应用

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000/docs

## 如果还有问题

### Python 3.12 也不行？

使用同步数据库驱动：

```bash
# 修改 backend/app/database.py 第 9 行
# 从这个：
DATABASE_URL = f"postgresql+asyncpg://{CURRENT_USER}@localhost:5432/leetcode_learning"

# 改成这个：
DATABASE_URL = f"postgresql+psycopg2://{CURRENT_USER}@localhost:5432/leetcode_learning"

# 然后安装 psycopg2
pip install psycopg2-binary
```

### PostgreSQL 无法连接？

```bash
# 启动 PostgreSQL
brew services start postgresql@14

# 检查状态
brew services list

# 测试连接
psql -d postgres -c "SELECT 1;"
```

### 端口被占用？

```bash
# 杀死占用端口的进程
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

## 一键脚本（如果你信任我）

保存为 `quick_fix.sh` 并运行：

```bash
#!/bin/bash
set -e

echo "🔧 Quick Fix Script"
echo "==================="

cd /Users/liangyue/Documents/school/cs5001_project

# 清理
echo "1. Cleaning up..."
rm -rf backend/venv frontend/node_modules

# 数据库
echo "2. Setting up database..."
psql -d postgres -c "CREATE DATABASE leetcode_learning;" 2>/dev/null || echo "Database already exists"

# 后端
echo "3. Setting up backend..."
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 初始化数据
echo "4. Initializing database..."
cd ..
python scripts/init_db.py

# 前端
echo "5. Setting up frontend..."
cd frontend
npm install --silent

echo ""
echo "✅ Setup complete!"
echo ""
echo "Start backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "Start frontend: cd frontend && npm run dev"
```

## 需要更多帮助？

查看 `TROUBLESHOOTING.md` 获取详细故障排除指南。


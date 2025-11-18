# 故障排除指南

## Python 3.13 兼容性问题

### 问题
```
ERROR: Failed building wheel for asyncpg
ERROR: Failed building wheel for pydantic-core
```

### 原因
Python 3.13 是最新版本，某些包可能还不完全支持。

### 解决方案

**方案 1：使用 Python 3.11 或 3.12（推荐）**

```bash
# 安装 Python 3.12
brew install python@3.12

# 删除现有虚拟环境
rm -rf backend/venv

# 使用 Python 3.12 创建新虚拟环境
cd backend
python3.12 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

**方案 2：使用预编译的二进制包**

```bash
cd backend
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装预编译的包
pip install --only-binary=:all: asyncpg pydantic pydantic-core

# 安装其他依赖
pip install -r requirements.txt
```

**方案 3：使用 psycopg2 代替 asyncpg**

如果 asyncpg 安装失败，可以暂时使用 psycopg2：

```bash
# 修改 DATABASE_URL
# 从: postgresql+asyncpg://...
# 到: postgresql+psycopg2://...
```

## PostgreSQL 用户问题

### 问题
```
psql: error: FATAL: role "postgres" does not exist
```

### 原因
macOS 上通过 Homebrew 安装的 PostgreSQL 默认没有 `postgres` 用户，而是使用当前系统用户。

### 解决方案

**方案 1：使用当前用户（推荐）**

已经更新了脚本，现在会自动使用当前用户。运行：

```bash
cd scripts
./create_db.sh
```

**方案 2：手动创建数据库**

```bash
# 查看当前用户
whoami

# 使用当前用户创建数据库
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# 更新 backend/.env 文件
cd backend
echo "DATABASE_URL=postgresql+asyncpg://$(whoami)@localhost:5432/leetcode_learning" > .env
```

**方案 3：创建 postgres 用户**

```bash
# 创建 postgres 超级用户
createuser -s postgres

# 然后运行脚本
cd scripts
./create_db.sh
```

## 端口占用问题

### 问题
```
ERROR: [Errno 48] Address already in use
Port 5173 is in use
```

### 解决方案

**查找并停止占用端口的进程：**

```bash
# 查看 8000 端口占用
lsof -i :8000
# 停止进程（替换 PID）
kill -9 <PID>

# 查看 5173 端口占用
lsof -i :5173
kill -9 <PID>
```

**或者使用不同端口：**

```bash
# 后端使用 8001 端口
cd backend
uvicorn main:app --reload --port 8001

# 前端会自动选择可用端口
cd frontend
npm run dev
```

## 完整重置步骤

如果遇到多个问题，从头开始：

```bash
# 1. 停止所有服务
killall -9 python3 node

# 2. 清理环境
cd /Users/liangyue/Documents/school/cs5001_project
rm -rf backend/venv
rm -rf frontend/node_modules

# 3. 确保使用 Python 3.11 或 3.12
python3.12 --version  # 应该显示 3.12.x

# 4. 创建数据库
cd scripts
./create_db.sh

# 5. 安装后端
cd ../backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. 初始化数据库
cd ..
python scripts/init_db.py

# 7. 安装前端
cd frontend
npm install

# 8. 启动后端（新终端）
cd backend
source venv/bin/activate
uvicorn main:app --reload

# 9. 启动前端（新终端）
cd frontend
npm run dev
```

## 快速测试命令

### 测试 Python 环境
```bash
cd backend
source venv/bin/activate
python -c "import fastapi, sqlalchemy, asyncpg; print('✓ All packages imported successfully')"
```

### 测试数据库连接
```bash
psql -d leetcode_learning -c "SELECT version();"
```

### 测试后端 API
```bash
# 在新终端
curl http://localhost:8000/health
```

### 测试前端
浏览器访问: http://localhost:5173

## 常见错误信息

### 1. `ModuleNotFoundError: No module named 'sqlalchemy'`
**解决：** 确保虚拟环境已激活并安装了依赖
```bash
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. `connection to server on socket "/tmp/.s.PGSQL.5432" failed`
**解决：** PostgreSQL 未运行
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql
```

### 3. `ETIMEDOUT: connection timed out`
**解决：** 网络问题，重试 npm install
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmmirror.com
```

## 获取帮助

如果问题仍未解决，请：

1. 检查 Python 版本：`python3 --version`
2. 检查 PostgreSQL 状态：`brew services list` 或 `systemctl status postgresql`
3. 查看后端日志：启动 uvicorn 时的完整输出
4. 查看浏览器控制台错误（F12）

## 推荐的开发环境

- **Python**: 3.11 或 3.12（不要用 3.13）
- **Node.js**: 18 LTS 或 20 LTS
- **PostgreSQL**: 14 或 15
- **操作系统**: macOS 12+, Ubuntu 20.04+


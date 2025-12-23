# 本地开发环境启动指南

## 快速启动

### 方式一：一键启动（推荐）

```bash
./scripts/start_all.sh
```

这会同时启动前后端服务。

### 方式二：分别启动

**启动后端：**
```bash
./scripts/start_backend.sh
```
后端将在 `http://localhost:8000` 运行

**启动前端：**
```bash
./scripts/start_frontend.sh
```
前端将在 `http://localhost:5173` 运行

## 访问地址

- 📱 **前端应用**: http://localhost:5173
- 🔧 **后端API**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs
- ❤️ **健康检查**: http://localhost:8000/health

## 配置说明

### 后端配置
- 端口: `8000`
- Host: `localhost`
- 数据库: PostgreSQL (localhost:5432)
- 环境变量: `backend/.env`

### 前端配置
- 端口: `5173`
- API代理: `/api` → `http://localhost:8000`
- API基础URL: `http://localhost:8000/api`

## 停止服务

```bash
./scripts/stop_all.sh
```

或手动停止：
- 后端：`Ctrl+C` 或查找进程 `uvicorn main:app`
- 前端：`Ctrl+C` 或查找进程 `vite`

## 注意事项

1. 确保 PostgreSQL 数据库已启动
2. 确保已创建数据库 `leetcode_learning`
3. 后端需要 Python 虚拟环境（脚本会自动创建）
4. 前端需要安装 npm 依赖（脚本会自动安装）

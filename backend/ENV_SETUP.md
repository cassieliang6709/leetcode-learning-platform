# 环境变量配置指南 / Environment Setup Guide

## 📋 快速开始

### 1. 复制模板文件
```bash
cd backend
cp env.template .env
```

### 2. 编辑 .env 文件，填入真实的配置

```bash
# 使用你喜欢的编辑器打开 .env
nano .env
# 或
vim .env
# 或
code .env
```

### 3. 配置说明

#### 必需配置 (Required)

**DATABASE_URL** - 数据库连接地址
```
DATABASE_URL=postgresql+asyncpg://YOUR_USERNAME@localhost:5432/leetcode_learning
```
- 将 `YOUR_USERNAME` 替换为你的 PostgreSQL 用户名
- 如果数据库不在本地或端口不是 5432，请相应修改

**SILICONFLOW_API_KEY** - SiliconFlow AI API 密钥
```
SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxx
```
- ⚠️ **重要**: 这是必需的，用于 AI 功能（代码检查、智能提示等）
- 获取地址: https://siliconflow.cn
- 登录后在控制台获取 API Key

#### 可选配置 (Optional)

**OPENAI_API_KEY** - OpenAI API 密钥（未来功能）
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

**服务器配置** - 通常不需要修改
```
HOST=0.0.0.0
PORT=8000
```

---

## 🔒 安全注意事项

1. ✅ `.env` 文件已经在 `.gitignore` 中，不会被提交到 Git
2. ⚠️ **永远不要**把 `.env` 文件提交到代码仓库
3. ⚠️ **永远不要**在代码中硬编码 API Key
4. 🔑 如果不小心泄露了 API Key，立即到对应平台重新生成新的密钥

---

## ✅ 验证配置

启动后端服务后，检查日志：
```bash
cd backend
source venv/bin/activate  # 如果使用虚拟环境
python main.py
```

如果看到类似以下输出，说明配置成功：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

如果看到以下错误，说明 API Key 未配置：
```
ValueError: SILICONFLOW_API_KEY environment variable not set
```

---

## 📝 完整的 .env 示例

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://myuser@localhost:5432/leetcode_learning

# SiliconFlow API Key (Required for AI features)
SILICONFLOW_API_KEY=sk-ywiqoiuhlfyfsknsjsdmyvdllhwxsajvvafmszzbarckwzdv

# OpenAI API Key (Optional - for AI features)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

---

## 🆘 常见问题

**Q: 我没有 SiliconFlow API Key 怎么办？**
A: 访问 https://siliconflow.cn 注册账号并获取免费 API Key

**Q: .env 文件放在哪里？**
A: 放在 `backend/` 目录下，与 `main.py` 同级

**Q: 启动时提示找不到环境变量怎么办？**
A: 确保：
1. `.env` 文件在正确的位置（backend/.env）
2. 文件格式正确（KEY=VALUE，没有多余空格）
3. 没有使用引号包裹值（除非值本身包含空格）

**Q: 我可以在生产环境使用 .env 文件吗？**
A: 不建议。生产环境应该使用：
- 云平台的环境变量配置（如 Heroku Config Vars、AWS Secrets Manager）
- Kubernetes Secrets
- Docker 环境变量

---

## 🚀 下一步

配置完成后，运行启动脚本：
```bash
# 从项目根目录
./scripts/start_all.sh

# 或分别启动
./scripts/start_backend.sh
./scripts/start_frontend.sh
```

访问 http://localhost:5173 开始使用！








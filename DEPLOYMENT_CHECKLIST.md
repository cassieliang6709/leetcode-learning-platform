# 🚀 快速部署清单

## 准备阶段 ✅

已完成的配置：
- ✅ `backend/Procfile` - Render 部署配置
- ✅ `backend/main.py` - CORS 配置已更新
- ✅ `frontend/src/services/api.js` - 支持环境变量
- ✅ `frontend/vercel.json` - Vercel 配置
- ✅ 前端构建测试通过

## 部署步骤

### 1️⃣ Supabase 数据库（5分钟）
```bash
□ 访问 https://supabase.com 注册
□ 创建项目：leetcode-learning
□ 获取连接字符串（记得添加 +asyncpg）
□ 本地初始化：python scripts/init_db.py
```

### 2️⃣ Render 后端（10分钟）
```bash
□ 访问 https://render.com 注册
□ 连接 GitHub 仓库
□ 配置：
  - Root Directory: backend
  - Build: pip install -r requirements.txt
  - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
□ 添加环境变量：DATABASE_URL
□ 记录后端 URL
```

### 3️⃣ Vercel 前端（5分钟）
```bash
□ 创建 frontend/.env.production（使用后端 URL）
□ 访问 https://vercel.com 注册
□ 导入项目，配置：
  - Root Directory: frontend
  - Framework: Vite
□ 添加环境变量：VITE_API_URL
□ 记录前端 URL
```

### 4️⃣ 更新 CORS（2分钟）
```bash
□ 修改 backend/main.py CORS 配置（添加 Vercel URL）
□ 推送代码触发重新部署
```

### 5️⃣ 测试（5分钟）
```bash
□ 访问前端 URL
□ 测试注册/登录
□ 测试查看题目
□ 测试提交代码
```

## 📝 需要记录的信息

```
Supabase URL: _______________________
Database 连接字符串: _______________________

Render URL: _______________________
Render Dashboard: https://dashboard.render.com

Vercel URL: _______________________
Vercel Dashboard: https://vercel.com/dashboard
```

## ⚠️ 重要提醒

- **Render 免费层会休眠**：15分钟无活动后休眠
- **演示策略**：演示前 5 分钟先访问一次后端
- **UptimeRobot**：可选配置 https://uptimerobot.com 防止休眠

## 🔗 有用的链接

- 完整部署指南：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Supabase：https://supabase.com
- Render：https://render.com
- Vercel：https://vercel.com
- UptimeRobot：https://uptimerobot.com

---

**总时间：约30分钟 | 总成本：$0**


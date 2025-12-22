# ⚡ Railway 快速部署指南

## 🎯 使用你的 Supabase 配置

你已经有了 Supabase 项目，现在只需要部署后端和前端。

---

## 第一步：配置 Supabase 数据库（2分钟）

### 方式一：使用脚本（推荐）

```bash
./scripts/setup_supabase.sh
```

脚本会：
- ✅ 创建 `backend/.env` 文件
- ✅ 测试数据库连接
- ✅ 初始化数据库表结构

### 方式二：手动配置

1. **创建 `backend/.env` 文件**
   ```bash
   cd backend
   cat > .env << EOF
   DATABASE_URL=postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[你的密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   EOF
   ```

2. **初始化数据库**
   ```bash
   cd ..
   python scripts/init_db.py
   ```

---

## 第二步：部署后端到 Railway（5分钟）

### 1. 注册 Railway
- 访问 https://railway.app
- 使用 GitHub 账号登录

### 2. 创建新项目
- Dashboard → "New Project"
- 选择 "Deploy from GitHub repo"
- 选择你的仓库：`leetcode-learning-platform`

### 3. 配置服务
Railway 会自动创建服务，需要配置：

1. **设置根目录**
   - 点击服务 → Settings
   - Root Directory: `backend`

2. **添加环境变量**
   - 点击服务 → Variables
   - 添加：
     ```
     DATABASE_URL=postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[你的密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
     ```
   
   可选：
     ```
     SILICONFLOW_API_KEY=你的API密钥
     OPENAI_API_KEY=你的API密钥
     ```

3. **确认启动命令**
   - 点击服务 → Settings → Deploy
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - （Railway 会自动检测，通常不需要修改）

### 4. 获取 URL
- 等待部署完成（3-5分钟）
- 点击服务 → Settings → Domains
- 记录你的 Railway URL：`https://xxx.up.railway.app`

### 5. 测试
```bash
curl https://你的railway-url.up.railway.app/health
# 应该返回: {"status":"healthy"}
```

---

## 第三步：部署前端到 Vercel（5分钟）

### 1. 访问 Vercel
- https://vercel.com
- GitHub 登录

### 2. 导入项目
- Dashboard → "Add New..." → "Project"
- 选择仓库：`leetcode-learning-platform`
- 点击 "Import"

### 3. 配置项目
```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

### 4. 添加环境变量
```
Key: VITE_API_URL
Value: https://你的railway-url.up.railway.app/api
Environment: Production, Preview, Development
```

### 5. 部署
- 点击 "Deploy"
- 等待完成
- 记录前端 URL：`https://xxx.vercel.app`

---

## 第四步：更新 CORS（2分钟）

修改 `backend/main.py`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://你的项目名.vercel.app",  # 添加这行
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

推送代码：
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push origin main
```

Railway 会自动重新部署。

---

## ✅ 验证部署

1. **访问前端**: `https://你的项目名.vercel.app`
2. **测试功能**:
   - ✅ 注册新用户
   - ✅ 登录
   - ✅ 查看题目
   - ✅ 提交代码

---

## 📝 部署信息记录

```
Supabase:
Project ID: xeqhcjgqlxddxsxvdrpy
Dashboard: https://app.supabase.com/project/xeqhcjgqlxddxsxvdrpy

Railway:
Backend URL: https://xxx.up.railway.app
Dashboard: https://railway.app/dashboard

Vercel:
Frontend URL: https://xxx.vercel.app
Dashboard: https://vercel.com/dashboard
```

---

## 🎉 完成！

你的应用现在：
- ✅ 后端 24/7 运行（Railway 不休眠）
- ✅ 前端全球 CDN（Vercel）
- ✅ 数据库 Supabase（免费 PostgreSQL）

---

## 🐛 常见问题

### Railway 部署失败
- 检查环境变量是否正确
- 查看 Railway Logs 获取详细错误

### 前端无法连接后端
- 检查 `VITE_API_URL` 环境变量
- 检查后端 CORS 配置
- 确认后端正常运行

### 数据库连接失败
- 确认 Supabase 项目正常运行
- 检查密码是否正确
- 确认连接字符串格式（包含 `+asyncpg`）

---

## 📚 详细文档

- **Railway 部署**: [DEPLOY_RAILWAY.md](./DEPLOY_RAILWAY.md)
- **Vercel 部署**: [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
- **替代方案**: [DEPLOY_ALTERNATIVES.md](./DEPLOY_ALTERNATIVES.md)

---

**Railway + Vercel + Supabase = 完美的免费部署方案！🚀**

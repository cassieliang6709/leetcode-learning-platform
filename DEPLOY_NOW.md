# 🚀 立即部署指南

## 📋 部署前检查清单

### ✅ 已完成的配置
- [x] Supabase 数据库已配置
- [x] `.env` 文件已创建
- [x] 数据库已初始化
- [x] Railway 配置文件已创建
- [x] Vercel 配置文件已创建
- [x] 前端 API 配置支持环境变量

---

## 🚂 第一步：部署后端到 Railway（5分钟）

### 1. 注册/登录 Railway
- 访问 https://railway.app
- 使用 GitHub 账号登录

### 2. 创建新项目
1. Dashboard → **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你的仓库：`leetcode-learning-platform`
4. Railway 会自动检测项目

### 3. 配置服务
1. **设置根目录**
   - 点击服务 → **Settings**
   - **Root Directory**: `backend`

2. **添加环境变量**
   - 点击服务 → **Variables**
   - 添加以下变量：

   ```
   DATABASE_URL=postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[你的密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```

   ⚠️ **重要**：将 `[你的密码]` 替换为你的实际 Supabase 密码

   可选（如果有）：
   ```
   SILICONFLOW_API_KEY=你的API密钥
   OPENAI_API_KEY=你的API密钥
   ```

3. **确认启动命令**
   - 点击服务 → **Settings** → **Deploy**
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - （Railway 会自动检测，通常不需要修改）

### 4. 获取后端 URL
- 等待部署完成（3-5分钟）
- 点击服务 → **Settings** → **Domains**
- 记录你的 Railway URL：`https://xxx.up.railway.app`

### 5. 测试后端
```bash
curl https://你的railway-url.up.railway.app/health
# 应该返回: {"status":"healthy"}
```

---

## 🎨 第二步：部署前端到 Vercel（5分钟）

### 1. 注册/登录 Vercel
- 访问 https://vercel.com
- 使用 GitHub 账号登录

### 2. 导入项目
1. Dashboard → **"Add New..."** → **"Project"**
2. 选择你的仓库：`leetcode-learning-platform`
3. 点击 **"Import"**

### 3. 配置项目
```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### 4. 添加环境变量
在 **"Environment Variables"** 部分添加：

```
Key: VITE_API_URL
Value: https://你的railway-url.up.railway.app/api
Environment: Production, Preview, Development (全选)
```

⚠️ **重要**：使用你刚才获取的 Railway URL！

### 5. 部署
- 点击 **"Deploy"**
- 等待 2-3 分钟
- 记录前端 URL：`https://xxx.vercel.app`

---

## 🔧 第三步：更新 CORS 配置（2分钟）

### 修改后端 CORS
编辑 `backend/main.py`，找到 CORS 配置部分：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://你的项目名.vercel.app",  # 添加这行
        "https://*.vercel.app",  # 或使用通配符
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 提交并推送代码
```bash
git add backend/main.py
git commit -m "Update CORS for production domain"
git push origin main
```

Railway 会自动检测并重新部署。

---

## ✅ 第四步：验证部署

### 1. 测试后端
```bash
curl https://你的railway-url.up.railway.app/health
```

### 2. 测试前端
- 访问你的 Vercel URL
- 打开浏览器开发者工具（F12）
- 尝试注册/登录
- 查看 Network 标签，确认 API 请求成功

### 3. 测试功能
- ✅ 用户注册
- ✅ 用户登录
- ✅ 查看知识点
- ✅ 答题功能
- ✅ 代码提交

---

## 📝 部署信息记录

记录你的部署信息：

```
Supabase:
Project ID: xeqhcjgqlxddxsxvdrpy
Dashboard: https://app.supabase.com/project/xeqhcjgqlxddxsxvdrpy

Railway:
Backend URL: https://________________.up.railway.app
Dashboard: https://railway.app/dashboard

Vercel:
Frontend URL: https://________________.vercel.app
Dashboard: https://vercel.com/dashboard
```

---

## 🐛 常见问题

### Railway 部署失败
- 检查环境变量 `DATABASE_URL` 是否正确
- 确认密码中没有特殊字符需要 URL 编码
- 查看 Railway Logs 获取详细错误

### 前端无法连接后端
- 检查 `VITE_API_URL` 环境变量是否正确
- 确认后端 CORS 配置包含前端域名
- 检查后端是否正常运行

### 数据库连接失败
- 确认 Supabase 项目正常运行
- 检查连接字符串格式（包含 `+asyncpg`）
- 确认密码正确

---

## 🎉 完成！

部署完成后，你的应用将：
- ✅ 后端 24/7 运行（Railway 不休眠）
- ✅ 前端全球 CDN（Vercel）
- ✅ 数据库 Supabase（免费 PostgreSQL）

**开始部署吧！🚀**

# ⚡ 快速部署指南

## 📋 部署方案

- **前端**: Vercel（免费，自动 HTTPS，全球 CDN）
- **后端**: Render（免费，支持 Python，自动部署）
- **数据库**: Supabase（免费 PostgreSQL）

---

## 🚀 三步部署

### 第一步：部署后端到 Render（10分钟）

#### 1. 准备数据库（Supabase）
```bash
# 1. 访问 https://supabase.com 注册
# 2. 创建新项目：leetcode-learning
# 3. 获取数据库连接字符串（Settings → Database → Connection string）
# 4. 转换为 asyncpg 格式：
#    postgresql://... → postgresql+asyncpg://...
```

#### 2. 部署到 Render
```bash
# 1. 访问 https://render.com 注册（GitHub 登录）
# 2. Dashboard → "New +" → "Web Service"
# 3. 连接 GitHub 仓库
# 4. 配置：
#    - Name: leetcode-backend
#    - Region: Singapore (或最近区域)
#    - Branch: main
#    - Root Directory: backend
#    - Runtime: Python 3
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
#    - Instance Type: Free
# 5. 添加环境变量：
#    - DATABASE_URL: postgresql+asyncpg://...（从 Supabase）
#    - SILICONFLOW_API_KEY: 你的 API Key（可选）
# 6. 点击 "Create Web Service"
# 7. 等待部署完成，记录 URL（如：https://leetcode-backend.onrender.com）
```

#### 3. 初始化数据库
```bash
# 在本地运行（使用 Supabase 数据库 URL）
cd backend
source venv/bin/activate

# 创建 .env 文件
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://你的Supabase连接字符串
EOF

# 初始化数据库
cd ..
python scripts/init_db.py
```

---

### 第二步：部署前端到 Vercel（5分钟）

#### 方式一：通过 Dashboard（推荐）

1. **访问 Vercel**
   - https://vercel.com
   - GitHub 登录

2. **导入项目**
   - Dashboard → "Add New..." → "Project"
   - 选择仓库：`leetcode-learning-platform`
   - 点击 "Import"

3. **配置项目**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **添加环境变量**
   ```
   Key: VITE_API_URL
   Value: https://你的Render后端URL/api
   Environment: Production, Preview, Development
   ```

5. **部署**
   - 点击 "Deploy"
   - 等待完成，记录 URL（如：https://leetcode-learning-platform.vercel.app）

#### 方式二：通过 CLI
```bash
# 安装 CLI
npm i -g vercel

# 登录
vercel login

# 部署
cd frontend
vercel

# 设置环境变量
vercel env add VITE_API_URL
# 输入：https://你的后端URL/api

# 生产部署
vercel --prod
```

---

### 第三步：更新 CORS 配置（2分钟）

修改 `backend/main.py` 的 CORS 配置：

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

推送代码触发重新部署：
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push origin main
```

---

## ✅ 验证部署

### 检查后端
```bash
curl https://你的后端URL.onrender.com/health
# 应该返回: {"status":"healthy"}
```

### 检查前端
1. 访问你的 Vercel URL
2. 打开浏览器开发者工具（F12）
3. 尝试登录/注册
4. 查看 Network 标签，确认 API 请求成功

---

## 📝 部署信息记录

```
数据库（Supabase）：
Project URL: https://app.supabase.com/project/...
Database URL: postgresql+asyncpg://...

后端（Render）：
Service URL: https://leetcode-backend.onrender.com
Dashboard: https://dashboard.render.com

前端（Vercel）：
Production URL: https://leetcode-learning-platform.vercel.app
Dashboard: https://vercel.com/dashboard
```

---

## ⚠️ 重要提示

### Render 免费层限制
- **休眠机制**: 15分钟无活动后休眠
- **唤醒时间**: 首次访问需要 30 秒
- **解决方案**: 使用 UptimeRobot（免费）每 5 分钟 ping 一次

### UptimeRobot 配置（可选）
1. 访问 https://uptimerobot.com
2. 注册账号
3. 添加监控：
   - Monitor Type: HTTP(s)
   - URL: https://你的后端URL.onrender.com/health
   - Interval: 5 minutes

---

## 🐛 常见问题

### 前端无法连接后端
- ✅ 检查 `VITE_API_URL` 环境变量是否正确
- ✅ 检查后端 CORS 配置
- ✅ 检查后端是否正常运行

### 后端启动失败
- ✅ 检查 `DATABASE_URL` 环境变量
- ✅ 确认数据库连接字符串格式（包含 `+asyncpg`）
- ✅ 查看 Render Logs 获取详细错误

### 数据库连接失败
- ✅ 确认 Supabase 项目正常运行
- ✅ 检查连接字符串中的密码是否正确
- ✅ 确认网络连接正常

---

## 📚 详细文档

- **前端部署**: [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
- **完整指南**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **快速清单**: [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

---

## 💰 成本

| 服务 | 月费用 | 限制 |
|------|--------|------|
| Supabase | $0 | 500MB 存储 |
| Render | $0 | 15分钟后休眠 |
| Vercel | $0 | 100GB 带宽 |
| **总计** | **$0** | 完全免费 |

---

**部署完成后，你的应用就可以在线上运行了！🎉**

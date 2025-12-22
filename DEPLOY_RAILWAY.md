# 🚂 Railway 后端部署指南

## 为什么选择 Railway？

- ✅ **免费层不会休眠** - 24/7 运行
- ✅ **更稳定** - 比 Render 更可靠
- ✅ **自动部署** - 连接 GitHub 自动部署
- ✅ **简单配置** - 零配置部署

---

## 快速部署步骤

### 第一步：准备 Supabase 数据库

你已经有了 Supabase 配置，现在需要：

1. **获取数据库连接字符串**
   - 进入 Supabase Dashboard
   - Settings → Database → Connection string
   - 选择 "URI" 格式
   - 复制连接字符串

2. **转换为 asyncpg 格式**
   ```
   原始格式：
   postgresql://postgres.xeqhcjgqlxddxsxvdrpy:[PASSWORD]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   
   转换为：
   postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[PASSWORD]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```

3. **初始化数据库（本地运行）**
   ```bash
   cd backend
   source venv/bin/activate
   
   # 创建 .env 文件
   cat > .env << EOF
   DATABASE_URL=postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[你的密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   EOF
   
   # 初始化数据库
   cd ..
   python scripts/init_db.py
   ```

---

### 第二步：部署到 Railway

#### 1. 注册 Railway
- 访问 https://railway.app
- 使用 GitHub 账号登录
- 点击 "New Project"

#### 2. 从 GitHub 部署
- 选择 "Deploy from GitHub repo"
- 选择你的仓库：`leetcode-learning-platform`
- Railway 会自动检测项目

#### 3. 配置服务
Railway 会自动检测到 `backend/railway.json`，但需要手动配置：

1. **设置根目录**
   - 点击服务 → Settings
   - Root Directory: `backend`

2. **添加环境变量**
   - 点击服务 → Variables
   - 添加以下变量：

   ```
   DATABASE_URL=postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[你的密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```

   可选（如果有）：
   ```
   SILICONFLOW_API_KEY=你的API密钥
   OPENAI_API_KEY=你的API密钥
   ```

3. **配置启动命令**
   - 点击服务 → Settings → Deploy
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 4. 部署
- Railway 会自动开始部署
- 等待 3-5 分钟
- 部署完成后，点击服务 → Settings → Domains
- 记录你的 Railway URL（如：`https://xxx.up.railway.app`）

---

### 第三步：测试部署

```bash
# 测试健康检查
curl https://你的railway-url.up.railway.app/health

# 应该返回: {"status":"healthy"}
```

---

### 第四步：部署前端到 Vercel

参考 [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)，在环境变量中使用 Railway URL：

```
VITE_API_URL=https://你的railway-url.up.railway.app/api
```

---

## Railway vs Render

| 特性 | Railway | Render |
|------|---------|--------|
| 免费层休眠 | ❌ 不休眠 | ✅ 15分钟后休眠 |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 配置复杂度 | 简单 | 简单 |
| 部署速度 | 快 | 中等 |
| 免费额度 | $5/月 | 有限制 |

---

## 常见问题

### Q: Railway 免费层有限制吗？
A: 有 $5/月的免费额度，对于小型项目足够使用。

### Q: 如何查看日志？
A: Railway Dashboard → 你的服务 → Deployments → 点击最新部署 → Logs

### Q: 如何更新代码？
A: 推送到 GitHub，Railway 会自动检测并重新部署。

### Q: 如何自定义域名？
A: Railway Dashboard → 服务 → Settings → Domains → 添加自定义域名

---

## 部署检查清单

- [ ] Supabase 数据库已创建
- [ ] 数据库连接字符串已获取并转换格式
- [ ] 本地已初始化数据库
- [ ] Railway 账号已注册
- [ ] 项目已连接到 GitHub
- [ ] 环境变量已配置
- [ ] 部署成功
- [ ] 健康检查通过
- [ ] 前端已配置 Railway URL

---

## 有用的链接

- Railway Dashboard: https://railway.app/dashboard
- Railway 文档: https://docs.railway.app
- Supabase Dashboard: https://app.supabase.com

---

**Railway 部署完成后，你的后端将 24/7 运行，不会休眠！🎉**

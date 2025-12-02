# 🚀 部署指南：Render + Supabase 免费方案

本指南将帮你把前端部署到 Vercel，后端部署到 Render，数据库使用 Supabase。

## ✅ 准备工作完成清单

已完成的配置：
- ✅ 创建 `backend/Procfile` - Render 部署配置
- ✅ 修改 `backend/main.py` - 更新 CORS 配置支持生产环境
- ✅ 修改 `frontend/src/services/api.js` - 支持环境变量配置 API URL
- ✅ 创建 `frontend/vercel.json` - Vercel 部署配置
- ✅ 测试前端构建成功

## 📋 部署步骤

### 第一步：部署数据库（Supabase）

1. **注册并创建项目**
   - 访问 https://supabase.com
   - 用 GitHub 登录
   - 点击 "New Project"
   - 填写信息：
     ```
     Name: leetcode-learning
     Database Password: [设置强密码并记住]
     Region: Northeast Asia (Tokyo) 或最近的区域
     ```
   - 点击 "Create new project"（等待2-3分钟）

2. **获取数据库连接字符串**
   - 项目创建完成后，进入 Settings → Database
   - 找到 "Connection string" → 选择 "URI"
   - 复制连接字符串，类似：
     ```
     postgresql://postgres.xxxxx:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres
     ```
   - ⚠️ 需要转换为 asyncpg 格式（添加 `+asyncpg`）：
     ```
     postgresql+asyncpg://postgres.xxxxx:[PASSWORD]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres
     ```

3. **初始化数据库（本地运行）**
   ```bash
   cd backend
   
   # 创建 .env 文件（如果还没有）
   cat > .env << 'EOF'
   DATABASE_URL=postgresql+asyncpg://postgres.xxxxx:[你的密码]@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres
   EOF
   
   # 激活虚拟环境
   source venv/bin/activate
   
   # 运行初始化脚本
   cd ..
   python scripts/init_db.py
   ```

---

### 第二步：部署后端到 Render

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration for Render and Vercel"
   git push origin main
   ```

2. **注册 Render**
   - 访问 https://render.com
   - 用 GitHub 账号登录

3. **创建 Web Service**
   - Dashboard → "New +" → "Web Service"
   - 连接 GitHub 仓库：`leetcode-learning-platform`
   - 配置服务：
     ```
     Name: leetcode-backend
     Region: Singapore (或离你近的区域)
     Branch: main
     Root Directory: backend
     Runtime: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
     Instance Type: Free
     ```

4. **添加环境变量**
   - 点击 "Advanced" → "Add Environment Variable"
   - 添加：
     ```
     Key: DATABASE_URL
     Value: postgresql+asyncpg://postgres.xxxxx:[密码]@...（从 Supabase 复制）
     ```
   - 可选（如果有 OpenAI API key）：
     ```
     Key: OPENAI_API_KEY
     Value: sk-...
     ```

5. **部署并测试**
   - 点击 "Create Web Service"
   - 等待部署完成（5-10分钟）
   - 记录后端 URL，例如：`https://leetcode-backend.onrender.com`
   - 测试健康检查：访问 `https://leetcode-backend.onrender.com/health`
   - 应该返回：`{"status": "healthy"}`

---

### 第三步：部署前端到 Vercel

1. **创建生产环境配置**
   在 `frontend` 目录创建 `.env.production` 文件：
   ```bash
   cat > frontend/.env.production << 'EOF'
   VITE_API_URL=https://leetcode-backend.onrender.com/api
   EOF
   ```
   ⚠️ 替换为你实际的 Render 后端 URL！

2. **推送更改**
   ```bash
   git add frontend/.env.production
   git commit -m "Add production API URL"
   git push origin main
   ```

3. **注册 Vercel**
   - 访问 https://vercel.com
   - 用 GitHub 账号登录

4. **导入项目**
   - Dashboard → "Add New..." → "Project"
   - 选择 `leetcode-learning-platform` 仓库
   - 配置项目：
     ```
     Framework Preset: Vite
     Root Directory: frontend
     Build Command: npm run build
     Output Directory: dist
     ```

5. **添加环境变量**
   - 展开 "Environment Variables"
   - 添加：
     ```
     Key: VITE_API_URL
     Value: https://leetcode-backend.onrender.com/api
     Environment: Production
     ```
   ⚠️ 使用你的实际 Render URL！

6. **部署**
   - 点击 "Deploy"
   - 等待部署完成（2-3分钟）
   - 记录前端 URL，例如：`https://leetcode-learning-platform.vercel.app`

---

### 第四步：更新后端 CORS 配置

1. **修改 `backend/main.py`**
   找到 CORS 配置部分，更新为：
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "http://localhost:3000",
           "https://leetcode-learning-platform.vercel.app",  # 你的实际 Vercel 域名
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **推送更改触发重新部署**
   ```bash
   git add backend/main.py
   git commit -m "Update CORS for production domain"
   git push origin main
   ```
   Render 会自动检测并重新部署。

---

### 第五步：测试部署

1. **访问前端** 
   ```
   https://leetcode-learning-platform.vercel.app
   ```

2. **测试功能**
   - ✅ 页面加载正常
   - ✅ 注册新用户
   - ✅ 登录功能
   - ✅ 查看知识点
   - ✅ 答题功能
   - ✅ 代码提交

3. **检查问题**
   - 如果 API 调用失败，检查浏览器控制台（F12）
   - 查看 Render 日志：Dashboard → 你的服务 → Logs
   - 查看 Vercel 日志：Dashboard → Deployments → 点击最新部署

---

## ⚠️ 重要注意事项

### Render 免费层限制

- **休眠机制**：15分钟无活动后休眠
- **唤醒时间**：首次访问需要 30 秒
- **演示策略**：演示前 5 分钟先访问一次后端

### 防止休眠方案（可选）

使用 **UptimeRobot** 保持后端活跃：

1. 访问 https://uptimerobot.com （免费）
2. 注册账号
3. 添加新监控：
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Leetcode Backend
   URL: https://leetcode-backend.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
4. 每 5 分钟自动 ping，保持后端不休眠

### Supabase 免费层限制

- 500MB 存储空间（足够用）
- 2GB 数据传输/月
- 7天不活动会暂停项目

---

## 🐛 常见问题排查

### 1. 前端无法连接后端

**检查项**：
- ✅ `.env.production` 中的 API URL 是否正确
- ✅ Vercel 环境变量 `VITE_API_URL` 是否设置
- ✅ 后端 CORS 配置是否包含前端域名
- ✅ 后端是否正常运行（访问 `/health` 端点）

**解决方案**：
```bash
# 在浏览器控制台查看错误
# 常见错误：CORS error、Network error、404
```

### 2. 后端启动失败

**检查项**：
- ✅ Render 环境变量 `DATABASE_URL` 是否正确
- ✅ 数据库连接字符串格式是否正确（包含 `+asyncpg`）
- ✅ Supabase 项目是否正常运行

**解决方案**：
```bash
# 在 Render Logs 中查看详细错误信息
# 常见错误：Database connection failed
```

### 3. 数据库初始化失败

**检查项**：
- ✅ 本地 `.env` 文件中的 `DATABASE_URL` 是否正确
- ✅ 网络连接是否正常
- ✅ 数据库密码是否正确

**解决方案**：
```bash
# 测试数据库连接
python -c "import asyncpg; import asyncio; asyncio.run(asyncpg.connect('你的连接字符串'))"
```

---

## 📊 部署检查清单

完成以下所有步骤：

- [ ] Supabase 项目创建成功
- [ ] 本地运行 `init_db.py` 初始化数据库
- [ ] 代码推送到 GitHub
- [ ] Render 后端部署成功
- [ ] 后端 `/health` 返回正常
- [ ] Vercel 前端部署成功
- [ ] 前端可以访问
- [ ] 前端可以调用后端 API
- [ ] 注册登录功能正常
- [ ] 更新 CORS 配置包含实际域名
- [ ] （可选）配置 UptimeRobot

---

## 🎯 部署后的 URL 记录

记录你的部署地址：

```
数据库（Supabase）：
Project URL: https://app.supabase.com/project/[YOUR_PROJECT_ID]
Database Host: aws-0-ap-northeast-1.pooler.supabase.com

后端（Render）：
Service URL: https://leetcode-backend.onrender.com
Dashboard: https://dashboard.render.com

前端（Vercel）：
Production URL: https://leetcode-learning-platform.vercel.app
Dashboard: https://vercel.com/dashboard
```

---

## 💡 成本总结

| 服务 | 月费用 | 限制 |
|------|--------|------|
| Supabase | $0 | 500MB 存储，2GB 传输 |
| Render | $0 | 15分钟后休眠 |
| Vercel | $0 | 100GB 带宽 |
| UptimeRobot | $0 | 50 个监控器 |
| **总计** | **$0** | 完全免费 |

---

## 📞 需要帮助？

如果遇到问题：
1. 查看本指南的"常见问题排查"部分
2. 检查服务的日志（Render Logs、Vercel Logs）
3. 查看浏览器控制台错误信息

---

**祝部署顺利！🎉**


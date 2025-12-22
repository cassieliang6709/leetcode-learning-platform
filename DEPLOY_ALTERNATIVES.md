# 🚀 后端部署替代方案

## 方案对比

| 平台 | 免费层休眠 | 稳定性 | 配置难度 | 推荐度 |
|------|-----------|--------|----------|--------|
| **Railway** | ❌ 不休眠 | ⭐⭐⭐⭐⭐ | 简单 | ⭐⭐⭐⭐⭐ |
| **Fly.io** | ❌ 不休眠 | ⭐⭐⭐⭐ | 中等 | ⭐⭐⭐⭐ |
| **Render** | ✅ 15分钟休眠 | ⭐⭐⭐ | 简单 | ⭐⭐⭐ |
| **Vercel Serverless** | ❌ 不休眠 | ⭐⭐⭐⭐ | 复杂（需重构） | ⭐⭐ |

---

## 🚂 方案一：Railway（推荐）

### 优点
- ✅ 免费层 **不会休眠**，24/7 运行
- ✅ 非常稳定
- ✅ 配置简单
- ✅ 自动部署

### 缺点
- ⚠️ 免费额度 $5/月（通常够用）

### 部署步骤
详见 [DEPLOY_RAILWAY.md](./DEPLOY_RAILWAY.md)

---

## 🪂 方案二：Fly.io

### 优点
- ✅ 免费层 **不会休眠**
- ✅ 全球边缘部署
- ✅ 支持 Docker
- ✅ 配置灵活

### 缺点
- ⚠️ 需要创建 Dockerfile
- ⚠️ 配置稍复杂

### 快速部署

#### 1. 安装 Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

#### 2. 登录
```bash
fly auth login
```

#### 3. 初始化项目
```bash
cd backend
fly launch
```

#### 4. 配置环境变量
```bash
fly secrets set DATABASE_URL="postgresql+asyncpg://..."
```

#### 5. 部署
```bash
fly deploy
```

---

## 🌐 方案三：Vercel Serverless Functions

### 优点
- ✅ 免费层充足
- ✅ 全球 CDN
- ✅ 与前端同平台

### 缺点
- ❌ 需要重构代码（FastAPI → Serverless Functions）
- ❌ 不支持 WebSocket
- ❌ 函数执行时间限制

### 不推荐
需要大量代码修改，不适合当前项目。

---

## 📊 推荐方案

### 首选：Railway ⭐⭐⭐⭐⭐
- 最适合当前项目
- 零配置部署
- 稳定可靠

### 备选：Fly.io ⭐⭐⭐⭐
- 如果需要全球边缘部署
- 如果需要 Docker 容器化

---

## 快速选择指南

**选择 Railway 如果：**
- ✅ 想要最简单的部署
- ✅ 需要 24/7 运行
- ✅ 不想处理 Docker

**选择 Fly.io 如果：**
- ✅ 需要全球边缘部署
- ✅ 熟悉 Docker
- ✅ 需要更多控制

**避免 Render 如果：**
- ❌ 不想处理休眠问题
- ❌ 需要稳定运行

---

## 部署后配置

无论选择哪个平台，都需要：

1. **配置环境变量**
   ```
   DATABASE_URL=postgresql+asyncpg://...
   SILICONFLOW_API_KEY=...（可选）
   ```

2. **更新前端 API URL**
   ```
   VITE_API_URL=https://你的后端URL/api
   ```

3. **更新 CORS 配置**
   在 `backend/main.py` 中添加前端域名

---

## 详细文档

- **Railway**: [DEPLOY_RAILWAY.md](./DEPLOY_RAILWAY.md)
- **Vercel 前端**: [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
- **完整指南**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

**推荐使用 Railway，简单、稳定、不休眠！🚂**

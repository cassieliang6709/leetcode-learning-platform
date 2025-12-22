# 🚀 Vercel 前端部署指南

## 快速部署步骤

### 前置条件
- ✅ 代码已推送到 GitHub
- ✅ 后端已部署（Render/Railway/其他平台）
- ✅ 已获取后端 API URL

---

## 方式一：通过 Vercel Dashboard（推荐）

### 1. 注册/登录 Vercel
- 访问 https://vercel.com
- 使用 GitHub 账号登录

### 2. 导入项目
1. Dashboard → **"Add New..."** → **"Project"**
2. 选择你的 GitHub 仓库：`leetcode-learning-platform`
3. 点击 **"Import"**

### 3. 配置项目
在项目配置页面：

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
Value: https://你的后端URL/api
Environment: Production, Preview, Development (全选)
```

**示例：**
- Render: `https://leetcode-backend.onrender.com/api`
- Railway: `https://your-app.railway.app/api`

### 5. 部署
- 点击 **"Deploy"**
- 等待 2-3 分钟
- 部署完成后会显示你的网站 URL

---

## 方式二：通过 Vercel CLI

### 1. 安装 Vercel CLI
```bash
npm i -g vercel
```

### 2. 登录
```bash
vercel login
```

### 3. 部署
```bash
cd frontend
vercel
```

按提示操作：
- 选择项目范围
- 链接到现有项目或创建新项目
- 确认配置

### 4. 设置环境变量
```bash
vercel env add VITE_API_URL
# 输入值：https://你的后端URL/api
# 选择环境：Production, Preview, Development
```

### 5. 重新部署
```bash
vercel --prod
```

---

## 部署后配置

### 更新后端 CORS
部署完成后，需要更新后端的 CORS 配置，允许你的 Vercel 域名：

**修改 `backend/main.py`：**
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

然后推送代码，触发后端重新部署。

---

## 验证部署

### 1. 检查前端
访问你的 Vercel URL，应该能看到应用界面。

### 2. 检查 API 连接
- 打开浏览器开发者工具（F12）
- 查看 Network 标签
- 尝试登录/注册
- 确认 API 请求成功（状态码 200）

### 3. 测试功能
- ✅ 页面加载
- ✅ 用户注册
- ✅ 用户登录
- ✅ 查看题目
- ✅ 提交代码

---

## 常见问题

### 问题 1: 构建失败
**原因：** 依赖问题或构建配置错误

**解决：**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 问题 2: API 请求失败（CORS 错误）
**原因：** 后端 CORS 未配置 Vercel 域名

**解决：** 按照上面的"更新后端 CORS"步骤操作

### 问题 3: API 请求 404
**原因：** 环境变量 `VITE_API_URL` 未设置或错误

**解决：**
1. 检查 Vercel Dashboard → Settings → Environment Variables
2. 确认 `VITE_API_URL` 值正确
3. 重新部署

### 问题 4: 页面空白
**原因：** 路由配置问题

**解决：** 确认 `vercel.json` 配置正确（已包含在项目中）

---

## 自动部署

Vercel 会自动：
- ✅ 监听 GitHub push 事件
- ✅ 自动触发部署
- ✅ 为每个 PR 创建预览环境

### 禁用自动部署（可选）
在 Vercel Dashboard → Settings → Git：
- 取消勾选 "Automatically deploy"

---

## 自定义域名（可选）

### 添加自定义域名
1. Vercel Dashboard → Settings → Domains
2. 输入你的域名
3. 按照提示配置 DNS

---

## 环境变量管理

### 生产环境变量
在 Vercel Dashboard → Settings → Environment Variables 中管理。

### 本地开发
创建 `frontend/.env.local`（不提交到 git）：
```env
VITE_API_URL=http://localhost:8000/api
```

---

## 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] 后端已部署并运行正常
- [ ] 获取了后端 API URL
- [ ] 在 Vercel 创建了项目
- [ ] 配置了 Root Directory: `frontend`
- [ ] 添加了环境变量 `VITE_API_URL`
- [ ] 部署成功
- [ ] 更新了后端 CORS 配置
- [ ] 测试了所有功能

---

## 有用的链接

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel 文档: https://vercel.com/docs
- 项目部署指南: [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)

---

**部署完成后，你的应用将在 `https://你的项目名.vercel.app` 运行！🎉**

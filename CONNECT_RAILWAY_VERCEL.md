# 🔗 连接 Railway 后端到 Vercel 前端

## 📝 说明

Railway 和 Vercel **不需要直接连接**，它们通过以下方式协作：

1. **Railway** 部署后端 API（例如：`https://xxx.up.railway.app`）
2. **Vercel** 部署前端应用
3. **前端通过环境变量** 知道后端 API 的地址
4. **前端发送 HTTP 请求** 到后端 API

---

## 🚀 连接步骤

### 第一步：获取 Railway 后端 URL

1. 登录 Railway Dashboard：https://railway.app/dashboard
2. 点击你的后端服务
3. 点击 **Settings** → **Domains**
4. 复制你的 Railway URL，例如：
   ```
   https://leetcode-backend-production.up.railway.app
   ```

### 第二步：在 Vercel 中配置环境变量

1. 登录 Vercel Dashboard：https://vercel.com/dashboard
2. 点击你的前端项目
3. 点击 **Settings** → **Environment Variables**
4. 添加新的环境变量：

   ```
   Name: VITE_API_URL
   Value: https://你的railway-url.up.railway.app/api
   Environment: Production, Preview, Development (全选)
   ```

   **示例：**
   ```
   Name: VITE_API_URL
   Value: https://leetcode-backend-production.up.railway.app/api
   Environment: Production, Preview, Development
   ```

5. 点击 **Save**

### 第三步：重新部署前端

环境变量添加后，Vercel 会自动触发重新部署。如果没有：

1. 点击 **Deployments**
2. 点击最新的部署右侧的 **"..."** 菜单
3. 选择 **Redeploy**

---

## ✅ 验证连接

### 1. 检查环境变量

在 Vercel Dashboard 中：
- Settings → Environment Variables
- 确认 `VITE_API_URL` 已添加且值正确

### 2. 测试前端

1. 访问你的 Vercel URL（例如：`https://xxx.vercel.app`）
2. 打开浏览器开发者工具（F12）
3. 切换到 **Console** 标签
4. 输入以下命令检查 API URL：
   ```javascript
   console.log(import.meta.env.VITE_API_URL)
   ```
   应该显示你的 Railway URL

### 3. 测试 API 调用

1. 在浏览器中尝试登录或注册
2. 切换到 **Network** 标签
3. 查看 API 请求，应该指向你的 Railway URL
4. 确认请求成功（状态码 200）

---

## 🔧 工作原理

### 前端代码（api.js）

```javascript
// 使用环境变量获取 API 地址
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
```

### 请求流程

```
用户浏览器
    ↓
Vercel 前端 (https://xxx.vercel.app)
    ↓ (HTTP 请求)
Railway 后端 (https://xxx.up.railway.app/api)
    ↓
Supabase 数据库
```

---

## 🐛 常见问题

### 问题 1: 前端无法连接后端

**检查项：**
- ✅ Vercel 环境变量 `VITE_API_URL` 是否正确
- ✅ Railway URL 是否包含 `/api` 后缀
- ✅ 后端 CORS 配置是否包含 Vercel 域名

**解决：**
1. 检查 Vercel 环境变量
2. 确认 Railway URL 格式：`https://xxx.up.railway.app/api`
3. 更新后端 CORS（见下方）

### 问题 2: CORS 错误

如果看到 CORS 错误，需要更新后端 CORS 配置：

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

然后推送代码：
```bash
git add backend/main.py
git commit -m "Update CORS for Vercel"
git push origin main
```

Railway 会自动重新部署。

### 问题 3: 环境变量不生效

**原因：** Vercel 需要重新部署才能应用新的环境变量

**解决：**
1. 在 Vercel Dashboard 中手动触发重新部署
2. 或者推送一个小的代码更改触发自动部署

---

## 📋 完整配置检查清单

- [ ] Railway 后端已部署并运行
- [ ] 获取了 Railway URL
- [ ] 在 Vercel 中添加了 `VITE_API_URL` 环境变量
- [ ] 环境变量值格式正确（包含 `/api` 后缀）
- [ ] 选择了所有环境（Production, Preview, Development）
- [ ] Vercel 已重新部署
- [ ] 后端 CORS 配置包含 Vercel 域名
- [ ] 测试了前端 API 调用

---

## 🎯 快速参考

### Railway URL 格式
```
https://你的服务名.up.railway.app
```

### Vercel 环境变量
```
VITE_API_URL=https://你的railway-url.up.railway.app/api
```

### 测试命令
```bash
# 测试后端
curl https://你的railway-url.up.railway.app/health

# 应该返回: {"status":"healthy"}
```

---

## 💡 提示

1. **环境变量名称**：必须是 `VITE_API_URL`（Vite 要求以 `VITE_` 开头）
2. **URL 格式**：确保包含 `/api` 后缀
3. **重新部署**：修改环境变量后需要重新部署前端
4. **CORS**：确保后端允许 Vercel 域名

---

**配置完成后，前端就可以通过 HTTP 请求连接到 Railway 后端了！🎉**

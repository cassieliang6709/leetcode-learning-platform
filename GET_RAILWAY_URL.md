# 🔗 如何获取 Railway 后端 URL

## 方法一：通过 Railway Dashboard（推荐）

1. **登录 Railway Dashboard**
   - 访问：https://railway.app/dashboard
   - 使用 GitHub 账号登录

2. **找到你的项目**
   - 在 Dashboard 中找到项目 ID：`7d4ef9ca-1ce3-4e6f-931e-5cb004c73776`
   - 点击进入项目

3. **获取服务 URL**
   - 点击你的后端服务（通常是第一个服务）
   - 点击 **Settings** 标签
   - 找到 **Domains** 部分
   - 你会看到类似这样的 URL：
     ```
     https://xxx-production.up.railway.app
     ```
   - 这就是你的 Railway 后端 URL！

---

## 方法二：通过 Railway CLI

如果你安装了 Railway CLI：

```bash
# 链接到项目
railway link -p 7d4ef9ca-1ce3-4e6f-931e-5cb004c73776

# 获取服务 URL
railway domain
```

---

## 方法三：查看部署日志

1. 在 Railway Dashboard 中
2. 点击你的服务
3. 查看 **Deployments** 标签
4. 点击最新的部署
5. 在日志中查找 URL 信息

---

## Railway URL 格式

Railway URL 通常格式为：
```
https://[服务名]-[环境].up.railway.app
```

例如：
- `https://leetcode-backend-production.up.railway.app`
- `https://web-production-xxx.up.railway.app`

---

## 找到 URL 后

拿到 URL 后，可以：

1. **测试后端**
   ```bash
   curl https://你的railway-url.up.railway.app/health
   ```

2. **配置 Vercel 环境变量**
   - 在 Vercel 中添加：`VITE_API_URL=https://你的railway-url.up.railway.app/api`

---

**找到 URL 后告诉我，我可以帮你测试！🚀**

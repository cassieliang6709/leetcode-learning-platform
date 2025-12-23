# 🔧 修复数据库连接错误

## 错误信息
```
Registration failed: [Errno 8] nodename nor servname provided, or not known
```

## 原因
密码中包含特殊字符 `@@`，可能导致 URL 解析问题。

## 解决方案

### 方法一：URL 编码密码（推荐）

密码 `abcd1234Ly@@` 需要 URL 编码：
- `@` → `%40`

**修改后的 DATABASE_URL：**
```
postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:abcd1234Ly%40%40@aws-1-us-east-2.pooler.supabase.com:5432/postgres
```

**注意：** `@@` 变成了 `%40%40`

---

### 方法二：使用 Supabase 连接字符串（如果可用）

在 Supabase Dashboard 中：
1. Settings → Database
2. 找到 "Connection string"
3. 选择 "URI" 格式
4. 复制连接字符串
5. 转换为 asyncpg 格式（添加 `+asyncpg`）
6. 确保使用端口 `5432`（不是 `6543`）

---

## 在 Railway 中修改

1. **Railway Dashboard** → 服务 → **Settings** → **Variables**
2. 找到 `DATABASE_URL`
3. 修改为（使用 URL 编码的密码）：
   ```
   postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:abcd1234Ly%40%40@aws-1-us-east-2.pooler.supabase.com:5432/postgres
   ```
4. **保存**
5. 等待重新部署

---

## 验证修复

部署完成后测试：
```bash
curl https://leetcode-learning-platform-production.up.railway.app/health
```

---

## 如果还是失败

检查：
1. ✅ Supabase 数据库是否正常运行
2. ✅ 网络连接是否正常
3. ✅ 密码是否正确
4. ✅ 尝试从 Supabase Dashboard 获取新的连接字符串


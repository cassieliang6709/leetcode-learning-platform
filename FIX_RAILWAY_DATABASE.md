# 🔧 修复 Railway 数据库连接问题

## 问题
错误：`connect() got an unexpected keyword argument 'pgbouncer'`

## 原因
Railway 环境变量中的 `DATABASE_URL` 包含 `pgbouncer=true` 参数，但 `asyncpg` 不支持。

## 解决方案

### 在 Railway Dashboard 中修改环境变量

1. **进入 Railway Dashboard**
   - 访问：https://railway.app/dashboard
   - 点击项目：`jubilant-endurance`
   - 点击你的后端服务

2. **修改环境变量**
   - 点击 **Settings** → **Variables**
   - 找到 `DATABASE_URL`
   - 点击编辑（铅笔图标）

3. **更新 DATABASE_URL**
   
   **当前值（错误）：**
   ```
   postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[密码]@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```
   
   **修改为（正确）：**
   ```
   postgresql+asyncpg://postgres.xeqhcjgqlxddxsxvdrpy:[密码]@aws-1-us-east-2.pooler.supabase.com:5432/postgres
   ```
   
   **重要修改：**
   - ✅ 端口从 `6543` 改为 `5432`（直连端口）
   - ✅ 移除 `?pgbouncer=true` 参数

4. **保存**
   - 点击 **Save** 或 **Update**
   - Railway 会自动重新部署

5. **等待部署完成**
   - 查看 **Deployments** 标签
   - 等待状态变为 "Active"

---

## 验证修复

部署完成后，测试：

```bash
# 测试健康检查
curl https://leetcode-learning-platform-production.up.railway.app/health

# 测试注册接口
curl -X POST https://leetcode-learning-platform-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'
```

应该返回成功响应，而不是 500 错误。

---

## 如果还是失败

检查：
1. ✅ 环境变量已保存
2. ✅ 服务已重新部署
3. ✅ 密码中没有特殊字符需要 URL 编码
4. ✅ Supabase 数据库允许来自 Railway 的连接

---

**修改环境变量后，Railway 会自动重新部署，通常需要 1-2 分钟。**

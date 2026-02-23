# 修复的 Bugs 记录

## Bug 1：user_id 硬编码为 1
**文件**: `backend/app/api/routes/code_execution.py`
**问题**: 所有代码提交的 user_id 永远是 1，所有用户的提交互相覆盖
**修复**: 从 JWT token 中提取 user_id，支持 guest 模式（未登录可执行但不保存）
**安全影响**: 原本任何人提交代码都以 user=1 身份存储，数据隔离完全失效

---

## Bug 2：内存限制设为 -1（无限制）
**文件**: `backend/app/services/code_executor.py`
**问题**: `run_memory_limit: -1` 表示无限制，恶意代码可以吃光服务器内存
**修复**: 设为 128MB (`128 * 1024 * 1024`)，compile 阶段设为 256MB
**安全影响**: 与简历中"strict resource quotas"直接矛盾

---

## Bug 3：get_learning_plan 新用户 404
**文件**: `backend/app/api/routes/knowledge.py`
**问题**: 新用户第一次进入 Roadmap 页面，后端返回 404，前端报错
**修复**: 返回 `{"plans": []}` 空列表，404 只用于"资源不存在"场景

---

## Bug 4：datetime.utcnow() 废弃警告
**文件**: `backend/app/services/auth_service.py`
**问题**: Python 3.12+ 中 `datetime.utcnow()` 已废弃（returns naive datetime）
**修复**: 改为 `datetime.now(timezone.utc)`（timezone-aware datetime）

---

## Bug 5：任何用户可查他人提交历史 ✅ 已修复
**文件**: `backend/app/api/routes/code_execution.py`
**问题**: `GET /submissions/{user_id}/recent` 没有认证，user_id 从路径参数取
**修复**: 改为 `GET /submissions/me/recent`，从 JWT token 取 user_id，未认证返回 401

---

## Bug 6：generate_learning_plan 推荐硬编码 ID ✅ 已修复
**文件**: `backend/app/api/routes/knowledge.py`
**问题**: 推荐的 knowledge_point_id 是写死的 1-9，数据库里不一定存在这些 ID 导致 FK 错误
**修复**: 先用 weak_areas 匹配 KnowledgePoint.category，没匹配时 fallback 到最小的几个真实 ID

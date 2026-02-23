# 面试准备资料 - AlgoMentor

按顺序阅读：

| 文件 | 内容 | 阅读时间 |
|------|------|---------|
| `00_PLAN.md` | 整体改进计划，项目现状，bug 列表 | 10 min |
| `01_ARCHITECTURE.md` | 系统架构图，数据流，技术选型理由 | 8 min |
| `02_QA.md` | 面试高频问题 + 标准答案（重点！） | 15 min |
| `03_BUGS_FIXED.md` | 修复了哪些 bug，为什么修 | 5 min |
| `04_RAG_EXPLAINED.md` | RAG 原理 + 代码逻辑详解 + demo 思路 | 10 min |
| `05_RESUME_BULLETS.md` | 更新后的简历内容 + 每条 bullet 追问答案 | 10 min |
| `06_DOCKER_DEPLOY.md` | Docker Compose 架构 + Piston 隔离机制 + 部署问答 | 8 min |

## 面试前 30 分钟速查

1. **项目一句话介绍**：AI 辅助的算法学习平台，用户可以在结构化路线图上学习算法知识、做题、获得实时 AI 辅导
2. **最大亮点**：RAG pipeline（pgvector 向量搜索 + sentence-transformers + SiliconFlow LLM）
3. **最容易被追问的**：Docker sandboxing（回答看 02_QA.md 第2节）
4. **已修复的 bug**：user_id 硬编码、memory_limit=-1、新用户404

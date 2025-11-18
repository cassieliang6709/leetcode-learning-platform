# 🚀 启动指南

## ✅ 当前状态

所有设置已完成：
- ✅ Python 3.12 虚拟环境已创建
- ✅ 所有 Python 依赖已安装（包括 greenlet）
- ✅ PostgreSQL 数据库已创建
- ✅ 数据库表已创建（7个表）
- ✅ 初始数据已填充（9个知识点 + 1个演示用户）
- ✅ 前端依赖已安装

## 🎯 立即启动

### 终端 1 - 启动后端

```bash
cd /Users/liangyue/Documents/school/cs5001_project/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**看到这个说明成功了：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 终端 2 - 启动前端

```bash
cd /Users/liangyue/Documents/school/cs5001_project/frontend
npm run dev
```

**看到这个说明成功了：**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

## 🌐 访问应用

启动成功后访问：

- **前端界面**: http://localhost:5173
- **后端 API 文档**: http://localhost:8000/docs
- **后端健康检查**: http://localhost:8000/health

## 📊 演示账户

- **用户 ID**: 1
- **用户名**: demo_user
- **邮箱**: demo@example.com

## 🎮 使用流程

1. **首页** → 完成知识测试（3个问题）
2. **查看结果** → AI 生成学习计划
3. **Roadmap** → 浏览 9 个知识点
4. **选择知识点** → 查看练习题
5. **练习题页面** → 使用三层提示系统：
   - Level 1: 算法策略提示
   - Level 2: 代码示例
   - Level 3: YouTube 视频
6. **Code Check** → 提交代码获取 AI 反馈

## ⚠️ 常见问题

### 端口被占用
```bash
# 杀死占用 8000 端口的进程
lsof -ti:8000 | xargs kill -9

# 杀死占用 5173 端口的进程
lsof -ti:5173 | xargs kill -9
```

### 重启服务
```bash
# 按 Ctrl+C 停止服务，然后重新运行启动命令
```

### 查看日志
- 后端日志会在终端 1 显示
- 前端日志会在终端 2 显示
- 浏览器控制台（F12）显示前端错误

## 📚 数据库信息

**连接信息：**
- 数据库名：leetcode_learning
- 用户：liangyue（你的系统用户）
- 主机：localhost
- 端口：5432

**已创建的表：**
1. users - 用户
2. knowledge_points - 知识点（已有9条数据）
3. knowledge_tests - 知识测试记录
4. learning_plans - 学习计划
5. quiz_questions - 练习题
6. quiz_attempts - 答题记录
7. code_submissions - 代码提交

## 🔧 快速测试

```bash
# 测试后端健康
curl http://localhost:8000/health

# 测试获取知识点
curl http://localhost:8000/api/knowledge/points

# 查看数据库
psql -d leetcode_learning -c "SELECT * FROM knowledge_points;"
```

## 🎨 界面预览

前端使用了现代化的紫色渐变主题：
- 首页：知识测试和结果展示
- Roadmap：知识点卡片网格
- Quiz：题目列表和三层提示
- Code Check：代码编辑和 AI 反馈

## 💡 下一步

项目运行后，你可以：
1. 体验完整的学习流程
2. 查看 API 文档了解所有端点
3. 根据需求添加更多功能
4. 集成真实的 OpenAI API

---

**准备好了吗？在两个终端运行启动命令开始使用！** 🚀


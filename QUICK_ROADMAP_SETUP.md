# 🚀 快速设置 Roadmap 数据

## 立即使用完整的 30 个知识点！

---

## 📋 准备工作

### 确认环境
```bash
# 1. 检查 Python 版本 (需要 3.8+)
python3 --version

# 2. 检查 Node.js 版本 (需要 14+)
node --version

# 3. 确认在项目根目录
pwd
# 应该显示：/Users/liangyue/Documents/school/cs5001_project
```

---

## 🎯 三步完成设置

### 步骤 1：初始化数据库（包含 30 个知识点）

```bash
# 运行新的初始化脚本
python3 scripts/init_db_with_roadmap.py
```

**预期输出：**
```
============================================================
DATABASE INITIALIZATION - NEETCODE STYLE ROADMAP
============================================================
Creating database tables...
✓ Tables created successfully

Seeding comprehensive knowledge points...
✓ Seeded 30 knowledge points

Knowledge Points by Category:
  • array: 6 topics
  • dp: 4 topics
  • graph: 4 topics
  • other: 9 topics
  • string: 2 topics
  • tree: 5 topics

Creating demo user...
✓ Created demo user (ID: 1)
  Username: demo_user
  Email: demo@example.com

============================================================
✓ Database initialization completed successfully!
============================================================

Roadmap Overview:
  📚 30 comprehensive topics
  🎯 Covers arrays, trees, graphs, DP, and more
  📈 Progressive difficulty from easy to hard
```

---

### 步骤 2：启动后端服务

```bash
# 进入后端目录
cd backend

# 启动 FastAPI 服务器
uvicorn main:app --reload
```

**预期输出：**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**保持这个终端运行！** 打开新终端继续下一步。

---

### 步骤 3：启动前端服务

```bash
# 打开新终端，进入前端目录
cd /Users/liangyue/Documents/school/cs5001_project/frontend

# 启动 Vite 开发服务器
npm run dev
```

**预期输出：**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🎉 查看效果

### 访问 Roadmap 页面

打开浏览器访问：**http://localhost:5173/roadmap**

你将看到：

```
┌─────────────────────────────────────────────────────────┐
│ 侧边栏分类          主内容区域                          │
├──────────────┬──────────────────────────────────────────┤
│ Categories   │  Learning Roadmap                        │
│              │  Master algorithms step by step    0/30  │
│ 📚 All (30)  │                                           │
│ 📊 Arrays(6) │  ┌────────────────────────────────────┐  │
│ 📝 String(2) │  │ 1  Easy                            │  │
│ 🌳 Trees(5)  │  │ Arrays & Hashing                   │  │
│ 🕸️ Graphs(4) │  │ Master array operations...         │  │
│ 🎯 DP(4)     │  │ array           0/5 problems       │  │
│ 🔧 Other(9)  │  └────────────────────────────────────┘  │
│              │  [... 29 more topics ...]                │
└──────────────┴──────────────────────────────────────────┘
```

---

## 🎯 功能测试清单

### ✅ 基础功能
- [ ] 看到 30 个知识点卡片
- [ ] 侧边栏显示 6 个分类
- [ ] 每个分类显示正确的数量
- [ ] 点击分类可以筛选
- [ ] 右上角显示进度（0/30）

### ✅ 交互效果
- [ ] 卡片悬停效果流畅
- [ ] 深色主题显示正常
- [ ] 可以切换浅色主题
- [ ] 移动端响应式正常

### ✅ 内容验证
- [ ] 每个卡片有难度标签（Easy/Medium/Hard）
- [ ] 描述文字清晰完整
- [ ] 分类标签正确
- [ ] 排序顺序合理

---

## 📊 数据概览

### 按分类统计

| 分类 | 图标 | 主题数 | 主要内容 |
|------|------|--------|----------|
| Arrays & More | 📊 | 6 | Arrays, Two Pointers, Sliding Window, Binary Search, Intervals, Bit Manipulation |
| Strings | 📝 | 2 | String Manipulation, Pattern Matching |
| Trees & Tries | 🌳 | 5 | Traversal, DFS, BFS, BST, Trie |
| Graphs | 🕸️ | 4 | DFS/BFS, Union Find, Topological Sort, Shortest Path |
| Dynamic Programming | 🎯 | 4 | 1-D DP, 2-D DP, Knapsack, String DP |
| Advanced Topics | 🔧 | 9 | Stack, Heap, Backtracking, Greedy, Math, etc. |

### 按难度统计

| 难度 | 数量 | 占比 |
|------|------|------|
| 🟢 Easy | 7 | 23% |
| 🟡 Medium | 17 | 57% |
| 🔴 Hard | 6 | 20% |

---

## 🔧 故障排除

### 问题 1：数据库初始化失败

**错误信息：** `Error connecting to database`

**解决方案：**
```bash
# 检查 PostgreSQL 是否运行
# Mac:
brew services list

# 如果没有运行，启动它
brew services start postgresql

# 重新运行初始化脚本
python3 scripts/init_db_with_roadmap.py
```

---

### 问题 2：前端看不到数据

**检查步骤：**

1. **后端是否运行？**
   ```bash
   # 访问 API 端点
   curl http://localhost:8000/api/knowledge-points
   ```
   应该返回 JSON 数据

2. **浏览器控制台是否有错误？**
   - 打开开发者工具 (F12)
   - 查看 Console 和 Network 标签

3. **API 路径是否正确？**
   - 检查 `frontend/src/services/api.js`
   - 确认 baseURL 是 `http://localhost:8000`

---

### 问题 3：卡片显示不完整

**可能原因：**
- 数据库数据不完整
- 前端渲染问题

**解决方案：**
```bash
# 重新初始化数据库
python3 scripts/init_db_with_roadmap.py

# 清除前端缓存
cd frontend
rm -rf node_modules/.vite
npm run dev
```

---

### 问题 4：分类筛选不工作

**检查：**
1. 确认 category 字段与前端定义一致
2. 查看浏览器控制台错误
3. 确认后端返回的数据格式正确

---

## 🎨 自定义数据

### 添加新知识点

编辑 `scripts/init_db_with_roadmap.py`，在 `knowledge_points` 列表中添加：

```python
{
    "name": "你的主题名称",
    "description": "详细描述（建议 100-150 字）",
    "difficulty": "easy",  # easy, medium, hard
    "category": "array",   # array, string, tree, graph, dp, other
    "order_index": 31      # 排序位置
}
```

然后重新运行初始化：
```bash
python3 scripts/init_db_with_roadmap.py
```

---

### 修改分类名称

编辑 `frontend/src/pages/RoadmapPage.jsx`，修改 `categories` 数组：

```javascript
const categories = [
  { id: 'array', name: '你的新名称', icon: '📊', count: 0 },
  // ...
]
```

---

## 📈 下一步

### 1. 添加题目数据
为每个知识点添加 5-10 道练习题：
- LeetCode 题号和链接
- 题目描述
- 分层 Hints
- 参考答案

### 2. 实现进度追踪
- 用户完成状态
- 做题记录
- 学习时长统计

### 3. 添加学习笔记
- Markdown 编辑器
- 代码高亮
- 笔记保存和导出

---

## 📚 相关文档

- 📖 **[完整数据说明](/ROADMAP_DATA.md)** - 所有 30 个知识点的详细信息
- 🎨 **[设计文档](/NEETCODE_REDESIGN.md)** - NeetCode 风格设计
- 🎬 **[骨架屏文档](/SKELETON_LOADING.md)** - 加载效果说明

---

## ✅ 完成检查

运行成功后，你应该能够：
- ✅ 看到 30 个知识点
- ✅ 使用分类筛选
- ✅ 查看进度统计
- ✅ 流畅的交互体验
- ✅ 深色/浅色主题切换

---

## 🎉 成功！

你现在拥有一个完整的、**NeetCode 级别**的学习路线图！

包含：
- 📚 **30 个精心设计的主题**
- 🎯 **6 大分类，循序渐进**
- 🎨 **优雅的界面设计**
- ⚡ **流畅的用户体验**

开始你的算法学习之旅吧！🚀

---

**需要帮助？** 
- 查看完整文档：`/ROADMAP_DATA.md`
- 检查 API：`http://localhost:8000/docs`
- 前端开发者工具：按 F12

*快速设置指南 - v1.0*


# 📅 每日Quiz功能设置指南

## 功能介绍

全新的每日Quiz功能让你每天完成5个精选算法题目，巩固算法基础！

### ✨ 特性

- 📝 **每日5题** - 从100+题库中随机抽取
- 🎯 **智能过滤** - 已答过的题目不会重复出现
- 💾 **实时保存** - 答一题存一题，不怕刷新
- 📊 **进度追踪** - 实时查看今日完成情况
- 🎨 **卡片设计** - 现代化UI，体验流畅

## 数据库设置

### 步骤1：运行数据库迁移

添加新的字段到 `quiz_questions` 表：

```bash
cd scripts
python migrate_add_quiz_fields.py
```

**注意**：运行前需要更新脚本中的 `DATABASE_URL`

### 步骤2：初始化100个题目

```bash
python init_quiz_questions.py
```

这将创建：
- ✅ 20题 数组与哈希表
- ✅ 15题 滑动窗口
- ✅ 15题 双指针
- ✅ 15题 二分查找
- ✅ 10题 栈与队列
- ✅ 10题 链表
- ✅ 15题 树与图
- ✅ 更多题目...

## 数据库结构

### quiz_questions 表新增字段

```sql
-- 选项（JSON数组）
options JSON  -- ["选项A", "选项B", "选项C", "选项D"]

-- 正确答案（索引，0-3）
correct_answer INTEGER

-- 答案解释
explanation TEXT
```

### 示例数据

```json
{
  "title": "哈希表查找时间复杂度",
  "description": "在理想情况下，哈希表的查找时间复杂度是多少？",
  "difficulty": "easy",
  "options": ["O(n)", "O(1)", "O(log n)", "O(n log n)"],
  "correct_answer": 1,
  "explanation": "哈希表在理想情况下（无哈希冲突）的查找时间复杂度为O(1)。"
}
```

## API端点

### 1. 获取每日题目

```http
GET /api/quiz/daily/{user_id}
```

**响应：**
```json
{
  "total_questions": 5,
  "answered_count": 2,
  "correct_count": 1,
  "questions": [
    {
      "id": 1,
      "title": "哈希表查找时间复杂度",
      "description": "...",
      "difficulty": "easy",
      "options": ["O(n)", "O(1)", "O(log n)", "O(n log n)"],
      "knowledge_point_name": "Hash Table",
      "is_answered": false
    }
  ]
}
```

### 2. 提交答案

```http
POST /api/quiz/answer/{user_id}
Content-Type: application/json

{
  "question_id": 1,
  "selected_option": 1
}
```

**响应：**
```json
{
  "is_correct": true,
  "message": "Great job! 🎉"
}
```

### 3. 获取今日进度

```http
GET /api/quiz/progress/{user_id}
```

**响应：**
```json
{
  "answered_count": 3,
  "correct_count": 2,
  "total_questions": 5,
  "percentage": 60
}
```

## 前端使用

### HomePage组件

新的首页采用卡片式设计：

```jsx
// 自动加载每日题目
useEffect(() => {
  loadDailyQuiz()
}, [])

// 提交答案（实时保存）
const handleSubmitAnswer = async (questionId) => {
  const response = await api.submitAnswer(userId, questionId, selectedOption)
  // 更新UI，显示结果
}
```

### UI特性

1. **进度卡片** - 显示今日完成情况
2. **题目卡片** - 点击展开答题
3. **实时反馈** - 提交后立即显示对错
4. **状态标记** - ✅已答对 ❌答错 🔒未答

## 使用流程

### 用户视角

1. **打开首页** → 自动加载今日5题
2. **查看进度** → 顶部显示完成情况
3. **点击题目** → 展开查看详情
4. **选择答案** → 点击选项
5. **提交** → 立即保存并反馈
6. **继续** → 完成剩余题目

### 数据流

```
用户访问首页
    ↓
GET /api/quiz/daily/{user_id}
    ↓
返回5个随机题目（排除今日已答）
    ↓
用户选择答案并提交
    ↓
POST /api/quiz/answer/{user_id}
    ↓
保存到 quiz_attempts 表
    ↓
返回正确/错误反馈
```

## 开发者注意事项

### 1. 用户认证

当前使用硬编码 `userId = 1`，需要集成真实的用户认证：

```jsx
// TODO: 从AuthContext获取
const { user } = useAuth()
const userId = user.id
```

### 2. 题目质量

初始化脚本中的题目是示例数据，建议：
- 📝 完善题目描述
- 🎯 确保答案正确
- 💡 添加详细解释
- 🔗 添加相关LeetCode链接

### 3. 随机算法

当前使用Python的 `random.sample()`，可以考虑：
- 🎲 加权随机（根据难度）
- 📊 基于用户历史表现推荐
- 🔄 保证知识点均衡分布

### 4. 性能优化

- ⚡ 缓存今日题目（Redis）
- 🔄 预加载下一题
- 📦 批量提交答案

## 故障排除

### 问题1：题目加载失败

**可能原因：**
- 数据库未初始化
- API连接失败

**解决方案：**
```bash
# 检查数据库
python scripts/init_quiz_questions.py

# 检查后端是否运行
curl http://localhost:8000/health
```

### 问题2：答案无法提交

**可能原因：**
- user_id不存在
- question_id不存在

**解决方案：**
```bash
# 检查users表
psql -d leetcode_learning -c "SELECT * FROM users;"

# 创建测试用户
python scripts/create_test_user.py
```

### 问题3：重复出现已答题目

**可能原因：**
- 时间判断错误
- quiz_attempts表未记录

**解决方案：**
- 检查服务器时区设置
- 确认quiz_attempts表有数据

## 下一步优化

- [ ] 添加答题统计分析
- [ ] 实现连续答题天数
- [ ] 添加答题排行榜
- [ ] 支持题目收藏功能
- [ ] 添加错题本功能
- [ ] 实现题目评论功能

## 技术栈

- **后端**: FastAPI + SQLAlchemy + PostgreSQL
- **前端**: React + Vite
- **状态管理**: React Hooks
- **样式**: CSS3 (自定义设计)

---

## 快速开始

```bash
# 1. 运行迁移
cd scripts
python migrate_add_quiz_fields.py

# 2. 初始化题目
python init_quiz_questions.py

# 3. 启动后端
cd ../backend
python -m uvicorn main:app --reload

# 4. 启动前端
cd ../frontend
npm run dev

# 5. 访问 http://localhost:5173
```

🎉 **开始你的每日算法之旅吧！**


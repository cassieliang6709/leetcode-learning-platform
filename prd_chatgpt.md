# 1. 🎯 **产品背景 & 目标**

用户在准备 LeetCode/算法时，经常遇到：

- 不知道自己知识点掌握程度
- 不知道从哪里开始练习
- 解题策略不清晰，容易卡住
- 想练习但不知道错在哪
- 想系统性学习某个知识点（DP / Graph / Two pointers / Heap…）

本产品目标：

- 用 **测试 → 生成 roadmap → 练习题 → AI 辅助学习 → 笔记沉淀** 的方式，帮助用户系统提升算法能力。
- 覆盖 **LeetCode Hot 100**。

---

# 2. 👤 **核心用户故事（User Stories）**

### US1：做测试判断水平

作为一个用户

我希望做一个 5 道题的基础测试

以便知道我目前哪类知识点掌握不好，从而生成学习计划

### US2：查看 Roadmap

作为一个用户

我希望看到一个清晰的知识点列表 & 学习路径

可以选择某个知识点继续学习

### US3：练习该知识点的题目

作为一个用户

我希望点进某个知识点后

看到推荐的练习题（quiz）

并得到 AI 的解释、策略、hint 分层提示

帮助我能自我解题

### US4：检查我写的代码

作为一个用户

我希望提交我的代码给 AI

AI 能告诉我：

- 哪部分错了
- 如何根据我的思路纠错
- 甚至直接给出正确答案（第二层）

### US5：学习资源

作为一个用户

我希望：

- 能看到你们整理的优质资料（写死）
- AI 帮我解释我不懂的地方
- 推荐 YouTube 学习视频

### US6：做题笔记

作为一个用户

我希望每道题都能添加我的学习笔记，方便复习

---

# 3. 🧭 **系统流程图（User Flow）**

```
                ┌──► 初始测试（5选题）
                │         │
  用户注册/进入 ─┤         ▼
                │   AI 生成学习规划（roadmap）
                │         │
                └──► Roadmap 页面（选择知识点）
                          │
                          ▼
                  知识点练习页面
            ┌──────────────┬──────────────┬──────────────┐
            ▼              ▼              ▼              ▼
        Quiz 题目      AI Hint      代码检查器        学习资源
        解答输入       策略层1-3     AI debug        YouTube推荐
            │                                                │
            └───────────► 用户笔记保存 ◄─────────────────────┘

```

---

# 4. 🧱 **核心功能需求（Functional Requirements）**

---

## **4.1 模块 1 — 测试（Test Module）**

### 功能

- 显示 5 道选择题
- 题目来自预设题库（覆盖不同知识点）
- 用户提交答案 → 后端通过 API 计算结果
- AI 根据结果生成：
    - 掌握情况
    - 弱点知识点
    - 学习路径（例如“先学 Two Pointers → Sliding Window → DP”）

### 后端逻辑

- 题库写死
- 评分规则写死
- “生成学习路径” 调用 AI

---

## **4.2 模块 2 — Roadmap（首页）**

### 页面

- 展示所有知识点（tags）
- 每个知识点显示：
    - 掌握度（百分比）
    - 推荐题目数量
    - AI 推荐难度顺序（Easy → Medium → Hard）

### 用户行为

- 点击某知识点 → 进入对应 Quiz 页面

---

## **4.3 模块 3 — 练习知识点（Quiz）**

### 功能

- 展示该知识点的若干题目（Hot 100 中筛选）
- 每题包含：
    - 题目描述
    - 示例
    - 难度
    - Tag
    - 用户提交代码（Python/JS）

### 返回内容（AI）

分三层 hint：

### ✔ 第一层：算法策略（不透露代码）

- 使用什么数据结构
- 思考路径
- 时间空间复杂度可能性
- 边界条件提醒

### ✔ 第二层：代码解答（参考）

- 提供清晰可用的解法
- 包括注释

### ✔ 第三层：YouTube 推荐

通过 prompt 让 AI：

```
“给我推荐 3 个最适合这个题的视频 YouTube 链接”
```

---

## **4.4 模块 4 — 代码检查（Debug by AI）**

用户写的代码 → 提交到后端 → FastAPI 调 AI 分析

AI 输出：

- 错误分析（line by line）
- 为什么错（逻辑/边界条件/数据结构）
- 根据用户思路调整后的正确解法
- 正确代码（对照）

---

## **4.5 模块 5 — 资源库（Knowledge Library）**

- 写死的资源（官网、技术博客、我与你平时记录的精华资源）
- AI 可以回答“这里看不懂”的问题

---

## **4.6 模块 6 — 笔记系统 Notes**

- 每道题可以添加自己的 markdown 笔记
- 支持保存、删除、编辑
- 后端存数据库

---

# 5. 🧬 **数据库设计（Data Model）**

### **User**

```
id
email
created_at
```

### **Test Result**

```
id
user_id
score
weak_topics (json)
roadmap (json)

```

### **Topic（知识点）**

```
id
name ("Two Pointers")
description
resources (json)

```

### **Question（题库）**

```
id
leetcode_id
title
topic_id
difficulty
description
examples (json)
solution_code (json)

```

### **User Notes**

```
id
user_id
question_id
note_md
updated_at

```

---

# 6. 🧰 **API 接口设计（FastAPI）**

---

## **1. /test/start**

GET | 获取测试题

## **2. /test/submit**

POST | 用户提交答案

返回学习路线（AI）

---

## **3. /topics**

GET | 获取所有知识点

## **4. /topics/{id}/questions**

GET | 获取该知识点题目列表

---

## **5. /ai/hint**

POST | 输入题目 + 用户当前代码（可空）

返回：

- 策略层
- 代码层
- 视频层

---

## **6. /ai/debug**

POST | 用户提交代码

返回代码错误分析 + 修正版代码

---

## **7. /notes**

POST | 添加/更新笔记

GET | 获取某题笔记

DELETE | 删除笔记

---

# 7. 🎨 **前端结构 (React)**

```
src/
  components/
    QuizItem.jsx
    CodeEditor.jsx
    HintCard.jsx
    TopicCard.jsx
  pages/
    TestStart.jsx
    Roadmap.jsx
    TopicDetail.jsx
    QuizPage.jsx
    DebugPage.jsx
  api/
    test.js
    roadmap.js
    ai.js

```

---

# 8. ⚙ **后端结构 (FastAPI)**

```
app/
  main.py
  routers/
    test.py
    topics.py
    quiz.py
    ai.py
    notes.py
  services/
    ai_service.py
    scoring.py
    roadmap.py
  models/
    user.py
    topic.py
    question.py
    notes.py
  db.py

```

---

# 9. 🧠 **AI Prompt 设计（核心）**

---

## **1. 生成学习规划**

```
You are an algorithm learning coach.
Given the user score and wrong topics, generate a personalized roadmap covering Hot 100.
Provide step-by-step modules, timeline, and difficulty progression.

```

---

## **2. 三层 Hint Prompt**

```
You are a senior algorithm instructor.
For the given LeetCode problem:
1. Provide a strategy explanation only (no code).
2. Provide a full reference solution code with comments.
3. Provide 3 best YouTube video links.

```

---

## **3. Debug Prompt**

```
You are a code reviewer.
Given user code + problem:
- Identify mistakes and why they occur.
- Provide corrected code following the user's thought process.
- Provide an alternative clean solution.

```

---

# 10. 📈 **未来扩展**

- 增加社交功能（好友一起刷题）
- 助教模式（同学互相 review）
- 每周挑战赛
- AI 自动出题（题难度智能调节）
- 用户复习计划（Spaced Repetition）
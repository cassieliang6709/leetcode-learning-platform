# 🚀 代码执行功能 - 快速测试指南

## 立即测试代码执行功能！

---

## ⚡ 3 步快速测试

### 步骤 1：安装依赖并添加题目 (2 分钟)
```bash
# 进入项目根目录
cd /Users/liangyue/Documents/school/cs5001_project

# 安装 httpx（代码执行需要）
cd backend
pip install httpx==0.27.0

# 添加示例题目
cd ..
python3 scripts/add_sample_questions.py
```

**预期输出：**
```
============================================================
ADDING SAMPLE QUESTIONS WITH TEST CASES
============================================================

📝 Adding sample questions with test cases...
✅ Added 2 sample questions with test cases:
  1. Two Sum (Easy)
  2. Valid Palindrome (Easy)

These questions can now be tested with real code execution!
```

---

### 步骤 2：启动后端 (1 分钟)
```bash
cd backend
uvicorn main:app --reload
```

**预期输出：**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### 步骤 3：测试 API (2 分钟)

#### 方法 A：使用 Swagger UI（推荐）⭐

1. 打开浏览器：**http://localhost:8000/docs**

2. 找到 **`execution`** 标签

3. 测试 **`POST /api/execute/run`** - 简单运行
   - 点击 "Try it out"
   - 输入：
     ```json
     {
       "code": "print('Hello from Piston!')",
       "language": "python",
       "question_id": 0,
       "test_mode": false
     }
     ```
   - 点击 "Execute"
   - 查看结果！

4. 测试 **`POST /api/execute/submit/1`** - Two Sum
   - 点击 "Try it out"
   - question_id = 1
   - 输入：
     ```json
     {
       "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target-num], i]\n        seen[num] = i\n    return []\n\nnums = eval(input())\ntarget = int(input())\nprint(twoSum(nums, target))",
       "language": "python",
       "test_mode": true
     }
     ```
   - 点击 "Execute"
   - 看到 4 个测试用例全部通过！ 🎉

---

#### 方法 B：使用 curl

```bash
# 测试 1：简单运行
curl -X POST "http://localhost:8000/api/execute/run" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello World\")",
    "language": "python"
  }'

# 测试 2：提交 Two Sum 解答
curl -X POST "http://localhost:8000/api/execute/submit/1" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target-num], i]\n        seen[num] = i\n    return []\n\nnums = eval(input())\ntarget = int(input())\nprint(twoSum(nums, target))",
    "language": "python"
  }'

# 测试 3：查看支持的语言
curl "http://localhost:8000/api/execute/supported-languages"
```

---

## 🎯 测试示例

### 示例 1：Hello World (Python)
```python
print("Hello from Piston!")
print("Python code execution works!")
```

**API 调用：**
```bash
curl -X POST "http://localhost:8000/api/execute/run" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from Piston!\")\nprint(\"Python works!\")", "language": "python"}'
```

**预期结果：**
```json
{
  "mode": "run",
  "result": {
    "success": true,
    "output": "Hello from Piston!\nPython works!\n",
    "error": null
  }
}
```

---

### 示例 2：Two Sum (完整测试)

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Read input
nums = eval(input())
target = int(input())

# Print result
print(twoSum(nums, target))
```

**预期结果：**
```json
{
  "mode": "test",
  "test_results": [
    {
      "test_case_id": 1,
      "input": "[2,7,11,15]\n9",
      "expected": "[0, 1]",
      "actual": "[0, 1]",
      "passed": true
    },
    {
      "test_case_id": 2,
      "input": "[3,2,4]\n6",
      "expected": "[1, 2]",
      "actual": "[1, 2]",
      "passed": true
    },
    {
      "test_case_id": 3,
      "input": "[3,3]\n6",
      "expected": "[0, 1]",
      "actual": "[0, 1]",
      "passed": true
    },
    {
      "test_case_id": 4,
      "input": "[1,5,3,7,9]\n12",
      "expected": "[2, 4]",
      "actual": "[2, 4]",
      "passed": true
    }
  ],
  "summary": {
    "total": 4,
    "passed": 4,
    "failed": 0,
    "pass_rate": 100.0
  }
}
```

✅ **全部通过！**

---

### 示例 3：JavaScript 代码
```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("World"));
console.log(greet("Piston"));
```

**API 调用：**
```bash
curl -X POST "http://localhost:8000/api/execute/run" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function greet(name) { return `Hello, ${name}!`; }\nconsole.log(greet(\"World\"));\nconsole.log(greet(\"Piston\"));",
    "language": "javascript"
  }'
```

---

### 示例 4：错误处理
```python
# 这段代码有语法错误
def broken_function()
    print("Missing colon")
```

**预期结果：**
```json
{
  "mode": "run",
  "result": {
    "success": false,
    "error": "SyntaxError: invalid syntax",
    "output": "",
    "compile_output": "..."
  }
}
```

---

## 📊 可用的 API 端点

### 1. 运行代码
```
POST /api/execute/run
```
简单执行代码，无测试用例

### 2. 提交代码（带测试）
```
POST /api/execute/submit/{question_id}
```
运行代码并验证所有测试用例

### 3. 获取起始代码
```
GET /api/execute/question/{question_id}/starter-code?language=python
```
获取题目的起始代码模板

### 4. 查看支持的语言
```
GET /api/execute/supported-languages
```
列出所有支持的编程语言

### 5. 获取提交历史
```
GET /api/execute/submissions/{user_id}/recent?limit=10
```
查看最近的代码提交记录

---

## 🌍 支持的语言

- ✅ Python 3.x
- ✅ JavaScript (Node.js)
- ✅ Java 17
- ✅ C++ 17
- ✅ C 11
- ✅ Go
- ✅ Rust
- ✅ TypeScript
- ✅ PHP
- ✅ Ruby
- ✅ Swift
- ✅ Kotlin

---

## 🎨 已添加的题目

### 1. Two Sum (Easy)
- **ID:** 1
- **LeetCode:** #1
- **测试用例:** 4 个
- **语言:** Python, JavaScript, Java

### 2. Valid Palindrome (Easy)
- **ID:** 2
- **LeetCode:** #125
- **测试用例:** 4 个
- **语言:** Python, JavaScript

---

## 🐛 常见问题

### Q: API 返回 404 错误？
**A:** 确保先运行了 `add_sample_questions.py` 添加题目

### Q: 代码执行超时？
**A:** 检查代码是否有无限循环，Piston 限制运行时间 5 秒

### Q: 输出格式不匹配？
**A:** 确保输出格式完全一致，包括空格和换行符

### Q: 连接 Piston API 失败？
**A:** 检查网络连接：
```bash
curl https://emkc.org/api/v2/piston/runtimes
```

---

## 📝 测试清单

完成测试后，你应该能够：

- [ ] ✅ 运行简单的 Python 代码
- [ ] ✅ 运行 JavaScript 代码
- [ ] ✅ 提交 Two Sum 并通过所有测试
- [ ] ✅ 提交 Valid Palindrome 并通过测试
- [ ] ✅ 看到错误的代码返回错误信息
- [ ] ✅ 获取题目的起始代码模板
- [ ] ✅ 查看支持的编程语言列表

---

## 🎉 成功！

如果上面的测试都通过了，恭喜！你现在拥有：

- ✨ **完整的代码执行系统**
- 🔒 **安全的沙箱环境**
- 📊 **自动化测试验证**
- 🌍 **多语言支持**
- 💾 **提交历史记录**

**这就是 LeetCode 的核心功能！** 🚀

---

## 📚 下一步

### 查看完整文档
- **详细实现：** `/CODE_EXECUTION_IMPLEMENTATION.md`
- **API 文档：** http://localhost:8000/docs

### 前端集成
- 添加代码编辑器 UI
- 实现测试结果展示
- 集成到 Quiz 页面

### 添加更多题目
- 参考 `scripts/add_sample_questions.py`
- 添加 LeetCode Hot 100 题目
- 配置更多测试用例

---

**准备好了吗？** 现在就开始测试吧！🎮

```bash
# 一键启动
cd backend && uvicorn main:app --reload

# 在另一个终端测试
curl -X POST "http://localhost:8000/api/execute/run" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"It works!\")", "language": "python"}'
```

---

*快速测试指南 - v1.0*
*让代码飞起来！✈️*


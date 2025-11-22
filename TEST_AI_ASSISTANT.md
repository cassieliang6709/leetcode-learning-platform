# 🧪 AI Assistant Testing Guide

## 快速测试指南

### 前提条件
- ✅ Backend 运行在 `http://localhost:8000`
- ✅ Frontend 运行在 `http://localhost:5173`
- ✅ 数据库已初始化
- ✅ SiliconFlow API Key 已配置

---

## Test 1: 检查 AI 服务健康状态

### 使用 curl 测试

```bash
curl http://localhost:8000/api/ai/health
```

**期望响应**：
```json
{
  "status": "healthy",
  "service": "SiliconFlow AI",
  "model": "Qwen/Qwen3-30B-A3B-Instruct-2507"
}
```

---

## Test 2: 测试自动 AI 建议

### Step 1: 提交错误代码

1. 打开浏览器访问 `http://localhost:5173/code-check`
2. 选择 "Two Sum" 问题
3. 输入**错误的代码**：

```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

4. 点击 **"✅ Submit"**

### Step 2: 查看 AI 建议

**期望结果**：
- ❌ 显示测试失败
- 🤖 自动显示 "AI Suggestion" 区域
- 📝 包含以下内容：
  - Root Cause Analysis（根本原因）
  - Key Insights（关键见解）
  - Hints（提示）
  - Edge Cases（边界情况）

**示例 AI 建议**：
```
🤖 AI Suggestion

Root Cause Analysis:
Your code has a bug where it can return the same 
index twice. When i equals j, you're using the 
same element twice, which violates the problem 
constraints.

Key Insights:
- The problem states "you may not use the same 
  element twice"
- Your nested loop allows i == j
- This causes incorrect results

Hints:
- Add a condition to skip when i == j
- Or better yet, use a hash map for O(n) solution
- Think: "Have I seen the complement before?"

Edge Cases:
- Empty array
- Array with only one element
- Duplicate values in array
```

---

## Test 3: 测试 AI 对话功能

### Step 1: 打开聊天窗口

1. 在 Code Check 页面
2. 点击右下角的 **💬 浮动按钮**
3. 聊天窗口弹出

### Step 2: 测试快速建议

点击预设问题按钮：
- "Explain the problem"
- "Debug my code"
- "Optimization tips"

**期望结果**：
- 消息自动填入输入框
- 或直接发送并获得回复

### Step 3: 自由对话

输入问题并测试：

**测试 1: 解释问题**
```
User: Can you explain what this problem is asking?

Expected AI Response:
The Two Sum problem asks you to find two numbers 
in an array that add up to a specific target value. 
You need to return the indices (positions) of 
these two numbers.

Example:
- Input: nums = [2, 7, 11, 15], target = 9
- Output: [0, 1]
- Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

**测试 2: 调试帮助**
```
User: Why is my code failing test case 2?

Expected AI Response:
Looking at your code and the failed test case, 
the issue is that you're allowing the same index 
to be used twice. In your nested loop, when i 
equals j, you're adding the same number to itself.

For test case 2:
- Input: [3, 2, 4], target = 6
- Your code might return [1, 1] instead of [1, 2]

To fix this, add a condition: if i != j before 
checking the sum.
```

**测试 3: 优化建议**
```
User: How can I make this code faster?

Expected AI Response:
Your current solution has O(n²) time complexity 
because of the nested loops. Here's how to 
optimize it to O(n):

Use a hash map approach:
1. Create an empty hash map
2. For each number, calculate: complement = target - num
3. Check if complement exists in hash map
4. If yes, return [hash_map[complement], current_index]
5. If no, add current number to hash map

This reduces time complexity from O(n²) to O(n)!
```

### Step 4: 测试多轮对话

```
User: What is a hash map?

AI: [Explains hash map]

User: Can you show me an example?

AI: [Shows example]

User: How do I implement it in Python?

AI: [Shows Python code]
```

**期望结果**：
- AI 记住对话上下文
- 回答连贯
- 不重复已说明的内容

---

## Test 4: UI 交互测试

### 测试聊天窗口

✅ **打开/关闭**：
- 点击浮动按钮打开
- 点击 ✕ 关闭
- 再次打开保持历史记录

✅ **发送消息**：
- 输入文本
- 点击 📤 发送
- 按 Enter 键发送
- Shift+Enter 换行

✅ **滚动行为**：
- 新消息自动滚动到底部
- 可以向上滚动查看历史
- 长消息正确显示

✅ **加载状态**：
- 发送后显示 "Thinking..."
- 输入框禁用
- 发送按钮显示 ⏳

✅ **错误处理**：
- 网络错误显示友好消息
- 可以重试
- 不影响已有对话

---

## Test 5: 响应式设计测试

### 桌面端 (> 1200px)
- 聊天窗口：420px 宽
- 位置：右下角
- 浮动按钮：60px

### 平板端 (768px - 1200px)
- 聊天窗口：380px 宽
- 位置：右下角
- 浮动按钮：55px

### 移动端 (< 768px)
- 聊天窗口：全宽（减去边距）
- 高度：70vh
- 浮动按钮：50px

---

## Test 6: 边界情况测试

### 测试空消息
1. 不输入任何内容
2. 点击发送按钮
3. **期望**：按钮禁用，无法发送

### 测试特殊字符
```
User: What about code with `backticks` and **bold**?
```
**期望**：正确显示，不破坏格式

### 测试长消息
```
User: [输入超过 1000 字的问题]
```
**期望**：
- 正确发送
- 消息框可滚动
- 不破坏布局

### 测试网络错误
1. 断开网络
2. 发送消息
3. **期望**：显示错误消息

### 测试 API 超时
1. 发送复杂问题
2. 等待超过 30 秒
3. **期望**：超时提示

---

## Test 7: 使用 curl 测试 API

### 测试失败建议 API

```bash
curl -X POST http://localhost:8000/api/ai/suggestion/failure \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "code": "def twoSum(nums, target):\n    return []",
    "language": "python",
    "test_results": [
      {
        "test_case_id": 1,
        "input": "nums = [2,7,11,15], target = 9",
        "expected": "[0, 1]",
        "actual": "[]",
        "passed": false
      }
    ]
  }'
```

**期望响应**：
```json
{
  "success": true,
  "suggestion": "Root Cause Analysis:\n...",
  "failed_count": 1,
  "question_title": "Two Sum"
}
```

### 测试聊天 API

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "code": "def twoSum(nums, target):\n    pass",
    "language": "python",
    "message": "Can you explain this problem?",
    "chat_history": null
  }'
```

**期望响应**：
```json
{
  "success": true,
  "response": "The Two Sum problem asks you to...",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 200,
    "total_tokens": 350
  }
}
```

---

## Test 8: 性能测试

### 响应时间

测量各操作的响应时间：

| 操作 | 期望时间 |
|------|----------|
| 打开聊天窗口 | < 100ms |
| 发送消息 | 2-5 秒 |
| 获取 AI 建议 | 3-8 秒 |
| 切换题目 | < 500ms |

### 并发测试

1. 同时发送多条消息
2. **期望**：按顺序处理，不混乱

---

## Test 9: 用户体验测试

### 场景 1: 新手用户第一次使用

1. 用户提交代码失败
2. 看到 AI 建议自动出现
3. 阅读建议
4. 修改代码
5. 再次提交

**评估**：
- AI 建议是否有帮助？
- 是否引导用户思考？
- 是否避免直接给答案？

### 场景 2: 用户主动寻求帮助

1. 用户不理解问题
2. 点击聊天按钮
3. 询问 "Can you explain this problem?"
4. 获得解释
5. 继续提问

**评估**：
- 对话是否流畅？
- AI 是否理解上下文？
- 回答是否有帮助？

### 场景 3: 用户寻求优化建议

1. 用户通过所有测试
2. 打开聊天
3. 询问 "How can I optimize this?"
4. 获得优化建议
5. 学习新方法

**评估**：
- 建议是否实用？
- 是否有代码示例？
- 是否解释了复杂度？

---

## 🐛 常见问题排查

### 问题 1: AI 建议不显示

**检查**：
- 测试是否真的失败了？
- 查看浏览器控制台错误
- 检查网络请求状态
- 验证 API Key 是否正确

**解决**：
```bash
# 检查后端日志
cd backend
# 查看终端输出

# 测试 API
curl http://localhost:8000/api/ai/health
```

### 问题 2: 聊天发送失败

**检查**：
- 网络连接
- API 端点是否正确
- 后端服务是否运行

**解决**：
```bash
# 重启后端
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 问题 3: AI 回复质量差

**可能原因**：
- Prompt 设计需要优化
- 模型参数需要调整
- 上下文信息不足

**优化**：
- 调整 `temperature` 参数
- 增加更多上下文
- 改进 prompt 模板

### 问题 4: 响应太慢

**优化**：
- 减少 `max_tokens`
- 使用更快的模型
- 添加缓存机制

---

## ✅ 测试检查清单

### 功能测试
- [ ] AI 建议自动显示
- [ ] 聊天窗口打开/关闭
- [ ] 发送消息成功
- [ ] 多轮对话正常
- [ ] 快速建议按钮工作
- [ ] 错误处理正确

### UI 测试
- [ ] 样式正确显示
- [ ] 动画流畅
- [ ] 响应式布局正常
- [ ] 移动端显示正确
- [ ] 滚动行为正确
- [ ] 加载状态显示

### 性能测试
- [ ] 响应时间合理
- [ ] 不阻塞主线程
- [ ] 内存使用正常
- [ ] 并发处理正确

### 用户体验测试
- [ ] 界面友好
- [ ] 操作直观
- [ ] 反馈及时
- [ ] 错误提示清晰

---

## 🎯 成功标准

✅ **功能完整**：所有功能正常工作
✅ **性能良好**：响应时间在预期范围内
✅ **用户友好**：界面直观，操作简单
✅ **错误处理**：优雅处理各种错误情况
✅ **AI 质量**：建议有帮助，回答准确

---

**测试状态**: 🧪 准备就绪
**最后更新**: 2025年11月22日


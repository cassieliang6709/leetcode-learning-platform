# 🚀 快速开始 - AI 功能使用指南

## 📋 新增功能概览

你的 Code Check 页面现在有了两个强大的 AI 功能：

1. **🤖 自动 AI 建议**：测试失败时自动生成帮助
2. **💬 AI 对话窗口**：随时与 AI 交流讨论代码

---

## 🎯 功能 1: 自动 AI 建议

### 如何触发？

当你提交代码后，如果有测试用例失败，AI 建议会**自动显示**！

### 使用步骤

1. **选择一个题目**（例如：Two Sum）
2. **编写代码**
3. **点击 "✅ Submit"**
4. 如果测试失败，在测试结果下方会自动出现：

```
┌─────────────────────────────────────────┐
│ 🤖 AI Suggestion                        │
├─────────────────────────────────────────┤
│ Root Cause Analysis:                    │
│ Your code has a bug where...            │
│                                         │
│ Key Insights:                           │
│ - Consider edge cases                   │
│ - Think about the algorithm             │
│                                         │
│ Hints:                                  │
│ - Try using a hash map                  │
│ - Check for duplicates                  │
└─────────────────────────────────────────┘
```

### 示例场景

**你的代码**：
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**测试失败**：
```
❌ Test Case 2
Input: [3, 2, 4], target = 6
Expected: [1, 2]
Your Output: [0, 0]  ← 错误！
```

**AI 自动建议**：
```
🤖 AI Suggestion

Root Cause Analysis:
Your nested loop allows i == j, which means you're 
using the same element twice. This violates the 
problem constraint "you may not use the same 
element twice."

Key Insights:
- When i equals j, you're checking if nums[i] + 
  nums[i] equals target
- This causes incorrect results when a number 
  happens to be half of the target

Hints:
- Add a condition: if i != j before checking sum
- Better approach: use a hash map to avoid nested 
  loops and naturally prevent using same index
- Think: "Have I seen the complement before?"

Edge Cases:
- Array with duplicate values
- Target that's twice a number in array
- Empty array or single element
```

---

## 🎯 功能 2: AI 对话窗口

### 如何打开？

点击页面右下角的 **💬 浮动按钮**！

### 使用步骤

1. **点击右下角 💬 按钮**
2. **对话窗口弹出**
3. **输入你的问题**
4. **按 Enter 或点击 📤 发送**
5. **AI 回复出现**
6. **继续对话**

### 快速开始

首次打开时，你会看到三个快速建议按钮：

```
┌─────────────────────────────────────┐
│ 🤖 AI Assistant              ✕     │
├─────────────────────────────────────┤
│                                     │
│ 👋 Hi! I'm your AI assistant.      │
│ Ask me anything about the problem!  │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Explain the problem             │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ Debug my code                   │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ Optimization tips               │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Type your message...]         📤  │
└─────────────────────────────────────┘
```

点击任何一个按钮，AI 会立即回答！

---

## 💡 使用场景示例

### 场景 1: 不理解题目

**你的问题**：
```
Can you explain what this problem is asking?
```

**AI 回复**：
```
🤖 The Two Sum problem asks you to find two 
numbers in an array that add up to a specific 
target value.

Given:
- An array of integers: nums
- A target integer: target

Return:
- The indices (positions) of the two numbers 
  that add up to target

Example:
nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Because: nums[0] + nums[1] = 2 + 7 = 9

Constraints:
- Each input has exactly one solution
- You can't use the same element twice
```

### 场景 2: 调试代码

**你的问题**：
```
Why is my code returning [0, 0] instead of [1, 2]?
```

**AI 回复**：
```
🤖 Looking at your code, the issue is in your 
nested loop. When i and j are both 0, you're 
checking if nums[0] + nums[0] equals target.

For the input [3, 2, 4] with target 6:
- When i=0, j=0: 3 + 3 = 6 ✓ (but wrong!)
- You return [0, 0]

The problem says "you may not use the same 
element twice", which means i must not equal j.

Quick fix:
Add this condition before checking the sum:
if i != j:
    if nums[i] + nums[j] == target:
        return [i, j]

This ensures you're using two different elements.
```

### 场景 3: 寻求优化

**你的问题**：
```
My code works but it's slow. How can I optimize it?
```

**AI 回复**：
```
🤖 Your current solution uses nested loops, 
giving O(n²) time complexity. Here's how to 
optimize it to O(n):

Use a Hash Map Approach:

1. Create an empty dictionary
2. For each number in the array:
   - Calculate: complement = target - current_num
   - Check if complement exists in dictionary
   - If yes: return [dict[complement], current_index]
   - If no: add current_num to dictionary

Why it's faster:
- Single loop: O(n)
- Dictionary lookup: O(1)
- Total: O(n) vs O(n²)

Example walkthrough:
nums = [2, 7, 11, 15], target = 9

Step 1: num=2, complement=7, dict={}, add 2
Step 2: num=7, complement=2, found! return [0,1]

Would you like me to show you the code?
```

### 场景 4: 学习概念

**你的问题**：
```
What is a hash map and why is it useful?
```

**AI 回复**：
```
🤖 Great question! A hash map (also called 
dictionary in Python) is a data structure that 
stores key-value pairs.

Think of it like a real dictionary:
- Key = word you look up
- Value = definition

Example in Python:
hash_map = {
    "apple": 1,
    "banana": 2,
    "orange": 3
}

Why it's useful:
1. Fast lookup: O(1) time
2. Fast insertion: O(1) time
3. Fast deletion: O(1) time

In Two Sum problem:
- Key = number from array
- Value = index of that number

hash_map = {
    2: 0,    # found 2 at index 0
    7: 1,    # found 7 at index 1
    11: 2,   # found 11 at index 2
}

When you need to find if 7 exists, instead of 
looping through the entire array (O(n)), you 
just check the hash map (O(1))!

This is why hash maps are so powerful for 
problems involving "finding" or "checking if 
something exists".
```

---

## ⌨️ 快捷操作

### 键盘快捷键

- **Enter**: 发送消息
- **Shift + Enter**: 换行（不发送）
- **Esc**: 关闭对话窗口（未来功能）

### 鼠标操作

- **点击 💬**: 打开/关闭对话窗口
- **点击 ✕**: 关闭对话窗口
- **点击快速建议**: 自动填入问题

---

## 🎨 界面说明

### AI 建议区域

```
┌────────────────────────────────────┐
│ 🤖 AI Suggestion    Analyzing...   │  ← 标题和加载状态
├────────────────────────────────────┤
│ [AI 建议内容]                      │  ← 自动生成的建议
└────────────────────────────────────┘
```

**颜色**：渐变蓝紫色边框
**位置**：测试结果下方
**触发**：自动（测试失败时）

### 浮动聊天按钮

```
                                  💬  ← 右下角浮动按钮
```

**样式**：圆形，渐变背景
**位置**：右下角固定
**动画**：悬停放大

### AI 对话窗口

```
┌─────────────────────────────────────┐
│ 🤖 AI Assistant              ✕     │  ← 头部
├─────────────────────────────────────┤
│                                     │
│ 👤 User                             │  ← 用户消息（蓝色）
│ ┌─────────────────────────────────┐ │
│ │ Can you help me?                │ │
│ └─────────────────────────────────┘ │
│                                     │
│                             🤖 AI   │  ← AI 消息（白色）
│ ┌─────────────────────────────────┐ │
│ │ Of course! What do you need?    │ │
│ └─────────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ [Type here...]                 📤  │  ← 输入区
└─────────────────────────────────────┘
```

---

## 💡 使用技巧

### 1. 先尝试自己解决

在寻求 AI 帮助之前：
- ✅ 仔细阅读题目
- ✅ 查看测试用例
- ✅ 尝试自己编写代码
- ✅ 运行测试看结果

### 2. 使用渐进式帮助

按顺序使用帮助功能：
1. 先看**提示系统**（💡 Strategy Hint）
2. 如果还不懂，看**自动 AI 建议**
3. 如果需要更多帮助，**打开聊天**

### 3. 提出具体问题

好的问题示例：
- ✅ "为什么我的代码在测试用例 2 失败？"
- ✅ "如何优化这个嵌套循环？"
- ✅ "什么时候应该使用 hash map？"

避免的问题：
- ❌ "帮我写代码"
- ❌ "答案是什么"
- ❌ "我不会"

### 4. 多轮对话

不要害怕继续提问：
```
You: What is a hash map?
AI: [Explains hash map]

You: Can you show me an example?
AI: [Shows example]

You: How do I use it in Python?
AI: [Shows Python code]
```

### 5. 学习而不是复制

AI 的目标是**帮你理解**，而不是直接给答案：
- 📚 理解 AI 的解释
- 💭 思考为什么这样做
- ✍️ 自己动手实现
- 🔄 测试并改进

---

## 🐛 常见问题

### Q: AI 建议没有出现？

**A**: 检查以下几点：
- 是否有测试用例失败？（只有失败才会触发）
- 等待几秒，AI 需要时间生成
- 查看浏览器控制台是否有错误
- 刷新页面重试

### Q: 聊天窗口打不开？

**A**: 
- 确保你已选择了一个题目
- 检查右下角是否有 💬 按钮
- 刷新页面重试
- 查看浏览器控制台错误

### Q: AI 回复很慢？

**A**: 
- 正常响应时间：3-8 秒
- 如果超过 10 秒，可能是网络问题
- 可以取消并重新发送

### Q: AI 的建议不准确？

**A**: 
- AI 是辅助工具，不是 100% 准确
- 结合自己的理解判断
- 可以继续提问澄清
- 使用聊天功能深入讨论

### Q: 对话历史会保存吗？

**A**: 
- 对话历史仅在当前会话保持
- 切换题目会清空历史
- 刷新页面会清空历史
- 不会保存到数据库

---

## 🎯 最佳实践

### 学习流程建议

```
1. 阅读题目 → 理解要求
   ↓
2. 查看测试用例 → 明确输入输出
   ↓
3. 思考解法 → 尝试编写代码
   ↓
4. 运行测试 → 查看结果
   ↓
5. 如果失败：
   ├─ 查看 AI 自动建议
   ├─ 理解问题所在
   ├─ 如需更多帮助，打开聊天
   └─ 修改代码重试
   ↓
6. 如果成功：
   ├─ 思考是否可以优化
   ├─ 询问 AI 优化建议
   └─ 学习更好的方法
```

### 提问技巧

**好的提问方式**：
```
✅ "我的代码在处理空数组时出错，应该如何处理？"
✅ "为什么使用 hash map 比嵌套循环更快？"
✅ "这道题有哪些常见的边界情况？"
✅ "我的时间复杂度是多少？如何优化？"
```

**避免的提问方式**：
```
❌ "给我答案"
❌ "帮我写代码"
❌ "这题怎么做"
❌ "我不会"
```

---

## 🎉 开始使用！

现在你已经了解了所有 AI 功能，开始你的编程学习之旅吧！

### 快速开始三步骤

1. **访问** `http://localhost:5173/code-check`
2. **选择** 一个题目开始
3. **编写** 代码并提交

记住：
- 💡 先尝试自己解决
- 🤖 失败时查看 AI 建议
- 💬 需要时打开聊天讨论
- 📚 重点是学习，不是答案

**Happy Coding! 🚀**

---

**文档版本**: 1.0
**最后更新**: 2025年11月22日


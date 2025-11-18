# 🎬 骨架屏加载效果测试指南

## 快速测试方法

### 方法 1：添加延迟代码（最简单）⭐

#### 测试 Roadmap 页面

1. 打开文件：`frontend/src/pages/RoadmapPage.jsx`

2. 在 `loadKnowledgePoints` 函数中添加延迟：

```javascript
const loadKnowledgePoints = async () => {
  try {
    // 👇 添加这行代码来延迟 2 秒
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const response = await api.getKnowledgePoints()
    setKnowledgePoints(response.data)
  } catch (error) {
    console.error('Error loading knowledge points:', error)
  } finally {
    setLoading(false)
  }
}
```

3. 保存文件，刷新浏览器
4. 访问 `/roadmap` 路径
5. 观察 2 秒的优雅骨架屏动画！

#### 测试 Quiz 页面

1. 打开文件：`frontend/src/pages/QuizPage.jsx`

2. 在 `loadQuestions` 函数中添加延迟：

```javascript
const loadQuestions = async () => {
  try {
    // 👇 添加这行代码来延迟 2 秒
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const response = await api.getQuizzesByKnowledge(knowledgePointId)
    setQuestions(response.data)
    if (response.data.length > 0) {
      setCurrentQuestion(response.data[0])
    }
  } catch (error) {
    console.error('Error loading questions:', error)
  } finally {
    setLoading(false)
  }
}
```

3. 保存文件，刷新浏览器
4. 访问任意题目页面
5. 观察骨架屏效果！

---

### 方法 2：使用 Chrome DevTools 网络限速

1. **打开开发者工具**
   - Windows/Linux: `F12` 或 `Ctrl + Shift + I`
   - Mac: `Cmd + Option + I`

2. **切换到 Network 标签**

3. **选择网络限速**
   - 点击 "No throttling" 下拉菜单
   - 选择 "Slow 3G" 或 "Fast 3G"

4. **刷新页面**
   - `F5` 或 `Cmd + R`
   - 观察加载过程中的骨架屏

5. **恢复正常速度**
   - 测试完成后选择 "No throttling"

---

### 方法 3：临时禁用加载完成

如果你想让骨架屏一直显示（用于截图或演示）：

```javascript
} finally {
  // setLoading(false)  // 👈 临时注释掉这行
}
```

**注意：** 记得测试完成后取消注释！

---

## 🎯 预期效果

### Roadmap 页面

```
┌─────────────────────────────────────────────────────┐
│ 侧边栏                     主内容区域               │
├─────────────┬───────────────────────────────────────┤
│             │  ██████ Learning Roadmap              │
│ Categories  │  ████ Master algorithms...            │
│             │                      ⚪ 0/10          │
│ 📚 ████████ │  ┌─────────────────────────────────┐ │
│ 📊 ████████ │  │ 🔢 ████  Easy                   │ │
│ 📝 ████████ │  │ ████████████                    │ │
│ 🌳 ████████ │  │ ████████████████                │ │
│ 🕸️ ████████ │  │ ██████    ████                  │ │
│ 🎯 ████████ │  └─────────────────────────────────┘ │
│ 🔧 ████████ │  ┌─────────────────────────────────┐ │
│             │  │ ...更多卡片...                   │ │
└─────────────┴───────────────────────────────────────┘
```

**动画效果：** 渐变光波从左到右扫过（1.5 秒循环）

### Quiz 页面

```
┌─────────────────────────────────────────────────────┐
│ Questions           题目详情                         │
├─────────────┬───────────────────────────────────────┤
│             │  ████████████████  [LeetCode]         │
│ Questions   │  ─────────────────────────────────────│
│             │  ████████████████████████             │
│ ████ ██████ │  ████████████████████                 │
│     Easy    │  ████████████████                     │
│             │  ██████████████                       │
│ ████ ██████ │  ┌────────────────────────────────┐  │
│   Medium    │  │ 💡 Get Hints                   │  │
│             │  │ ███████                        │  │
│ ████ ██████ │  │ [█████] [█████] [█████]        │  │
│     Hard    │  └────────────────────────────────┘  │
└─────────────┴───────────────────────────────────────┘
```

---

## 📸 截图建议

### 捕捉骨架屏效果

1. **延长延迟时间**
   ```javascript
   await new Promise(resolve => setTimeout(resolve, 10000)) // 10 秒
   ```

2. **打开页面**

3. **立即截图**（10 秒内）

4. **恢复代码**
   ```javascript
   // await new Promise(resolve => setTimeout(resolve, 10000)) // 注释掉
   ```

---

## 🎨 自定义测试

### 调整动画速度

编辑 `frontend/src/styles/skeleton.css`：

```css
.skeleton {
  /* 改变动画持续时间 */
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  
  /* 更快：0.8s */
  /* 更慢：2.5s */
}
```

### 调整颜色强度

```css
.skeleton {
  /* 改变不透明度 */
  opacity: 0.7;
  
  /* 更淡：0.5 */
  /* 更明显：0.9 */
}
```

---

## 🐛 故障排除

### 问题：看不到骨架屏效果

**可能原因：**
1. 数据加载太快
2. 延迟代码没有保存
3. 浏览器缓存问题

**解决方案：**
```bash
# 清除缓存
Ctrl/Cmd + Shift + R  # 硬刷新

# 或者
rm -rf frontend/node_modules/.vite
npm run dev
```

### 问题：骨架屏显示异常

**检查清单：**
- ✅ 是否引入了 `skeleton.css`
- ✅ CSS 变量是否正确设置
- ✅ 主题切换是否正常工作
- ✅ 浏览器是否支持 CSS 动画

---

## ⏱️ 推荐延迟时间

| 用途 | 延迟时间 | 说明 |
|------|----------|------|
| 快速预览 | 1000ms (1s) | 快速查看效果 |
| 正常测试 | 2000ms (2s) | 标准测试时间 |
| 详细观察 | 5000ms (5s) | 详细查看动画 |
| 截图/录屏 | 10000ms (10s) | 有足够时间操作 |

---

## 🎬 录屏演示

### 推荐工具
- **Windows**: Xbox Game Bar, OBS Studio
- **Mac**: QuickTime Player, Cmd + Shift + 5
- **Linux**: Kazam, SimpleScreenRecorder

### 录制步骤
1. 设置 5 秒延迟
2. 开始录屏
3. 刷新页面
4. 等待加载动画完成
5. 停止录屏
6. 编辑（可选）

---

## 🎯 测试检查清单

- [ ] Roadmap 页面骨架屏显示正常
- [ ] Quiz 页面骨架屏显示正常
- [ ] 深色主题下骨架屏正常
- [ ] 浅色主题下骨架屏正常
- [ ] 动画流畅（60fps）
- [ ] 移动端显示正常
- [ ] 平板端显示正常
- [ ] 桌面端显示正常
- [ ] 删除了测试延迟代码

---

## 📝 注意事项

### ⚠️ 测试完成后务必：

1. **删除或注释掉延迟代码**
   ```javascript
   // await new Promise(resolve => setTimeout(resolve, 2000)) // ❌ 删除这行
   ```

2. **取消注释 setLoading**
   ```javascript
   } finally {
     setLoading(false) // ✅ 确保这行没有被注释
   }
   ```

3. **恢复网络设置**
   - Chrome DevTools 设置回 "No throttling"

### ✅ 提交前检查

```bash
# 1. 确保代码干净
git diff

# 2. 确保没有遗留测试代码
grep -r "setTimeout.*2000" frontend/src/

# 3. 测试正常功能
npm run dev
```

---

## 🎉 完成！

现在你可以：
- ✨ 向用户展示专业的加载效果
- 📸 截图用于文档和宣传
- 🎬 录制演示视频
- 🚀 部署到生产环境

**享受 NeetCode 级别的用户体验！** 🎨

---

*测试愉快！有问题随时查看 `/SKELETON_LOADING.md` 完整文档。*


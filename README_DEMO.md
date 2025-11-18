# LeetCode Learning Platform - Demo

一个基于 AI 的算法学习平台，帮助用户系统化地学习 LeetCode 题目。

## 🚀 技术栈

### 后端
- **FastAPI** - 现代、快速的 Python Web 框架
- **SQLAlchemy** - Python SQL 工具包和 ORM
- **PostgreSQL** - 关系型数据库
- **asyncpg** - 异步 PostgreSQL 驱动

### 前端
- **React** - 用户界面库
- **Vite** - 下一代前端构建工具
- **React Router** - 单页应用路由
- **Axios** - HTTP 客户端

## 📁 项目结构

```
cs5001_project/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   └── routes/
│   │   │       ├── knowledge.py   # 知识点和学习计划
│   │   │       ├── quiz.py        # 练习题管理
│   │   │       └── code_check.py  # 代码检查
│   │   ├── services/       # 业务逻辑
│   │   │   └── ai_service.py     # AI 相关服务
│   │   ├── database.py     # 数据库连接
│   │   ├── models.py       # 数据库模型
│   │   └── schemas.py      # Pydantic 模型
│   ├── main.py             # FastAPI 应用入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # React 前端
│   ├── src/
│   │   ├── pages/         # 页面组件
│   │   │   ├── HomePage.jsx      # 首页和知识测试
│   │   │   ├── RoadmapPage.jsx   # 学习路线图
│   │   │   ├── QuizPage.jsx      # 练习题页面
│   │   │   └── CodeCheckPage.jsx # 代码检查页面
│   │   ├── services/      # API 服务
│   │   │   └── api.js
│   │   └── App.jsx        # 主应用组件
│   ├── package.json       # Node 依赖
│   └── vite.config.js     # Vite 配置
└── scripts/               # 工具脚本
    ├── init_db.py         # 数据库初始化
    └── create_db.sh       # 创建数据库脚本
```

## 🎯 核心功能

### 1. 知识点测试与学习规划
- 📝 用户完成初始测试评估当前水平
- 🤖 AI 分析测试结果生成个性化学习计划
- 📊 显示推荐的学习路径和时间估计

### 2. 学习路线图（Roadmap）
- 🗺️ 展示所有知识点的结构化学习路径
- 🎯 按难度和类别分类（数组、树、图等）
- ✅ 跟踪学习进度

### 3. 练习题系统
- 📚 每个知识点包含精选练习题
- 💡 三层提示系统：
  - **第一层**：算法策略提示（文字描述）
  - **第二层**：代码示例
  - **第三层**：YouTube 视频讲解链接
- 🔗 关联 LeetCode 题目编号

### 4. AI 代码检查
- 🔍 提交代码获取 AI 反馈
- ❌ 识别代码错误
- ✨ 提供改进建议
- 📝 生成修正后的代码
- ⚡ 复杂度分析

## 🛠️ 安装和运行

### 前置要求

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### 1. 数据库设置

#### macOS
```bash
# 安装 PostgreSQL
brew install postgresql
brew services start postgresql

# 创建数据库
cd scripts
chmod +x create_db.sh
./create_db.sh
```

#### Linux
```bash
# 安装 PostgreSQL
sudo apt-get install postgresql

# 创建数据库
cd scripts
chmod +x create_db.sh
./create_db.sh
```

或者手动创建：
```bash
psql -U postgres
CREATE DATABASE leetcode_learning;
\q
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（创建表并填充初始数据）
cd ..
python scripts/init_db.py

# 启动后端服务器
cd backend
uvicorn main:app --reload --port 8000
```

后端将运行在 http://localhost:8000
API 文档：http://localhost:8000/docs

### 3. 前端设置

打开新终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:5173

## 📊 数据库架构

### 主要表结构

- **users** - 用户信息
- **knowledge_points** - 知识点（数组、链表、树等）
- **knowledge_tests** - 用户知识测试记录
- **learning_plans** - 个性化学习计划
- **quiz_questions** - 练习题库
- **quiz_attempts** - 练习题尝试记录
- **code_submissions** - 代码提交记录

## 🎮 使用流程

1. **首页** - 完成知识点测试
   - 回答 3 个问题评估当前水平
   - 获取 AI 生成的学习计划

2. **Roadmap 页面** - 查看学习路线
   - 浏览所有知识点
   - 选择一个主题开始学习

3. **Quiz 页面** - 练习题目
   - 阅读题目描述
   - 需要帮助时请求提示
   - 完成后标记为已完成

4. **Code Check 页面** - 提交代码
   - 粘贴你的代码
   - 获取 AI 分析和建议
   - 查看修正后的代码

## 🧪 API 端点

### 知识点相关
- `GET /api/knowledge/points` - 获取所有知识点
- `POST /api/knowledge/test/{user_id}` - 提交知识测试
- `GET /api/knowledge/plan/{user_id}` - 获取学习计划

### 练习题相关
- `GET /api/quiz/by-knowledge/{knowledge_point_id}` - 获取知识点的题目
- `GET /api/quiz/{question_id}` - 获取题目详情
- `GET /api/quiz/{question_id}/hint/{level}` - 获取提示
- `POST /api/quiz/{question_id}/attempt/{user_id}` - 提交答题记录

### 代码检查相关
- `POST /api/code/check/{user_id}` - 检查代码
- `POST /api/code/hint/{question_id}/{user_id}` - 获取代码提示
- `GET /api/code/submissions/{user_id}` - 获取提交历史

## 🔧 配置

### 环境变量

在 `backend/` 目录创建 `.env` 文件：

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/leetcode_learning
OPENAI_API_KEY=your_openai_api_key_here  # 可选，用于真实的 AI 功能
```

## 🚧 当前限制（Demo 版本）

1. **AI 功能是模拟的** - 使用简单逻辑而非真实的 AI API
   - 学习计划生成使用预设规则
   - 代码分析使用基本的正则表达式
   - 练习题使用硬编码数据

2. **用户认证未实现** - 使用固定的 user_id=1

3. **题目库有限** - 仅包含示例题目

## 🎯 未来改进

### 短期目标
- [ ] 集成真实的 OpenAI API
- [ ] 添加用户认证系统
- [ ] 导入更多 LeetCode Hot 100 题目
- [ ] 添加代码执行功能

### 长期目标
- [ ] 实现社区讨论功能
- [ ] 添加学习统计和进度追踪
- [ ] 移动端应用
- [ ] 支持多语言界面

## 📝 开发注意事项

### 代码规范
- 每个文件不超过 500 行
- 使用有意义的变量名和函数名
- 添加必要的注释
- 保持代码简洁高效

### 提交规范
- 使用清晰的 commit 消息
- 每次提交一个功能或修复
- 提交前运行 linter

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

## 🆘 常见问题

### Q: 数据库连接失败怎么办？
A: 检查 PostgreSQL 是否正在运行：
```bash
# macOS
brew services list
# Linux
sudo systemctl status postgresql
```

### Q: 前端无法连接后端？
A: 确保：
1. 后端在 8000 端口运行
2. 检查 CORS 配置
3. 查看浏览器控制台的错误信息

### Q: 如何重置数据库？
A: 运行：
```bash
python scripts/init_db.py
```

### Q: 如何添加新的知识点？
A: 在 `scripts/init_db.py` 的 `seed_knowledge_points()` 函数中添加新的知识点，然后重新运行脚本。

---

**Happy Coding! 🎉**

如果遇到问题，请查看：
- 后端 API 文档：http://localhost:8000/docs
- 后端日志输出
- 浏览器开发者工具的 Console 和 Network 标签



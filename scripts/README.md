# Scripts 目录

这个目录包含了项目的数据库初始化和管理脚本。

## 主要脚本

### 1. 清理数据库
**文件**: `clean_and_reinit_db.py`

**功能**: 清空数据库中的所有题目和知识点数据，为重新导入做准备。

**使用方法**:
```bash
cd backend
source venv/bin/activate
PYTHONPATH=/path/to/backend python3 ../scripts/clean_and_reinit_db.py
```

**执行内容**:
- 删除所有 quiz_attempts (题目尝试记录)
- 删除所有 code_submissions (代码提交记录)
- 删除所有 quiz_questions (题目)
- 删除所有 knowledge_points (知识点)
- 重置 ID 序列

### 2. 初始化 LeetCode Hot 89 数据集
**文件**: `init_leetcode_hot100_complete.py`

**功能**: 导入 89 道精选 LeetCode 题目，每题包含完整的 3 级 Hint 系统。

**使用方法**:
```bash
cd backend
source venv/bin/activate
PYTHONPATH=/path/to/backend python3 ../scripts/init_leetcode_hot100_complete.py
```

**数据内容**:
- 13 个知识点分类
- 89 道 LeetCode 题目
- 每题 3 级 Hints（策略、代码、视频）
- YouTube 视频教程链接

**数据分布**:
- Array & Hash Table: 8 题
- Two Pointers: 6 题
- Sliding Window: 6 题
- Binary Search: 6 题
- Linked List: 8 题
- Stack: 6 题
- Binary Tree: 13 题
- Dynamic Programming: 13 题
- Graph: 7 题
- Greedy: 4 题
- Backtracking: 6 题
- Heap: 3 题
- Bit Manipulation: 3 题

### 3. 旧版初始化脚本
**文件**: `init_leetcode_hot100.py`

**状态**: 已弃用，保留用于参考

**说明**: 这是早期版本的初始化脚本，包含 19 道题目。建议使用 `init_leetcode_hot100_complete.py`。

### 4. 完整数据结构定义
**文件**: `leetcode_hot100_full.py`

**功能**: 定义了完整的 LeetCode Hot 100 题目结构模板。

**说明**: 这是一个数据结构定义文件，展示了如何组织题目数据。

### 5. 添加学习内容字段
**文件**: `add_learning_content.py`

**功能**: 为知识点表添加文章内容和阅读理解问题字段，支持 Duolingo 风格的学习流程。

**使用方法**:
```bash
cd backend
source venv/bin/activate
PYTHONPATH=/path/to/backend python3 ../scripts/add_learning_content.py
```

**执行内容**:
- 添加 `article_content` 字段（TEXT）- 英文文章讲解
- 添加 `reading_questions` 字段（JSON）- 阅读理解问题
- 可选：为第一个知识点添加示例内容

### 6. 其他脚本
- `init_db.py`: 基础数据库初始化（如果存在）
- `init_quiz_questions.py`: 早期的题目初始化脚本
- `migrate_add_quiz_fields.py`: 数据库迁移脚本

## 完整工作流程

### 重新初始化数据库

如果需要清空数据并重新导入：

```bash
# 1. 进入后端目录并激活虚拟环境
cd backend
source venv/bin/activate

# 2. 清理数据库
PYTHONPATH=/Users/liangyue/Documents/school/cs5001_project/backend \
python3 ../scripts/clean_and_reinit_db.py

# 3. 导入完整数据集
PYTHONPATH=/Users/liangyue/Documents/school/cs5001_project/backend \
python3 ../scripts/init_leetcode_hot100_complete.py

# 4. 添加学习内容字段（新功能）
PYTHONPATH=/Users/liangyue/Documents/school/cs5001_project/backend \
python3 ../scripts/add_learning_content.py
```

### 验证数据

```bash
# 查看题目总数
psql -d leetcode_learning -c "SELECT COUNT(*) FROM quiz_questions;"

# 查看知识点分布
psql -d leetcode_learning -c "
SELECT kp.name, COUNT(q.id) as count 
FROM knowledge_points kp 
LEFT JOIN quiz_questions q ON kp.id = q.knowledge_point_id 
GROUP BY kp.name 
ORDER BY count DESC;
"

# 验证 hints 完整性
psql -d leetcode_learning -c "
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN jsonb_array_length(hints::jsonb) = 3 THEN 1 END) as with_3_hints,
  COUNT(CASE WHEN video_link IS NOT NULL THEN 1 END) as with_video
FROM quiz_questions;
"
```

## 注意事项

### 环境要求
- Python 3.12+
- PostgreSQL 数据库
- 已安装 backend/requirements.txt 中的依赖

### PYTHONPATH 设置
脚本需要正确设置 PYTHONPATH 才能导入 backend 模块：
```bash
PYTHONPATH=/path/to/backend python3 script.py
```

### 数据库连接
确保数据库连接信息正确配置在：
- `backend/app/database.py` 中的 DATABASE_URL
- 或通过环境变量 DATABASE_URL 设置

### 清理数据的影响
⚠️ **警告**: `clean_and_reinit_db.py` 会删除所有题目、知识点及相关的用户提交记录。在生产环境使用前请务必备份数据！

## 添加新题目

要添加新题目，编辑 `init_leetcode_hot100_complete.py`：

```python
{
    "knowledge_point": "类别名称",
    "category": "category_slug",
    "difficulty": "easy/medium/hard",
    "description": "类别描述",
    "problems": [
        {
            "id": LeetCode题号,
            "title": "题目名称",
            "difficulty": "easy/medium/hard",
            "description": "题目描述",
            "video": "YouTube视频链接"
        }
    ]
}
```

然后重新运行初始化脚本即可。

## Hint 生成规则

当前使用模板化 Hint 生成，格式为：

**Hint 1 (Strategy)**:
```
For {title}: Analyze the problem and identify the key data structure 
and algorithm pattern. Consider the constraints and think about 
optimal time/space complexity.
```

**Hint 2 (Code)**:
```python
# {title} - {difficulty}
# Category: {category}
# Implement your solution here
# Time: O(?), Space: O(?)
```

**Hint 3 (Video)**:
```
Watch NeetCode's explanation for detailed walkthrough
```

如需更详细的 Hints，可以在数据结构中手动指定每道题的具体内容。

## 故障排查

### 常见问题

**问题**: `ModuleNotFoundError: No module named 'sqlalchemy'`  
**解决**: 确保已激活虚拟环境并安装依赖
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**问题**: `sqlalchemy.exc.ArgumentError: Textual SQL expression should be declared as text()`  
**解决**: 已在 `clean_and_reinit_db.py` 中修复，使用 `text()` 包装 SQL 语句

**问题**: 数据库连接失败  
**解决**: 检查 PostgreSQL 服务是否运行，数据库是否存在
```bash
psql -l  # 列出所有数据库
createdb leetcode_learning  # 如果数据库不存在
```

## 文件结构

```
scripts/
├── README.md                          # 本文件
├── clean_and_reinit_db.py            # 清理数据库脚本
├── init_leetcode_hot100_complete.py  # 完整数据集初始化（推荐）
├── init_leetcode_hot100.py           # 旧版初始化脚本
├── leetcode_hot100_full.py           # 数据结构定义
├── init_db.py                         # 基础数据库初始化
├── init_quiz_questions.py            # 早期题目初始化
└── migrate_add_quiz_fields.py        # 数据库迁移
```

## 更新日志

### 2025-11-22
- ✅ 创建 `add_learning_content.py` 迁移脚本
- ✅ 添加知识点文章内容和阅读问题字段
- ✅ 实现 Duolingo 风格的学习流程
- ✅ 支持文章 → Q&A → 练习题的学习路径

### 2025-11-21
- ✅ 创建 `clean_and_reinit_db.py` 清理脚本
- ✅ 创建 `init_leetcode_hot100_complete.py` 完整数据集
- ✅ 成功导入 89 道 LeetCode 题目
- ✅ 每题包含 3 级 Hints 和视频链接
- ✅ 添加本 README 文档

### 早期版本
- 创建基础初始化脚本
- 导入 19 道示例题目

## 联系与支持

如有问题或建议，请查看项目主 README 或相关文档。

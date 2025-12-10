# Code Execution System - 系统设计文档

## 📋 文档概述

本文档详细描述了 LeetCode Learning Platform 的代码执行系统的架构设计、技术选型、数据流程和实现细节。

---

## 🎯 系统目标

### 核心功能
1. **多语言支持**：支持 Python, JavaScript, Java, C++, C, Go, Rust 等主流编程语言
2. **安全执行**：在隔离的沙箱环境中执行用户代码，防止恶意代码攻击
3. **测试验证**：支持多个测试用例的自动化测试和结果对比
4. **性能监控**：记录代码执行时间和内存使用情况
5. **实时反馈**：提供即时的执行结果、错误信息和 AI 建议

### 设计原则
- **安全第一**：所有代码在隔离环境中执行
- **快速响应**：执行超时限制 5 秒，确保用户体验
- **可扩展性**：易于添加新的编程语言支持
- **容错性**：完善的错误处理和降级策略

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐    │
│  │ Monaco Editor│  │ Test Results │  │  AI Suggestions   │    │
│  └──────────────┘  └──────────────┘  └───────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS/REST API
┌────────────────────────────┴────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Code Execution Router                          │  │
│  │  • POST /api/execution/submit/{question_id}              │  │
│  │  • GET  /api/execution/question/{id}/starter-code        │  │
│  │  • GET  /api/execution/supported-languages               │  │
│  │  • GET  /api/execution/submissions/{user_id}/recent      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         PistonExecutor Service                           │  │
│  │  • execute_code() - 单次执行                             │  │
│  │  • run_test_cases() - 批量测试                           │  │
│  │  • get_supported_languages() - 语言查询                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Database Layer                              │  │
│  │  • Save submissions (PostgreSQL)                         │  │
│  │  • Store test results                                    │  │
│  │  • Track user history                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS API
┌────────────────────────────┴────────────────────────────────────┐
│                    Piston API (Third-party)                     │
│                  https://emkc.org/api/v2/piston                 │
│  • 隔离的容器环境                                               │
│  • 多语言运行时支持                                             │
│  • 资源限制和超时控制                                           │
└─────────────────────────────────────────────────────────────────┘
```

### 架构层次

#### 1. 前端层 (Frontend)
- **Monaco Editor**：专业的代码编辑器，支持语法高亮和智能提示
- **Test Results Panel**：展示测试用例执行结果
- **AI Suggestions**：集成 AI 分析，提供代码优化建议
- **Real-time Feedback**：即时显示执行状态和错误信息

#### 2. API 层 (Backend Routes)
- **路由处理**：接收前端请求，参数验证
- **权限控制**：用户认证和授权
- **请求转发**：调用执行服务
- **响应封装**：统一的响应格式

#### 3. 服务层 (Executor Service)
- **代码预处理**：添加必要的导入和类型声明
- **测试执行**：批量运行测试用例
- **结果分析**：对比实际输出和期望输出
- **性能统计**：记录执行时间和资源使用

#### 4. 数据层 (Database)
- **提交记录**：保存用户代码和语言
- **测试结果**：存储每次测试的详细结果
- **AI 反馈**：保存 AI 分析结果
- **历史追踪**：用户提交历史

#### 5. 执行层 (Piston API)
- **容器隔离**：每次执行在独立容器中运行
- **资源限制**：CPU、内存和时间限制
- **多语言支持**：预装多种编程语言运行时
- **安全保护**：防止恶意代码和资源滥用

---

## 🔧 核心模块

### 1. PistonExecutor 类

#### 职责
封装 Piston API 的调用逻辑，提供统一的代码执行接口。

#### 主要方法

```python
class PistonExecutor:
    """Piston API client for executing code"""
    
    BASE_URL = "https://emkc.org/api/v2/piston"
    
    async def execute_code(
        self,
        code: str,
        language: str,
        stdin: str = "",
        args: List[str] = None
    ) -> Dict[str, Any]:
        """
        执行单次代码
        
        参数:
            code: 源代码
            language: 编程语言
            stdin: 标准输入
            args: 命令行参数
            
        返回:
            {
                "success": bool,
                "output": str,
                "error": str,
                "compile_output": str,
                "run_time": int,
                "memory": int
            }
        """
    
    async def run_test_cases(
        self,
        code: str,
        language: str,
        test_cases: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量运行测试用例
        
        返回:
            [
                {
                    "test_case_id": int,
                    "input": str,
                    "expected": str,
                    "actual": str,
                    "passed": bool,
                    "error": str,
                    "run_time": int
                }
            ]
        """
```

#### 特性

1. **语言映射**
```python
LANGUAGE_MAP = {
    "python": "python",
    "javascript": "javascript",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "go": "go",
    "rust": "rust",
}
```

2. **代码预处理**
```python
def _preprocess_code(self, code: str, language: str) -> str:
    """
    为 Python 代码自动添加 typing 导入
    解决 LeetCode 风格代码的类型提示问题
    """
    if language == "python":
        if "from typing import" not in code:
            return "from typing import List, Dict, Optional, Set, Tuple, Any\n\n" + code
    return code
```

3. **超时控制**
```python
payload = {
    "compile_timeout": 10000,  # 编译超时 10 秒
    "run_timeout": 5000,       # 运行超时 5 秒
}
```

4. **错误处理**
- 编译错误检测
- 运行时错误捕获
- 超时异常处理
- 网络错误降级

---

### 2. Code Execution Router

#### API 端点

##### 1. 提交代码执行
```http
POST /api/execution/submit/{question_id}

Request Body:
{
    "code": "def twoSum(nums, target):\n    ...",
    "language": "python"
}

Response:
{
    "mode": "test",
    "test_results": [
        {
            "test_case_id": 1,
            "input": "[2,7,11,15]\n9",
            "expected": "[0,1]",
            "actual": "[0,1]",
            "passed": true,
            "error": "",
            "run_time": 45
        }
    ],
    "summary": {
        "total": 5,
        "passed": 5,
        "failed": 0,
        "pass_rate": 100.0
    }
}
```

##### 2. 获取起始代码
```http
GET /api/execution/question/{question_id}/starter-code?language=python

Response:
{
    "question_id": 1,
    "language": "python",
    "code": "from typing import List\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        pass",
    "available_languages": ["python", "javascript", "java", "cpp"]
}
```

##### 3. 支持的语言列表
```http
GET /api/execution/supported-languages

Response:
{
    "languages": [
        {
            "language": "python",
            "version": "3.x",
            "display_name": "Python 3"
        }
    ],
    "default": "python"
}
```

##### 4. 最近提交记录
```http
GET /api/execution/submissions/{user_id}/recent?limit=10

Response:
{
    "submissions": [
        {
            "id": 123,
            "question_id": 1,
            "language": "python",
            "created_at": "2024-12-09T10:30:00Z",
            "passed": true
        }
    ]
}
```

---

### 3. 数据模型

#### CodeSubmission 模型

```python
class CodeSubmission(Base):
    __tablename__ = "code_submissions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    code = Column(Text, nullable=False)
    language = Column(String(20), default="python")
    ai_feedback = Column(JSON)  # 存储测试结果和 AI 分析
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

#### QuizQuestion 模型

```python
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    difficulty = Column(String(20))  # easy, medium, hard
    
    # 代码执行相关字段
    test_cases = Column(JSON)
    # Format: [{"input": "...", "expected": "..."}]
    
    starter_code = Column(JSON)
    # Format: {"python": "...", "javascript": "...", "java": "..."}
```

#### 测试用例格式

```json
{
    "test_cases": [
        {
            "input": "[2,7,11,15]\n9",
            "expected": "[0,1]"
        },
        {
            "input": "[3,2,4]\n6",
            "expected": "[1,2]"
        }
    ]
}
```

---

## 🔄 执行流程

### 完整执行流程图

```
┌─────────┐
│ 用户编写 │
│   代码   │
└────┬────┘
     │
     ↓
┌─────────────────┐
│ 点击 Submit 按钮 │
└────┬────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ Frontend: 调用 API                    │
│ POST /api/execution/submit/{id}       │
│ { code, language }                    │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ Backend Router:                       │
│ 1. 验证参数                           │
│ 2. 查询题目信息和测试用例              │
│ 3. 调用 execute_user_code()           │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ PistonExecutor:                       │
│ 1. 预处理代码（添加导入等）            │
│ 2. 遍历测试用例                       │
│ 3. 对每个测试用例调用 execute_code()   │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ Piston API:                           │
│ 1. 创建隔离容器                       │
│ 2. 编译代码（如需要）                  │
│ 3. 执行代码                           │
│ 4. 捕获输出和错误                     │
│ 5. 返回结果                           │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ PistonExecutor:                       │
│ 1. 收集所有测试结果                   │
│ 2. 对比实际输出 vs 期望输出            │
│ 3. 计算统计信息（通过率等）            │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ Backend Router:                       │
│ 1. 保存 CodeSubmission 到数据库       │
│ 2. 返回结果给前端                     │
└────┬─────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────┐
│ Frontend:                             │
│ 1. 显示测试结果（通过/失败）           │
│ 2. 如果失败，自动调用 AI 获取建议      │
│ 3. 如果全部通过，获取优化建议          │
└──────────────────────────────────────┘
```

### 关键步骤详解

#### Step 1: 前端提交
```javascript
const handleSubmit = async () => {
  setLoading(true)
  const response = await api.submitCode(questionId, code, language)
  setTestResults(response.data)
  
  // 根据结果决定后续操作
  if (response.data.summary?.failed > 0) {
    fetchAiSuggestion(response.data.test_results)
  } else {
    fetchOptimizationSuggestion()
  }
}
```

#### Step 2: 后端处理
```python
@router.post("/submit/{question_id}")
async def submit_code(question_id: int, request: CodeExecutionRequest, db: AsyncSession):
    # 1. 获取题目和测试用例
    question = await db.get(QuizQuestion, question_id)
    
    # 2. 执行代码
    execution_result = await execute_user_code(
        code=request.code,
        language=request.language,
        test_cases=question.test_cases
    )
    
    # 3. 保存提交记录
    submission = CodeSubmission(
        user_id=user_id,
        question_id=question_id,
        code=request.code,
        language=request.language,
        ai_feedback=execution_result
    )
    db.add(submission)
    await db.commit()
    
    return execution_result
```

#### Step 3: 执行服务
```python
async def execute_user_code(code: str, language: str, test_cases: List[Dict]) -> Dict:
    executor = get_executor()
    
    if test_cases:
        # 批量测试模式
        results = await executor.run_test_cases(code, language, test_cases)
        
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        
        return {
            "mode": "test",
            "test_results": results,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": (passed / total * 100) if total > 0 else 0
            }
        }
```

---

## 🛡️ 安全性设计

### 1. 沙箱隔离

- **容器隔离**：每次执行在独立的 Docker 容器中运行
- **网络隔离**：容器无法访问外部网络
- **文件系统隔离**：容器只能访问临时文件系统
- **进程隔离**：限制子进程创建

### 2. 资源限制

```json
{
    "compile_timeout": 10000,     // 编译超时 10 秒
    "run_timeout": 5000,          // 运行超时 5 秒
    "compile_memory_limit": -1,   // 编译内存限制（由 Piston 控制）
    "run_memory_limit": -1        // 运行内存限制（由 Piston 控制）
}
```

### 3. 输入验证

- **代码长度限制**：防止超大代码提交
- **语言白名单**：只允许支持的编程语言
- **SQL 注入防护**：使用 SQLAlchemy ORM
- **XSS 防护**：前端输出转义

### 4. 错误处理

```python
try:
    response = await self.client.post(f"{self.BASE_URL}/execute", json=payload)
    response.raise_for_status()
except httpx.TimeoutException:
    return {"success": False, "error": "Execution timeout (5 seconds limit)"}
except httpx.HTTPError as e:
    return {"success": False, "error": f"API error: {str(e)}"}
except Exception as e:
    return {"success": False, "error": f"Execution error: {str(e)}"}
```

---

## ⚡ 性能优化

### 1. 异步执行

```python
# 使用异步 HTTP 客户端
self.client = httpx.AsyncClient(timeout=30.0)

# 所有执行方法都是异步的
async def execute_code(...) -> Dict:
    response = await self.client.post(...)
```

### 2. 连接复用

```python
# 全局 Executor 实例，复用 HTTP 连接
_executor = None

def get_executor() -> PistonExecutor:
    global _executor
    if _executor is None:
        _executor = PistonExecutor()
    return _executor
```

### 3. 批量测试优化

- **顺序执行**：测试用例按顺序执行，避免并发资源竞争
- **早停策略**：可以添加失败后立即停止的选项
- **结果缓存**：相同代码相同输入可以缓存结果（可选）

### 4. 数据库优化

```python
# 使用异步 ORM
async with AsyncSession(engine) as session:
    # 批量插入
    session.add_all(submissions)
    await session.commit()
```

---

## 📊 监控和日志

### 1. 执行监控

需要监控的指标：
- **成功率**：成功执行 / 总执行次数
- **平均执行时间**：所有测试用例的平均时间
- **超时率**：超时次数 / 总执行次数
- **错误率**：各类错误的分布

### 2. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

# 记录关键操作
logger.info(f"Executing code for user {user_id}, question {question_id}, language {language}")
logger.error(f"Execution failed: {error_message}")
logger.warning(f"Execution timeout for question {question_id}")
```

### 3. 性能追踪

```python
import time

start_time = time.time()
result = await executor.execute_code(code, language)
execution_time = time.time() - start_time

logger.info(f"Execution completed in {execution_time:.2f}s")
```

---

## 🔮 扩展性设计

### 1. 支持新语言

添加新语言只需要：

```python
# 1. 在 LANGUAGE_MAP 中添加映射
LANGUAGE_MAP = {
    # ... existing languages
    "kotlin": "kotlin",  # 新增
}

# 2. 添加文件扩展名映射
def _get_filename(self, language: str) -> str:
    extensions = {
        # ... existing extensions
        "kotlin": "main.kt",  # 新增
    }
    return extensions.get(language.lower(), "main.txt")

# 3. 如有需要，添加预处理逻辑
def _preprocess_code(self, code: str, language: str) -> str:
    if language == "kotlin":
        # Kotlin 特定的预处理
        pass
```

### 2. 自定义执行器

可以添加其他执行引擎：

```python
class LocalExecutor:
    """本地执行器（用于开发环境）"""
    async def execute_code(self, code, language, stdin=""):
        # 本地执行逻辑
        pass

class AWSLambdaExecutor:
    """AWS Lambda 执行器（用于生产环境）"""
    async def execute_code(self, code, language, stdin=""):
        # Lambda 执行逻辑
        pass
```

### 3. 结果处理插件

```python
class ResultProcessor:
    """结果处理基类"""
    async def process(self, result: Dict) -> Dict:
        pass

class ComplexityAnalyzer(ResultProcessor):
    """复杂度分析"""
    async def process(self, result: Dict) -> Dict:
        # 分析时间和空间复杂度
        pass

class CodeStyleChecker(ResultProcessor):
    """代码风格检查"""
    async def process(self, result: Dict) -> Dict:
        # 检查代码风格
        pass
```

---

## 🚀 部署建议

### 1. 环境配置

```bash
# .env 文件
PISTON_API_URL=https://emkc.org/api/v2/piston
EXECUTION_TIMEOUT=5
COMPILE_TIMEOUT=10
MAX_CODE_LENGTH=50000
```

### 2. 依赖项

```txt
# requirements.txt
fastapi>=0.104.0
httpx>=0.25.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
```

### 3. Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. 扩展部署

- **水平扩展**：可以部署多个 Backend 实例
- **负载均衡**：使用 Nginx 或云负载均衡器
- **缓存层**：Redis 缓存常见测试结果
- **CDN**：静态资源（Monaco Editor）使用 CDN

---

## 📝 最佳实践

### 1. 代码提交

```python
# ✅ 好的实践：使用函数式代码
def twoSum(nums, target):
    # 用户只需要实现核心逻辑
    pass

# ❌ 避免：全局副作用
import sys
sys.exit(0)  # 这会影响测试执行
```

### 2. 测试用例设计

```json
{
    "test_cases": [
        {
            "input": "简单输入",
            "expected": "预期输出"
        },
        {
            "input": "边界情况",
            "expected": "边界输出"
        },
        {
            "input": "大数据量",
            "expected": "性能测试"
        }
    ]
}
```

### 3. 错误提示

```python
# 提供清晰的错误信息
if result.get("error"):
    return {
        "success": False,
        "error": "Your code has a runtime error",
        "details": result["error"],
        "suggestion": "Check line 5: division by zero"
    }
```

---

## 🐛 常见问题

### 1. 超时问题

**问题**：代码执行超时
**原因**：
- 算法复杂度过高
- 死循环
- 递归深度过大

**解决**：
- 提示用户优化算法
- AI 分析并提供优化建议
- 增加超时前的警告

### 2. 内存问题

**问题**：内存不足
**原因**：
- 创建过大的数据结构
- 内存泄漏

**解决**：
- 限制输入数据大小
- 提供内存使用提示

### 3. 编译错误

**问题**：代码无法编译
**原因**：
- 语法错误
- 缺少依赖

**解决**：
- 前端 Linter 实时检查
- 提供详细的编译错误信息
- Starter Code 包含必要的导入

### 4. 输出格式不匹配

**问题**：实际输出和期望输出不一致
**原因**：
- 多余的调试输出
- 输出格式不正确

**解决**：
```python
# ❌ 避免额外输出
print("Debug info")
print(result)

# ✅ 只返回结果
return result
```

---

## 📈 未来优化方向

### 1. 功能增强

- [ ] **实时执行**：边写边执行，提供即时反馈
- [ ] **协作调试**：多人共享代码和结果
- [ ] **性能基准**：与其他用户的解决方案对比
- [ ] **可视化调试**：显示变量变化和执行路径
- [ ] **代码回放**：查看历史提交和结果

### 2. 性能提升

- [ ] **结果缓存**：缓存相同代码的执行结果
- [ ] **预热容器**：预先启动容器减少冷启动时间
- [ ] **并行测试**：对独立的测试用例并行执行
- [ ] **边缘计算**：部署边缘节点减少延迟

### 3. 安全加固

- [ ] **代码静态分析**：执行前扫描恶意代码
- [ ] **资源配额**：每用户每日执行次数限制
- [ ] **审计日志**：记录所有执行历史
- [ ] **异常检测**：自动识别可疑行为

### 4. 用户体验

- [ ] **智能提示**：根据错误类型提供针对性建议
- [ ] **代码模板**：提供常见算法模板
- [ ] **快捷键支持**：Vim/Emacs 模式
- [ ] **主题自定义**：多种编辑器主题

---

## 📚 参考资料

### 技术文档

1. **Piston API**
   - 官方文档: https://github.com/engineer-man/piston
   - API 端点: https://emkc.org/api/v2/piston

2. **FastAPI**
   - 官方文档: https://fastapi.tiangolo.com/
   - 异步编程: https://fastapi.tiangolo.com/async/

3. **Monaco Editor**
   - 官方文档: https://microsoft.github.io/monaco-editor/
   - React 集成: https://github.com/suren-atoyan/monaco-react

### 相关项目

1. **LeetCode**：https://leetcode.com/
2. **HackerRank**：https://www.hackerrank.com/
3. **CodeSignal**：https://codesignal.com/
4. **Exercism**：https://exercism.org/

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- **Issues**：提交 GitHub Issue
- **Email**：技术支持邮箱
- **文档更新**：2024-12-09

---

## 附录

### A. API 完整示例

#### 提交代码
```bash
curl -X POST "http://localhost:8000/api/execution/submit/1" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i",
    "language": "python"
  }'
```

#### 响应示例
```json
{
    "mode": "test",
    "test_results": [
        {
            "test_case_id": 1,
            "input": "[2,7,11,15]\n9",
            "expected": "[0,1]",
            "actual": "[0,1]",
            "passed": true,
            "error": "",
            "run_time": 45,
            "memory": 0
        }
    ],
    "summary": {
        "total": 5,
        "passed": 5,
        "failed": 0,
        "pass_rate": 100.0
    }
}
```

### B. 错误代码对照表

| 错误代码 | 含义 | 处理方式 |
|---------|------|---------|
| 400 | 请求参数错误 | 检查代码格式和语言 |
| 404 | 题目不存在 | 确认题目 ID |
| 408 | 执行超时 | 优化算法复杂度 |
| 500 | 服务器错误 | 联系技术支持 |
| 503 | Piston API 不可用 | 稍后重试 |

### C. 支持的语言版本

| 语言 | 版本 | 备注 |
|------|------|------|
| Python | 3.10+ | 支持类型提示 |
| JavaScript | Node.js 18+ | ES2022 |
| Java | JDK 17 | 标准库 |
| C++ | C++17 | STL |
| C | C11 | 标准库 |
| Go | 1.19+ | 标准库 |
| Rust | 1.70+ | 标准库 |

---

**文档版本**: v1.0  
**最后更新**: 2024-12-09  
**维护者**: LeetCode Learning Platform Team


# Code Execution Feature - LeetCode Style Implementation

## 📋 Overview

The Code Check page has been upgraded to provide a **real LeetCode-style coding experience** with the following features:

### ✨ New Features

1. **Real Code Execution** 🚀
   - Run code directly in the browser
   - Execute against test cases
   - Get immediate feedback on correctness

2. **Three Action Modes** 🎯
   - **Run Code**: Quick test without test cases (like LeetCode's "Run Code")
   - **Submit**: Run all test cases and get pass/fail results (like LeetCode's "Submit")
   - **AI Check**: Get AI-powered code review and suggestions

3. **Starter Code Templates** 📝
   - Auto-load language-specific starter code
   - Switch between Python, JavaScript, Java, C++
   - Maintains code when switching problems

4. **Test Cases Display** 📊
   - View all test cases before coding
   - See input and expected output
   - Understand requirements clearly

5. **Detailed Test Results** ✅❌
   - Pass/fail status for each test case
   - Side-by-side comparison of expected vs actual output
   - Runtime information
   - Error messages and stack traces

---

## 🏗️ Architecture

### Backend Components

#### 1. Code Execution Service (`backend/app/services/code_executor.py`)
- Uses **Piston API** for secure code execution
- Supports multiple programming languages
- Handles test case execution and comparison
- Returns detailed results with timing information

#### 2. Execution API Routes (`backend/app/api/routes/code_execution.py`)
```
POST /api/execution/run
  - Quick code execution without test cases
  - Returns: output, errors, runtime

POST /api/execution/submit/{question_id}
  - Execute code against all test cases
  - Returns: test results, pass/fail summary
  - Saves submission to database

GET /api/execution/question/{question_id}/starter-code
  - Get starter code template for a language
  - Returns: code template, available languages

GET /api/execution/supported-languages
  - List all supported programming languages
```

#### 3. Database Models (`backend/app/models.py`)
```python
class QuizQuestion:
    test_cases: JSON  # [{"input": "...", "expected": "..."}]
    starter_code: JSON  # {"python": "...", "javascript": "..."}
    
class CodeSubmission:
    code: Text
    language: String
    ai_feedback: JSON  # Stores test results
```

### Frontend Components

#### 1. Updated API Service (`frontend/src/services/api.js`)
```javascript
// New endpoints
runCode(code, language)
submitCode(questionId, code, language)
getStarterCode(questionId, language)
getSupportedLanguages()
```

#### 2. Enhanced CodeCheckPage (`frontend/src/pages/CodeCheckPage.jsx`)

**New State Variables:**
- `testResults`: Stores test case execution results
- `runOutput`: Stores simple run output
- `activeTab`: Switches between 'testcases' and 'result' views

**New Functions:**
- `handleRun()`: Execute code without test cases
- `handleSubmit()`: Submit code and run all test cases
- `handleAICheck()`: Get AI code review
- `loadStarterCode()`: Load language-specific templates
- `handleLanguageChange()`: Switch language and reload starter code

**New UI Components:**
- **Result Tabs**: Switch between Test Cases and Results
- **Action Buttons**: Run, Submit, AI Check
- **Test Cases Panel**: Display all test cases
- **Test Results Panel**: Show detailed pass/fail results
- **Run Output Panel**: Display simple execution output

---

## 🎨 User Interface

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    🤖 LeetCode Code Check                    │
└─────────────────────────────────────────────────────────────┘

┌──────────┬─────────────────────────────┬──────────────────┐
│          │                             │                  │
│ Problems │   Problem Description       │  📋 Test Cases   │
│ Sidebar  │   + Hints                   │  📊 Results      │
│          │   + Code Editor             │                  │
│          │   [Run] [Submit] [AI Check] │                  │
│          │                             │                  │
└──────────┴─────────────────────────────┴──────────────────┘
```

### Test Results Display

**Success Case:**
```
✅ Accepted
3 / 3 test cases passed (100.0%)

✅ Test Case 1                          45ms
Input: [2,7,11,15], target = 9
Expected: [0,1]
Your Output: [0,1]
```

**Failure Case:**
```
❌ Wrong Answer
1 / 3 test cases passed (33.3%)

❌ Test Case 2                          52ms
Input: [3,2,4], target = 6
Expected: [1,2]
Your Output: [0,2]
```

---

## 🔧 How It Works

### 1. User Selects a Problem
```javascript
selectProblem(problemId)
  → getProblemDetail(problemId)
  → loadStarterCode(problemId, language)
  → Display problem description
  → Display test cases
  → Load starter code into editor
```

### 2. User Clicks "Run Code"
```javascript
handleRun()
  → api.runCode(code, language)
  → Piston API executes code
  → Display output in Results tab
```

### 3. User Clicks "Submit"
```javascript
handleSubmit()
  → api.submitCode(questionId, code, language)
  → Piston API runs each test case
  → Compare actual vs expected output
  → Display detailed results
  → Save submission to database
```

### 4. User Clicks "AI Check"
```javascript
handleAICheck()
  → api.checkCode(userId, submissionData)
  → AI analyzes code
  → Display errors, suggestions, complexity
```

---

## 📊 Test Case Format

Test cases are stored in the database as JSON:

```json
{
  "test_cases": [
    {
      "input": "nums = [2,7,11,15]\ntarget = 9",
      "expected": "[0, 1]"
    },
    {
      "input": "nums = [3,2,4]\ntarget = 6",
      "expected": "[1, 2]"
    }
  ]
}
```

---

## 🎯 Starter Code Format

Starter code templates are stored per language:

```json
{
  "starter_code": {
    "python": "def twoSum(nums, target):\n    # Write your code here\n    pass",
    "javascript": "function twoSum(nums, target) {\n    // Write your code here\n}",
    "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your code here\n    }\n}",
    "cpp": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your code here\n    }\n};"
  }
}
```

---

## 🚀 Usage Example

### Step 1: Select a Problem
- Choose "Two Sum" from the problems list
- Problem description loads
- Starter code appears in editor
- Test cases visible in right panel

### Step 2: Write Code
```python
def twoSum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

### Step 3: Run Code (Quick Test)
- Click **"▶️ Run Code"**
- See output immediately
- No test case validation

### Step 4: Submit Solution
- Click **"✅ Submit"**
- All test cases execute
- See pass/fail for each test
- Get acceptance status

### Step 5: Get AI Feedback (Optional)
- Click **"🤖 AI Check"**
- Receive code review
- Get optimization suggestions
- Learn complexity analysis

---

## 🔐 Security

- Code execution happens in **isolated Piston containers**
- No direct server access
- Timeout limits prevent infinite loops
- Resource limits prevent memory exhaustion

---

## 🎨 Styling

New CSS classes added to `CodeCheckPage.css`:

- `.result-tabs` - Tab navigation
- `.testcases-panel` - Test cases display
- `.test-results` - Test execution results
- `.result-summary` - Pass/fail summary
- `.test-result-item` - Individual test result
- `.action-buttons` - Run/Submit/AI Check buttons
- `.btn-run`, `.btn-submit`, `.btn-ai-check` - Button styles

---

## 📝 Future Enhancements

1. **Code Editor Upgrade**
   - Integrate Monaco Editor (VS Code editor)
   - Syntax highlighting
   - Auto-completion
   - Line numbers

2. **More Test Features**
   - Custom test cases
   - Hidden test cases
   - Performance benchmarks
   - Memory usage tracking

3. **Social Features**
   - Share solutions
   - View others' solutions after acceptance
   - Discussion forum

4. **Progress Tracking**
   - Submission history
   - Success rate per problem
   - Language statistics
   - Time spent coding

---

## 🐛 Troubleshooting

### Backend not responding
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend not connecting
- Check API_BASE_URL in `frontend/src/services/api.js`
- Ensure backend is running on port 8000
- Check browser console for errors

### Test cases not loading
- Verify test_cases field in database
- Check QuizQuestion model has test_cases column
- Run database migrations if needed

---

## 📚 Related Files

### Backend
- `backend/app/api/routes/code_execution.py` - Execution endpoints
- `backend/app/services/code_executor.py` - Piston integration
- `backend/app/models.py` - Database models

### Frontend
- `frontend/src/pages/CodeCheckPage.jsx` - Main component
- `frontend/src/pages/CodeCheckPage.css` - Styling
- `frontend/src/services/api.js` - API client

### Documentation
- `CODE_CHECK_IMPLEMENTATION.md` - Original implementation
- `CODE_EXECUTION_FEATURE.md` - This document

---

## ✅ Completion Checklist

- [x] Add code execution API endpoints
- [x] Implement Run Code functionality
- [x] Implement Submit functionality
- [x] Add test results display
- [x] Load starter code templates
- [x] Add test cases panel
- [x] Style LeetCode-like interface
- [x] Handle errors gracefully
- [x] Update documentation

---

**Status**: ✅ Complete and Ready for Testing

**Last Updated**: November 22, 2025


# Testing Code Execution Feature

## 🧪 Quick Test Guide

### Prerequisites
1. Backend server running on `http://localhost:8000`
2. Frontend running on `http://localhost:5173`
3. Database initialized with LeetCode problems

---

## Test 1: Check API Endpoints

### Test Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Test Supported Languages
```bash
curl http://localhost:8000/api/execution/supported-languages
# Expected: List of supported languages
```

### Test Get Problems
```bash
curl http://localhost:8000/api/code/problems
# Expected: List of LeetCode problems with test cases
```

---

## Test 2: Test Code Execution (Python)

### Simple Run Test
```bash
curl -X POST http://localhost:8000/api/execution/run \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello, World!\")",
    "language": "python"
  }'
```

**Expected Response:**
```json
{
  "mode": "run",
  "result": {
    "success": true,
    "output": "Hello, World!\n",
    "error": null,
    "run_time": 45
  }
}
```

---

## Test 3: Test Code Submission with Test Cases

### Get a Problem's Starter Code
```bash
curl "http://localhost:8000/api/execution/question/1/starter-code?language=python"
```

### Submit Code for Testing
```bash
curl -X POST http://localhost:8000/api/execution/submit/1 \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def twoSum(nums, target):\n    hash_map = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hash_map:\n            return [hash_map[complement], i]\n        hash_map[num] = i\n    return []",
    "language": "python"
  }'
```

**Expected Response:**
```json
{
  "mode": "test",
  "test_results": [
    {
      "test_case_id": 1,
      "input": "nums = [2,7,11,15]\ntarget = 9",
      "expected": "[0, 1]",
      "actual": "[0, 1]",
      "passed": true,
      "error": null,
      "run_time": 52
    }
  ],
  "summary": {
    "total": 3,
    "passed": 3,
    "failed": 0,
    "pass_rate": 100.0
  }
}
```

---

## Test 4: Frontend UI Testing

### Step-by-Step Manual Test

1. **Navigate to Code Check Page**
   - Go to `http://localhost:5173`
   - Click on "Code Check" or navigate to `/code-check`

2. **Select a Problem**
   - Click on any problem from the left sidebar
   - Verify problem description loads
   - Check that starter code appears in editor

3. **View Test Cases**
   - Click on "📋 Test Cases" tab
   - Verify test cases are displayed
   - Check input and expected output format

4. **Test Run Code**
   - Write simple code: `print("Hello")`
   - Click "▶️ Run Code"
   - Switch to "📊 Results" tab
   - Verify output appears

5. **Test Submit**
   - Write a complete solution
   - Click "✅ Submit"
   - Verify test results appear
   - Check pass/fail status for each test case

6. **Test Language Switch**
   - Change language dropdown to JavaScript
   - Verify starter code updates
   - Try running code in different language

7. **Test AI Check**
   - Write some code
   - Click "🤖 AI Check"
   - Verify AI feedback appears

---

## Test 5: Error Handling

### Test Syntax Error
```python
# In the code editor, write:
def twoSum(nums, target)
    return []  # Missing colon
```
- Click Submit
- Verify error message appears

### Test Runtime Error
```python
# In the code editor, write:
def twoSum(nums, target):
    return nums[100]  # Index out of range
```
- Click Submit
- Verify error is caught and displayed

### Test Wrong Answer
```python
# In the code editor, write:
def twoSum(nums, target):
    return [0, 0]  # Wrong answer
```
- Click Submit
- Verify test cases fail with correct comparison

---

## Test 6: Edge Cases

### Empty Code
- Leave code editor empty
- Click Submit
- Verify alert: "Please enter your code first"

### No Problem Selected
- Clear problem selection (refresh page)
- Try to submit
- Verify alert: "Please select a problem first"

### Problem Without Test Cases
- If any problem has no test cases
- Try to submit
- Verify error message

---

## Expected UI Behavior

### ✅ Success State
```
✅ Accepted
3 / 3 test cases passed (100.0%)

✅ Test Case 1                          45ms
Input: [2,7,11,15], target = 9
Expected: [0,1]
Your Output: [0,1]
```

### ❌ Failure State
```
❌ Wrong Answer
1 / 3 test cases passed (33.3%)

❌ Test Case 2                          52ms
Input: [3,2,4], target = 6
Expected: [1,2]
Your Output: [0,2]
```

### 💻 Run Output
```
💻 Output
Hello, World!
Runtime: 45ms
```

### 🤖 AI Check Result
```
✅ Code Looks Good!

💡 Suggestions:
- Consider edge cases
- Add comments
- Optimize time complexity
```

---

## Performance Benchmarks

### Expected Response Times
- **Run Code**: < 2 seconds
- **Submit (3 test cases)**: < 5 seconds
- **AI Check**: < 3 seconds
- **Load Starter Code**: < 500ms

---

## Common Issues & Solutions

### Issue: Backend not responding
**Solution:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Issue: CORS errors
**Solution:** Check `main.py` CORS settings:
```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

### Issue: Piston API timeout
**Solution:** Piston API might be slow. Wait or use alternative:
```python
# In code_executor.py, increase timeout
timeout=aiohttp.ClientTimeout(total=30)
```

### Issue: Test cases not loading
**Solution:** Check database has test_cases:
```sql
SELECT id, title, test_cases FROM quiz_questions LIMIT 1;
```

---

## Database Check

### Verify Test Cases Exist
```sql
SELECT 
    id,
    title,
    test_cases,
    starter_code
FROM quiz_questions
WHERE test_cases IS NOT NULL
LIMIT 5;
```

### Add Test Cases (if missing)
```python
# Run this script to add test cases
python scripts/add_test_cases.py
```

---

## Browser Console Testing

Open browser console (F12) and run:

```javascript
// Test API connection
fetch('http://localhost:8000/api/execution/supported-languages')
  .then(r => r.json())
  .then(console.log)

// Test run code
fetch('http://localhost:8000/api/execution/run', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    code: 'print("Hello")',
    language: 'python'
  })
})
  .then(r => r.json())
  .then(console.log)
```

---

## Success Criteria

✅ All API endpoints respond correctly
✅ Code execution works for Python, JavaScript, Java, C++
✅ Test cases execute and compare results
✅ UI displays test results correctly
✅ Error handling works properly
✅ Language switching loads correct starter code
✅ Run, Submit, and AI Check all function
✅ No console errors in browser
✅ No server errors in backend logs

---

## Next Steps After Testing

1. **Add More Test Cases** to existing problems
2. **Add Starter Code** for all languages
3. **Optimize Performance** if needed
4. **Add Custom Test Cases** feature
5. **Implement Monaco Editor** for better code editing

---

**Testing Status**: Ready for Testing
**Last Updated**: November 22, 2025


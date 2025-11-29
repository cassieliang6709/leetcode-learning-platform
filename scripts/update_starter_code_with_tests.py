#!/usr/bin/env python3
"""
Update starter_code to include test framework
添加测试代码框架，使代码能够从 stdin 读取输入并输出结果
"""
import os
import sys
import json
import psycopg2
from psycopg2.extras import Json, RealDictCursor

# Database connection
DB_CONFIG = {
    "dbname": "leetcode_learning",
    "user": os.getenv("DB_USER", "liangyue"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}


def get_method_name_from_code(code: str, language: str = "python") -> str:
    """从代码中提取方法名"""
    if language == "python":
        # 查找 "def method_name(" 模式
        import re
        match = re.search(r'def\s+(\w+)\s*\(', code)
        if match:
            return match.group(1)
    elif language == "javascript":
        match = re.search(r'function\s+(\w+)\s*\(', code)
        if match:
            return match.group(1)
    return None


def create_python_starter_with_tests(original_code: str, method_name: str, test_cases: list) -> str:
    """
    创建包含测试框架的 Python starter code
    
    Args:
        original_code: 原始的函数定义
        method_name: 方法名
        test_cases: 测试用例列表
    
    Returns:
        完整的可运行代码
    """
    
    # 添加必要的 imports
    imports = "from typing import List, Dict, Optional, Set, Tuple, Any\nimport sys\nimport json\n\n"
    
    # 包装成 Solution 类
    class_code = f"""class Solution:
    {original_code.replace('def ', 'def ', 1).replace(original_code.split('(')[0], '    def ' + method_name)}
"""
    
    # 添加测试代码
    test_code = f"""

# Test code - reads from stdin and outputs result
if __name__ == "__main__":
    # Read input from stdin
    input_lines = sys.stdin.read().strip().split('\\n')
    
    # Parse input based on the problem
    # For most problems, inputs are on separate lines
    sol = Solution()
    
    try:
        # Parse first line as the main input
        if len(input_lines) >= 1:
            # Try to parse as JSON
            try:
                args = []
                for line in input_lines:
                    args.append(json.loads(line))
                
                # Call the solution method
                result = sol.{method_name}(*args)
                
                # Output result as JSON
                print(json.dumps(result))
            except json.JSONDecodeError:
                # If not JSON, treat as raw strings
                result = sol.{method_name}(*input_lines)
                print(result)
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
        sys.exit(1)
"""
    
    return imports + class_code + test_code


def create_simple_python_starter(original_code: str, method_name: str) -> str:
    """
    创建简单的可运行 Python 代码（不依赖 stdin）
    用户可以直接修改测试数据
    """
    
    imports = "from typing import List, Dict, Optional, Set, Tuple, Any\n\n"
    
    # 修复方法定义：添加 self 参数（如果缺少）
    fixed_code = original_code.strip()
    if f"def {method_name}(" in fixed_code and "self" not in fixed_code.split("def " + method_name + "(")[1].split(")")[0].split(",")[0]:
        # 在方法参数中添加 self
        fixed_code = fixed_code.replace(f"def {method_name}(", f"def {method_name}(self, ")
    
    # 包装成 Solution 类，确保正确缩进
    lines = fixed_code.split('\n')
    indented_lines = ['    ' + line if line.strip() else line for line in lines]
    class_code = f"""class Solution:
{chr(10).join(indented_lines)}


# Test your code here
if __name__ == "__main__":
    sol = Solution()
    
    # Example test case - modify these values to test your code
    # When you click 'Run', this will execute
    # When you click 'Submit', test cases from the problem will be used
    
    # TODO: Add your test here
    result = sol.{method_name}([2, 7, 11, 15], 9)  # Example for Two Sum
    print(result)
    
    # You can add more test cases:
    # result2 = sol.{method_name}([3, 2, 4], 6)
    # print(result2)
"""
    
    return imports + class_code


def update_database():
    """更新数据库中的 starter_code"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 获取所有有 starter_code 的题目
        cursor.execute("""
            SELECT id, leetcode_id, title, starter_code, test_cases 
            FROM quiz_questions 
            WHERE starter_code IS NOT NULL
            ORDER BY leetcode_id
        """)
        
        questions = cursor.fetchall()
        print(f"Found {len(questions)} questions with starter_code")
        
        updated_count = 0
        
        for question in questions:
            question_id = question['id']
            title = question['title']
            starter_code = question['starter_code']
            test_cases = question['test_cases'] or []
            
            print(f"\nProcessing: #{question['leetcode_id']} - {title}")
            
            # 只更新 Python 代码
            if 'python' in starter_code:
                original_python = starter_code['python']
                
                # 检查是否已经包含测试代码
                if 'if __name__ == "__main__":' in original_python:
                    print(f"  ✓ Already has test code, skipping...")
                    continue
                
                # 提取方法名
                method_name = get_method_name_from_code(original_python, 'python')
                
                if not method_name:
                    print(f"  ✗ Could not extract method name, skipping...")
                    continue
                
                print(f"  → Method name: {method_name}")
                
                # 创建新的 starter code（使用简单版本，更适合用户测试）
                new_python_code = create_simple_python_starter(original_python, method_name)
                
                # 更新 starter_code
                new_starter_code = starter_code.copy()
                new_starter_code['python'] = new_python_code
                
                # 保存到数据库
                cursor.execute("""
                    UPDATE quiz_questions 
                    SET starter_code = %s
                    WHERE id = %s
                """, (Json(new_starter_code), question_id))
                
                updated_count += 1
                print(f"  ✓ Updated!")
        
        conn.commit()
        print(f"\n{'='*60}")
        print(f"✅ Successfully updated {updated_count} questions")
        print(f"{'='*60}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Update Starter Code with Test Framework")
    print("=" * 60)
    
    response = input("\nThis will update starter_code for all problems. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    update_database()


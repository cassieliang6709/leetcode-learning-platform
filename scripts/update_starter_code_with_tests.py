#!/usr/bin/env python3
"""
Update starter_code to include test framework
Add test code framework to enable reading input from stdin and outputting results
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
    """Extract method name from code"""
    if language == "python":
        # Find "def method_name(" pattern
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
    Create Python starter code with test framework
    
    Args:
        original_code: Original function definition
        method_name: Method name
        test_cases: List of test cases
    
    Returns:
        Complete runnable code
    """
    
    # Add necessary imports
    imports = "from typing import List, Dict, Optional, Set, Tuple, Any\nimport sys\nimport json\n\n"
    
    # Wrap in Solution class
    class_code = f"""class Solution:
    {original_code.replace('def ', 'def ', 1).replace(original_code.split('(')[0], '    def ' + method_name)}
"""
    
    # Add test code
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
    Create simple runnable Python code (does not depend on stdin)
    Users can directly modify test data
    """
    
    imports = "from typing import List, Dict, Optional, Set, Tuple, Any\n\n"
    
    # Fix method definition: add self parameter (if missing)
    fixed_code = original_code.strip()
    if f"def {method_name}(" in fixed_code and "self" not in fixed_code.split("def " + method_name + "(")[1].split(")")[0].split(",")[0]:
        # Add self to method parameters
        fixed_code = fixed_code.replace(f"def {method_name}(", f"def {method_name}(self, ")
    
    # Wrap in Solution class, ensure correct indentation
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
    """Update starter_code in database"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get all questions with starter_code
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
            
            # Only update Python code
            if 'python' in starter_code:
                original_python = starter_code['python']
                
                # Check if already contains test code
                if 'if __name__ == "__main__":' in original_python:
                    print(f"  ✓ Already has test code, skipping...")
                    continue
                
                # Extract method name
                method_name = get_method_name_from_code(original_python, 'python')
                
                if not method_name:
                    print(f"  ✗ Could not extract method name, skipping...")
                    continue
                
                print(f"  → Method name: {method_name}")
                
                # Create new starter code (use simple version, more suitable for user testing)
                new_python_code = create_simple_python_starter(original_python, method_name)
                
                # Update starter_code
                new_starter_code = starter_code.copy()
                new_starter_code['python'] = new_python_code
                
                # Save to database
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


#!/usr/bin/env python3
"""
Fix method definitions to include 'self' parameter
修复方法定义，添加 self 参数
"""
import os
import sys
import json
import re
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


def fix_python_code(code: str, method_name: str) -> str:
    """修复 Python 代码，确保方法有 self 参数并正确缩进"""
    
    # 找到方法定义行
    pattern = rf'def {method_name}\s*\('
    match = re.search(pattern, code)
    
    if not match:
        return code
    
    # 检查是否已经有 self
    method_line_start = match.start()
    method_line_end = code.find(')', method_line_start)
    method_signature = code[method_line_start:method_line_end + 1]
    
    # 如果没有 self，添加它
    if 'self' not in method_signature.split('(')[1].split(',')[0]:
        # 替换方法定义
        new_signature = method_signature.replace(f'def {method_name}(', f'def {method_name}(self, ')
        code = code[:method_line_start] + new_signature + code[method_line_end + 1:]
    
    return code


def update_database():
    """更新数据库中的代码"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 获取所有有 starter_code 的题目
        cursor.execute("""
            SELECT id, leetcode_id, title, starter_code 
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
            
            if 'python' not in starter_code:
                continue
            
            python_code = starter_code['python']
            
            # 检查是否需要修复
            if 'def ' not in python_code or 'if __name__' not in python_code:
                continue
            
            # 提取方法名
            match = re.search(r'def\s+(\w+)\s*\(', python_code)
            if not match:
                continue
            
            method_name = match.group(1)
            
            # 检查是否缺少 self
            if f'def {method_name}(' in python_code:
                params_part = python_code.split(f'def {method_name}(')[1].split(')')[0]
                first_param = params_part.split(',')[0].strip()
                
                if first_param != 'self' and first_param != '':
                    print(f"\nFixing: #{question['leetcode_id']} - {title}")
                    print(f"  Method: {method_name}")
                    print(f"  First param: {first_param}")
                    
                    # 修复代码
                    fixed_code = fix_python_code(python_code, method_name)
                    
                    # 更新
                    new_starter_code = starter_code.copy()
                    new_starter_code['python'] = fixed_code
                    
                    cursor.execute("""
                        UPDATE quiz_questions 
                        SET starter_code = %s
                        WHERE id = %s
                    """, (Json(new_starter_code), question_id))
                    
                    updated_count += 1
                    print(f"  ✓ Fixed!")
        
        conn.commit()
        print(f"\n{'='*60}")
        print(f"✅ Successfully fixed {updated_count} questions")
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
    print("Fix Method Self Parameter")
    print("=" * 60)
    
    response = input("\nThis will fix method definitions. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    update_database()


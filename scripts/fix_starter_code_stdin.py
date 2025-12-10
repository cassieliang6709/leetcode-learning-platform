#!/usr/bin/env python3
"""
Fix starter_code to support stdin input for test cases
Update starter_code to read test input from stdin and use correct method names
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

# LeetCode official method name mapping
OFFICIAL_METHOD_NAMES = {
    1: "twoSum",
    2: "addTwoNumbers",
    3: "lengthOfLongestSubstring",
    5: "longestPalindrome",  # Note: it's longestPalindrome, not longestPalindromicSubstring
    11: "maxArea",
    15: "threeSum",
    17: "letterCombinations",
    19: "removeNthFromEnd",
    20: "isValid",
    21: "mergeTwoLists",
    22: "generateParenthesis",
    23: "mergeKLists",
    33: "search",
    34: "searchRange",
    39: "combinationSum",
    42: "trap",
    46: "permute",
    48: "rotate",
    49: "groupAnagrams",
    53: "maxSubArray",
    55: "canJump",
    56: "merge",
    62: "uniquePaths",
    70: "climbStairs",
    72: "minDistance",
    75: "sortColors",
    76: "minWindow",
    78: "subsets",
    79: "exist",
    84: "largestRectangleArea",
    85: "maximalRectangle",
    94: "inorderTraversal",
    96: "numTrees",
    98: "isValidBST",
    101: "isSymmetric",
    102: "levelOrder",
    104: "maxDepth",
    105: "buildTree",
    114: "flatten",
    121: "maxProfit",
    124: "maxPathSum",
    125: "isPalindrome",
    128: "longestConsecutive",
    136: "singleNumber",
    139: "wordBreak",
    141: "hasCycle",
    142: "detectCycle",
    146: "LRUCache",
    148: "sortList",
    152: "maxProduct",
    155: "MinStack",
    160: "getIntersectionNode",
    169: "majorityElement",
    198: "rob",
    200: "numIslands",
    206: "reverseList",
    207: "canFinish",
    208: "Trie",
    215: "findKthLargest",
    217: "containsDuplicate",
    226: "invertTree",
    234: "isPalindrome",
    236: "lowestCommonAncestor",
    238: "productExceptSelf",
    239: "maxSlidingWindow",
    240: "searchMatrix",
    242: "isAnagram",
    253: "minMeetingRooms",
    283: "moveZeroes",
    287: "findDuplicate",
    295: "MedianFinder",
    297: "Codec",
    300: "lengthOfLIS",
    309: "maxProfit",
    322: "coinChange",
    337: "rob",
    338: "countBits",
    347: "topKFrequent",
    394: "decodeString",
    416: "canPartition",
    424: "characterReplacement",
    438: "findAnagrams",
    448: "findDisappearedNumbers",
    461: "hammingDistance",
    494: "findTargetSumWays",
    538: "convertBST",
    543: "diameterOfBinaryTree",
    560: "subarraySum",
    567: "checkInclusion",
    581: "findUnsortedSubarray",
    617: "mergeTrees",
    621: "leastInterval",
    647: "countSubstrings",
    704: "search",
    739: "dailyTemperatures",
}


def extract_method_name(code: str) -> str:
    """Extract method name from code"""
    match = re.search(r'def\s+(\w+)\s*\(', code)
    if match:
        return match.group(1)
    return None


def extract_method_signature(code: str) -> str:
    """Extract complete method signature (including parameters and return type)"""
    # Match def method_name(...) -> return_type:
    match = re.search(r'def\s+\w+\s*\([^)]*\)(?:\s*->\s*[^:]+)?:', code)
    if match:
        return match.group(0).rstrip(':')
    return None


def create_stdin_test_framework(method_name: str, method_signature: str, test_cases: list) -> str:
    """
    Create test framework that supports stdin input
    Automatically infer input parsing method based on test cases
    """
    
    # Extract parameters from method signature
    # Example: def twoSum(self, nums: List[int], target: int) -> List[int]:
    params_match = re.search(r'\(([^)]+)\)', method_signature)
    if not params_match:
        params = []
    else:
        params_str = params_match.group(1)
        # Remove self and type annotations, keep only parameter names
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if param and param != 'self':
                # Extract parameter name (remove type annotation)
                param_name = param.split(':')[0].strip()
                params.append(param_name)
    
    # Analyze test cases to infer input format
    has_multiple_inputs = False
    if test_cases and len(test_cases) > 0:
        first_input = test_cases[0].get('input', '')
        # If input contains newlines, it means there are multiple parameters
        has_multiple_inputs = '\n' in first_input
    
    # Generate test code
    if has_multiple_inputs:
        # Multiple parameters case
        test_code = f"""
# Test framework - DO NOT MODIFY
if __name__ == "__main__":
    import sys
    import json
    
    # Read input from stdin
    input_lines = sys.stdin.read().strip().split('\\n')
    
    sol = Solution()
    
    try:
        # Parse each line as a separate argument
        args = []
        for line in input_lines:
            if line:
                try:
                    # Try to parse as JSON
                    args.append(json.loads(line))
                except json.JSONDecodeError:
                    # If not JSON, use as string
                    args.append(line)
        
        # Call the solution method
        result = sol.{method_name}(*args)
        
        # Output result
        if isinstance(result, (list, dict)):
            print(json.dumps(result, separators=(',', ':')))
        else:
            print(result)
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
        sys.exit(1)
"""
    else:
        # Single parameter case
        test_code = f"""
# Test framework - DO NOT MODIFY
if __name__ == "__main__":
    import sys
    import json
    
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    sol = Solution()
    
    try:
        # Try to parse as JSON first
        try:
            arg = json.loads(input_data)
        except json.JSONDecodeError:
            # If not JSON, use as string
            arg = input_data
        
        # Call the solution method
        result = sol.{method_name}(arg)
        
        # Output result
        if isinstance(result, (list, dict)):
            print(json.dumps(result, separators=(',', ':')))
        else:
            print(result)
    except Exception as e:
        print(f"Error: {{e}}", file=sys.stderr)
        sys.exit(1)
"""
    
    return test_code


def create_fixed_starter_code(original_code: str, correct_method_name: str, test_cases: list) -> str:
    """
    Create fixed starter code
    1. Extract Solution class definition (remove old test code)
    2. Fix method name
    3. Add new stdin test framework
    """
    
    # Add necessary imports
    imports = "from typing import List, Dict, Optional, Set, Tuple, Any\nimport sys\nimport json\n\n"
    
    # Extract current method name and signature
    current_method = extract_method_name(original_code)
    method_signature = extract_method_signature(original_code)
    
    if not method_signature:
        # If signature cannot be extracted, use basic template
        solution_class = f"""class Solution:
    def {correct_method_name}(self):
        # Write your solution here
        pass
"""
    else:
        # Replace method name but keep signature
        if current_method and current_method != correct_method_name:
            method_signature = method_signature.replace(f'def {current_method}', f'def {correct_method_name}')
        
        # Extract method body (if exists)
        # Find the end position of method definition
        method_def_match = re.search(r'def\s+\w+\s*\([^)]*\)(?:\s*->\s*[^:]+)?:\s*\n', original_code)
        if method_def_match:
            after_def = original_code[method_def_match.end():]
            # Extract method body (until class ends or if __name__)
            method_body_lines = []
            for line in after_def.split('\n'):
                if line and not line.startswith('    '):
                    # No longer part of the method
                    break
                if 'if __name__' in line:
                    break
                method_body_lines.append(line)
            
            method_body = '\n'.join(method_body_lines).rstrip()
            if not method_body or method_body.strip() == 'pass':
                method_body = '        # Write your solution here\n        pass'
        else:
            method_body = '        # Write your solution here\n        pass'
        
        solution_class = f"""class Solution:
    {method_signature}:
{method_body}
"""
    
    # Generate test framework
    test_framework = create_stdin_test_framework(correct_method_name, method_signature or f'def {correct_method_name}(self)', test_cases)
    
    return imports + solution_class + test_framework


def main():
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
        print(f"Found {len(questions)} questions with starter_code\n")
        print("=" * 80)
        
        updated_count = 0
        skipped_count = 0
        
        for question in questions:
            leetcode_id = question['leetcode_id']
            title = question['title']
            starter_code = question['starter_code']
            test_cases = question['test_cases'] or []
            
            print(f"\n📝 #{leetcode_id} - {title}")
            
            # Only process Python code
            if 'python' not in starter_code:
                print("   ⚠️  No Python starter code, skipping...")
                skipped_count += 1
                continue
            
            python_code = starter_code['python']
            
            # Check if already has correct test framework
            if '# Test framework - DO NOT MODIFY' in python_code:
                print("   ✓ Already has correct test framework")
                skipped_count += 1
                continue
            
            # Get correct method name
            correct_method_name = OFFICIAL_METHOD_NAMES.get(leetcode_id)
            if not correct_method_name:
                # Try to extract from existing code
                correct_method_name = extract_method_name(python_code)
                if not correct_method_name:
                    print("   ✗ Could not determine method name, skipping...")
                    skipped_count += 1
                    continue
            
            current_method = extract_method_name(python_code)
            print(f"   Current method: {current_method}")
            print(f"   Correct method: {correct_method_name}")
            
            # Create fixed code
            try:
                fixed_python_code = create_fixed_starter_code(
                    python_code, 
                    correct_method_name, 
                    test_cases
                )
                
                # Update database
                new_starter_code = starter_code.copy()
                new_starter_code['python'] = fixed_python_code
                
                cursor.execute("""
                    UPDATE quiz_questions 
                    SET starter_code = %s
                    WHERE id = %s
                """, (Json(new_starter_code), question['id']))
                
                updated_count += 1
                print(f"   ✅ Fixed!")
                
            except Exception as e:
                print(f"   ✗ Error: {e}")
                skipped_count += 1
        
        conn.commit()
        
        print("\n" + "=" * 80)
        print(f"\n✅ Summary:")
        print(f"   Total questions: {len(questions)}")
        print(f"   Updated: {updated_count}")
        print(f"   Skipped: {skipped_count}")
        print("=" * 80)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()


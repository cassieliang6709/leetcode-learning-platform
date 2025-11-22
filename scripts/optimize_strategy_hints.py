import asyncio
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from sqlalchemy import select, update
from app.database import AsyncSessionLocal
from app.models import QuizQuestion

# Strategy hints for each problem (100 words, includes complexity and approach)
STRATEGY_HINTS = {
    # Array & Hashing
    "Contains Duplicate": "Use a HashSet to track seen elements. Iterate through array once, adding each element to set. If element already exists in set, return true (duplicate found). Time: O(n), Space: O(n). This is optimal as we need to remember seen elements. Alternative O(1) space solution requires O(n²) time with nested loops, which is inefficient for large inputs.",
    
    "Valid Anagram": "Use HashMap (frequency counter) to count character occurrences in both strings. First, check if lengths differ - if so, not anagrams. Build frequency map for first string, then decrement counts using second string. If any count goes negative or final map has non-zero values, not anagrams. Time: O(n), Space: O(1) since max 26 letters.",
    
    "Two Sum": "Use HashMap to store {value: index} pairs while iterating. For each number, calculate complement (target - current). Check if complement exists in map - if yes, return indices. Otherwise, add current number to map. Time: O(n), Space: O(n). This one-pass solution beats the O(n²) brute force approach significantly for large arrays.",
    
    "Group Anagrams": "Use HashMap with sorted string as key. For each word, sort its characters to create key (anagrams have same sorted form). Add original word to list at that key. Time: O(n * k log k) where n is number of words, k is max word length. Space: O(n * k) for storing results. Alternative: use character frequency as key.",
    
    "Top K Frequent Elements": "Use HashMap to count frequencies, then use Min-Heap of size K to track top K elements. Time: O(n log k) with heap, or O(n) with bucket sort. Space: O(n). Min-heap keeps only K elements, making it space-efficient. For very large datasets, bucket sort (O(n) time) is faster but uses more space.",
    
    "Product of Array Except Self": "Use two-pass approach with prefix/suffix products. First pass calculates prefix products (left to right), second pass multiplies with suffix products (right to left) while building result. Time: O(n), Space: O(1) excluding output array. No division needed. This elegant solution maintains O(n) time while using constant extra space.",
    
    "Valid Sudoku": "Use three HashSets to track seen numbers in: 1) rows, 2) columns, 3) 3x3 sub-boxes. Box index calculated as (row//3, col//3). Single pass through board, checking and updating sets. Time: O(1) since board is fixed 9x9 (81 cells), Space: O(1). Fixed-size board makes this effectively constant complexity.",
    
    "Encode and Decode Strings": "Use length-prefixed encoding: 'length#string' format. Encode: prepend each string with 'length#'. Decode: parse length, extract that many characters, repeat. Handles special characters and delimiters naturally. Time: O(n) for both operations, Space: O(n). The # delimiter after length ensures we can handle any string content including numbers and special chars.",
    
    "Longest Consecutive Sequence": "Use HashSet for O(1) lookups. Add all numbers to set, then for each potential sequence start (num-1 not in set), count consecutive numbers. Track maximum length found. Time: O(n), Space: O(n). Key insight: only start counting from sequence beginnings to avoid redundant work, achieving linear time complexity.",
    
    # Two Pointers
    "Valid Palindrome": "Use two pointers from both ends, moving inward. Skip non-alphanumeric characters, compare characters case-insensitively. If mismatch found, return false. Time: O(n), Space: O(1). This is optimal - we must check each character at least once. In-place comparison avoids creating cleaned string copy, saving space.",
    
    "3Sum": "Sort array first. Use three pointers: fix first pointer, then two-pointer technique on remaining array to find pairs that sum to -nums[i]. Skip duplicates to avoid repeat triplets. Time: O(n²), Space: O(1) excluding output. Sorting enables efficient duplicate skipping and two-pointer search. Better than O(n³) brute force.",
    
    "Container With Most Water": "Use two pointers at array ends. Calculate area, then move pointer pointing to shorter line inward (moving taller line can't increase area). Track maximum area found. Time: O(n), Space: O(1). Greedy approach works because width decreases, so we must increase height to potentially improve area.",
    
    "Trapping Rain Water": "Use two pointers with left_max and right_max trackers. Move pointer with lower max inward, adding water trapped at that position (min(left_max, right_max) - height). Time: O(n), Space: O(1). Alternative: use two arrays for precomputed max heights, trading space for clarity. Both O(n) time solutions.",
    
    "Two Sum II": "Use two pointers on sorted array: one at start, one at end. If sum equals target, return indices. If sum too small, move left pointer right. If too large, move right pointer left. Time: O(n), Space: O(1). Sorted array property enables this efficient approach without extra space for HashMap.",
    
    # Sliding Window
    "Best Time to Buy and Sell Stock": "Track minimum price seen so far and maximum profit. Single pass: update min price, calculate potential profit (current - min), update max profit. Time: O(n), Space: O(1). One-pass greedy solution works because we only need lowest price before current day to maximize profit.",
    
    "Longest Substring Without Repeating Characters": "Use sliding window with HashSet. Expand window by moving right pointer, adding characters to set. When duplicate found, shrink window from left until duplicate removed. Track max window size. Time: O(n), Space: O(min(n, charset_size)). Each character visited at most twice (once by right, once by left pointer).",
    
    "Longest Repeating Character Replacement": "Use sliding window with frequency map. Track character with max frequency in window. If window_length - max_frequency > k, window invalid - shrink from left. Time: O(n), Space: O(1) since at most 26 uppercase letters. The key insight: valid window needs at most k non-max-frequency characters.",
    
    "Permutation in String": "Use sliding window of s1.length on s2, comparing character frequencies. Use two frequency maps or single map tracking differences. Slide window, updating frequency map. If frequencies match, permutation found. Time: O(n), Space: O(1) for 26 letters. Fixed window size enables efficient sliding with O(1) updates per position.",
    
    "Minimum Window Substring": "Use sliding window with two HashMaps. Expand window until all target chars included, then contract from left while maintaining validity. Track minimum window size. Time: O(m + n), Space: O(m + n) for maps. Complex but optimal - must check all characters at least once.",
    
    "Sliding Window Maximum": "Use Deque (double-ended queue) to maintain indices of potential maximums in decreasing order. For each position, remove outdated indices, add current index, first index in deque is maximum. Time: O(n), Space: O(k) for deque of window size k. Each element enters and exits deque at most once.",
    
    # Stack
    "Valid Parentheses": "Use Stack to track opening brackets. For each closing bracket, check if stack top matches (proper pairing). If stack empty at closing bracket or mismatched, invalid. Finally, stack should be empty. Time: O(n), Space: O(n). Stack naturally handles nested structure - LIFO matches bracket pairing rules.",
    
    "Min Stack": "Use two stacks: one for values, one for minimums. When pushing, also push min(value, current_min) to min stack. Both stacks stay synchronized. Time: O(1) for all ops, Space: O(n) for two stacks. This elegant solution maintains O(1) getMin by duplicating min values when needed.",
    
    "Evaluate Reverse Polish Notation": "Use Stack to evaluate. Push numbers onto stack. When operator encountered, pop two operands, apply operator, push result back. Final stack element is result. Time: O(n), Space: O(n). RPN's postfix notation naturally maps to stack operations - no need for operator precedence handling.",
    
    "Generate Parentheses": "Use backtracking with counter tracking. Add '(' if open count < n. Add ')' if close count < open count. Build all valid combinations. Time: O(4^n / √n) Catalan number, Space: O(n) recursion depth. Constraint checking ensures only valid combinations generated, pruning invalid branches early.",
    
    "Daily Temperatures": "Use monotonic decreasing Stack storing indices. For each temperature, pop all smaller temperatures from stack and set their answers. Push current index. Time: O(n), Space: O(n). Each index pushed and popped exactly once - amortized O(1) per element. Stack maintains indices waiting for warmer day.",
    
    "Car Fleet": "Sort cars by starting position (closer to target first). Iterate from closest to target: calculate time to reach target. If current car's time ≤ previous fleet time, joins fleet. Time: O(n log n) for sorting, Space: O(n). Greedy approach works because cars can't pass - faster cars catch up to slower ones.",
    
    "Largest Rectangle in Histogram": "Use monotonic increasing Stack storing indices. When shorter bar encountered, calculate areas for all taller bars in stack. Height from stack, width from indices. Time: O(n), Space: O(n). Each bar pushed and popped once - classic stack optimization for nested extrema problems.",
    
    # Binary Search
    "Binary Search": "Classic binary search on sorted array. Compare middle element with target. If equal, found. If target smaller, search left half. If larger, search right half. Time: O(log n), Space: O(1) iterative or O(log n) recursive. Halving search space each iteration gives logarithmic complexity.",
    
    "Search a 2D Matrix": "Treat 2D matrix as sorted 1D array. Use binary search with index mapping: mid_row = mid // cols, mid_col = mid % cols. Time: O(log(m*n)), Space: O(1). Alternative: two binary searches (find row, then find column), also O(log m + log n) = O(log(m*n)).",
    
    "Koko Eating Bananas": "Binary search on eating speed (1 to max pile size). For each speed, check if Koko can finish in h hours. Find minimum feasible speed. Time: O(n log m) where m is max pile size, Space: O(1). Problem transforms to: find minimum value where condition holds.",
    
    "Find Minimum in Rotated Sorted Array": "Binary search comparing mid with right boundary. If mid > right, minimum in right half. Otherwise, minimum in left half (including mid). Time: O(log n), Space: O(1). Rotation creates exactly one point where array decreases - binary search finds this inflection point efficiently.",
    
    "Search in Rotated Sorted Array": "Binary search with rotation handling. Determine which half is properly sorted (compare mid with left/right). If target in sorted half, search there. Otherwise, search other half. Time: O(log n), Space: O(1). Key: one half is always properly sorted in rotated array.",
    
    "Time Based Key-Value Store": "Use HashMap of key to list of {timestamp, value} pairs. List naturally sorted by timestamp (append only). Binary search on timestamp list for get operation. Time: O(log n) for get, O(1) for set, Space: O(n). Binary search leverages sorted timestamp order.",
    
    "Median of Two Sorted Arrays": "Binary search on smaller array to find partition point. Ensure left half of both arrays ≤ right half. Median from max of left halves and min of right halves. Time: O(log(min(m,n))), Space: O(1). Optimal solution requires logarithmic time by partitioning smartly.",
    
    # Linked List
    "Reverse Linked List": "Use three pointers: prev, current, next. Iterate through list, reversing each link: current.next = prev, then shift all pointers forward. Time: O(n), Space: O(1) iterative or O(n) recursive. Iterative is preferred for space efficiency. In-place reversal by pointer manipulation only.",
    
    "Merge Two Sorted Lists": "Use dummy node and pointer. Compare heads of both lists, attach smaller node to result, advance that list pointer. Continue until both lists exhausted. Time: O(m + n), Space: O(1) iterative or O(m + n) recursive. Iterative saves space. Similar to merge step in merge sort.",
    
    "Reorder List": "Three steps: 1) Find middle using slow/fast pointers, 2) Reverse second half, 3) Merge two halves alternately. Time: O(n), Space: O(1). Each step is O(n) time, combined still O(n). No extra data structures needed - all pointer manipulation.",
    
    "Remove Nth Node From End": "Use two pointers with n gap. Move first pointer n steps ahead, then move both until first reaches end. Second pointer at n-th from end. Time: O(n), Space: O(1). Single pass solution with dummy node to handle edge cases elegantly.",
    
    "Copy List with Random Pointer": "Three-pass approach: 1) Create nodes interleaved with original, 2) Set random pointers using original.random.next, 3) Separate lists. Time: O(n), Space: O(1) excluding output. Alternative: use HashMap for O(n) space but clearer logic. Interleaving trick eliminates HashMap need.",
    
    "Add Two Numbers": "Iterate both lists simultaneously, maintaining carry. Sum digits with carry, create new node with sum % 10, update carry = sum // 10. Continue until both lists and carry exhausted. Time: O(max(m,n)), Space: O(max(m,n)) for result. Like elementary school addition.",
    
    "Linked List Cycle": "Use fast and slow pointers (Floyd's cycle detection). Fast moves 2 steps, slow moves 1. If they meet, cycle exists. If fast reaches end, no cycle. Time: O(n), Space: O(1). Elegant constant-space solution - meeting point proves cycle existence mathematically.",
    
    "Find Duplicate Number": "Treat array as linked list (value as next pointer). Use Floyd's cycle detection: find meeting point, then find cycle start (duplicate). Time: O(n), Space: O(1). Problem cleverly maps to cycle detection - duplicate creates cycle. No array modification needed.",
    
    "LRU Cache": "Use HashMap + Doubly Linked List. HashMap for O(1) access, DLL for O(1) removal/addition. Most recent at head, least recent at tail. Get moves node to head. Time: O(1) for both get/put, Space: O(capacity). DLL enables O(1) reordering which array can't provide.",
    
    "Merge K Sorted Lists": "Use Min-Heap to track smallest element from each list. Pop minimum, add to result, push next element from that list to heap. Time: O(n log k) where n is total nodes, k is number of lists. Space: O(k) for heap. Better than merging pairs iteratively.",
    
    "Reverse Nodes in K-Group": "Identify k-sized groups, reverse each group using standard reversal. Reconnect groups maintaining links. Need helper to reverse and check if k nodes remaining. Time: O(n), Space: O(1) iterative. Complex pointer manipulation but achieves constant space requirement.",
    
    # Trees
    "Invert Binary Tree": "Recursively swap left and right children for each node. Base case: null node returns null. Post-order: process children first, then swap. Time: O(n), Space: O(h) for recursion stack where h is height. BFS with queue also works. Each node visited once.",
    
    "Maximum Depth of Binary Tree": "Recursively compute: max_depth = 1 + max(left_depth, right_depth). Base case: null node has depth 0. Simple recursive solution is elegant. Time: O(n), Space: O(h) for recursion. BFS/DFS iterative approaches use O(n) space for queue/stack but avoid recursion.",
    
    "Diameter of Binary Tree": "For each node, calculate max path through that node: left_depth + right_depth. Track global maximum. Use post-order traversal. Time: O(n), Space: O(h). Tricky part: diameter might not pass through root - need to check all nodes. Return depth up, track diameter globally.",
    
    "Balanced Binary Tree": "Recursively check if both subtrees balanced AND height difference ≤ 1. Return {is_balanced, height} from each call. Short-circuit when unbalanced subtree found. Time: O(n), Space: O(h). Compute height during balance check to avoid redundant height calculations.",
    
    "Same Tree": "Recursively compare: 1) both null → true, 2) one null → false, 3) values differ → false, 4) recurse on both subtrees. Time: O(min(n,m)), Space: O(min(h1,h2)). Early termination on first difference. Structural and value equality both checked.",
    
    "Subtree of Another Tree": "For each node in main tree, check if identical to subRoot using isSameTree. Recursively check all nodes. Time: O(m * n) worst case where m, n are tree sizes. Space: O(h1 + h2) for recursion. Naive but correct approach.",
    
    "Lowest Common Ancestor of BST": "Use BST property: if both nodes < root, LCA in left. If both > root, LCA in right. Otherwise, root is LCA (split point). Time: O(h), Space: O(1) iterative or O(h) recursive. BST property enables optimal solution without checking all nodes.",
    
    "Binary Tree Level Order Traversal": "Use BFS with Queue. Process level by level: track level size, process that many nodes, add their children. Time: O(n), Space: O(w) where w is max width. Queue holds at most one level of nodes. Classic BFS application.",
    
    "Binary Tree Right Side View": "BFS level order, take last node of each level. Or DFS with level tracking, visiting right child first. Time: O(n), Space: O(h). Multiple approaches work - BFS more intuitive, DFS more space-efficient for skewed trees.",
    
    "Count Good Nodes": "DFS with max value seen on path from root. If current >= max, it's good node. Update max and recurse. Count good nodes. Time: O(n), Space: O(h). Single pass with path tracking - each node checked once.",
    
    "Validate Binary Search Tree": "Pass valid range [min, max] down recursion. Check if node value within range. Left child: range [min, node.val-1], right child: range [node.val+1, max]. Time: O(n), Space: O(h). Range method cleaner than in-order traversal approach.",
    
    "Kth Smallest Element in BST": "In-order traversal (left, root, right) visits BST in sorted order. Count nodes during traversal, return kth. Time: O(h + k), Space: O(h). Can optimize for repeated queries by augmenting tree with subtree sizes. In-order exploits BST property.",
    
    "Construct Binary Tree from Preorder and Inorder": "Preorder gives root order. Inorder gives left/right split. Use preorder[0] as root, find in inorder to partition subtrees. Recurse on partitions. Time: O(n), Space: O(n) for HashMap + recursion. HashMap speeds up inorder position lookup from O(n) to O(1).",
    
    "Binary Tree Maximum Path Sum": "Post-order DFS: for each node, calculate max path from that node going down. Track global max considering path through node (left + node + right). Time: O(n), Space: O(h). Key: distinguish between max path down (return value) vs through node (global max).",
    
    "Serialize and Deserialize Binary Tree": "Preorder traversal for serialize with null markers. Deserialize recursively consuming from queue/list. Use '#' or 'null' for null nodes. Time: O(n), Space: O(n). Preorder + null markers uniquely represent tree. Queue makes deserialize straightforward.",
    
    # Tries
    "Implement Trie": "Use TrieNode with children HashMap and isEnd flag. Insert: create nodes for missing chars. Search: follow path, check isEnd. StartsWith: follow path only. Time: O(L) per operation where L is word length. Space: O(N * L) for N words. Efficient for prefix operations.",
    
    "Design Add and Search Words Data Structure": "Extend Trie with wildcard support. For '.' in search, try all possible children paths recursively. Regular chars follow normal path. Time: O(26^dots * L) worst case, Space: O(N * L). Backtracking handles wildcards. Trie structure enables efficient prefix matching.",
    
    "Word Search II": "Use Trie to store all words. DFS from each cell, pruning with Trie. Mark visited cells, unmark on backtrack. Remove found words from Trie to avoid duplicates. Time: O(m * n * 4^L) where L is word length, Space: O(N * L) for Trie. Trie significantly reduces search space.",
    
    # Heap / Priority Queue
    "Kth Largest Element in Stream": "Use Min-Heap of size K. Maintain K largest elements. Add new element, if heap exceeds K, pop minimum. Heap top is kth largest. Time: O(log k) per add, O(n log k) initial, Space: O(k). Min-heap keeps K largest efficiently - smaller than K-th are irrelevant.",
    
    "Last Stone Weight": "Use Max-Heap. Repeatedly pop two heaviest stones, compute difference, add back if non-zero. Continue until ≤1 stone remains. Time: O(n log n), Space: O(n). Heap maintains largest stones efficiently. Python uses min-heap, so negate weights.",
    
    "K Closest Points to Origin": "Use Max-Heap of size K storing distances. Keep K smallest distances. Time: O(n log k), Space: O(k). Alternative: QuickSelect for O(n) average time. Heap approach is simpler and good enough for most cases. Calculate distance without sqrt.",
    
    "Kth Largest Element in Array": "QuickSelect algorithm (QuickSort variant). Partition around pivot, recurse on side containing kth. Average O(n) time, O(n²) worst case. Space: O(1). Alternative: Min-Heap of size k in O(n log k). QuickSelect is optimal average case.",
    
    "Task Scheduler": "Use Max-Heap for task frequencies. Greedily schedule most frequent task, use cooling slots. Track cooldown with queue. Time: O(n log 26) ≈ O(n), Space: O(26) ≈ O(1). Key: most frequent task determines minimum time - schedule around it.",
    
    "Design Twitter": "Use HashMap for follow relationships and tweets. Merge K sorted lists (user's + followees' tweets) using Min-Heap. Time: O(k log N) for getNewsFeed where N is followees, Space: O(U + T) for users and tweets. Heap merges sorted timelines efficiently.",
    
    "Find Median from Data Stream": "Use two heaps: Max-Heap for smaller half, Min-Heap for larger half. Maintain balance: size difference ≤ 1. Median from heap tops. Time: O(log n) per add, O(1) for median, Space: O(n). Two heaps partition data elegantly around median.",
    
    # Backtracking
    "Subsets": "Backtracking with inclusion/exclusion. For each element: include it and recurse, then backtrack (exclude) and recurse. Generate all 2^n combinations. Time: O(2^n * n), Space: O(n) recursion depth. Each element has two choices - included or excluded in subset.",
    
    "Combination Sum": "Backtracking with remaining target. Sort candidates to enable pruning. Include current candidate (can reuse), recurse with reduced target. Backtrack and try next candidate. Time: O(n^(target/min)), Space: O(target/min) depth. Pruning when target exceeded essential for efficiency.",
    
    "Permutations": "Backtracking with used array or swapping. Build permutation element by element, marking used. When length = n, add to result. Time: O(n! * n), Space: O(n) depth. Each position has decreasing choices: n, n-1, ..., 1, giving n! permutations.",
    
    "Subsets II": "Backtracking with duplicate handling. Sort array first. Skip duplicates at same level: if nums[i] == nums[i-1] and i-1 not used, skip. Time: O(2^n * n), Space: O(n). Sorting groups duplicates, enabling skip logic to prevent duplicate subsets.",
    
    "Combination Sum II": "Backtracking with duplicates. Sort array, skip duplicates at same recursion level (i > start and nums[i] == nums[i-1]). Each element used at most once. Time: O(2^n * k), Space: O(target). Sorting + skip logic handles duplicates while avoiding reuse.",
    
    "Word Search": "Backtracking DFS from each cell. Mark visited, explore 4 directions, check if character matches. Unmark on backtrack. Time: O(m * n * 4^L) where L is word length, Space: O(L) recursion. Each path explored exhaustively - early termination on mismatch essential.",
    
    "Palindrome Partitioning": "Backtracking to build all partitions. For each position, try all possible palindrome partitions. If substring is palindrome, add to current partition and recurse. Time: O(n * 2^n), Space: O(n). Exponential because every position can be partition point.",
    
    "Letter Combinations of Phone Number": "Backtracking through digit-to-letter mapping. For each digit, try each letter, recurse to next digit. Time: O(4^n * n) where n is digit count, Space: O(n) depth. Each digit has ≤4 letters, generating ≤4^n combinations.",
    
    "N-Queens": "Backtracking placing queens row by row. Track attacked columns, diagonals. For each row, try each column, check if safe, place queen, recurse. Backtrack and try next position. Time: O(n!), Space: O(n). Constraint checking prunes invalid placements early.",
    
    # Graphs
    "Number of Islands": "DFS/BFS to mark connected land cells. Iterate grid, when '1' found, increment count and mark entire island via DFS. Time: O(m * n), Space: O(m * n) for recursion/queue. Each cell visited once. DFS naturally groups connected components.",
    
    "Clone Graph": "DFS/BFS with HashMap to track cloned nodes. For each node, create clone, recursively clone neighbors, use HashMap to avoid cycles. Time: O(V + E), Space: O(V) for HashMap. HashMap prevents infinite loops on cycles and enables O(1) clone lookup.",
    
    "Max Area of Island": "DFS from each land cell, counting connected cells. Track maximum area found. Mark visited cells to avoid recounting. Time: O(m * n), Space: O(m * n) for recursion. Similar to Number of Islands but tracks size.",
    
    "Pacific Atlantic Water Flow": "Two DFS/BFS: one from Pacific borders, one from Atlantic borders. Cell reaches both if visited in both searches. Time: O(m * n), Space: O(m * n). Reverse thinking: start from oceans and flow upward (reverse direction).",
    
    "Surrounded Regions": "DFS/BFS from border 'O' cells to mark unsurrounded regions. Then flip all unmarked 'O' to 'X'. Time: O(m * n), Space: O(m * n). Border-connected 'O's cannot be surrounded - mark them first.",
    
    "Rotting Oranges": "Multi-source BFS. Start from all rotten oranges simultaneously. Each minute, rot adjacent fresh oranges (BFS level). Track time and remaining fresh oranges. Time: O(m * n), Space: O(m * n). BFS naturally models simultaneous spreading. Return -1 if fresh oranges unreachable.",
    
    "Course Schedule": "Detect cycle in directed graph using DFS. Build adjacency list from prerequisites. If cycle exists, cannot finish all courses. Time: O(V + E), Space: O(V + E). Three states: unvisited, visiting, visited. Cycle detected when visiting node encountered again.",
    
    "Course Schedule II": "Topological sort using DFS or Kahn's algorithm (BFS). Build adjacency list, perform DFS postorder for reverse topological order. Time: O(V + E), Space: O(V + E). Valid order exists iff no cycle. Topological sort gives valid course order.",
    
    "Number of Connected Components": "Union-Find (Disjoint Set Union) or DFS. Union-Find: initially n components, union edges, count remaining components. Time: O(E * α(n)) ≈ O(E) with path compression, Space: O(n). Union-Find efficient for connectivity queries with dynamic edges.",
    
    "Graph Valid Tree": "Check: n-1 edges AND no cycles. Use Union-Find or DFS. Tree has exactly n-1 edges and is connected (no cycles). Time: O(E * α(n)), Space: O(n). Tree is connected acyclic graph - both conditions necessary.",
    
    "Redundant Connection": "Union-Find to detect cycle-causing edge. Process edges sequentially, union endpoints. First edge where both endpoints in same set is redundant. Time: O(E * α(n)), Space: O(n). Edge causing cycle must connect two already-connected components.",
    
    "Word Ladder": "BFS for shortest transformation path. Each word differs by one character. Build adjacency list or try all single-char changes. Time: O(M² * N) where M is word length, N is word count. Space: O(M * N). BFS guarantees shortest path in unweighted graph.",
}


async def optimize_all_hints():
    """Optimize all strategy hints with algorithm strategies and complexity"""
    async with AsyncSessionLocal() as session:
        # Get all questions
        result = await session.execute(select(QuizQuestion))
        questions = result.scalars().all()
        
        updated_count = 0
        for question in questions:
            if question.title in STRATEGY_HINTS:
                # Get current hints
                hints = question.hints or []
                
                # Update strategy hint
                new_hints = []
                for hint in hints:
                    if hint.get('type') == 'strategy':
                        # Replace with optimized strategy
                        new_hints.append({
                            'type': 'strategy',
                            'content': STRATEGY_HINTS[question.title]
                        })
                    else:
                        new_hints.append(hint)
                
                # Update question
                await session.execute(
                    update(QuizQuestion)
                    .where(QuizQuestion.id == question.id)
                    .values(hints=new_hints)
                )
                
                updated_count += 1
                print(f"✅ Updated: {question.title}")
            else:
                print(f"⚠️  No hint for: {question.title}")
        
        await session.commit()
        print(f"\n✅ Successfully updated {updated_count} questions with optimized strategy hints!")


if __name__ == "__main__":
    asyncio.run(optimize_all_hints())


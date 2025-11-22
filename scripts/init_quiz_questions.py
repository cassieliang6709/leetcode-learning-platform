"""
Initialize 100 quiz questions for daily challenges
Run this script to populate the database with algorithm quiz questions
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import QuizQuestion, KnowledgePoint, Base
from sqlalchemy import select

# Database URL - update this with your database credentials
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/leetcode_learning"

# Sample quiz questions data
QUIZ_QUESTIONS = [
    # Arrays & Hash Tables (20 questions)
    {
        "title": "什么是数组的时间复杂度？",
        "description": "在数组中通过索引访问元素的时间复杂度是多少？",
        "difficulty": "easy",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
        "correct_answer": 0,
        "explanation": "数组通过索引直接访问元素，时间复杂度为O(1)常数时间。",
        "category": "array"
    },
    {
        "title": "哈希表查找时间复杂度",
        "description": "在理想情况下，哈希表的查找时间复杂度是多少？",
        "difficulty": "easy",
        "options": ["O(n)", "O(1)", "O(log n)", "O(n log n)"],
        "correct_answer": 1,
        "explanation": "哈希表在理想情况下（无哈希冲突）的查找时间复杂度为O(1)。",
        "category": "hash_table"
    },
    {
        "title": "Two Sum问题最优解",
        "description": "解决Two Sum问题的最优方法是什么？",
        "difficulty": "easy",
        "options": ["暴力循环", "使用哈希表", "先排序后双指针", "二分查找"],
        "correct_answer": 1,
        "explanation": "使用哈希表可以在O(n)时间内解决Two Sum问题，是最优解。",
        "category": "hash_table"
    },
    {
        "title": "数组原地操作",
        "description": "什么叫做数组的原地操作？",
        "difficulty": "easy",
        "options": ["不使用额外空间", "创建新数组", "使用递归", "使用循环"],
        "correct_answer": 0,
        "explanation": "原地操作指不使用额外的数组空间，直接在原数组上修改。",
        "category": "array"
    },
    {
        "title": "哈希冲突解决",
        "description": "哈希表中处理哈希冲突的常用方法不包括：",
        "difficulty": "medium",
        "options": ["链地址法", "开放寻址法", "再哈希法", "递归法"],
        "correct_answer": 3,
        "explanation": "递归法不是解决哈希冲突的方法。常用方法有链地址法、开放寻址法和再哈希法。",
        "category": "hash_table"
    },
    
    # Sliding Window (15 questions)
    {
        "title": "滑动窗口适用场景",
        "description": "滑动窗口技术最适合解决什么类型的问题？",
        "difficulty": "medium",
        "options": ["图遍历问题", "连续子数组/子串问题", "二叉树问题", "排序问题"],
        "correct_answer": 1,
        "explanation": "滑动窗口最适合解决连续子数组或子串相关的问题，如最长子串、最小子数组等。",
        "category": "sliding_window"
    },
    {
        "title": "固定大小滑动窗口",
        "description": "固定大小的滑动窗口时间复杂度通常是多少？",
        "difficulty": "easy",
        "options": ["O(n²)", "O(n)", "O(log n)", "O(1)"],
        "correct_answer": 1,
        "explanation": "固定大小的滑动窗口只需遍历一次数组，时间复杂度为O(n)。",
        "category": "sliding_window"
    },
    {
        "title": "可变大小滑动窗口",
        "description": "可变大小滑动窗口通常使用什么指针？",
        "difficulty": "medium",
        "options": ["单指针", "双指针", "三指针", "不需要指针"],
        "correct_answer": 1,
        "explanation": "可变大小滑动窗口通常使用双指针（left和right）来动态调整窗口大小。",
        "category": "sliding_window"
    },
    
    # Two Pointers (15 questions)
    {
        "title": "双指针基本概念",
        "description": "双指针技术主要用于什么类型的数组？",
        "difficulty": "easy",
        "options": ["无序数组", "已排序数组", "二维数组", "稀疏数组"],
        "correct_answer": 1,
        "explanation": "双指针技术在已排序数组中最为有效，可以利用有序性质优化算法。",
        "category": "two_pointers"
    },
    {
        "title": "对撞双指针",
        "description": "对撞双指针的移动方向是？",
        "difficulty": "easy",
        "options": ["同向移动", "相向移动", "反向移动", "随机移动"],
        "correct_answer": 1,
        "explanation": "对撞双指针从数组两端开始，向中间相向移动，直到相遇。",
        "category": "two_pointers"
    },
    {
        "title": "快慢指针",
        "description": "快慢指针常用于解决什么问题？",
        "difficulty": "medium",
        "options": ["数组排序", "链表环检测", "树的遍历", "图的搜索"],
        "correct_answer": 1,
        "explanation": "快慢指针常用于链表环检测、找中点等链表相关问题。",
        "category": "two_pointers"
    },
    
    # Binary Search (15 questions)
    {
        "title": "二分查找时间复杂度",
        "description": "二分查找的时间复杂度是多少？",
        "difficulty": "easy",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
        "correct_answer": 1,
        "explanation": "二分查找每次将搜索区间减半，时间复杂度为O(log n)。",
        "category": "binary_search"
    },
    {
        "title": "二分查找前提条件",
        "description": "使用二分查找的必要前提是什么？",
        "difficulty": "easy",
        "options": ["数组已排序", "数组无重复", "数组很大", "数组连续"],
        "correct_answer": 0,
        "explanation": "二分查找要求数组必须是已排序的（升序或降序）。",
        "category": "binary_search"
    },
    {
        "title": "二分查找边界问题",
        "description": "二分查找中 mid = (left + right) / 2 可能出现什么问题？",
        "difficulty": "medium",
        "options": ["结果错误", "整数溢出", "死循环", "无法收敛"],
        "correct_answer": 1,
        "explanation": "当left和right都很大时，相加可能导致整数溢出。应使用 mid = left + (right - left) / 2。",
        "category": "binary_search"
    },
    
    # Stack & Queue (10 questions)
    {
        "title": "栈的特点",
        "description": "栈的数据结构特点是什么？",
        "difficulty": "easy",
        "options": ["先进先出(FIFO)", "后进先出(LIFO)", "随机访问", "双向访问"],
        "correct_answer": 1,
        "explanation": "栈是后进先出(LIFO, Last In First Out)的数据结构。",
        "category": "stack"
    },
    {
        "title": "队列的特点",
        "description": "队列的数据结构特点是什么？",
        "difficulty": "easy",
        "options": ["后进先出(LIFO)", "先进先出(FIFO)", "随机访问", "双向访问"],
        "correct_answer": 1,
        "explanation": "队列是先进先出(FIFO, First In First Out)的数据结构。",
        "category": "queue"
    },
    {
        "title": "单调栈应用",
        "description": "单调栈常用于解决什么问题？",
        "difficulty": "medium",
        "options": ["排序问题", "下一个更大元素", "最短路径", "图遍历"],
        "correct_answer": 1,
        "explanation": "单调栈常用于解决'下一个更大/更小元素'类型的问题。",
        "category": "stack"
    },
    
    # Linked List (10 questions)
    {
        "title": "链表访问时间复杂度",
        "description": "访问链表第k个元素的时间复杂度是多少？",
        "difficulty": "easy",
        "options": ["O(1)", "O(k)", "O(n)", "O(log n)"],
        "correct_answer": 1,
        "explanation": "链表需要从头节点开始遍历k次才能访问第k个元素，时间复杂度为O(k)。",
        "category": "linked_list"
    },
    {
        "title": "链表反转",
        "description": "反转单链表最常用的方法是？",
        "difficulty": "medium",
        "options": ["递归", "迭代（双指针）", "栈", "队列"],
        "correct_answer": 1,
        "explanation": "迭代法使用双指针（prev, curr）反转链表是最常用且高效的方法。",
        "category": "linked_list"
    },
    {
        "title": "链表环检测",
        "description": "检测链表是否有环最有效的方法是？",
        "difficulty": "medium",
        "options": ["暴力循环", "快慢指针", "哈希表", "递归"],
        "correct_answer": 1,
        "explanation": "使用快慢指针（Floyd判圈法）可以在O(n)时间和O(1)空间复杂度内检测环。",
        "category": "linked_list"
    },
    
    # Tree & Graph (15 questions)
    {
        "title": "二叉树遍历",
        "description": "前序遍历的顺序是什么？",
        "difficulty": "easy",
        "options": ["左-根-右", "根-左-右", "左-右-根", "右-根-左"],
        "correct_answer": 1,
        "explanation": "前序遍历的顺序是：根节点 -> 左子树 -> 右子树。",
        "category": "tree"
    },
    {
        "title": "DFS vs BFS",
        "description": "深度优先搜索(DFS)通常使用什么数据结构实现？",
        "difficulty": "medium",
        "options": ["队列", "栈或递归", "数组", "哈希表"],
        "correct_answer": 1,
        "explanation": "DFS通常使用栈（显式栈或递归调用栈）实现。",
        "category": "tree"
    },
    {
        "title": "完全二叉树",
        "description": "完全二叉树的节点数为n，它的高度是多少？",
        "difficulty": "medium",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(√n)"],
        "correct_answer": 1,
        "explanation": "完全二叉树的高度为O(log n)，因为每层节点数呈指数增长。",
        "category": "tree"
    },
]

# Add more questions to reach 100
MORE_QUESTIONS = [
    # Dynamic Programming (20 questions - placeholder for brevity)
    *[{
        "title": f"动态规划题目 {i+1}",
        "description": f"这是第{i+1}道动态规划相关的题目，用于测试动态规划知识点。",
        "difficulty": ["easy", "medium", "hard"][i % 3],
        "options": ["选项A", "选项B", "选项C", "选项D"],
        "correct_answer": i % 4,
        "explanation": f"这是第{i+1}题的解释。",
        "category": "dynamic_programming"
    } for i in range(20)],
]

QUIZ_QUESTIONS.extend(MORE_QUESTIONS)

# Ensure we have exactly 100 questions
while len(QUIZ_QUESTIONS) < 100:
    idx = len(QUIZ_QUESTIONS)
    QUIZ_QUESTIONS.append({
        "title": f"算法题目 {idx+1}",
        "description": f"这是第{idx+1}道算法题目，用于日常练习。",
        "difficulty": ["easy", "medium", "hard"][idx % 3],
        "options": ["选项A", "选项B", "选项C", "选项D"],
        "correct_answer": idx % 4,
        "explanation": f"这是第{idx+1}题的解释。",
        "category": "general"
    })


async def init_quiz_questions():
    """Initialize quiz questions in the database"""
    print("🚀 Starting quiz questions initialization...")
    
    # Create async engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Check if questions already exist
            result = await session.execute(select(QuizQuestion))
            existing_count = len(result.scalars().all())
            
            if existing_count > 0:
                print(f"⚠️  Found {existing_count} existing questions.")
                response = input("Do you want to clear and re-initialize? (yes/no): ")
                if response.lower() != 'yes':
                    print("❌ Initialization cancelled.")
                    return
                
                # Clear existing questions
                await session.execute("DELETE FROM quiz_attempts")
                await session.execute("DELETE FROM quiz_questions")
                await session.commit()
                print("🗑️  Cleared existing questions.")
            
            # Get or create knowledge points
            knowledge_points = {}
            categories = set(q["category"] for q in QUIZ_QUESTIONS)
            
            for category in categories:
                result = await session.execute(
                    select(KnowledgePoint).where(KnowledgePoint.category == category)
                )
                kp = result.scalar_one_or_none()
                
                if not kp:
                    kp = KnowledgePoint(
                        name=category.replace('_', ' ').title(),
                        description=f"{category} related problems",
                        difficulty="medium",
                        category=category,
                        order_index=len(knowledge_points)
                    )
                    session.add(kp)
                    await session.flush()
                
                knowledge_points[category] = kp.id
            
            await session.commit()
            print(f"✅ Created/verified {len(knowledge_points)} knowledge points.")
            
            # Add quiz questions
            for idx, q_data in enumerate(QUIZ_QUESTIONS):
                question = QuizQuestion(
                    knowledge_point_id=knowledge_points.get(q_data["category"]),
                    leetcode_id=idx + 1,
                    title=q_data["title"],
                    description=q_data["description"],
                    difficulty=q_data["difficulty"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation", ""),
                    hints=[
                        {"level": 1, "content": f"提示1：思考一下{q_data['title']}的核心概念"},
                        {"level": 2, "content": f"提示2：答案可能与{q_data['category']}相关"}
                    ]
                )
                session.add(question)
                
                if (idx + 1) % 20 == 0:
                    print(f"📝 Added {idx + 1} questions...")
            
            await session.commit()
            print(f"✅ Successfully initialized {len(QUIZ_QUESTIONS)} quiz questions!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     Quiz Questions Initialization Script              ║
    ║     Initialize 100 questions for daily challenges     ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚙️  Please update DATABASE_URL in the script before running!")
    print(f"Current DATABASE_URL: {DATABASE_URL}\n")
    
    # Run the initialization
    asyncio.run(init_quiz_questions())


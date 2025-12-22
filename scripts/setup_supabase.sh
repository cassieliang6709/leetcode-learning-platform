#!/bin/bash
# 使用 Supabase 配置快速设置脚本

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔧 Supabase 配置设置${NC}"
echo ""

# 提示用户输入密码
echo -e "${YELLOW}请输入你的 Supabase 数据库密码：${NC}"
read -s SUPABASE_PASSWORD
echo ""

if [ -z "$SUPABASE_PASSWORD" ]; then
    echo -e "${RED}❌ 密码不能为空${NC}"
    exit 1
fi

# Supabase 配置
SUPABASE_PROJECT_ID="xeqhcjgqlxddxsxvdrpy"
SUPABASE_HOST="aws-1-us-east-2.pooler.supabase.com"
SUPABASE_PORT="6543"

# 构建连接字符串
DATABASE_URL="postgresql+asyncpg://postgres.${SUPABASE_PROJECT_ID}:${SUPABASE_PASSWORD}@${SUPABASE_HOST}:${SUPABASE_PORT}/postgres?pgbouncer=true"
DIRECT_URL="postgresql+asyncpg://postgres.${SUPABASE_PROJECT_ID}:${SUPABASE_PASSWORD}@${SUPABASE_HOST}:5432/postgres"

echo -e "${BLUE}📝 创建后端 .env 文件...${NC}"
cat > backend/.env << EOF
# Supabase Database Configuration
DATABASE_URL=${DATABASE_URL}

# Direct connection for migrations (if needed)
DIRECT_URL=${DIRECT_URL}

# SiliconFlow API Key (Optional)
SILICONFLOW_API_KEY=your_siliconflow_api_key_here

# OpenAI API Key (Optional)
OPENAI_API_KEY=your_openai_api_key_here
EOF

echo -e "${GREEN}✅ 后端 .env 文件已创建${NC}"
echo ""

# 测试数据库连接
echo -e "${BLUE}🔍 测试数据库连接...${NC}"
cd backend
source venv/bin/activate 2>/dev/null || {
    echo -e "${YELLOW}⚠️  虚拟环境不存在，正在创建...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
}

# 创建临时测试脚本（避免 python-dotenv 在 Python 3.13 中的 bug）
TEST_SCRIPT="/tmp/test_db_connection_$$.py"
ENV_FILE_PATH="$PROJECT_ROOT/backend/.env"

cat > "$TEST_SCRIPT" << PYEOF
import asyncio
import asyncpg
import sys
from pathlib import Path

# 使用传入的 .env 文件路径
env_file = Path("$ENV_FILE_PATH")
if not env_file.exists():
    print(f"❌ .env 文件不存在: {env_file}")
    sys.exit(1)

# 解析 .env 文件
db_url = None
with open(env_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DATABASE_URL=') and not line.startswith('#'):
            db_url = line.split('=', 1)[1].strip()
            break

if not db_url:
    print("❌ DATABASE_URL 未找到")
    sys.exit(1)

async def test_connection():
    try:
        # asyncpg 不支持 postgresql+asyncpg:// 格式，需要改为 postgresql://
        test_url = db_url.replace('postgresql+asyncpg://', 'postgresql://')
        # 移除 pgbouncer 参数用于测试（asyncpg 不支持 pgbouncer）
        test_url = test_url.replace('?pgbouncer=true', '').replace('&pgbouncer=true', '')
        # 使用端口 5432 而不是 6543（连接池端口，asyncpg 需要直连）
        test_url = test_url.replace(':6543/', ':5432/')
        
        conn = await asyncpg.connect(test_url)
        await conn.close()
        print("✅ 数据库连接成功！")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

result = asyncio.run(test_connection())
sys.exit(0 if result else 1)
PYEOF

# 运行测试脚本（从项目根目录运行，确保路径正确）
cd "$PROJECT_ROOT"
python3 "$TEST_SCRIPT"
TEST_RESULT=$?
rm -f "$TEST_SCRIPT"
cd backend

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ 数据库连接测试通过${NC}"
    echo ""
    echo -e "${BLUE}📊 初始化数据库...${NC}"
    cd ..
    python scripts/init_db.py
    echo -e "${GREEN}✅ 数据库初始化完成${NC}"
else
    echo -e "${RED}❌ 数据库连接失败，请检查密码和网络连接${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Supabase 配置完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📝 下一步：${NC}"
echo -e "   1. 部署后端到 Railway: 查看 DEPLOY_RAILWAY.md"
echo -e "   2. 部署前端到 Vercel: 查看 DEPLOY_VERCEL.md"
echo ""
echo -e "${BLUE}💡 提示：${NC}"
echo -e "   - DATABASE_URL 已配置为连接池模式（pgbouncer）"
echo -e "   - 如需迁移，使用 DIRECT_URL"
echo ""

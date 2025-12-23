#!/bin/bash
# 测试 Railway 后端 API

if [ -z "$1" ]; then
    echo "用法: ./test_railway.sh <你的railway-url>"
    echo "示例: ./test_railway.sh https://leetcode-backend.up.railway.app"
    exit 1
fi

RAILWAY_URL="$1"

echo "🔍 测试 Railway 后端: $RAILWAY_URL"
echo ""

# 测试健康检查
echo "1. 测试健康检查..."
curl -s "$RAILWAY_URL/health" | jq . || curl -s "$RAILWAY_URL/health"
echo ""
echo ""

# 测试注册接口
echo "2. 测试注册接口..."
RANDOM_USER="testuser$(date +%s)"
curl -X POST "$RAILWAY_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$RANDOM_USER\",\"email\":\"$RANDOM_USER@example.com\",\"password\":\"test123\"}" \
  -w "\nHTTP Status: %{http_code}\n" \
  | jq . 2>/dev/null || echo "响应不是 JSON 格式"
echo ""

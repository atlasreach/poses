#!/bin/bash
# Test Lambda function manually

set -e

FUNCTION_NAME="instagram-scraper-daily"
REGION="us-east-2"

echo "🧪 Testing Lambda function manually..."

aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --region $REGION \
    --log-type Tail \
    --query 'LogResult' \
    --output text \
    /tmp/lambda_output.json | base64 -d

echo ""
echo "📄 Response:"
cat /tmp/lambda_output.json | jq .

echo ""
echo "✅ Test complete!"

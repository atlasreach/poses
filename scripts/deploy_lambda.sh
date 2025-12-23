#!/bin/bash
# Deploy Lambda function for automated Instagram scraping

set -e

FUNCTION_NAME="instagram-scraper-daily"
REGION="us-east-2"
ROLE_NAME="instagram-scraper-lambda-role"

echo "🚀 Deploying Lambda function for automated Instagram scraping"

# Create deployment package directory
echo "📦 Creating deployment package..."
mkdir -p lambda_package
cd lambda_package

# Copy Lambda function
cp ../lambda_scrape_migrate.py lambda_function.py

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r ../lambda_requirements.txt -t .

# Create deployment package
echo "📦 Creating ZIP package..."
zip -r ../lambda_deployment.zip . -q

cd ..

echo "✅ Deployment package created: lambda_deployment.zip"

# Check if Lambda function exists
if aws lambda get-function --function-name $FUNCTION_NAME --region $REGION 2>/dev/null; then
    echo "♻️  Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://lambda_deployment.zip \
        --region $REGION
else
    echo "🆕 Creating new Lambda function..."

    # Get IAM role ARN
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>/dev/null || echo "")

    if [ -z "$ROLE_ARN" ]; then
        echo "❌ IAM role $ROLE_NAME not found. Please create it first using setup_lambda_iam.sh"
        exit 1
    fi

    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime python3.12 \
        --role $ROLE_ARN \
        --handler lambda_function.lambda_handler \
        --zip-file fileb://lambda_deployment.zip \
        --timeout 900 \
        --memory-size 512 \
        --region $REGION
fi

echo "✅ Lambda function deployed successfully!"
echo ""
echo "Next steps:"
echo "1. Set environment variables using: ./configure_lambda.sh"
echo "2. Set up daily schedule using: ./setup_eventbridge.sh"
echo "3. Test the function using: ./test_lambda.sh"

# Cleanup
rm -rf lambda_package lambda_deployment.zip

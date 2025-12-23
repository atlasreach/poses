#!/bin/bash
# All-in-one setup script for automated Instagram scraping

set -e

echo "=========================================="
echo "AWS Lambda Automated Scraping Setup"
echo "=========================================="
echo ""

# Load from .env.local
if [ -f "../.env.local" ]; then
    export $(cat ../.env.local | grep -v '^#' | xargs)
fi

# Configuration
APIFY_TOKEN=${APIFY_API_TOKEN}
INSTAGRAM_USERNAME="madison.moorgan"
S3_BUCKET="madison-morgan-instagram"
MODEL_NAME="madison-morgan"
MAX_POSTS=100
REGION="us-east-2"

if [ -z "$APIFY_TOKEN" ]; then
    echo "❌ Error: APIFY_API_TOKEN not found in .env.local"
    exit 1
fi

echo "Configuration:"
echo "  Username: $INSTAGRAM_USERNAME"
echo "  S3 Bucket: $S3_BUCKET"
echo "  Model Name: $MODEL_NAME"
echo "  Region: $REGION"
echo ""
read -p "Continue with this configuration? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Step 1: IAM Setup
echo ""
echo "Step 1/5: Setting up IAM role and policies..."
./setup_lambda_iam.sh

echo ""
echo "⏳ Waiting 15 seconds for IAM changes to propagate..."
sleep 15

# Step 2: Deploy Lambda
echo ""
echo "Step 2/5: Deploying Lambda function..."
./deploy_lambda.sh

# Step 3: Configure environment
echo ""
echo "Step 3/5: Configuring environment variables..."
./configure_lambda.sh "$APIFY_TOKEN" "$INSTAGRAM_USERNAME" "$S3_BUCKET" "$MODEL_NAME" "$MAX_POSTS"

# Step 4: Set up schedule
echo ""
echo "Step 4/5: Setting up daily schedule..."
./setup_eventbridge.sh

# Step 5: Test
echo ""
echo "Step 5/5: Testing Lambda function..."
read -p "Test the function now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./test_lambda.sh
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Your Instagram account will be scraped daily at 3 AM UTC."
echo ""
echo "📊 Monitor logs:"
echo "   aws logs tail /aws/lambda/instagram-scraper-daily --follow"
echo ""
echo "🧪 Test manually:"
echo "   ./test_lambda.sh"
echo ""
echo "⚙️  Change schedule:"
echo "   Edit setup_eventbridge.sh and re-run it"
echo ""
echo "📚 Full documentation:"
echo "   See LAMBDA_SETUP.md"

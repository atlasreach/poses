#!/bin/bash
# Configure Lambda function environment variables

set -e

FUNCTION_NAME="instagram-scraper-daily"
REGION="us-east-2"

# Load from .env.local
if [ -f "../.env.local" ]; then
    export $(cat ../.env.local | grep -v '^#' | xargs)
fi

# Get configuration from arguments or environment
APIFY_TOKEN=${1:-$APIFY_API_TOKEN}
INSTAGRAM_USERNAME=${2:-"madison.moorgan"}
S3_BUCKET=${3:-"madison-morgan-instagram"}
MODEL_NAME=${4:-"madison-morgan"}
MAX_POSTS=${5:-100}

if [ -z "$APIFY_TOKEN" ]; then
    echo "❌ Error: APIFY_API_TOKEN not found"
    echo "Usage: ./configure_lambda.sh <apify_token> [username] [bucket] [model_name] [max_posts]"
    exit 1
fi

echo "⚙️  Configuring Lambda function environment variables..."

aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment "Variables={
        APIFY_API_TOKEN=$APIFY_TOKEN,
        INSTAGRAM_USERNAME=$INSTAGRAM_USERNAME,
        S3_BUCKET_NAME=$S3_BUCKET,
        MODEL_NAME=$MODEL_NAME,
        AWS_REGION=$REGION,
        MAX_POSTS=$MAX_POSTS
    }" \
    --region $REGION

echo "✅ Lambda environment variables configured!"
echo ""
echo "Configuration:"
echo "  Username: $INSTAGRAM_USERNAME"
echo "  S3 Bucket: $S3_BUCKET"
echo "  Model Name: $MODEL_NAME"
echo "  Max Posts: $MAX_POSTS"
echo "  Region: $REGION"

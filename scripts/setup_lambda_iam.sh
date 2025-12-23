#!/bin/bash
# Set up IAM role and policies for Lambda function

set -e

ROLE_NAME="instagram-scraper-lambda-role"
POLICY_NAME="instagram-scraper-lambda-policy"

echo "🔐 Setting up IAM role and policies for Lambda"

# Create trust policy for Lambda
cat > /tmp/lambda-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create IAM role
echo "Creating IAM role: $ROLE_NAME"
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document file:///tmp/lambda-trust-policy.json \
    --description "Role for Instagram scraper Lambda function" \
    2>/dev/null || echo "Role already exists"

# Attach basic Lambda execution policy
echo "Attaching Lambda execution policy..."
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
    2>/dev/null || echo "Policy already attached"

# Create custom policy for S3 access
cat > /tmp/lambda-s3-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::*-instagram/*",
        "arn:aws:s3:::*-instagram"
      ]
    }
  ]
}
EOF

# Create or update the policy
POLICY_ARN="arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/$POLICY_NAME"

if aws iam get-policy --policy-arn $POLICY_ARN 2>/dev/null; then
    echo "Policy already exists, creating new version..."
    aws iam create-policy-version \
        --policy-arn $POLICY_ARN \
        --policy-document file:///tmp/lambda-s3-policy.json \
        --set-as-default
else
    echo "Creating IAM policy: $POLICY_NAME"
    aws iam create-policy \
        --policy-name $POLICY_NAME \
        --policy-document file:///tmp/lambda-s3-policy.json \
        --description "Policy for Instagram scraper Lambda to access S3"
fi

# Attach custom policy to role
echo "Attaching S3 policy to role..."
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn $POLICY_ARN \
    2>/dev/null || echo "Policy already attached"

echo "✅ IAM role and policies configured successfully!"
echo ""
echo "Role ARN: $(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)"
echo ""
echo "⚠️  Note: Wait 10-15 seconds for IAM changes to propagate before deploying Lambda"

# Cleanup
rm -f /tmp/lambda-trust-policy.json /tmp/lambda-s3-policy.json

# AWS Lambda Automated Instagram Scraping Setup

This guide will help you set up automated daily Instagram scraping to S3 using AWS Lambda + EventBridge.

## What This Does

- **Scrapes** Instagram daily at 3 AM UTC (configurable)
- **Downloads** all images immediately
- **Uploads** to S3 with permanent URLs
- **Saves** JSON to S3
- **Cost**: ~$0/month (within AWS free tier)
- **No server** needed - fully serverless!

## Prerequisites

- AWS CLI configured with credentials
- AWS account
- Apify API token (you already have this)

## Quick Setup (5 minutes)

Run these commands in order:

### 1. Set up IAM permissions
```bash
cd scripts
chmod +x *.sh
./setup_lambda_iam.sh
```

Wait 10-15 seconds for IAM changes to propagate.

### 2. Deploy Lambda function
```bash
./deploy_lambda.sh
```

### 3. Configure environment variables
```bash
# Using your current setup:
./configure_lambda.sh \
    $APIFY_API_TOKEN \
    madison.moorgan \
    madison-morgan-instagram \
    madison-morgan \
    100
```

### 4. Set up daily schedule
```bash
./setup_eventbridge.sh
```

### 5. Test it manually
```bash
./test_lambda.sh
```

That's it! Your Instagram account will now be scraped daily at 3 AM UTC.

---

## Configuration

### Change Schedule

Edit `setup_eventbridge.sh` and change `SCHEDULE_EXPRESSION`:

```bash
# Daily at 3 AM UTC
SCHEDULE_EXPRESSION="cron(0 3 * * ? *)"

# Daily at 6 PM UTC
SCHEDULE_EXPRESSION="cron(0 18 * * ? *)"

# Every 12 hours
SCHEDULE_EXPRESSION="cron(0 */12 * * ? *)"

# Every day (simple)
SCHEDULE_EXPRESSION="rate(1 day)"
```

Then re-run: `./setup_eventbridge.sh`

### Add Another Model/Influencer

To add another Instagram account:

1. Create S3 bucket:
```bash
aws s3 mb s3://new-model-instagram --region us-east-2
aws s3api put-bucket-policy --bucket new-model-instagram --policy file://bucket-policy.json
```

2. Deploy new Lambda function (change FUNCTION_NAME in scripts):
```bash
# Edit each .sh file and change:
FUNCTION_NAME="new-model-scraper-daily"
```

3. Run setup again with new configuration

---

## Monitoring

### View Lambda logs
```bash
aws logs tail /aws/lambda/instagram-scraper-daily --follow
```

### Check last execution
```bash
aws lambda get-function --function-name instagram-scraper-daily \
    --query 'Configuration.LastModified'
```

### View S3 uploads
```bash
aws s3 ls s3://madison-morgan-instagram/madison-morgan/posts/ --recursive
```

---

## Cost Estimate

**Free Tier:**
- Lambda: 1M requests + 400,000 GB-seconds/month FREE
- EventBridge: 1M events/month FREE
- S3: 5 GB storage FREE

**Your usage (daily scraping):**
- Lambda: ~30 executions/month
- Each run: ~2-3 minutes
- Storage: ~5-10 GB/model

**Estimated cost: $0/month** (within free tier)

After free tier:
- Lambda: ~$0.01/month
- S3 storage: ~$0.23/month for 10 GB

---

## Troubleshooting

### Lambda timeout
If scraping >100 posts, increase timeout:
```bash
aws lambda update-function-configuration \
    --function-name instagram-scraper-daily \
    --timeout 900
```

### Not running on schedule
Check EventBridge rule status:
```bash
aws events describe-rule --name instagram-scraper-daily-schedule
```

### S3 permission errors
Re-run IAM setup:
```bash
./setup_lambda_iam.sh
```

---

## Disable/Enable

### Disable daily scraping
```bash
aws events disable-rule --name instagram-scraper-daily-schedule
```

### Enable daily scraping
```bash
aws events enable-rule --name instagram-scraper-daily-schedule
```

### Delete everything
```bash
# Delete EventBridge rule
aws events remove-targets --rule instagram-scraper-daily-schedule --ids 1
aws events delete-rule --name instagram-scraper-daily-schedule

# Delete Lambda function
aws lambda delete-function --function-name instagram-scraper-daily

# Delete IAM role
aws iam detach-role-policy --role-name instagram-scraper-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws iam detach-role-policy --role-name instagram-scraper-lambda-role \
    --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/instagram-scraper-lambda-policy

aws iam delete-role --role-name instagram-scraper-lambda-role
```

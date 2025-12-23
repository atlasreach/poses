#!/bin/bash
# Set up EventBridge (CloudWatch Events) schedule for daily scraping

set -e

FUNCTION_NAME="instagram-scraper-daily"
RULE_NAME="instagram-scraper-daily-schedule"
REGION="us-east-2"

# Schedule: Daily at 3 AM UTC (adjust as needed)
# Use cron expression: cron(0 3 * * ? *)
# Or rate expression for testing: rate(1 day)
SCHEDULE_EXPRESSION="cron(0 3 * * ? *)"

echo "⏰ Setting up EventBridge schedule for daily scraping"

# Get Lambda function ARN
FUNCTION_ARN=$(aws lambda get-function --function-name $FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text)

echo "Lambda ARN: $FUNCTION_ARN"

# Create or update EventBridge rule
echo "Creating EventBridge rule: $RULE_NAME"
aws events put-rule \
    --name $RULE_NAME \
    --schedule-expression "$SCHEDULE_EXPRESSION" \
    --state ENABLED \
    --description "Daily Instagram scraping and S3 migration" \
    --region $REGION

# Get rule ARN
RULE_ARN=$(aws events describe-rule --name $RULE_NAME --region $REGION --query 'Arn' --output text)

echo "Rule ARN: $RULE_ARN"

# Add Lambda permission for EventBridge to invoke
echo "Adding Lambda permission for EventBridge..."
aws lambda add-permission \
    --function-name $FUNCTION_NAME \
    --statement-id AllowEventBridgeInvoke \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn $RULE_ARN \
    --region $REGION \
    2>/dev/null || echo "Permission already exists"

# Add Lambda as target for the rule
echo "Adding Lambda as target..."
aws events put-targets \
    --rule $RULE_NAME \
    --targets "Id"="1","Arn"="$FUNCTION_ARN" \
    --region $REGION

echo "✅ EventBridge schedule configured successfully!"
echo ""
echo "Schedule: $SCHEDULE_EXPRESSION (Daily at 3 AM UTC)"
echo "Next run: $(date -u -d 'tomorrow 03:00' '+%Y-%m-%d %H:%M UTC' 2>/dev/null || echo 'Check AWS Console')"
echo ""
echo "To change the schedule, edit the SCHEDULE_EXPRESSION in this script and re-run."
echo ""
echo "Schedule examples:"
echo "  - Daily at 3 AM UTC:    cron(0 3 * * ? *)"
echo "  - Every 12 hours:       cron(0 */12 * * ? *)"
echo "  - Every day at 6 PM:    cron(0 18 * * ? *)"
echo "  - Every 1 day:          rate(1 day)"

"""
AWS Lambda function for automated Instagram scraping and S3 migration
Triggers daily via EventBridge
"""

import json
import os
import requests
import boto3
from apify_client import ApifyClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

def get_image_extension(url):
    """Extract image extension from URL or default to jpg"""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    if ext and ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
        return ext.lower()
    return '.jpg'

def generate_image_key(url, model_name, post_id, image_index):
    """Generate a unique S3 key for the image"""
    ext = get_image_extension(url)
    return f"{model_name}/posts/{post_id}/image_{image_index:03d}{ext}"

def download_image(url, max_retries=3):
    """Download image from URL with retries"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                if attempt == max_retries - 1:
                    print(f"Failed to download {url}: Status {response.status_code}")
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error downloading {url}: {e}")
    return None

def upload_to_s3(s3_client, bucket_name, key, image_data):
    """Upload image data to S3"""
    try:
        content_type = 'image/jpeg'
        if key.endswith('.png'):
            content_type = 'image/png'
        elif key.endswith('.webp'):
            content_type = 'image/webp'

        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=image_data,
            ContentType=content_type,
            CacheControl='public, max-age=31536000'
        )
        return True
    except Exception as e:
        print(f"Error uploading to S3 {key}: {e}")
        return False

def process_image(args):
    """Process a single image: download and upload to S3"""
    url, s3_client, bucket_name, s3_key, region = args

    # Download image immediately
    image_data = download_image(url)
    if not image_data:
        return None, None

    # Upload to S3
    if upload_to_s3(s3_client, bucket_name, s3_key, image_data):
        # Generate S3 URL
        s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
        return url, s3_url

    return None, None

def scrape_and_migrate(username, bucket_name, model_name, apify_token, region='us-east-2', max_posts=100):
    """Main function to scrape Instagram and immediately migrate to S3"""

    print(f"Starting scrape for @{username}...")

    # Initialize clients
    client = ApifyClient(apify_token)
    s3_client = boto3.client('s3', region_name=region)

    # Prepare Actor input
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
    }

    # Run the Actor
    print("Running Apify scraper...")
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)

    # Get dataset
    dataset_id = run["defaultDatasetId"]
    print(f"Scrape complete! Dataset: {dataset_id}")

    # Fetch all items
    posts = []
    print("Fetching posts from dataset...")
    for item in client.dataset(dataset_id).iterate_items():
        posts.append(item)

    print(f"Found {len(posts)} posts")

    # Collect all images to process
    image_tasks = []
    url_to_post_map = {}

    for post_idx, post in enumerate(posts):
        post_id = post.get('id', f'post_{post_idx}')

        # Process displayUrl
        if 'displayUrl' in post and post['displayUrl']:
            s3_key = generate_image_key(post['displayUrl'], model_name, post_id, 0)
            image_tasks.append((post['displayUrl'], s3_client, bucket_name, s3_key, region))
            url_to_post_map[post['displayUrl']] = (post_idx, 0, 'displayUrl')

        # Process images array
        if 'images' in post and post['images']:
            for img_idx, img_url in enumerate(post['images']):
                s3_key = generate_image_key(img_url, model_name, post_id, img_idx)
                image_tasks.append((img_url, s3_client, bucket_name, s3_key, region))
                url_to_post_map[img_url] = (post_idx, img_idx, 'images')

    print(f"Processing {len(image_tasks)} images...")

    # Process images in parallel
    url_mapping = {}
    successful = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_image, task) for task in image_tasks]

        for future in as_completed(futures):
            old_url, new_url = future.result()
            if old_url and new_url:
                url_mapping[old_url] = new_url
                successful += 1
            else:
                failed += 1

    print(f"Upload complete: {successful}/{len(image_tasks)} successful")

    # Update posts with S3 URLs
    for post in posts:
        if 'displayUrl' in post and post['displayUrl'] in url_mapping:
            post['displayUrl'] = url_mapping[post['displayUrl']]

        if 'images' in post and post['images']:
            post['images'] = [
                url_mapping.get(url, url) for url in post['images']
            ]

    # Save to S3 as JSON
    json_key = f"{model_name}/instagram_data.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=json_key,
        Body=json.dumps(posts, indent=2, ensure_ascii=False),
        ContentType='application/json'
    )

    print(f"Saved JSON to s3://{bucket_name}/{json_key}")

    return {
        'posts': len(posts),
        'images_total': len(image_tasks),
        'images_successful': successful,
        'images_failed': failed
    }

def lambda_handler(event, context):
    """
    AWS Lambda handler function

    Environment variables required:
    - APIFY_API_TOKEN: Your Apify API token
    - INSTAGRAM_USERNAME: Instagram username to scrape
    - S3_BUCKET_NAME: S3 bucket name
    - MODEL_NAME: Model name for folder structure
    - AWS_REGION: AWS region (default: us-east-2)
    - MAX_POSTS: Maximum posts to scrape (default: 100)
    """

    try:
        # Get configuration from environment variables
        apify_token = os.environ['APIFY_API_TOKEN']
        username = os.environ['INSTAGRAM_USERNAME']
        bucket_name = os.environ['S3_BUCKET_NAME']
        model_name = os.environ['MODEL_NAME']
        region = os.environ.get('AWS_REGION', 'us-east-2')
        max_posts = int(os.environ.get('MAX_POSTS', '100'))

        print(f"Lambda triggered for @{username}")

        # Run scrape and migrate
        result = scrape_and_migrate(
            username=username,
            bucket_name=bucket_name,
            model_name=model_name,
            apify_token=apify_token,
            region=region,
            max_posts=max_posts
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scrape and migration completed successfully',
                'result': result
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error during scrape and migration',
                'error': str(e)
            })
        }

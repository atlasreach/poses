#!/usr/bin/env python3
"""
Combined scrape and migrate script for Instagram → S3
Processes images immediately to avoid URL expiration
"""

import os
import json
import requests
import boto3
from dotenv import load_dotenv
from apify_client import ApifyClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from urllib.parse import urlparse

# Load environment variables
load_dotenv('.env.local')

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
                    print(f"❌ Failed to download {url}: Status {response.status_code}")
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ Error downloading {url}: {e}")
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
        print(f"❌ Error uploading to S3 {key}: {e}")
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

def scrape_and_migrate(username, bucket_name, model_name, region='us-east-2', max_posts=100, max_workers=10):
    """
    Main function to scrape Instagram and immediately migrate to S3
    """

    # Initialize clients
    apify_token = os.getenv('APIFY_API_TOKEN')
    client = ApifyClient(apify_token)
    s3_client = boto3.client('s3', region_name=region)

    print(f"🔄 Scraping Instagram @{username}...")

    # Prepare Actor input
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
    }

    # Run the Actor and wait for it to finish
    print(f"⏳ Running Apify scraper (this may take a few minutes)...")
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)

    # Get dataset
    dataset_id = run["defaultDatasetId"]
    print(f"✅ Scrape complete! Dataset: https://console.apify.com/storage/datasets/{dataset_id}")

    # Fetch all items from dataset
    posts = []
    print(f"📥 Fetching posts from dataset...")
    for item in client.dataset(dataset_id).iterate_items():
        posts.append(item)

    print(f"✅ Found {len(posts)} posts")

    # Collect all images to process IMMEDIATELY
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

    print(f"📸 Processing {len(image_tasks)} images immediately...")
    print(f"⚡ Starting parallel upload to S3 (this will take a few minutes)...")

    # Process images in parallel IMMEDIATELY
    url_mapping = {}
    successful = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, task) for task in image_tasks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Uploading to S3"):
            old_url, new_url = future.result()
            if old_url and new_url:
                url_mapping[old_url] = new_url
                successful += 1
            else:
                failed += 1

    print(f"\n📊 Upload Results:")
    print(f"   ✅ Successful: {successful}/{len(image_tasks)}")
    print(f"   ❌ Failed: {failed}/{len(image_tasks)}")

    # Update posts with S3 URLs
    print("🔄 Updating posts with S3 URLs...")
    for post in posts:
        if 'displayUrl' in post and post['displayUrl'] in url_mapping:
            post['displayUrl'] = url_mapping[post['displayUrl']]

        if 'images' in post and post['images']:
            post['images'] = [
                url_mapping.get(url, url) for url in post['images']
            ]

    # Save updated JSON
    output_file = f'viewer/public/instagram_data.json'
    print(f"💾 Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Complete!")
    print(f"   - Posts scraped: {len(posts)}")
    print(f"   - Images uploaded: {successful}/{len(image_tasks)}")
    print(f"   - S3 Bucket: https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}")
    print(f"   - JSON saved: {output_file}")

    return posts, successful, failed

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python scrape_and_migrate_to_s3.py <username> <bucket_name> <model_name> [region] [max_posts]")
        print("Example: python scrape_and_migrate_to_s3.py madison.moorgan madison-morgan-instagram madison-morgan us-east-2 100")
        sys.exit(1)

    username = sys.argv[1]
    bucket_name = sys.argv[2]
    model_name = sys.argv[3]
    region = sys.argv[4] if len(sys.argv) > 4 else 'us-east-2'
    max_posts = int(sys.argv[5]) if len(sys.argv) > 5 else 100

    scrape_and_migrate(username, bucket_name, model_name, region, max_posts)

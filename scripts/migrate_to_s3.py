#!/usr/bin/env python3
"""
Script to migrate Instagram images from CDN URLs to AWS S3.
Usage: python migrate_to_s3.py <json_file> <bucket_name> <model_name>
Example: python migrate_to_s3.py instagram_data.json madison-morgan-instagram madison-morgan
"""

import json
import sys
import os
import requests
import boto3
from urllib.parse import urlparse
from pathlib import Path
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to download {url}: Status {response.status_code}")
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error downloading {url}: {e}")
                return None
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

    # Download image
    image_data = download_image(url)
    if not image_data:
        return None, None

    # Upload to S3
    if upload_to_s3(s3_client, bucket_name, s3_key, image_data):
        # Generate S3 URL
        s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
        return url, s3_url

    return None, None

def migrate_instagram_to_s3(json_file, bucket_name, model_name, region='us-east-2', max_workers=10):
    """Main function to migrate Instagram images to S3"""

    # Initialize S3 client
    s3_client = boto3.client('s3', region_name=region)

    # Read JSON file
    print(f"Reading {json_file}...")
    with open(json_file, 'r') as f:
        posts = json.load(f)

    print(f"Found {len(posts)} posts")

    # Collect all images to process
    image_tasks = []
    url_to_post_map = {}  # Map URL to (post_index, image_index, field_name)

    for post_idx, post in enumerate(posts):
        # Process displayUrl
        if 'displayUrl' in post and post['displayUrl']:
            s3_key = generate_image_key(post['displayUrl'], model_name, post['id'], 0)
            image_tasks.append((post['displayUrl'], s3_client, bucket_name, s3_key, region))
            url_to_post_map[post['displayUrl']] = (post_idx, 0, 'displayUrl')

        # Process images array
        if 'images' in post and post['images']:
            for img_idx, img_url in enumerate(post['images']):
                s3_key = generate_image_key(img_url, model_name, post['id'], img_idx)
                image_tasks.append((img_url, s3_client, bucket_name, s3_key, region))
                url_to_post_map[img_url] = (post_idx, img_idx, 'images')

    print(f"Processing {len(image_tasks)} images...")

    # Process images in parallel
    url_mapping = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, task) for task in image_tasks]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Uploading images"):
            old_url, new_url = future.result()
            if old_url and new_url:
                url_mapping[old_url] = new_url

    # Update posts with S3 URLs
    print("Updating JSON with S3 URLs...")
    for post in posts:
        if 'displayUrl' in post and post['displayUrl'] in url_mapping:
            post['displayUrl'] = url_mapping[post['displayUrl']]

        if 'images' in post and post['images']:
            post['images'] = [
                url_mapping.get(url, url) for url in post['images']
            ]

    # Save updated JSON
    output_file = json_file.replace('.json', '_s3.json')
    print(f"Saving updated JSON to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)

    print(f"\n✅ Migration complete!")
    print(f"   - Processed: {len(image_tasks)} images")
    print(f"   - Uploaded: {len(url_mapping)} images successfully")
    print(f"   - Updated JSON saved to: {output_file}")
    print(f"\nS3 Bucket: https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python migrate_to_s3.py <json_file> <bucket_name> <model_name> [region]")
        print("Example: python migrate_to_s3.py instagram_data.json madison-morgan-instagram madison-morgan")
        sys.exit(1)

    json_file = sys.argv[1]
    bucket_name = sys.argv[2]
    model_name = sys.argv[3]
    region = sys.argv[4] if len(sys.argv) > 4 else 'us-east-2'

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        sys.exit(1)

    migrate_instagram_to_s3(json_file, bucket_name, model_name, region)

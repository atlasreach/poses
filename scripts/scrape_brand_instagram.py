#!/usr/bin/env python3
"""Scrape brand Instagram - matches ISMÊ structure"""
import os
import json
import requests
import sys
from dotenv import load_dotenv

load_dotenv('.env.local')
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')

def scrape_instagram(username, max_posts=1000):
    """Scrape Instagram posts using Apify"""
    print(f"\n📸 Scraping @{username} (up to {max_posts} posts)")

    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    payload = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "addParentData": False
    }

    try:
        print("⏳ This will take 2-5 minutes...")
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )

        if response.status_code in [200, 201]:
            posts = response.json()
            print(f"✅ Scraped {len(posts)} posts")
            return posts
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_instagram_data(brand_slug, posts):
    """Save Instagram data - matches ISMÊ structure"""
    instagram_dir = f"brands/{brand_slug}/instagram"
    os.makedirs(instagram_dir, exist_ok=True)

    # Process posts
    processed = []
    all_images = []

    for post in posts:
        item = {
            'post_id': post.get('id'),
            'post_url': post.get('url'),
            'shortcode': post.get('shortCode'),
            'caption': post.get('caption', ''),
            'type': post.get('type'),
            'timestamp': post.get('timestamp'),
            'likes': post.get('likesCount', 0),
            'comments': post.get('commentsCount', 0),
            'images': []
        }

        # Main image
        if post.get('displayUrl'):
            item['images'].append(post['displayUrl'])
            all_images.append({
                'url': post['displayUrl'],
                'post_url': post.get('url'),
                'likes': post.get('likesCount', 0)
            })

        # Video
        if post.get('type') == 'Video' and post.get('videoUrl'):
            item['video_url'] = post.get('videoUrl')

        # Carousel images
        if post.get('childPosts'):
            for child in post['childPosts']:
                if child.get('displayUrl'):
                    item['images'].append(child['displayUrl'])
                    all_images.append({
                        'url': child['displayUrl'],
                        'post_url': post.get('url'),
                        'likes': post.get('likesCount', 0)
                    })

        processed.append(item)

    # Save like ISMÊ: {brand}_instagram_processed.json
    posts_file = f"{instagram_dir}/{brand_slug}_instagram_processed.json"
    with open(posts_file, 'w') as f:
        json.dump(processed, f, indent=2)

    # Save images
    images_file = f"{instagram_dir}/{brand_slug}_instagram_images.json"
    with open(images_file, 'w') as f:
        json.dump(all_images, f, indent=2)

    return len(processed), len(all_images)

def print_summary(brand_name, total_posts, total_images, brand_slug):
    """Print summary"""
    print(f"\n{'='*60}")
    print(f"✅ {brand_name.upper()} INSTAGRAM - COMPLETE")
    print('='*60)
    print(f"\n📸 Posts: {total_posts}")
    print(f"🖼️  Images: {total_images}")
    print(f"\n💾 Saved to: brands/{brand_slug}/instagram/")
    print(f"   - {brand_slug}_instagram_processed.json")
    print(f"   - {brand_slug}_instagram_images.json")
    print('='*60)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scrape_brand_instagram.py <brand-slug> <instagram-username>")
        sys.exit(1)

    brand_slug = sys.argv[1]
    instagram_username = sys.argv[2]
    brand_name = sys.argv[3] if len(sys.argv) > 3 else brand_slug

    # Scrape
    posts = scrape_instagram(instagram_username, max_posts=1000)

    if posts:
        total_posts, total_images = save_instagram_data(brand_slug, posts)
        print_summary(brand_name, total_posts, total_images, brand_slug)
    else:
        print("\n❌ Instagram scraping failed!")

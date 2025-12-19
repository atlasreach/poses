import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
APIFY_API_URL = os.getenv('APIFY_API_URL')

def scrape_instagram_profile(username, max_posts=100):
    """
    Scrape Instagram profile using Apify API

    Args:
        username: Instagram username (e.g., 'ismeswim')
        max_posts: Maximum number of posts to scrape
    """

    # Apify Instagram scraper input configuration
    payload = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "searchType": "hashtag",
        "searchLimit": 1,
        "addParentData": False
    }

    print(f"🔄 Starting Instagram scrape for @{username}...")
    print(f"📊 Requesting up to {max_posts} posts")

    # Make request to Apify API
    try:
        response = requests.post(
            f"{APIFY_API_URL}?token={APIFY_API_TOKEN}",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300  # 5 minute timeout for sync API
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully scraped {len(data)} posts!")
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("⏰ Request timed out. Try reducing max_posts or use async API.")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_instagram_data(data, filename='isme_instagram_data.json'):
    """Save scraped Instagram data to JSON file"""
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to {filename}")
        return True
    return False

def extract_product_images(data):
    """Extract just the image URLs and captions for product analysis"""
    products = []

    for post in data:
        product_info = {
            'id': post.get('id'),
            'shortcode': post.get('shortCode'),
            'url': post.get('url'),
            'caption': post.get('caption', ''),
            'timestamp': post.get('timestamp'),
            'likes': post.get('likesCount'),
            'comments': post.get('commentsCount'),
            'images': []
        }

        # Extract image URLs
        if post.get('displayUrl'):
            product_info['images'].append(post['displayUrl'])

        # Check for carousel images
        if post.get('childPosts'):
            for child in post['childPosts']:
                if child.get('displayUrl'):
                    product_info['images'].append(child['displayUrl'])

        products.append(product_info)

    return products

if __name__ == "__main__":
    # Scrape ISMÊ Swim Instagram
    username = "ismeswim"
    max_posts = 100  # Adjust as needed

    data = scrape_instagram_profile(username, max_posts)

    if data:
        # Save full data
        save_instagram_data(data, 'isme_instagram_full.json')

        # Extract and save just product images
        products = extract_product_images(data)
        save_instagram_data(products, 'isme_instagram_products.json')

        # Print summary
        print("\n📈 Summary:")
        print(f"Total posts scraped: {len(data)}")
        print(f"Total images extracted: {sum(len(p['images']) for p in products)}")
        print(f"\nTop 3 most liked posts:")
        sorted_posts = sorted(products, key=lambda x: x.get('likes', 0), reverse=True)
        for i, post in enumerate(sorted_posts[:3], 1):
            print(f"{i}. {post['likes']:,} likes - {post['url']}")

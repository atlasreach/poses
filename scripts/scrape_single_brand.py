#!/usr/bin/env python3
"""Scrape single brand - products + Instagram"""
import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv('.env.local')
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')

def scrape_shopify_products(website_url, brand_name):
    """Scrape all products from Shopify store"""
    print(f"\n🛍️  SCRAPING PRODUCTS from {website_url}")

    try:
        # Try Shopify products.json API
        products_url = f"{website_url.rstrip('/')}/products.json?limit=250"
        response = requests.get(products_url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Found {len(products)} products via Shopify API")
            return products
        else:
            print(f"❌ Shopify API failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def scrape_instagram(username, max_posts=1000):
    """Scrape Instagram posts using Apify"""
    print(f"\n📸 SCRAPING INSTAGRAM @{username} (up to {max_posts} posts)")

    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    payload = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "addParentData": False
    }

    try:
        print("⏳ Starting Instagram scrape (this may take 2-5 minutes)...")
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )

        if response.status_code in [200, 201]:
            posts = response.json()
            print(f"✅ Scraped {len(posts)} Instagram posts")
            return posts
        else:
            print(f"❌ Instagram scrape failed: {response.status_code}")
            print(response.text[:500])
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_brand_data(brand_name, products, instagram_posts):
    """Save all brand data to organized folders"""
    brand_slug = brand_name.lower().replace(' ', '-').replace('&', 'and')
    brand_dir = f"../brands/{brand_slug}"

    # Create directories
    os.makedirs(f"{brand_dir}/products", exist_ok=True)
    os.makedirs(f"{brand_dir}/instagram", exist_ok=True)

    # Save products
    if products:
        with open(f"{brand_dir}/products/catalog.json", 'w') as f:
            json.dump(products, f, indent=2)

        # Extract just image URLs
        all_images = []
        for product in products:
            for img in product.get('images', []):
                all_images.append({
                    'product_title': product['title'],
                    'image_url': img['src'],
                    'product_url': f"https://www.vitaminaswim.com/products/{product['handle']}"
                })

        with open(f"{brand_dir}/products/images.json", 'w') as f:
            json.dump(all_images, f, indent=2)

        with open(f"{brand_dir}/products/image_urls.txt", 'w') as f:
            for img in all_images:
                f.write(img['image_url'] + '\n')

    # Save Instagram
    if instagram_posts:
        with open(f"{brand_dir}/instagram/posts.json", 'w') as f:
            json.dump(instagram_posts, f, indent=2)

        # Extract image URLs
        ig_images = []
        for post in instagram_posts:
            item = {
                'post_url': post.get('url'),
                'caption': post.get('caption', '')[:100],
                'likes': post.get('likesCount', 0),
                'comments': post.get('commentsCount', 0),
                'images': []
            }

            if post.get('displayUrl'):
                item['images'].append(post['displayUrl'])
                ig_images.append({
                    'url': post['displayUrl'],
                    'post_url': post.get('url'),
                    'likes': post.get('likesCount', 0)
                })

            if post.get('childPosts'):
                for child in post['childPosts']:
                    if child.get('displayUrl'):
                        item['images'].append(child['displayUrl'])
                        ig_images.append({
                            'url': child['displayUrl'],
                            'post_url': post.get('url'),
                            'likes': post.get('likesCount', 0)
                        })

        with open(f"{brand_dir}/instagram/images.json", 'w') as f:
            json.dump(ig_images, f, indent=2)

        with open(f"{brand_dir}/instagram/image_urls.txt", 'w') as f:
            for img in ig_images:
                f.write(img['url'] + '\n')

    return brand_dir

def generate_summary(brand_name, brand_dir, products, instagram_posts):
    """Generate summary report"""
    print(f"\n" + "="*60)
    print(f"📊 SUMMARY: {brand_name}")
    print("="*60)

    if products:
        total_variants = sum(len(p.get('variants', [])) for p in products)
        total_images = sum(len(p.get('images', [])) for p in products)
        print(f"\n🛍️  PRODUCTS:")
        print(f"   Total products: {len(products)}")
        print(f"   Total variants: {total_variants}")
        print(f"   Total images: {total_images}")

    if instagram_posts:
        total_ig_images = sum(1 + len(p.get('childPosts', [])) for p in instagram_posts)
        print(f"\n📸 INSTAGRAM:")
        print(f"   Total posts: {len(instagram_posts)}")
        print(f"   Total images: {total_ig_images}")

        # Top posts
        sorted_posts = sorted(instagram_posts, key=lambda x: x.get('likesCount', 0), reverse=True)
        print(f"\n🔥 Top 5 Posts:")
        for i, post in enumerate(sorted_posts[:5], 1):
            print(f"   {i}. {post.get('likesCount', 0):,} likes - {post.get('url')}")

    print(f"\n💾 Data saved to: {brand_dir}/")
    print(f"   - products/catalog.json")
    print(f"   - products/images.json")
    print(f"   - instagram/posts.json")
    print(f"   - instagram/images.json")
    print("="*60)

if __name__ == "__main__":
    # Brand info
    brand = {
        "name": "Vitamin A",
        "website": "https://www.vitaminaswim.com",
        "instagram": "vitaminaswim"
    }

    print(f"\n🚀 SCRAPING: {brand['name']}")
    print(f"   Website: {brand['website']}")
    print(f"   Instagram: @{brand['instagram']}")

    # Scrape products
    products = scrape_shopify_products(brand['website'], brand['name'])

    # Scrape Instagram
    instagram_posts = scrape_instagram(brand['instagram'], max_posts=1000)

    # Save everything
    if products or instagram_posts:
        brand_dir = save_brand_data(brand['name'], products, instagram_posts)
        generate_summary(brand['name'], brand_dir, products, instagram_posts)
    else:
        print("\n❌ No data scraped!")

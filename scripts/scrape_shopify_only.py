#!/usr/bin/env python3
"""Simple Shopify product scraper - no Apify needed"""
import json
import requests
import os

def scrape_shopify_products(website_url, brand_name):
    """Scrape all products from Shopify store using /products.json API"""
    print(f"🛍️  Scraping {brand_name} products from {website_url}")

    try:
        products_url = f"{website_url.rstrip('/')}/products.json?limit=250"
        response = requests.get(products_url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Found {len(products)} products")
            return products
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_products(brand_name, products):
    """Save products to organized folder"""
    brand_slug = brand_name.lower().replace(' ', '-')
    brand_dir = f"../brands/{brand_slug}/products"
    os.makedirs(brand_dir, exist_ok=True)

    # Save full catalog
    with open(f"{brand_dir}/catalog.json", 'w') as f:
        json.dump(products, f, indent=2)

    # Extract all images with product info
    all_images = []
    for product in products:
        for img in product.get('images', []):
            all_images.append({
                'product_id': product['id'],
                'product_title': product['title'],
                'product_handle': product['handle'],
                'image_url': img['src'],
                'image_id': img['id']
            })

    with open(f"{brand_dir}/images.json", 'w') as f:
        json.dump(all_images, f, indent=2)

    # Save plain text URLs for downloading
    with open(f"{brand_dir}/image_urls.txt", 'w') as f:
        for img in all_images:
            f.write(img['image_url'] + '\n')

    return brand_dir, all_images

def print_summary(brand_name, products, all_images, brand_dir):
    """Print summary"""
    print(f"\n{'='*60}")
    print(f"📊 {brand_name.upper()} - SCRAPE COMPLETE")
    print('='*60)
    print(f"\n📦 Products: {len(products)}")

    total_variants = sum(len(p.get('variants', [])) for p in products)
    print(f"🎨 Variants: {total_variants}")
    print(f"🖼️  Images: {len(all_images)}")

    # Price range
    prices = []
    for p in products:
        for v in p['variants']:
            try:
                prices.append(float(v['price']))
            except:
                pass

    if prices:
        print(f"\n💰 Price Range:")
        print(f"   Min: ${min(prices):.2f}")
        print(f"   Max: ${max(prices):.2f}")
        print(f"   Avg: ${sum(prices)/len(prices):.2f}")

    print(f"\n💾 Files saved:")
    print(f"   {brand_dir}/catalog.json")
    print(f"   {brand_dir}/images.json")
    print(f"   {brand_dir}/image_urls.txt")
    print('='*60)

if __name__ == "__main__":
    # Brand to scrape
    brand_name = "Vitamin A"
    website = "https://www.vitaminaswim.com"

    # Scrape
    products = scrape_shopify_products(website, brand_name)

    if products:
        brand_dir, all_images = save_products(brand_name, products)
        print_summary(brand_name, products, all_images, brand_dir)
    else:
        print("❌ No products found!")

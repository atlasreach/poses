#!/usr/bin/env python3
"""Scrape brand Shopify - matches ISMÊ folder structure"""
import json
import requests
import os
import sys

def scrape_shopify(website_url, brand_name):
    """Scrape Shopify products - returns ALL fields like ISMÊ"""
    print(f"\n🛍️  Scraping {brand_name}")
    print(f"   Website: {website_url}")

    try:
        url = f"{website_url.rstrip('/')}/products.json?limit=250"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])

            # Process products to match ISMÊ structure
            processed = []
            for p in products:
                product = {
                    "id": p['id'],
                    "title": p['title'],
                    "handle": p['handle'],
                    "url": f"{website_url.rstrip('/')}/products/{p['handle']}",
                    "description": p.get('body_html', ''),
                    "vendor": p.get('vendor', ''),
                    "product_type": p.get('product_type', ''),
                    "tags": p.get('tags', []) if isinstance(p.get('tags'), list) else p.get('tags', '').split(', '),
                    "created_at": p.get('created_at', ''),
                    "published_at": p.get('published_at', ''),
                    "variants": [],
                    "images": []
                }

                # Variants
                for v in p.get('variants', []):
                    product['variants'].append({
                        "id": v['id'],
                        "title": v['title'],
                        "option1": v.get('option1'),
                        "option2": v.get('option2'),
                        "option3": v.get('option3'),
                        "price": v['price'],
                        "compare_at_price": v.get('compare_at_price'),
                        "available": v.get('available', True),
                        "sku": v.get('sku')
                    })

                # Images
                for img in p.get('images', []):
                    product['images'].append(img['src'])

                processed.append(product)

            print(f"✅ Found {len(processed)} products")
            return processed
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_brand_data(brand_slug, brand_name, products):
    """Save in same structure as ISMÊ"""
    # Create folder structure
    brand_dir = f"brands/{brand_slug}"
    products_dir = f"{brand_dir}/products"
    os.makedirs(products_dir, exist_ok=True)

    # Save complete catalog (like isme_complete_product_catalog.json)
    catalog_file = f"{products_dir}/{brand_slug}_complete_product_catalog.json"
    with open(catalog_file, 'w') as f:
        json.dump(products, f, indent=2)

    # Extract all images (like isme_all_product_images.json)
    all_images = []
    for product in products:
        for img_url in product['images']:
            all_images.append({
                'product_id': product['id'],
                'product_title': product['title'],
                'product_url': product['url'],
                'image_url': img_url
            })

    images_file = f"{products_dir}/{brand_slug}_all_product_images.json"
    with open(images_file, 'w') as f:
        json.dump(all_images, f, indent=2)

    return brand_dir, len(all_images)

def print_summary(brand_name, products, total_images, brand_dir):
    """Print summary"""
    print(f"\n{'='*60}")
    print(f"✅ {brand_name.upper()} - COMPLETE")
    print('='*60)

    total_variants = sum(len(p['variants']) for p in products)

    print(f"\n📦 Products: {len(products)}")
    print(f"🎨 Variants: {total_variants}")
    print(f"🖼️  Images: {total_images}")

    # Sample vendor/product type info
    vendors = set(p['vendor'] for p in products if p['vendor'])
    product_types = set(p['product_type'] for p in products if p['product_type'])

    if vendors:
        print(f"\n🏷️  Vendors: {', '.join(list(vendors)[:3])}")
    if product_types:
        print(f"📂 Product Types: {', '.join(list(product_types)[:5])}")

    print(f"\n💾 Saved to: {brand_dir}/products/")
    print(f"   - {brand_dir.split('/')[-1]}_complete_product_catalog.json")
    print(f"   - {brand_dir.split('/')[-1]}_all_product_images.json")
    print('='*60)

if __name__ == "__main__":
    # Brand to scrape (can be passed as argument)
    if len(sys.argv) > 1:
        brand_slug = sys.argv[1]
        brand_name = sys.argv[2] if len(sys.argv) > 2 else brand_slug
        website = sys.argv[3] if len(sys.argv) > 3 else f"https://{brand_slug}.com"
    else:
        # Default: Vitamin A
        brand_slug = "vitamin-a"
        brand_name = "Vitamin A"
        website = "https://www.vitaminaswim.com"

    # Scrape
    products = scrape_shopify(website, brand_name)

    if products:
        brand_dir, total_images = save_brand_data(brand_slug, brand_name, products)
        print_summary(brand_name, products, total_images, brand_dir)
    else:
        print("\n❌ Scraping failed!")

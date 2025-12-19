import json

# Load the Shopify products data
with open('isme_all_products_shopify.json', 'r') as f:
    data = json.load(f)

products = data['products']
print(f"📦 Processing {len(products)} products...")

# Extract full product catalog
catalog = []
all_images = []

for product in products:
    # Basic product info
    item = {
        'id': product['id'],
        'title': product['title'],
        'handle': product['handle'],
        'url': f"https://ismeswim.com/products/{product['handle']}",
        'description': product.get('body_html', ''),
        'vendor': product.get('vendor', ''),
        'product_type': product.get('product_type', ''),
        'tags': product.get('tags', []),
        'created_at': product.get('created_at', ''),
        'published_at': product.get('published_at', ''),
        'variants': [],
        'images': []
    }

    # Extract variants (sizes, colors, prices)
    for variant in product.get('variants', []):
        item['variants'].append({
            'id': variant['id'],
            'title': variant['title'],
            'option1': variant.get('option1'),  # Usually size
            'option2': variant.get('option2'),  # Usually color
            'option3': variant.get('option3'),
            'price': variant['price'],
            'compare_at_price': variant.get('compare_at_price'),
            'available': variant.get('available', True),
            'sku': variant.get('sku', '')
        })

    # Extract all images
    for img in product.get('images', []):
        image_url = img['src']
        item['images'].append(image_url)
        all_images.append({
            'product_id': product['id'],
            'product_title': product['title'],
            'product_url': f"https://ismeswim.com/products/{product['handle']}",
            'image_url': image_url,
            'image_id': img['id'],
            'width': img.get('width'),
            'height': img.get('height')
        })

    catalog.append(item)

# Save complete catalog
with open('isme_complete_product_catalog.json', 'w') as f:
    json.dump(catalog, f, indent=2)

# Save all image URLs
with open('isme_all_product_images.json', 'w') as f:
    json.dump(all_images, f, indent=2)

# Save image URLs as plain text for downloading
with open('isme_all_image_urls.txt', 'w') as f:
    for img in all_images:
        f.write(img['image_url'] + '\n')

# Generate stats
total_variants = sum(len(p['variants']) for p in catalog)
total_images = len(all_images)

print(f"\n✅ EXTRACTION COMPLETE!\n")
print(f"📊 Statistics:")
print(f"   Total products: {len(catalog)}")
print(f"   Total variants (sizes/colors): {total_variants}")
print(f"   Total product images: {total_images}")

# Show product types
product_types = {}
for p in catalog:
    ptype = p['product_type'] or 'Other'
    product_types[ptype] = product_types.get(ptype, 0) + 1

print(f"\n📦 Product Types:")
for ptype, count in sorted(product_types.items(), key=lambda x: x[1], reverse=True):
    print(f"   {ptype}: {count}")

# Show price range
prices = []
for p in catalog:
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

print(f"\n💾 Files Created:")
print(f"   - isme_complete_product_catalog.json (full product data)")
print(f"   - isme_all_product_images.json (all images with metadata)")
print(f"   - isme_all_image_urls.txt (plain URLs for bulk download)")

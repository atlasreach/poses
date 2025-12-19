#!/bin/bash

# Create organized folder structure
mkdir -p brands/isme/{products,instagram}
mkdir -p scripts
mkdir -p research

# KEEP - Move essential ISMÊ files to organized folders
echo "📁 Organizing ISMÊ data..."
mv isme_complete_product_catalog.json brands/isme/products/
mv isme_all_product_images.json brands/isme/products/
mv isme_instagram_processed.json brands/isme/instagram/

# DELETE - Remove duplicates and failed attempts
echo "🗑️  Removing unnecessary files..."
rm -f bikini_library.json
rm -f isme_complete_catalog.json
rm -f isme_all_products_shopify.json
rm -f isme_instagram_latest.json
rm -f isme_instagram_notes.md
rm -f isme_your_crawl.json
rm -f your_isme_crawl.json
rm -f isme_full_website_crawl.json
rm -f isme_all_image_urls.txt
rm -f isme_image_urls.txt
rm -f isme_image_urls.json

# Move scripts to scripts folder
echo "📝 Moving scripts..."
mv *.py scripts/ 2>/dev/null

# Check what's left
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Current structure:"
tree -L 3 brands/ 2>/dev/null || find brands/ -type f

import json

# Load the Instagram data
with open('isme_instagram_latest.json', 'r') as f:
    posts = json.load(f)

print(f"📊 Processing {len(posts)} Instagram posts...")

# Extract product images and metadata
products = []
all_image_urls = []

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
        'images': [],
        'video_url': None
    }

    # Main display image
    if post.get('displayUrl'):
        item['images'].append(post['displayUrl'])
        all_image_urls.append({
            'url': post['displayUrl'],
            'post_url': post.get('url'),
            'caption': post.get('caption', '')[:100]
        })

    # Video URL if it's a video post
    if post.get('type') == 'Video' and post.get('videoUrl'):
        item['video_url'] = post['videoUrl']

    # Carousel/Sidecar images
    if post.get('childPosts'):
        for child in post['childPosts']:
            if child.get('displayUrl'):
                item['images'].append(child['displayUrl'])
                all_image_urls.append({
                    'url': child['displayUrl'],
                    'post_url': post.get('url'),
                    'caption': post.get('caption', '')[:100]
                })

    products.append(item)

# Save processed data
with open('isme_instagram_processed.json', 'w') as f:
    json.dump(products, f, indent=2)

# Save just image URLs for easy downloading
with open('isme_image_urls.json', 'w') as f:
    json.dump(all_image_urls, f, indent=2)

# Create a simple text file with just URLs (for wget/curl)
with open('isme_image_urls.txt', 'w') as f:
    for img in all_image_urls:
        f.write(img['url'] + '\n')

# Generate summary statistics
print(f"\n✅ PROCESSING COMPLETE!\n")
print(f"📊 Summary:")
print(f"   Total posts: {len(products)}")
print(f"   Total images: {len(all_image_urls)}")
print(f"   Videos: {sum(1 for p in products if p['type'] == 'Video')}")
print(f"   Photo posts: {sum(1 for p in products if p['type'] == 'Image')}")
print(f"   Carousel posts: {sum(1 for p in products if p['type'] == 'Sidecar')}")

# Top performing posts
print(f"\n🔥 Top 10 Most Liked Posts:")
sorted_by_likes = sorted(products, key=lambda x: x['likes'], reverse=True)
for i, post in enumerate(sorted_by_likes[:10], 1):
    caption_preview = post['caption'][:50] + '...' if len(post['caption']) > 50 else post['caption']
    print(f"{i}. {post['likes']:,} likes | {len(post['images'])} imgs | {caption_preview}")

print(f"\n💬 Top 10 Most Commented Posts:")
sorted_by_comments = sorted(products, key=lambda x: x['comments'], reverse=True)
for i, post in enumerate(sorted_by_comments[:10], 1):
    caption_preview = post['caption'][:50] + '...' if len(post['caption']) > 50 else post['caption']
    print(f"{i}. {post['comments']:,} comments | {len(post['images'])} imgs | {caption_preview}")

print(f"\n💾 Files created:")
print(f"   - isme_instagram_processed.json (full data with metadata)")
print(f"   - isme_image_urls.json (image URLs with context)")
print(f"   - isme_image_urls.txt (plain text URLs for downloading)")

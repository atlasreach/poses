import os
import json
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

def start_instagram_scrape(username, max_posts=100):
    """Start an Apify Instagram scrape run"""

    # Apify Instagram scraper input configuration
    payload = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "searchType": "hashtag",
        "searchLimit": 1,
        "addParentData": False
    }

    print(f"🚀 Starting Instagram scrape for @{username}...")

    # Start the actor run
    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs?token={APIFY_API_TOKEN}"

    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code in [200, 201]:
            run_data = response.json()
            run_id = run_data['data']['id']
            print(f"✅ Scrape started! Run ID: {run_id}")
            return run_id
        else:
            print(f"❌ Error starting scrape: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def check_run_status(run_id):
    """Check if the scrape is complete"""
    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs/{run_id}?token={APIFY_API_TOKEN}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            status = data['data']['status']
            return status
        return None
    except Exception as e:
        print(f"❌ Error checking status: {str(e)}")
        return None

def wait_for_completion(run_id, max_wait=600):
    """Wait for the scrape to complete"""
    print("⏳ Waiting for scrape to complete...")
    start_time = time.time()

    while (time.time() - start_time) < max_wait:
        status = check_run_status(run_id)

        if status == "SUCCEEDED":
            print("✅ Scrape completed successfully!")
            return True
        elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"❌ Scrape {status}")
            return False
        elif status == "RUNNING":
            elapsed = int(time.time() - start_time)
            print(f"⏳ Still running... ({elapsed}s elapsed)")
            time.sleep(10)
        else:
            print(f"📊 Status: {status}")
            time.sleep(5)

    print("⏰ Timeout waiting for scrape to complete")
    return False

def get_results(run_id):
    """Fetch the scraped data"""
    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/runs/{run_id}/dataset/items?token={APIFY_API_TOKEN}"

    print("📥 Fetching results...")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} posts!")
            return data
        else:
            print(f"❌ Error fetching results: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_data(data, filename):
    """Save data to JSON file"""
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to {filename}")
        return True
    return False

def extract_image_urls(data):
    """Extract just image URLs and metadata"""
    simplified = []

    for post in data:
        item = {
            'post_id': post.get('id'),
            'url': post.get('url'),
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

        # Video thumbnail
        if post.get('type') == 'Video' and post.get('displayUrl'):
            item['video_url'] = post.get('videoUrl')

        # Carousel images
        if post.get('childPosts'):
            for child in post['childPosts']:
                if child.get('displayUrl'):
                    item['images'].append(child['displayUrl'])

        simplified.append(item)

    return simplified

if __name__ == "__main__":
    username = "ismeswim"
    max_posts = 100

    # Start the scrape
    run_id = start_instagram_scrape(username, max_posts)

    if run_id:
        # Wait for completion
        if wait_for_completion(run_id):
            # Get results
            data = get_results(run_id)

            if data:
                # Save full data
                save_data(data, 'isme_instagram_full.json')

                # Extract and save simplified version
                simplified = extract_image_urls(data)
                save_data(simplified, 'isme_instagram_images.json')

                # Print summary
                print("\n📊 SUMMARY:")
                print(f"Total posts: {len(data)}")
                print(f"Total images: {sum(len(p['images']) for p in simplified)}")
                print(f"\nTop 5 most engaged posts:")
                sorted_posts = sorted(simplified, key=lambda x: x.get('likes', 0), reverse=True)
                for i, post in enumerate(sorted_posts[:5], 1):
                    print(f"{i}. {post['likes']:,} likes | {len(post['images'])} images | {post['url']}")

                print(f"\n✅ All data saved! Check isme_instagram_full.json and isme_instagram_images.json")

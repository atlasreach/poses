import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv('.env.local')

APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

def crawl_isme_website():
    """Use Apify Website Content Crawler to scrape entire ISMÊ website"""

    # Configuration for the crawler
    payload = {
        "startUrls": [
            {"url": "https://ismeswim.com/collections/all-products"},
            {"url": "https://ismeswim.com/collections/tops"},
            {"url": "https://ismeswim.com/collections/bottoms"},
        ],
        "crawlerType": "cheerio",  # Fast HTTP crawler for e-commerce
        "maxCrawlDepth": 3,
        "maxCrawlPages": 500,
        "saveHtml": False,
        "saveMarkdown": True,
        "saveFiles": False,
        "removeElementsCssSelector": "header, footer, nav, .header, .footer, .navigation, .cookie-banner",
        "removeCookieWarnings": True,
        "clickElementsCssSelector": "",
        "htmlTransformer": "readableText",
        "readableTextCharThreshold": 100,
    }

    print("🚀 Starting Website Content Crawler for ISMÊ Swim...")

    # Start the crawler
    url = f"https://api.apify.com/v2/acts/apify~website-content-crawler/runs?token={APIFY_API_TOKEN}"

    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})

    if response.status_code in [200, 201]:
        run_data = response.json()
        run_id = run_data['data']['id']
        print(f"✅ Crawler started! Run ID: {run_id}")
        return run_id
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def check_status(run_id):
    """Check crawler status"""
    url = f"https://api.apify.com/v2/acts/apify~website-content-crawler/runs/{run_id}?token={APIFY_API_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']['status']
    return None

def wait_for_completion(run_id, max_wait=600):
    """Wait for crawler to finish"""
    print("⏳ Crawling website...")
    start_time = time.time()

    while (time.time() - start_time) < max_wait:
        status = check_status(run_id)

        if status == "SUCCEEDED":
            print("✅ Crawl completed!")
            return True
        elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"❌ Crawl {status}")
            return False
        elif status == "RUNNING":
            elapsed = int(time.time() - start_time)
            print(f"⏳ Still running... ({elapsed}s)", end='\r')
            time.sleep(5)

    print("⏰ Timeout")
    return False

def get_results(run_id):
    """Fetch crawled data"""
    url = f"https://api.apify.com/v2/acts/apify~website-content-crawler/runs/{run_id}/dataset/items?token={APIFY_API_TOKEN}"

    print("📥 Fetching results...")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data)} pages!")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        return None

def extract_products(data):
    """Extract product information from crawled pages"""
    products = []

    for page in data:
        url = page.get('url', '')

        # Only process product pages
        if '/products/' in url:
            text = page.get('text', '')
            markdown = page.get('markdown', '')

            # Extract product info from text/markdown
            product = {
                'url': url,
                'title': page.get('metadata', {}).get('title', ''),
                'description': page.get('metadata', {}).get('description', ''),
                'text': text,
                'markdown': markdown,
                'crawled_at': page.get('crawl', {}).get('loadedTime', '')
            }
            products.append(product)

    return products

if __name__ == "__main__":
    # Start crawl
    run_id = crawl_isme_website()

    if run_id:
        # Wait for completion
        if wait_for_completion(run_id):
            # Get results
            data = get_results(run_id)

            if data:
                # Save full crawl
                with open('isme_website_full_crawl.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"💾 Full crawl saved to isme_website_full_crawl.json")

                # Extract products
                products = extract_products(data)
                with open('isme_products_extracted.json', 'w') as f:
                    json.dump(products, f, indent=2)

                print(f"\n📊 SUMMARY:")
                print(f"   Total pages crawled: {len(data)}")
                print(f"   Product pages found: {len(products)}")
                print(f"\n✅ Done! Check isme_website_full_crawl.json and isme_products_extracted.json")

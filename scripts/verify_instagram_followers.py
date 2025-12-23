#!/usr/bin/env python3
"""Verify Instagram follower counts for brands"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.local')
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')

def check_instagram_profile(username):
    """Check Instagram profile using Apify"""
    url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    payload = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "details",
        "resultsLimit": 1
    }

    try:
        print(f"🔍 Checking @{username}...")
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=120)

        if response.status_code in [200, 201]:
            data = response.json()
            if data and len(data) > 0:
                profile = data[0]
                followers = profile.get('followersCount', 0)
                full_name = profile.get('fullName', '')
                bio = profile.get('biography', '')[:100]
                print(f"✅ @{username}: {followers:,} followers - {full_name}")
                return {
                    'username': username,
                    'followers': followers,
                    'full_name': full_name,
                    'bio': bio,
                    'url': f"https://www.instagram.com/{username}/"
                }
            else:
                print(f"❌ @{username}: No data returned")
                return None
        else:
            print(f"❌ @{username}: Error {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ @{username}: {str(e)}")
        return None

if __name__ == "__main__":
    # Brands to verify
    brands_to_check = [
        "honeybeeswim",
        "kaohs_swim",
        "swamisswimwear",
        "coverswim",
    ]

    results = []
    for username in brands_to_check:
        result = check_instagram_profile(username)
        if result:
            results.append(result)

    # Save results
    with open('../research/verified_followers.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Verified {len(results)}/{len(brands_to_check)} brands")
    print("Results saved to research/verified_followers.json")

#!/usr/bin/env python3
"""
Test NanaBanana API for background replacement
"""

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv('.env.local')

def edit_image_background(image_url, prompt, output_path, sync_mode=True):
    """
    Use NanaBanana API to edit image background
    """

    api_key = os.getenv('WAVESPEED_API_KEY')
    api_url = os.getenv('WAVESPEED_API_URL')

    if not api_key or not api_url:
        print("❌ API credentials not found in .env.local")
        return None

    print(f"📸 Image URL: {image_url}")
    print(f"🤖 Sending to NanaBanana API...")
    print(f"   Prompt: {prompt}")

    # Prepare request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'enable_base64_output': False,
        'enable_sync_mode': sync_mode,
        'images': [image_url],
        'output_format': 'jpeg',
        'prompt': prompt,
        'resolution': '2k'
    }

    try:
        # Submit job
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

        result = response.json()

        if result.get('code') != 200:
            print(f"❌ API returned error: {result}")
            return None

        data = result.get('data', {})
        job_id = data.get('id')
        status = data.get('status')

        print(f"✅ Job created: {job_id}")
        print(f"   Status: {status}")

        # If sync mode, result should be ready
        if sync_mode:
            outputs = data.get('outputs', [])
            if outputs and len(outputs) > 0:
                output_url = outputs[0]
                print(f"✅ Image ready: {output_url}")

                # Download
                img_response = requests.get(output_url)
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)

                print(f"✅ Downloaded to: {output_path}")
                return output_path

        # Async mode - poll for results
        result_url = data.get('urls', {}).get('get')
        if not result_url:
            print(f"❌ No result URL provided")
            return None

        print(f"⏳ Polling for results...")

        max_attempts = 60  # 5 minutes max
        for attempt in range(max_attempts):
            time.sleep(5)  # Wait 5 seconds between polls

            poll_response = requests.get(result_url, headers=headers)

            if poll_response.status_code != 200:
                print(f"❌ Poll error {poll_response.status_code}")
                continue

            poll_data = poll_response.json().get('data', {})
            status = poll_data.get('status')

            print(f"   [{attempt+1}/{max_attempts}] Status: {status}")

            if status == 'completed':
                outputs = poll_data.get('outputs', [])
                if outputs and len(outputs) > 0:
                    output_url = outputs[0]
                    print(f"✅ Image ready: {output_url}")

                    # Download
                    img_response = requests.get(output_url)
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)

                    print(f"✅ Downloaded to: {output_path}")
                    return output_path
                else:
                    print(f"❌ No outputs in completed job")
                    return None

            elif status in ['failed', 'error']:
                error = poll_data.get('error', 'Unknown error')
                print(f"❌ Job failed: {error}")
                return None

        print(f"❌ Timeout waiting for job to complete")
        return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python test_nana_banana.py <image_url> <prompt> [output_path]")
        print("")
        print("Example:")
        print('  python test_nana_banana.py "https://example.com/image.jpg" "Change background to Waikiki Beach" output.jpg')
        sys.exit(1)

    image_url = sys.argv[1]
    prompt = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else '/tmp/edited_image.jpg'

    result = edit_image_background(image_url, prompt, output_path, sync_mode=False)

    if result:
        print(f"\n🎉 Edit complete!")
        print(f"   Original: {image_url}")
        print(f"   Edited: {output_path}")

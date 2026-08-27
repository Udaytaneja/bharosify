import os
import sys
import json
import urllib.request

def test_download():
    print("Testing DocLayNet source access...")
    url = "https://huggingface.co/datasets/ibm/doclaynet/raw/main/README.md"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            print("Successfully accessed DocLayNet repository on HuggingFace!")
            print("License check in README:", "cc-by-4.0" in content.lower() or "creative commons" in content.lower())
            return True
    except Exception as e:
        print(f"Failed to access DocLayNet remote source: {e}")
        return False

if __name__ == "__main__":
    test_download()

import urllib.request
import json

def test_hf_datasets():
    urls = [
        "https://huggingface.co/api/datasets/ibm/doclaynet",
        "https://datasets-server.huggingface.co/info?dataset=ibm/doclaynet"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                print(f"URL: {url} -> SUCCESS!")
                if "license" in str(data).lower():
                    print("Found license info in response.")
        except Exception as e:
            print(f"URL: {url} -> FAILED ({e})")

if __name__ == "__main__":
    test_hf_datasets()

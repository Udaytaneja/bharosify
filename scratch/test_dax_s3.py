import urllib.request

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"
print(f"Testing direct S3 URL: {url}")
try:
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Status:", resp.status)
        print("Content-Length:", resp.headers.get("Content-Length"))
        print("Content-Type:", resp.headers.get("Content-Type"))
        print("ETag / Checksum:", resp.headers.get("ETag"))
except Exception as e:
    print("HEAD request failed:", e)

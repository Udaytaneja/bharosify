import urllib.request
import struct
import io
import zipfile

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"
total_len = 30012083650

print("Testing HTTP Range request for DocLayNet zip central directory...")
# Range request for the last 1MB of the 30GB zip file
range_header = f"bytes={total_len - 1048576}-{total_len - 1}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': range_header})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
        print(f"Successfully downloaded last 1MB slice ({len(data)} bytes)!")
except Exception as e:
    print("Range request failed:", e)

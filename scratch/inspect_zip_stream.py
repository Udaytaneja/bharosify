import urllib.request
import zipfile
import io
import os

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"

print("Downloading first 50MB of DocLayNet_core.zip to inspect directory structure...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-52428800'})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        print(f"Downloaded {len(data)} bytes. Attempting zip file extraction...")
        # Save chunk to disk for inspection
        os.makedirs("data/raw", exist_ok=True)
        chunk_path = "data/raw/doclaynet_chunk_50mb.zip"
        with open(chunk_path, "wb") as f:
            f.write(data)
        
        try:
            with zipfile.ZipFile(chunk_path, 'r') as z:
                namelist = z.namelist()
                print(f"Zip chunk contains {len(namelist)} file entries!")
                for n in namelist[:20]:
                    print(" -", n)
        except Exception as ze:
            print("Zip chunk incomplete (expected for partial range stream):", ze)
except Exception as e:
    print("Download failed:", e)

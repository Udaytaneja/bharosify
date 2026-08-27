import urllib.request
import re

url = "https://raw.githubusercontent.com/DS4SD/DocLayNet/main/README.md"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    content = resp.read().decode('utf-8')

print("=== DOCLAYNET DOWNLOAD LINKS IN README ===")
links = re.findall(r'https?://[^\s\)]+', content)
for l in links:
    if "doclaynet" in l.lower() or "zip" in l.lower() or "tar" in l.lower() or "huggingface" in l.lower() or "box" in l.lower():
        print(l)

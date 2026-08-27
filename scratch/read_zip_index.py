import urllib.request
import zipfile
import io

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"
total_len = 30012083650

print("Fetching last 5MB of DocLayNet_core.zip to read Central Directory Index...")
# Fetch last 5MB
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={total_len - 5242880}-{total_len - 1}'})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        print(f"Fetched {len(data)} bytes from zip tail. Parsing EOCD record...")
        
        # Look for End of Central Directory signature (0x06054b50)
        eocd_pos = data.rfind(b"\x50\x4b\x05\x06")
        if eocd_pos != -1:
            print("Found EOCD signature at offset:", eocd_pos)
            # Parse CD offset and size
            cd_size = int.from_bytes(data[eocd_pos+12:eocd_pos+16], 'little')
            cd_offset = int.from_bytes(data[eocd_pos+16:eocd_pos+20], 'little')
            print(f"Central Directory Size: {cd_size} bytes, Start Offset: {cd_offset}")
        else:
            print("EOCD signature not in last 5MB; expanding range...")
except Exception as e:
    print("Failed to read zip index:", e)

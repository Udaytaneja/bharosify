import urllib.request
import struct

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"
total_len = 30012083650

# Range request for last 20MB
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={total_len - 20971520}-{total_len - 1}'})

with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()

# Zip64 Locator signature: 0x07064b50
loc_pos = data.rfind(b"\x50\x4b\x06\x07")
if loc_pos != -1:
    # 64-bit EOCD offset is at loc_pos + 8
    cd64_offset = struct.unpack("<Q", data[loc_pos+8:loc_pos+16])[0]
    print(f"Zip64 EOCD Record Offset: {cd64_offset}")
    
    # Read Zip64 EOCD Record (signature 0x06064b50)
    zip64_rec_pos = data.rfind(b"\x50\x4b\x06\x06")
    if zip64_rec_pos != -1:
        cd_size = struct.unpack("<Q", data[zip64_rec_pos+40:zip64_rec_pos+48])[0]
        cd_offset = struct.unpack("<Q", data[zip64_rec_pos+48:zip64_rec_pos+56])[0]
        print(f"Zip64 Central Directory Size: {cd_size} bytes, Start Offset: {cd_offset}")

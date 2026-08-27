import urllib.request
import struct
import json
import os
import zipfile

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"
cd_start = 29999021762
cd_size = 13061790

print(f"Downloading Zip Central Directory ({cd_size} bytes)...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={cd_start}-{cd_start + cd_size - 1}'})

with urllib.request.urlopen(req, timeout=60) as resp:
    cd_data = resp.read()

print(f"Downloaded {len(cd_data)} bytes. Parsing Zip Central Directory headers...")

entries = []
pos = 0
while pos < len(cd_data):
    if cd_data[pos:pos+4] != b"\x50\x4b\x01\x02":
        break
    # Header format: https://en.wikipedia.org/wiki/ZIP_(file_format)#Central_directory_file_header
    filename_len = struct.unpack("<H", cd_data[pos+28:pos+30])[0]
    extra_len = struct.unpack("<H", cd_data[pos+30:pos+32])[0]
    comment_len = struct.unpack("<H", cd_data[pos+32:pos+34])[0]
    comp_size = struct.unpack("<I", cd_data[pos+20:pos+24])[0]
    uncomp_size = struct.unpack("<I", cd_data[pos+24:pos+28])[0]
    local_header_offset = struct.unpack("<I", cd_data[pos+42:pos+46])[0]

    filename = cd_data[pos+46:pos+46+filename_len].decode('utf-8', errors='ignore')

    # If Zip64 extra field exists (offset 0xFFFFFFFF)
    if local_header_offset == 0xFFFFFFFF or comp_size == 0xFFFFFFFF:
        extra_pos = pos + 46 + filename_len
        extra_end = extra_pos + extra_len
        while extra_pos < extra_end - 4:
            header_id, block_size = struct.unpack("<HH", cd_data[extra_pos:extra_pos+4])
            if header_id == 0x0001:  # Zip64 Extra Field
                zip64_data = cd_data[extra_pos+4:extra_pos+4+block_size]
                off = 0
                if uncomp_size == 0xFFFFFFFF and len(zip64_data) >= off + 8:
                    uncomp_size = struct.unpack("<Q", zip64_data[off:off+8])[0]
                    off += 8
                if comp_size == 0xFFFFFFFF and len(zip64_data) >= off + 8:
                    comp_size = struct.unpack("<Q", zip64_data[off:off+8])[0]
                    off += 8
                if local_header_offset == 0xFFFFFFFF and len(zip64_data) >= off + 8:
                    local_header_offset = struct.unpack("<Q", zip64_data[off:off+8])[0]
                    off += 8
                break
            extra_pos += 4 + block_size

    entries.append({
        "filename": filename,
        "offset": local_header_offset,
        "comp_size": comp_size,
        "uncomp_size": uncomp_size
    })

    pos += 46 + filename_len + extra_len + comment_len

print(f"Parsed {len(entries)} file entries from DocLayNet_core.zip!")

# Filter annotation JSON files and PNG images
coco_jsons = [e for e in entries if "COCO/" in e["filename"] and e["filename"].endswith(".json")]
png_images = [e for e in entries if "PNG/" in e["filename"] and e["filename"].endswith(".png")]

print("\nCOCO JSON files found:")
for j in coco_jsons:
    print(f" - {j['filename']} (Offset: {j['offset']}, Size: {j['uncomp_size']} bytes)")

print(f"\nPNG Images found: {len(png_images)} pages.")

os.makedirs("scratch", exist_ok=True)
with open("scratch/doclaynet_index.json", "w") as f:
    json.dump(entries, f, indent=2)
print("Saved central directory index to scratch/doclaynet_index.json.")

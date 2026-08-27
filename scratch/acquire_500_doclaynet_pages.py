import json
import os
import random
import struct
import urllib.request
import zlib
from PIL import Image

URL = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"

def download_zip_entry(entry_offset, entry_comp_size, entry_filename, output_path):
    """Downloads and uncompresses a single zip entry from S3 DAX using exact comp_size."""
    fetch_len = entry_comp_size + 2048
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={entry_offset}-{entry_offset + fetch_len - 1}'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    if data[:4] != b"\x50\x4b\x03\x04":
        raise ValueError(f"Invalid local header at offset {entry_offset}")

    fn_len = struct.unpack("<H", data[26:28])[0]
    extra_len = struct.unpack("<H", data[28:30])[0]
    comp_method = struct.unpack("<H", data[8:10])[0]
    
    header_size = 30 + fn_len + extra_len
    payload = data[header_size:header_size + entry_comp_size]

    if comp_method == 8:  # Deflated
        decompressed = zlib.decompress(payload, -15)
    elif comp_method == 0:  # Stored (uncompressed)
        decompressed = payload
    else:
        raise ValueError(f"Unsupported compression method: {comp_method}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(decompressed)
    return output_path

def acquire_500_pages():
    raw_dir = "data/raw/doclaynet_subset"
    img_dir = os.path.join(raw_dir, "images")
    val_json_path = os.path.join(raw_dir, "val.json")
    index_json_path = "scratch/doclaynet_index.json"

    assert os.path.exists(val_json_path), f"val.json missing at {val_json_path}"
    assert os.path.exists(index_json_path), f"doclaynet_index.json missing at {index_json_path}"

    with open(index_json_path, "r") as f:
        index_entries = json.load(f)
    entry_map = {e["filename"]: e for e in index_entries}

    with open(val_json_path, "r") as f:
        coco_val = json.load(f)

    images = coco_val["images"]
    annotations = coco_val["annotations"]

    print(f"Loaded val.json: {len(images)} total images in metadata, {len(annotations)} total annotations.")

    # Select deterministic 500-page subset (seed = 42)
    random.seed(42)
    sample_images = random.sample(images, 500)
    print(f"Selected deterministic 500-page subset.")

    existing_files = set(os.listdir(img_dir)) if os.path.exists(img_dir) else set()
    print(f"Already downloaded images in {img_dir}: {len(existing_files)}")

    download_needed = []
    for img in sample_images:
        fn = img["file_name"]
        if fn not in existing_files:
            download_needed.append(img)

    print(f"Images to download: {len(download_needed)} / 500")

    downloaded_new = 0
    for idx, img in enumerate(download_needed):
        fn = img["file_name"]
        png_key = [k for k in entry_map.keys() if k.endswith(fn)]
        if png_key:
            entry = entry_map[png_key[0]]
            dest = os.path.join(img_dir, fn)
            download_zip_entry(entry["offset"], entry["comp_size"], entry["filename"], dest)
            downloaded_new += 1
            if downloaded_new % 25 == 0 or downloaded_new == len(download_needed):
                print(f"Downloaded {downloaded_new}/{len(download_needed)} new images...")

    # Final check on all 500 images
    valid_count = 0
    corrupt_count = 0
    for img in sample_images:
        dest = os.path.join(img_dir, img["file_name"])
        if os.path.exists(dest):
            try:
                with Image.open(dest) as im:
                    im.verify()
                valid_count += 1
            except Exception as e:
                print(f"Corrupt image: {img['file_name']} ({e})")
                corrupt_count += 1
        else:
            print(f"Missing image file: {img['file_name']}")

    print(f"\nACQUISITION COMPLETE: {valid_count} valid, decodable DocLayNet page images ready!")
    assert valid_count == 500, f"Expected 500 valid images, but got {valid_count}"

if __name__ == "__main__":
    acquire_500_pages()

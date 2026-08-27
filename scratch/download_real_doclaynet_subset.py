import urllib.request
import zipfile
import json
import os
import random
import io
import zlib
import struct

url = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/DocLayNet_core.zip"

def download_zip_entry(entry_offset, entry_comp_size, entry_filename, output_path):
    """Downloads and uncompresses a single zip entry from S3 DAX using exact comp_size."""
    print(f"Downloading entry '{entry_filename}' (compressed size: {entry_comp_size} bytes)...")
    # Fetch local header (30 bytes + name/extra) + exact comp_size
    fetch_len = entry_comp_size + 2048
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={entry_offset}-{entry_offset + fetch_len - 1}'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    # Verify Local File Header signature (0x04034b50)
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
    print(f"Successfully saved '{output_path}' ({len(decompressed)} bytes).")
    return output_path

def acquire_subset():
    with open("scratch/doclaynet_index.json", "r") as f:
        index_entries = json.load(f)

    # Map filename -> entry dict
    entry_map = {e["filename"]: e for e in index_entries}

    raw_dir = "data/raw/doclaynet_subset"
    os.makedirs(raw_dir, exist_ok=True)

    # 1. Download COCO val.json annotations
    val_json_entry = [e for e in index_entries if "COCO/val.json" in e["filename"]][0]
    val_json_path = os.path.join(raw_dir, "val.json")
    if not os.path.exists(val_json_path):
        download_zip_entry(val_json_entry["offset"], val_json_entry["comp_size"], val_json_entry["filename"], val_json_path)

    # Load annotations
    with open(val_json_path, "r") as f:
        coco_val = json.load(f)

    images = coco_val["images"]
    annotations = coco_val["annotations"]

    print(f"Loaded val.json: {len(images)} images, {len(annotations)} annotations.")

    # 2. Select a deterministic subset of 500 document images (seed = 42)
    random.seed(42)
    sample_images = random.sample(images, 500)
    sample_img_ids = {img["id"] for img in sample_images}

    sample_annotations = [ann for ann in annotations if ann["image_id"] in sample_img_ids]

    print(f"Selected deterministic 500-page subset ({len(sample_annotations)} annotations).")

    # Save subset COCO JSON
    subset_coco = {
        "info": coco_val.get("info", {}),
        "licenses": coco_val.get("licenses", []),
        "categories": coco_val.get("categories", []),
        "images": sample_images,
        "annotations": sample_annotations
    }
    subset_json_path = os.path.join(raw_dir, "subset_val_500.json")
    with open(subset_json_path, "w") as f:
        json.dump(subset_coco, f)

    # 3. Download the exact 500 PNG page images
    img_dir = os.path.join(raw_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    downloaded_count = 0
    for idx, img in enumerate(sample_images):
        fn = img["file_name"]
        png_key = [k for k in entry_map.keys() if k.endswith(fn)]
        if png_key:
            entry = entry_map[png_key[0]]
            dest = os.path.join(img_dir, fn)
            if not os.path.exists(dest):
                download_zip_entry(entry["offset"], entry["comp_size"], entry["filename"], dest)
            downloaded_count += 1
            if downloaded_count % 50 == 0:
                print(f"Downloaded {downloaded_count}/500 images...")

    print(f"Acquisition complete! Downloaded {downloaded_count} real DocLayNet page images.")

if __name__ == "__main__":
    acquire_subset()

import os

img_dir = "data/raw/doclaynet_subset/images"
if os.path.exists(img_dir):
    files = os.listdir(img_dir)
    print(f"Downloaded {len(files)} real DocLayNet PNG page images!")
    for f in files[:5]:
        sz = os.path.getsize(os.path.join(img_dir, f))
        print(f" - {f} ({sz} bytes)")
else:
    print("Image directory does not exist yet.")

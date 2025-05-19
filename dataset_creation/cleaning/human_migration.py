import os
import shutil

# Configure source and destination paths
SOURCE_DIR = "/vol/bitbucket/sg2121/fypdataset/dataset_large/human/fma_medium"
DEST_DIR = "/vol/bitbucket/sg2121/fypdataset/dataset_large/human/renamed"

# Create destination directory if it doesn't exist
os.makedirs(DEST_DIR, exist_ok=True)

# Counter for renaming
counter = 1

# Walk through source directory
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.lower().endswith(".mp3"):
            src_path = os.path.join(root, file)
            dest_filename = f"H{counter}.mp3"
            dest_path = os.path.join(DEST_DIR, dest_filename)

            # Move and rename the file
            shutil.move(src_path, dest_path)
            print(f"Moved: {src_path} → {dest_path}")
            counter += 1

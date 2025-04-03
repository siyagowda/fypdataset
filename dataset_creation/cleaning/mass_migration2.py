import os
import shutil

# Source and destination directories
source_dir = "C://Users//sg16g//Music//dataset//udio" 
destination_dir = "C://Users//sg16g//Documents//fyp//dataset//udio"  

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Track existing files in the destination folder
existing_files = set(os.listdir(destination_dir))

# Walk through all subdirectories
for root, _, files in os.walk(source_dir):

    if root != source_dir:  # If we're inside a subfolder
        print(f"Entering subfolder: {root}")

    for file in files:
        # Full file path in source
        old_path = os.path.join(root, file)

        # Skip empty files
        if os.path.getsize(old_path) == 0:
            print(f"Skipping empty file: {file}")
            continue  

        # Check if file already exists in destination
        if file in existing_files:
            print(f"Skipping duplicate: {file}")
            continue  # Skip the file without moving it

        # Move file to destination
        new_path = os.path.join(destination_dir, file)
        shutil.move(old_path, new_path)
        existing_files.add(file)  # Track moved files

print("All files moved successfully, skipping duplicates!")

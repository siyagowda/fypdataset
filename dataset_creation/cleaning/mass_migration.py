import os
import shutil
import re

# Source and destination directories
source_dir = "C://Users//sg16g//Music//suno"  
destination_dir = "C://Users//sg16g//Music//dataset//suno" 
duplicates_dir = "C://Users//sg16g//Music//dataset//suno//duplicates" 

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)
os.makedirs(duplicates_dir, exist_ok=True)

# Track files to detect duplicates
existing_files = set(os.listdir(destination_dir))  # Store existing file names

# Walk through all subdirectories
for root, _, files in os.walk(source_dir):

  if root != source_dir:  # If we're inside a subfolder
    print(f"Entering subfolder: {root}")

  for file in files:

    # Full file paths
    old_path = os.path.join(root, file)

    if os.path.getsize(old_path) == 0:
      print(f"Skipping empty file: {file}")
      continue  # Skip empty files

    new_path = os.path.join(destination_dir, file)

    # Check if the file already exists in the destination
    if new_name in existing_files:
      # Check if the file is already in the destination folder
      duplicate_path = os.path.join(duplicates_dir, new_name)

      # If file exists, rename with a number suffix and move it to the duplicates folder
      base, ext = os.path.splitext(new_name)
      count = 1
      while os.path.exists(duplicate_path):  # Check for conflicts in duplicates folder
        duplicate_path = os.path.join(duplicates_dir, f"{base}_{count}{ext}")
        count += 1

      shutil.move(old_path, duplicate_path)
      print(f"Duplicate found: {file} → Moved to duplicates folder as {os.path.basename(duplicate_path)}.")
    else:
      shutil.move(old_path, new_path)
      existing_files.add(new_name)  # Track moved files

print("All files moved successfully!")

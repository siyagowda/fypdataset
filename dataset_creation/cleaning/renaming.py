import os

# Directories
source_dir = "C://Users//sg16g//Music//dataset//suno" 
# You can choose to either rename files in source or destination folder.

# File counter for renaming
count = 1

# Walk through all files in source folder (including subfolders)
for root, _, files in os.walk(source_dir):

    for file in files:
        ext = os.path.splitext(file)[1]  # Get file extension
        new_name = f"S{count:02d}R{ext}"  # Rename to "song count.extension"
        old_path = os.path.join(root, file)
        new_path = os.path.join(root, new_name)

        # Ensure the new name doesn't already exist in the same folder
        if os.path.exists(new_path):
            print(f"Skipping {file}: {new_name} already exists.")
        else:
            os.rename(old_path, new_path)
            count += 1  # Increment the count for the next file
            print(f"Renamed: {file} → {new_name}")

print("Renaming completed.")

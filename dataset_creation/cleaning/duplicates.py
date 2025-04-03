import os
import shutil

# Directories
destination_dir = "C://Users//sg16g//Music//dataset//suno" 
duplicates_dir = "C://Users//sg16g//Music//dataset//suno//duplicates" 

# Ensure duplicates folder exists
if not os.path.exists(duplicates_dir):
    print("No duplicates folder found. Exiting.")
    exit()

# Get file sizes in destination folder
destination_files = {f: os.path.getsize(os.path.join(destination_dir, f)) for f in os.listdir(destination_dir)}

# Process duplicates
for file in os.listdir(duplicates_dir):
    old_path = os.path.join(duplicates_dir, file)

    # Rename file (remove leading numbers and hyphen)
    new_name = re.sub(r'^\d+\s*-\s*', '', file)
    new_path = os.path.join(destination_dir, new_name)

    if new_name in destination_files:
        dup_size = os.path.getsize(old_path)
        dest_size = destination_files[new_name]

        if dup_size != dest_size:
            # File exists but has a different size → Rename with a number suffix
            base, ext = os.path.splitext(new_name)
            count = 1
            while os.path.exists(new_path):
                new_path = os.path.join(destination_dir, f"{base}_{count}{ext}")
                count += 1

            shutil.move(old_path, new_path)
            print(f"Renamed & moved: {file} → {os.path.basename(new_path)} (Different size)")
        else:
            print(f"File {new_name} is identical in size → Keeping in duplicates folder.")
    else:
        shutil.move(old_path, new_path)
        print(f"Renamed & moved: {file} → {new_name} (New file)")

print("Duplicate processing completed.")


import os

def count_files(folder_path):
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)
    return total_files

folder_path = "C://Users//sg16g//Documents//fyp//dataset"
print(f"Total files: {count_files(folder_path)}")

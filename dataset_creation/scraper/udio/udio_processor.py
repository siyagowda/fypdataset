import os
import requests

# File containing MP3 links (one per line)
links_file = "udio_links.txt"

# Destination folder to save the MP3 files
download_folder = "C://Users//sg16g//Music//udio" 
os.makedirs(download_folder, exist_ok=True)  # Ensure folder exists

# Read links from file into a set (to remove duplicates)
with open("udio_links.txt", "r") as file:
    links = set(line.strip() for line in file if line.strip())  # Remove blank lines

# Function to download an MP3 file with custom naming
count = 1 
def download_mp3(url, folder):
    global count
    try:
        response = requests.get(url, stream=True)  # Stream the file
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        filename = f"U{count}R.mp3"  # Rename file with "U<count>R"
        file_path = os.path.join(folder, filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        count += 1  # Increment count for the next file
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


# Download all unique MP3 links
for link in links:
    download_mp3(link, download_folder)

print("Download process completed!")

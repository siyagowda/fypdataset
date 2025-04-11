from pydub import AudioSegment
import os

def cut_mp3(input_file, output_folder, segment_length=30):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_file)
    duration_ms = len(audio)  # in milliseconds
    segment_ms = segment_length * 1000

    # Calculate the starting point for the two 30s segments from the middle
    total_needed_ms = segment_ms * 2
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # If the audio is too short for two 30-second segments, just make one
    if duration_ms < total_needed_ms:
        print(f"Audio is too short for two 30-second segments. Creating one segment.")
        segment1 = audio[:segment_ms]
        segment1.export(f"{output_folder}/{file_name}_segment_1.mp3", format="mp3")
        print(f"Saved: {file_name}_seg1.mp3")
        return
    
    # For audio long enough for two segments
    middle_start = (duration_ms - total_needed_ms) // 2

    # First segment
    segment1 = audio[middle_start:middle_start + segment_ms]
    # Second segment
    segment2 = audio[middle_start + segment_ms:middle_start + 2 * segment_ms]

    # Save segments
    os.makedirs(output_folder, exist_ok=True)
    segment1.export(f"{output_folder}/{file_name}_segment_1.mp3", format="mp3")
    segment2.export(f"{output_folder}/{file_name}_segment_2.mp3", format="mp3")

    print(f"Saved: {file_name}_seg1.mp3")
    print(f"Saved: {file_name}_seg2.mp3")

def process_folder(input_folder, output_folder):
    # Loop through all MP3 files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp3"):
            input_file = os.path.join(input_folder, file_name)
            cut_mp3(input_file, output_folder)

input_folder = '/data/sg2121/fypdataset/dataset/normal_data'  
output_folder = '/data/sg2121/fypdataset/dataset/normal_data/segments'
process_folder(input_folder, output_folder)

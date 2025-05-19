from pydub import AudioSegment
import os

def cut_mp3(input_file, output_folder, segment_length=30):
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(input_file)
        duration_ms = len(audio)  # in milliseconds
        segment_ms = segment_length * 1000
        total_needed_ms = segment_ms * 2

        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_path_1 = os.path.join(output_folder, f"{file_name}_segment_1.mp3")
        output_path_2 = os.path.join(output_folder, f"{file_name}_segment_2.mp3")

        # Skip if segment 1 already exists
        if os.path.exists(output_path_1):
            print(f"Skipping '{file_name}': segments already exist.")
            return

        os.makedirs(output_folder, exist_ok=True)

        # If the audio is too short for two 30-second segments, just make one
        if duration_ms < total_needed_ms:
            print(f"Audio is too short for two 30-second segments. Creating one segment.")
            segment1 = audio[:segment_ms]
            segment1.export(output_path_1, format="mp3")
            print(f"Saved: {output_path_1}")
            return

        # For audio long enough for two segments, start from the middle
        middle_start = (duration_ms - total_needed_ms) // 2
        segment1 = audio[middle_start:middle_start + segment_ms]
        segment2 = audio[middle_start + segment_ms:middle_start + 2 * segment_ms]

        # Export both segments
        segment1.export(output_path_1, format="mp3")
        segment2.export(output_path_2, format="mp3")

        print(f"Saved: {output_path_1}")
        print(f"Saved: {output_path_2}")

    except Exception as e:
        print(f"Error processing '{input_file}': {e}")


def process_folder(input_folder, output_folder):
    # Loop through all MP3 files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp3"):
            input_file = os.path.join(input_folder, file_name)
            cut_mp3(input_file, output_folder)

input_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/normal_data/ai'  
output_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/normal_data/ai_segments'
process_folder(input_folder, output_folder)

from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf
import os

def resample_and_normalize(input_file, output_file, target_sample_rate=24000):
    # Load the MP3 file using pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # Resample the audio to the target sample rate
    audio_resampled = audio.set_frame_rate(target_sample_rate)

    # Export the resampled audio to a temporary WAV file
    temp_wav = "temp_resampled.wav"
    audio_resampled.export(temp_wav, format="wav")

    # Load the WAV file using librosa for normalization
    y, sr = librosa.load(temp_wav, sr=target_sample_rate)
    
    # Normalize the audio signal to be between -1 and 1
    y_normalized = librosa.util.normalize(y)

    # Save normalized WAV using soundfile
    sf.write(temp_wav, y_normalized, sr)

    # Convert back to MP3 using pydub
    audio_normalized = AudioSegment.from_wav(temp_wav)
    audio_normalized.export(output_file, format="mp3")

    print(f"Resampled and normalized audio saved to {output_file}")

import os

def process_files_in_folder(input_folder, output_folder, target_sample_rate=24000):
    print("HELLO")

    # List all MP3 files in the folder
    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.mp3')]
    print(len(audio_files))

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for audio_file in audio_files:
        try:
            base_name = os.path.splitext(audio_file)[0]
            output_file = os.path.join(output_folder, f"{base_name}N.mp3")

            # Skip if the output file already exists
            if os.path.exists(output_file):
                print(f"Skipping '{audio_file}': output file already exists.")
                continue

            input_file = os.path.join(input_folder, audio_file)

            # Resample and normalize each file
            resample_and_normalize(input_file, output_file, target_sample_rate)

        except Exception as e:
            print(f"Error processing file '{audio_file}': {e}")



# Example usage:
input_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/raw/human'  # Replace with your input folder path
output_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/normal_data/human'  # Replace with your output folder path

# Process all files in the folder
process_files_in_folder(input_folder, output_folder, target_sample_rate=24000)



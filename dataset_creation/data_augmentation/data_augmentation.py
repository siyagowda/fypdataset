import os
import librosa
import librosa.effects
import random
from pydub import AudioSegment
import numpy as np

def apply_time_stretch(y, sr, rate, target_duration=30.0):
    """Apply time stretching and trim/pad to target duration (in seconds)."""
    y_stretched = librosa.effects.time_stretch(y, rate=rate)
    
    target_length = int(target_duration * sr)
    current_length = len(y_stretched)
    
    if current_length > target_length:
        # Trim
        y_stretched = y_stretched[:target_length]
    elif current_length < target_length:
        # Pad with zeros (silence)
        padding = target_length - current_length
        y_stretched = np.pad(y_stretched, (0, padding), mode='constant')
    
    return y_stretched


def apply_pitch_shift(y, sr, n_steps):
    """Apply pitch shifting to the audio signal."""
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

def save_as_mp3(y, sr, output_file):
    """Save the audio as an MP3 file using pydub."""
    # Convert numpy array to AudioSegment using pydub
    audio_segment = AudioSegment(
        y.tobytes(), 
        frame_rate=sr, 
        sample_width=y.dtype.itemsize, 
        channels=1
    )
    # Export as MP3
    audio_segment.export(output_file, format="mp3")

def augment_and_save_dataset(dataset_folder, output_folder):
    """Apply augmentation (time stretching, pitch shifting) to all files in the dataset."""
    # List all audio files in the dataset folder
    audio_files = [f for f in os.listdir(dataset_folder) if f.endswith('.mp3')]
    
    for audio_file in audio_files:
        file_path = os.path.join(dataset_folder, audio_file)
        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)
        
        # Apply time stretching and pitch shifting
        y_stretched = apply_time_stretch(y, sr=sr, rate=0.8)  # Example: Slow down by 20%
        y_shifted = apply_pitch_shift(y, sr, n_steps=5)  # Example: Shift up by 5 semitones
        
        # Prepare file names for saving
        base_name = os.path.splitext(audio_file)[0]
        time_stretched_file = os.path.join(output_folder, f'{base_name}_stretched.mp3')
        pitch_shifted_file = os.path.join(output_folder, f'{base_name}_shifted.mp3')

        # Save the augmented audio as MP3
        save_as_mp3(y_stretched, sr, time_stretched_file)
        save_as_mp3(y_shifted, sr, pitch_shifted_file)
        
        print(f"Processed and saved: {time_stretched_file} and {pitch_shifted_file}")

def random_augment_and_save_dataset(dataset_folder, output_folder):
    audio_files = [f for f in os.listdir(dataset_folder) if f.endswith('.mp3')]
    print(len(audio_files))
    
    for audio_file in audio_files:
        try:
            file_path = os.path.join(dataset_folder, audio_file)
            y, sr = librosa.load(file_path, sr=None)
            base_name = os.path.splitext(audio_file)[0]

            if random.random() < 0.5:
                # Randomly choose time stretching rate between 0.7 and 1.3 (slow down or speed up)
                rate = random.uniform(0.7, 1.3)
                y_stretched = apply_time_stretch(y, sr=sr, rate=rate)
                changed_file = os.path.join(output_folder, f'{base_name}_stretched.mp3')
                save_as_mp3(y_stretched, sr, changed_file)

            else:
                # Randomly choose pitch shift between -5 and 5 semitones
                n_steps = random.randint(-5, 5)
                y_shifted = apply_pitch_shift(y, sr, n_steps)
                changed_file = os.path.join(output_folder, f'{base_name}_shifted.mp3')
                save_as_mp3(y_shifted, sr, changed_file)

            print(f"Processed and saved: {changed_file}")
                
        except Exception as e:
            print(f"Error processing '{audio_file}': {e}")

# Example usage:
dataset_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/normal_data/ai_segments'  # Replace with your folder path
output_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large/normal_data/augmented_ai'  # Replace with your output folder path

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Augment and save the dataset
random_augment_and_save_dataset(dataset_folder, output_folder)

import os
import librosa
import random
from pydub import AudioSegment

def time_stretch(y, rate):
    """Apply time stretching to the audio signal."""
    return librosa.effects.time_stretch(y, rate)

def pitch_shift(y, sr, n_steps):
    """Apply pitch shifting to the audio signal."""
    return librosa.effects.pitch_shift(y, sr, n_steps)

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
        y_stretched = time_stretch(y, rate=0.8)  # Example: Slow down by 20%
        y_shifted = pitch_shift(y, sr, n_steps=5)  # Example: Shift up by 5 semitones
        
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
    
    for audio_file in audio_files:
        file_path = os.path.join(dataset_folder, audio_file)
        y, sr = librosa.load(file_path, sr=None)
        
        # Randomly choose time stretching rate between 0.7 and 1.3 (slow down or speed up)
        rate = random.uniform(0.7, 1.3)
        
        # Randomly choose pitch shift between -5 and 5 semitones
        n_steps = random.randint(-5, 5)
        
        # Apply transformations
        y_stretched = time_stretch(y, rate)
        y_shifted = pitch_shift(y, sr, n_steps)
        
        # Prepare file names for saving
        base_name = os.path.splitext(audio_file)[0]
        time_stretched_file = os.path.join(output_folder, f'{base_name}_stretched.mp3')
        pitch_shifted_file = os.path.join(output_folder, f'{base_name}_shifted.mp3')

        # Save the augmented audio as MP3
        save_as_mp3(y_stretched, sr, time_stretched_file)
        save_as_mp3(y_shifted, sr, pitch_shifted_file)
        
        print(f"Processed and saved: {time_stretched_file} and {pitch_shifted_file}")

# Example usage:
dataset_folder = 'path_to_your_dataset_folder'  # Replace with your folder path
output_folder = 'path_to_output_folder'  # Replace with your output folder path

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Augment and save the dataset
augment_and_save_dataset(dataset_folder, output_folder)

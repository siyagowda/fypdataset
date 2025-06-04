import parselmouth
import os
import librosa
import pandas as pd
import numpy as np

def calculate_hnr(y, sr):
    # Convert waveform to a Parselmouth Sound object
    sound = parselmouth.Sound(y, sr)
    # Extract harmonicity object (HNR)
    harmonicity = sound.to_harmonicity_cc()
    # Return the mean HNR (in dB)
    return harmonicity.values[harmonicity.values != -200].mean()

def analyze_audio_file(file_path):
    y, sr = librosa.load(file_path, sr=None)
    hnr = calculate_hnr(y, sr)

    return {
        'file': os.path.basename(file_path),
        'hnr': hnr
    }

def analyze_dataset(dataset_folder):
    # List all audio files in the dataset folder
    audio_files = [f for f in os.listdir(dataset_folder) if f.endswith('.mp3')]
    print(len(audio_files))

    # Analyze each file and store the results in a list
    results = []
    for file in audio_files:
        file_path = os.path.join(dataset_folder, file)
        analysis_result = analyze_audio_file(file_path)
        results.append(analysis_result)
    
    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(results)
    return df

dataset_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data/ai_segments'  # Replace with your folder path
df = analyze_dataset(dataset_folder)
print(df)
#df.to_csv("test_output.csv", index=False)

# Calculate average values for each feature
average_values = df.select_dtypes(include=[np.number]).mean()
print("Average values for each feature:")
print(average_values)
import librosa
import numpy as np
import os
import pandas as pd
import parselmouth

def calculate_rhythmic_entropy(y, sr):
    # Onset detection
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    
    # Calculate entropy of inter-onset intervals
    intervals = np.diff(onset_times)
    if len(intervals) > 0:
        entropy = -np.sum(intervals * np.log2(intervals))
    else:
        entropy = 0
    return entropy

def calculate_melodic_range(y, sr):
    # Harmonic-Percussive separation to focus on melody
    y_harmonic, _ = librosa.effects.hpss(y)
    # Extract pitch information
    pitches, magnitudes = librosa.core.piptrack(y=y_harmonic, sr=sr)
    # Calculate the melodic range as the difference between max and min pitch
    pitch_range = np.max(pitches) - np.min(pitches)
    return pitch_range

def calculate_hnr(y, sr):
    # Convert waveform to a Parselmouth Sound object
    sound = parselmouth.Sound(y, sr)
    # Extract harmonicity object (HNR)
    harmonicity = sound.to_harmonicity_cc()
    # Return the mean HNR (in dB)
    return harmonicity.values[harmonicity.values != -200].mean()

def calculate_spectral_centroid(y, sr):
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    return np.mean(centroid)

def calculate_spectral_bandwidth(y, sr):
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    return np.mean(bandwidth)

def calculate_zero_crossing_rate(y):
    zcr = librosa.feature.zero_crossing_rate(y)
    return np.mean(zcr)

def calculate_rms_energy(y):
    rms = librosa.feature.rms(y=y)
    return np.mean(rms)

def analyze_audio_file(file_path):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)
    
    # Calculate the features
    rhythmic_entropy = calculate_rhythmic_entropy(y, sr)
    melodic_range = calculate_melodic_range(y, sr)
    hnr = calculate_hnr(y, sr)
    spectral_centroid = calculate_spectral_centroid(y, sr)
    spectral_bandwidth = calculate_spectral_bandwidth(y, sr)
    zcr = calculate_zero_crossing_rate(y)
    rms_energy = calculate_rms_energy(y)

    file_name = os.path.basename(file_path)
    
    # Return the results as a dictionary
    return {
        'file': file_name,
        'rhythmic_entropy': rhythmic_entropy,
        'melodic_range': melodic_range,
        'hnr': hnr,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'zero_crossing_rate': zcr,
        'rms_energy': rms_energy
    }

def analyze_dataset(dataset_folder):
    # List all audio files in the dataset folder
    audio_files = [f for f in os.listdir(dataset_folder) if f.endswith('.mp3')]
    
    # Analyze each file and store the results in a list
    results = []
    for file in audio_files:
        file_path = os.path.join(dataset_folder, file)
        analysis_result = analyze_audio_file(file_path)
        results.append(analysis_result)
    
    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(results)
    return df

dataset_folder = '/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data/augmented_ai'  # Replace with your folder path
df = analyze_dataset(dataset_folder)
print(df)
df.to_csv("normal_large_ai_aug_anal_output.csv", index=False)

# Calculate average values for each feature
average_values = df.select_dtypes(include=[np.number]).mean()
print("Average values for each feature:")
print(average_values)

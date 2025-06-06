import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from collections import defaultdict

def extract_features(file_path, mp3_file, sr=22050, n_mfcc=13, output_dir="features", timing_dict=None):
    y, sr = librosa.load(file_path, sr=sr)
    base_filename = os.path.basename(file_path).replace('.mp3', '')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    features = {}

    # 1. Mel Spectrogram
    start = time.time()
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    features['Mel_Spectrogram'] = mel_spectrogram_db
    timing_dict['Mel_Spectrogram'].append(time.time() - start)

    # 2. MFCC
    start = time.time()
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    features['MFCC'] = mfcc
    timing_dict['MFCC'].append(time.time() - start)

    # 3. CQT
    start = time.time()
    cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
    features['CQT'] = cqt
    timing_dict['CQT'].append(time.time() - start)

    # 4. Chromagram
    start = time.time()
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features['Chromagram'] = chroma
    timing_dict['Chromagram'].append(time.time() - start)

    # Save feature images
    for name, data in features.items():
        folder = os.path.join(output_dir, name)
        os.makedirs(folder, exist_ok=True)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(data, x_axis='time', sr=sr)
        plt.colorbar(format='%+2.0f dB')
        plt.title(name)
        plt.tight_layout()

        output_path = os.path.join(folder, f"{base_filename}-{name}.png")
        plt.savefig(output_path)
        plt.close()

folder_path = "/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data/ai_segments"
output_dir = "/vol/bitbucket/sg2121/fypdataset/dataset_timing/features/ai"
mp3_files = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]

timing_data = defaultdict(list)
file_count = 0

for mp3_file in mp3_files:
    file_path = os.path.join(folder_path, mp3_file)
    print(f"Processing {file_path}...")
    try:
        extract_features(file_path, mp3_file, output_dir=output_dir, timing_dict=timing_data)
        file_count += 1
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")

# Save timing summary
summary_path = os.path.join(output_dir, "avg_feature_times.txt")
with open(summary_path, "w") as f:
    f.write(f"Processed {file_count} files\n\n")
    for feature, times in timing_data.items():
        avg_time = sum(times) / len(times) if times else 0
        f.write(f"{feature}: {avg_time:.6f} sec (n={len(times)})\n")

print(f"Per-feature timing saved to {summary_path}")

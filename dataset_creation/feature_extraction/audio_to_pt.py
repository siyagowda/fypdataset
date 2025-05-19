import os
import torchaudio
import torchaudio.transforms as T
import torch
from tqdm import tqdm

# === Configuration ===
input_dir = "/vol/bitbucket/sg2121/fypdataset/dataset/normal_data"             # Folder with mp3 files organized in subfolders (e.g., ai/, human/)
output_dir = "/vol/bitbucket/sg2121/fypdataset/dataset/tensors"      # Where to save .pt files
target_sr = 22050                     # Sample rate for resampling
n_mels = 128                          # Mel bands
target_width = 256                   # Time dimension (pad or crop to this width)

# === Transformations ===
resample = T.Resample(orig_freq=44100, new_freq=target_sr)
mel_spec = T.MelSpectrogram(sample_rate=target_sr, n_fft=1024, hop_length=512, n_mels=n_mels)
to_db = T.AmplitudeToDB(top_db=80)

# === Core processing function ===
def process_and_save(input_path, output_path):
    waveform, sr = torchaudio.load(input_path)

    # Resample if needed
    if sr != target_sr:
        waveform = resample(waveform)

    # Convert to mono
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Compute mel spectrogram
    mel = mel_spec(waveform)
    mel_db = to_db(mel)  # shape: (1, 128, T)

    # Pad or crop to target width
    _, _, time_dim = mel_db.shape
    if time_dim < target_width:
        pad_amt = target_width - time_dim
        mel_db = torch.nn.functional.pad(mel_db, (0, pad_amt))
    else:
        start = (time_dim - target_width) // 2
        mel_db = mel_db[:, :, start:start+target_width]

    # Save as .pt file
    torch.save(mel_db, output_path)

# === Walk through dataset folders ===
for label in os.listdir(input_dir):
    label_dir = os.path.join(input_dir, label)
    if not os.path.isdir(label_dir):
        continue

    tensor_output_dir = os.path.join(output_dir, label, "mel_spec_tensor")
    os.makedirs(tensor_output_dir, exist_ok=True)

    for file in tqdm(os.listdir(label_dir), desc=f"Processing {label}"):
        if file.endswith(".mp3"):
            input_path = os.path.join(label_dir, file)
            output_filename = file.replace(".mp3", ".pt")
            output_path = os.path.join(tensor_output_dir, output_filename)

            try:
                process_and_save(input_path, output_path)
            except Exception as e:
                print(f"⚠️ Failed {file}: {e}")

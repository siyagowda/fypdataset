import os
import torchaudio
import torchaudio.transforms as T
import torch
from tqdm import tqdm

# === Configuration ===
input_dir = "/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data"  # Folder with mp3 files organized in subfolders (e.g., ai/, human/)
output_dir = "/vol/bitbucket/sg2121/fypdataset/dataset_large2/tensors"     # Where to save .pt files
target_sr = 22050
n_mfcc = 40                        # Number of MFCCs to keep (commonly 13 or 40)
target_width = 256                # Time dimension (pad or crop to this width)

# === Transformations ===
resample = T.Resample(orig_freq=44100, new_freq=target_sr)
mfcc_transform = T.MFCC(
    sample_rate=target_sr,
    n_mfcc=n_mfcc,
    melkwargs={
        "n_fft": 1024,
        "hop_length": 512,
        "n_mels": 128,
        "center": True,
        "power": 2.0,
    },
)

# === Core processing function ===
def process_and_save(input_path, output_path):
    waveform, sr = torchaudio.load(input_path)

    # Resample if needed
    if sr != target_sr:
        waveform = resample(waveform)

    # Convert to mono
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Compute MFCC
    mfcc = mfcc_transform(waveform)  # shape: (1, n_mfcc, T)

    # Pad or crop to target width
    _, _, time_dim = mfcc.shape
    if time_dim < target_width:
        pad_amt = target_width - time_dim
        mfcc = torch.nn.functional.pad(mfcc, (0, pad_amt))
    else:
        start = (time_dim - target_width) // 2
        mfcc = mfcc[:, :, start:start+target_width]

    # Save as .pt file
    torch.save(mfcc, output_path)

# === Walk through dataset folders ===
for label in os.listdir(input_dir):
    label_dir = os.path.join(input_dir, label)
    if not os.path.isdir(label_dir):
        continue

    tensor_output_dir = os.path.join(output_dir, label, "mfcc_tensor")
    os.makedirs(tensor_output_dir, exist_ok=True)

    for file in tqdm(os.listdir(label_dir), desc=f"Processing {label}"):
        if file.endswith(".mp3"):
            input_path = os.path.join(label_dir, file)
            output_filename = file.replace(".mp3", ".pt")
            output_path = os.path.join(tensor_output_dir, output_filename)

            if os.path.exists(output_path):
                continue

            try:
                process_and_save(input_path, output_path)
            except Exception as e:
                print(f"⚠️ Failed {file}: {e}")

import os
import torchaudio
import torchaudio.transforms as T
import torch
from tqdm import tqdm
import time

input_dir = "/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data"  
output_dir = "/vol/bitbucket/sg2121/fypdataset/dataset_timing/tensors" 
timing_output_file = os.path.join(output_dir, "mfcc_avg_time.txt")   
target_sr = 22050
n_mfcc = 40                        # Number of MFCCs to keep
target_width = 256                # Time dimension (pad or crop to this width)

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

total_time = 0.0
file_count = 0

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
                start_time = time.time()
                process_and_save(input_path, output_path)
                elapsed = time.time() - start_time
                total_time += elapsed
                file_count += 1
            except Exception as e:
                print(f"Failed {file}: {e}")

if file_count > 0:
    avg_time = total_time / file_count
    with open(timing_output_file, "w") as f:
        f.write(f"Processed {file_count} files\n")
        f.write(f"Total processing time: {total_time:.4f} seconds\n")
        f.write(f"Average time per file: {avg_time:.6f} seconds\n")
    print(f"Average processing time saved to: {timing_output_file}")
else:
    print("No files were processed.")
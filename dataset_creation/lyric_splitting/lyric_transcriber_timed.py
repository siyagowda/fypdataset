import whisper
import torch
import time
from pathlib import Path

# Settings
input_dir = Path("/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data/ai_segments")
output_dir = Path("/vol/bitbucket/sg2121/fypdataset/dataset_timing/lyrics/ai")
timing_file = output_dir / "average_transcription_time.txt"

output_dir.mkdir(parents=True, exist_ok=True)

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)
print(f"Using device: {device}")

# Timing accumulation
total_time = 0.0
num_files = 0

# Transcription loop
for audio_path in input_dir.glob("*.*"):
    output_path = output_dir / f"{audio_path.stem}_lyrics.txt"

    if output_path.exists():
        print(f"Skipping (already exists): {output_path.name}")
        continue

    print(f"Transcribing: {audio_path.name}")
    try:
        start = time.perf_counter()
        result = model.transcribe(str(audio_path), fp16=(device == "cuda"))
        end = time.perf_counter()

        # Save lyrics
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"].strip())

        duration = end - start
        total_time += duration
        num_files += 1
        print(f"Transcribed {audio_path.name} in {duration:.2f}s")

    except Exception as e:
        print(f"Failed to transcribe {audio_path.name}: {e}")

# Save average transcription time
if num_files > 0:
    avg_time = total_time / num_files
    with open(timing_file, "w") as f:
        f.write(f"Device used: {device}\n")
        f.write(f"Transcribed {num_files} files\n")
        f.write(f"Average transcription time: {avg_time:.4f} seconds\n")
    print(f"\nAverage transcription time saved to {timing_file}")
else:
    print("No files were transcribed.")

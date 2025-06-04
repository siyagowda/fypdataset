import whisper
import torch
from pathlib import Path

# Settings
input_dir = Path("/vol/bitbucket/sg2121/fypdataset/test_dataset/normal_data/human")
output_dir = Path("/vol/bitbucket/sg2121/fypdataset/test_dataset/lyrics/human")

output_dir.mkdir(parents=True, exist_ok=True)

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

# Loop through audio files
for audio_path in input_dir.glob("*.*"):  
    output_path = output_dir / f"{audio_path.stem}_lyrics.txt"

    # Skip if already transcribed
    if output_path.exists():
        print(f"Skipping (already exists): {output_path.name}")
        continue

    print(f"Transcribing: {audio_path.name}")
    try:
        result = model.transcribe(str(audio_path), fp16=True)
        text = result["text"].strip()

        # Save transcript
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved: {audio_path.name}")

    except Exception as e:
        print(f"Failed to transcribe {audio_path.name}: {e}")


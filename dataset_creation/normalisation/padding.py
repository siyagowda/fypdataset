from pydub import AudioSegment
import os

def pad_to_30_seconds(audio, target_duration_ms=30_000):
    duration = len(audio)
    if duration < target_duration_ms:
        silence = AudioSegment.silent(duration=target_duration_ms - duration)
        audio += silence
    return audio

def process_folder(input_folder):
    count = 0
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mp3"):
            try:
                input_file = os.path.join(input_folder, file_name)

                # Load and check length
                audio = AudioSegment.from_mp3(input_file)
                duration_ms = len(audio)
                duration_sec = duration_ms / 1000

                if duration_sec >= 30:
                    print("SKIPPED")
                    continue  # Skip if already at least 30 seconds

                print(f"PADDING: {file_name} ({duration_sec:.2f}s)")
                padded_audio = pad_to_30_seconds(audio)
                padded_audio.export(input_file, format="mp3")
                count += 1

            except Exception as e:
                print(f"Error processing '{file_name}': {e}")

    print(f"{count} files padded to 30 seconds")

input_folder = '/vol/bitbucket/sg2121/fypdataset/test_dataset/normal_data/human'
process_folder(input_folder)

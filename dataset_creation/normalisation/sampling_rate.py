from pydub import AudioSegment
import librosa
import numpy as np

def resample_and_normalize(input_file, output_file, target_sample_rate=16000):
    # Load the MP3 file using pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # Resample the audio to the target sample rate
    audio_resampled = audio.set_frame_rate(target_sample_rate)

    # Export the resampled audio to a temporary WAV file
    temp_wav = "temp_resampled.wav"
    audio_resampled.export(temp_wav, format="wav")

    # Load the WAV file using librosa for normalization
    y, sr = librosa.load(temp_wav, sr=target_sample_rate)  # sr ensures consistency
    
    # Normalize the audio signal to be between -1 and 1
    y_normalized = librosa.util.normalize(y)

    # Export the normalized audio as an MP3
    librosa.output.write_wav(temp_wav, y_normalized, sr)  # Save normalized WAV (optional)
    audio_resampled = AudioSegment.from_wav(temp_wav)
    audio_resampled.export(output_file, format="mp3")  # Save as MP3

    print(f"Resampled and normalized audio saved to {output_file}")

# Example usage
input_file = 'path_to_input_file.mp3'
output_file = 'path_to_output_file.mp3'
resample_and_normalize(input_file, output_file, target_sample_rate=16000)

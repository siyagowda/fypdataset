from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf

def resample_and_normalize(input_file, output_file, target_sample_rate=24000):
    # Load the MP3 file using pydub
    audio = AudioSegment.from_mp3(input_file)
    
    # Resample the audio to the target sample rate
    audio_resampled = audio.set_frame_rate(target_sample_rate)

    # Export the resampled audio to a temporary WAV file
    temp_wav = "temp_resampled.wav"
    audio_resampled.export(temp_wav, format="wav")

    # Load the WAV file using librosa for normalization
    y, sr = librosa.load(temp_wav, sr=target_sample_rate)
    
    # Normalize the audio signal to be between -1 and 1
    y_normalized = librosa.util.normalize(y)

    # Save normalized WAV using soundfile
    sf.write(temp_wav, y_normalized, sr)

    # Convert back to MP3 using pydub
    audio_normalized = AudioSegment.from_wav(temp_wav)
    audio_normalized.export(output_file, format="mp3")

    print(f"Resampled and normalized audio saved to {output_file}")

input_file = '/vol/bitbucket/sg2121/fypdataset/dataset/test/S1803R.mp3'  
output_file = '/vol/bitbucket/sg2121/fypdataset/dataset/test/S1803RN1.mp3'
resample_and_normalize(input_file, output_file, target_sample_rate=24000)

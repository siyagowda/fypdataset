import os
import librosa
import numpy as np
from python_speech_features import base
from scipy.fftpack import dct
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
import time

def extract_plp_from_mp3(file_path, sr=16000, n_ceps=13, winlen=0.025, winstep=0.01, 
                         nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97):
    """
    Extract PLP coefficients from an MP3 file.
    
    Parameters:
    -----------
    file_path : str
        Path to the MP3 file
    sr : int
        Sample rate to load the audio with
    n_ceps : int
        Number of cepstral coefficients
    winlen : float
        Window length in seconds
    winstep : float
        Window step in seconds
    nfilt : int
        Number of filters in the filterbank
    nfft : int
        FFT size
    lowfreq : int
        Lowest band edge of mel filters
    highfreq : int
        Highest band edge of mel filters
    preemph : float
        Pre-emphasis coefficient
    
    Returns:
    --------
    plp_features : ndarray
        PLP coefficients
    """
    # Load audio file
    y, sr = librosa.load(file_path, sr=sr, mono=True)
    
    # Get PLP coefficients using python_speech_features
    fbank_feat = base.fbank(y, samplerate=sr, winlen=winlen, winstep=winstep,
                          nfilt=nfilt, nfft=nfft, lowfreq=lowfreq, highfreq=highfreq,
                          preemph=preemph)
    
    # 1. Get filter bank energies
    fb_energies = fbank_feat[0]
    
    # 2. Apply equal-loudness curve and cubic-root compression 
    loudness_fb = np.power(fb_energies, 0.33)  # Cube root compression
    
    # 3. Apply DCT 
    plp_coeffs = dct(loudness_fb, type=2, axis=1, norm='ortho')[:, :n_ceps]
    
    return plp_coeffs

def plot_plp_coefficients(plp_coeffs, output_path, sr=16000, winstep=0.01):
    """
    Plot PLP coefficients as a heatmap and save to file.
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(plp_coeffs.T, aspect='auto', origin='lower')
    plt.title('PLP Coefficients')
    plt.ylabel('PLP Coefficient Index')
    plt.xlabel('Frame')
    
    # Set x-axis labels to reflect time in seconds
    plt.colorbar(label='Coefficient Value')
    
    # Set x-tick labels to show time in seconds
    x_ticks = np.arange(0, plp_coeffs.shape[0], max(1, int(plp_coeffs.shape[0]/5)))
    x_tick_labels = [f"{t * winstep:.1f}" for t in x_ticks]
    plt.xticks(x_ticks, x_tick_labels)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def save_plp_plots_from_mp3s(input_dir, output_dir, n_ceps=13):
    """
    Process all MP3 files in a directory and save PLP plots as images.
    
    Parameters:
    -----------
    input_dir : str
        Directory containing MP3 files
    output_dir : str
        Directory to save plot images
    n_ceps : int
        Number of cepstral coefficients
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of MP3 files
    mp3_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print(f"No MP3 files found in {input_dir}")
        return
    
    # Process each MP3 file
    print(f"Processing {len(mp3_files)} MP3 files...")
    
    progress_bar = tqdm(mp3_files, desc="Generating PLP plots", ncols=100)
    
    # Log file for detailed output
    log_path = os.path.join(output_dir, "processing_log.txt")
    total_time = 0.0
    file_count = 0
    
    with open(log_path, 'w') as log_file:
        for mp3_file in progress_bar:
            # Construct full input path
            input_path = os.path.join(input_dir, mp3_file)
            
            # Get base filename without extension
            base_name = os.path.splitext(mp3_file)[0]
            
            # Extract PLP coefficients and save plot
            try:
                start_time = time.time()
                
                # Extract PLP coefficients
                plp_features = extract_plp_from_mp3(input_path, n_ceps=n_ceps)
                
                # Save visualization
                plot_path = os.path.join(output_dir, f"{base_name}_plp.png")
                plot_plp_coefficients(plp_features, plot_path)
                
                progress_bar.set_postfix_str(f"Processed: {mp3_file}")
                
                # Write to log file instead of printing to console
                log_file.write(f"Saved plot for {mp3_file}\n")
                elapsed = time.time() - start_time
                total_time += elapsed
                file_count += 1
                
            except Exception as e:
                error_msg = f"Error processing {mp3_file}: {str(e)}"
                # Write errors to log file
                log_file.write(error_msg + "\n")
                # Also update progress bar with error info
                progress_bar.set_postfix_str(f"Error: {mp3_file}")
    
    print(f"Processing complete. PLP plots saved to {output_dir}")
    print(f"Detailed processing log saved to {log_path}")

    return total_time, file_count

total_time, file_count = save_plp_plots_from_mp3s('/vol/bitbucket/sg2121/fypdataset/dataset_large2/normal_data/ai', '/vol/bitbucket/sg2121/fypdataset/dataset_timing/features/ai/PLP')

timing_output_file = os.path.join('/vol/bitbucket/sg2121/fypdataset/dataset_timing/features/ai/PLP', "plp_avg_time.txt")

if file_count > 0:
    avg_time = total_time / file_count
    with open(timing_output_file, "w") as f:
        f.write(f"Processed {file_count} files\n")
        f.write(f"Total processing time: {total_time:.4f} seconds\n")
        f.write(f"Average time per file: {avg_time:.6f} seconds\n")
    print(f"Average processing time saved to: {timing_output_file}")
else:
    print("No files were processed.")
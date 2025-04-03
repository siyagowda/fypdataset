from pydub import AudioSegment

def cut_mp3(input_file, output_folder, segment_length=60):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_file)
    
    # Calculate the number of segments
    duration_ms = len(audio)  # duration in milliseconds
    num_segments = duration_ms // (segment_length * 1000)  # 1000 ms = 1 second
    
    for i in range(num_segments):
        start_time = i * segment_length * 1000  # start time in milliseconds
        end_time = start_time + (segment_length * 1000)  # end time in milliseconds
        
        # Cut the segment
        segment = audio[start_time:end_time]
        
        # Export the segment
        output_file = f"{output_folder}/segment_{i+1}.mp3"
        segment.export(output_file, format="mp3")
        print(f"Segment {i+1} saved as {output_file}")

# Example usage
input_file = 'path_to_your_file.mp3'  # Path to your MP3 file
output_folder = 'output_folder_path'   # Folder to save the segments
cut_mp3(input_file, output_folder)

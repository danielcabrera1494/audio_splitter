import argparse
import os
import subprocess
from pydub import AudioSegment

# Get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t',
    help='Time in milliseconds for each chunk. Default: 10000',
    nargs='?',
    type=int,
    dest='chunk_size',
    default=10000)
parser.add_argument('-i', '--inputfile',
    help='Input .wav filepath. Default: africa-toto.wav',
    nargs='?',
    type=str,
    dest='input',
    default='africa-toto.wav')
parser.add_argument('-d', '--directory',
    help='Output directory path. Default: .',
    nargs='?',
    type=str,
    dest='outdir',
    default='.')
parser.add_argument('-v', '--verbose',
    help='Verbose. Default: false',
    action='store_true',
    dest='verbose',
    default=False)
ARGS = parser.parse_args()

def save_chunk(audio_file, t1, t2, filename_out):
 
    if t2 - t1 < ARGS.chunk_size:
        if ARGS.verbose:
            print(f'Skipping short chunk: {filename_out}')
        return
    try:
        # Extract the audio chunk
        audio_chunk = audio_file[t1:t2]

        # Prepare the file paths
        audio_path_orig = os.path.splitext(filename_out)[0] + '_orig.wav'
        wav_path = os.path.splitext(filename_out)[0] + '_16k_mono.wav'

        # Export the chunk in the original format temporarily
        audio_chunk.export(audio_path_orig, format='wav')

        # Convert the saved chunk to 16kHz mono using FFmpeg
        ffmpeg_command = f"ffmpeg -i {audio_path_orig} -ac 1 -ar 16000 {wav_path}"
        subprocess.run(ffmpeg_command, shell=True, check=True)

        # Remove the temporary original format file
        os.remove(audio_path_orig)

        if ARGS.verbose:
            print(f'Converted to 16kHz mono: {wav_path}')

    except Exception as e:
        print('Failed to process: '+filename_out)
        print(e)

def process_audio_file(input_file):
    if ARGS.verbose:
        print('Processing: {}'.format(input_file))

    # Get the name of the directory containing the input file
    input_dir_name = os.path.dirname(input_file)

    # Get the base name of the input file (without extension)
    input_base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create a subfolder for each subdirectory in the path
    subfolders = input_dir_name.split(os.path.sep)
    subfolder_path = ARGS.outdir
    for subfolder in subfolders:
        subfolder_path = os.path.join(subfolder_path, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)

    # Create a folder with the name of the input file inside the last subfolder
    output_dir = os.path.join(subfolder_path, input_base_name)
    os.makedirs(output_dir, exist_ok=True)

    # Open .wav file
    audio_file = AudioSegment.from_wav(input_file)
    prev_time = 0
    i = 0

    # Save and convert chunks
    for curr_time in range(ARGS.chunk_size, len(audio_file), ARGS.chunk_size):
        save_chunk(audio_file, prev_time, curr_time,
                   os.path.join(output_dir, '{}_{:04}.wav'.format(input_base_name, i)))
        prev_time = curr_time
        i += 1

    # Save and convert last chunk
    if prev_time < len(audio_file):
        save_chunk(audio_file, prev_time, len(audio_file),
                   os.path.join(output_dir, '{}_{:04}.wav'.format(input_base_name, i)))

def main():
    if os.path.isfile(ARGS.input):
        # If the input is a file, process that file
        process_audio_file(ARGS.input)
    elif os.path.isdir(ARGS.input):
        # If the input is a directory, process all audio files in that directory and its subdirectories
        for root, dirs, files in os.walk(ARGS.input):
            for file in files:
                if file.lower().endswith('.wav'):
                    audio_path = os.path.join(root, file)
                    process_audio_file(audio_path)
    else:
        print('Invalid input: {}'.format(ARGS.input))

if __name__ == '__main__':
    main()

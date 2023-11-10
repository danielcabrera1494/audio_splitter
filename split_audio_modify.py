import argparse
import os
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
parser.add_argument('-f', '--filenameout',
	help='Output filename prefix e.g. \'output\' saved as \'output_1.wav\''+
		 '\'output_2.wav\', ... Default: output',
	nargs='?',
	type=str,
	dest='outfile',
	default='output')
parser.add_argument('-v', '--verbose',
	help='Verbose. Default: false',
	action='store_true',
	dest='verbose',
	default=False)
ARGS = parser.parse_args()

def save_chunk(audio_file, t1, t2, filename_out):
	try:
		audio_chunk = audio_file[t1:t2]
		audio_chunk.export(filename_out, format='wav')
		if ARGS.verbose:
			print('Saved: '+filename_out)
	except Exception as e:
		print('Failed to save: '+filename_out)
		print(e)

def process_audio_file(input_file):
	if ARGS.verbose:
		print('Processing: {}'.format(input_file))
	# Open .wav file
	audio_file = AudioSegment.from_wav(input_file)
	prev_time = 0
	i = 0
	# Save chunks
	for curr_time in range(ARGS.chunk_size, len(audio_file), ARGS.chunk_size):
		save_chunk(audio_file, prev_time, curr_time,
				   '{}/{}_{:04}.wav'.format(ARGS.outdir, ARGS.outfile, i))
		prev_time = curr_time
		i+=1
	# Save last chunk
	if prev_time < len(audio_file):
		save_chunk(audio_file, prev_time, len(audio_file),
				   '{}/{}_{:04}.wav'.format(ARGS.outdir, ARGS.outfile, i))

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
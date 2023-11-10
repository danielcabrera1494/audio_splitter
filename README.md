# Python Audio Splitter

Script to split an audio file into equal sized chunks of n-milliseconds length.

## Help

```
usage: split_audio.py [-h] [-t [CHUNK_SIZE]] [-i [INPUT]] [-d [OUTDIR]]
                      [-f [OUTFILE]] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -t [CHUNK_SIZE]       Time in milliseconds for each chunk. Default: 10000
  -i [INPUT], --inputfile [INPUT]
                        Input .wav filepath. Default: africa-toto.wav
  -d [OUTDIR], --directory [OUTDIR]
                        Output directory path. Default: .
  -f [OUTFILE], --filenameout [OUTFILE]
                        Output filename prefix e.g. 'output' saved as
                        'output_1.wav''output_2.wav', ... Default: output
  -v, --verbose         Verbose. Default: false
```

### Note

Script assumes .wav as input. Change script for other input as necessary

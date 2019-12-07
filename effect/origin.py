import struct
import math
from myfunctions import clip16
import pyaudio
import wave

def origin(wavfile):

    wf = wave.open(wavfile, 'rb')

    # Read wave file properties
    RATE        = wf.getframerate()     # Frame rate (frames/second)
    WIDTH       = wf.getsampwidth()     # Number of bytes per sample
    LEN         = wf.getnframes()       # Signal length
    CHANNELS    = wf.getnchannels()     # Number of channels

    print('The file has %d channel(s).'         % CHANNELS)
    print('The file has %d frames/second.'      % RATE)
    print('The file has %d frames.'             % LEN)
    print('The file has %d bytes per sample.'   % WIDTH)

    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                    channels    = CHANNELS,
                    rate        = RATE,
                    input       = False,
                    output      = True )

    for n in range(0,LEN):
        input_bytes = wf.readframes(1)
        stream.write(input_bytes)

    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

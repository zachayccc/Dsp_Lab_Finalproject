import struct
import math
from myfunctions import clip16
import pyaudio
import wave

def echo(wavfile):

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


    # Set parameters of delay system
    b0 = 1.0            # direct-path gain
    G = 2            # feed-forward gain
    delay_sec = 0.25    # delay in seconds, 50 milliseconds   Try delay_sec = 0.02
    N = int( RATE * delay_sec )   # delay in samples
    BUFFER_LEN =  N          # Set buffer length.
    buffer_1 = BUFFER_LEN * [0]   # list of zeros
    buffer_2 = BUFFER_LEN * [0] 
    k = 0                   # Initialize buffer index (circular index)
    input_bytes = wf.readframes(1)
    print('* Start')

    while len(input_bytes) > 0:
        x0,x1 = struct.unpack('hh', input_bytes)    # Convert binary data to number
        # Compute output value
        # y(n) = b0 x(n) + G x(n-N)
        y0 = b0 * x0 + G * buffer_1[k]
        y1 = b0 * x1 + G * buffer_2[k]

        # Update buffer
        buffer_1[k] = x0
        buffer_2[k] = x1
        # Increment buffer index
        k = k + 1
        if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
            k = 0
        # Clip and convert output value to binary data
        output_bytes = struct.pack('hh', int(clip16(y0)),int(clip16(y1)))
        # Write output value to audio stream
        stream.write(output_bytes)
        # Get next frame
        input_bytes = wf.readframes(1)  
    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
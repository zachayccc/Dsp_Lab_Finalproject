import struct
import math
from myfunctions import clip16
import pyaudio
import wave

def vibrato(wavfile):

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
    f0 = 2
    W = 0.2   # W = 0 for no effect
    BUFFER_LEN =  1024          # Set buffer length.
    buffer_1 = BUFFER_LEN * [0]   # list of zeros
    buffer_2 = BUFFER_LEN * [0] 

    # Buffer (delay line) indices
    kr = 0  # read index
    kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

    for n in range(0,LEN):

        input_bytes = wf.readframes(1)

        x0,x1 = struct.unpack('hh', input_bytes)

        kr_prev = int(math.floor(kr))
        frac = kr - kr_prev    # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == BUFFER_LEN:
            kr_next = 0

        # Compute output value using interpolation
        y0 = (1-frac) * buffer_1[kr_prev] + frac * buffer_1[kr_next]
        y1 = (1-frac) * buffer_2[kr_prev] + frac * buffer_2[kr_next]
        # Update buffer
        buffer_1[kw] = x0
        buffer_2[kw] = x1
        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = kr - BUFFER_LEN

        # Increment write index    
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0

        output_bytes = struct.pack('hh', int(clip16(y0)),int(clip16(y1)))
        stream.write(output_bytes)
    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

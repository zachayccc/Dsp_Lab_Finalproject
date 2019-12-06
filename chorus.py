import struct
import math
from myfunctions import clip16
import pyaudio
import wave
import numpy as np

def chorus(wavfile):
    wf = wave.open(wavfile, 'rb')
    RATE= wf.getframerate()
    WIDTH= wf.getsampwidth()     # Number of bytes per sample
    LEN= wf.getnframes()
    CHANNELS= wf.getnchannels()     # Number of channels

    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                channels    = CHANNELS,
                rate        = RATE,
                input       = False,
                output      = True )
    l=20
    g1=10  
    g2=5
    f0 = 2  
    W1 = 0.2   # W = 0 for no effect
    W2=0.8  
    BUFFER_LEN =  1024          # Set buffer length.
    buffer_1 = BUFFER_LEN * [0]   # list of zeros
    buffer_2 = BUFFER_LEN * [0]
    buffer_3 = BUFFER_LEN * [0]   # list of zeros
    buffer_4 = BUFFER_LEN * [0]

    kr1 = 0  # read index
    kw1 = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)
    kr2=0
    kw2=int(0.5 * BUFFER_LEN)
    for n in range(0,LEN):
        input_bytes = wf.readframes(1)
        x0,x1 = struct.unpack('hh', input_bytes)

        kr_prev1 = int(math.floor(kr1))
        frac1 = kr1 - kr_prev1    # 0 <= frac < 1
        kr_next1 = kr_prev1 + 1
        if kr_next1 == BUFFER_LEN:
            kr_next1 = 0
        y0 = (1-frac1) * buffer_1[kr_prev1] + frac1 * buffer_1[kr_next1]
        y1 = (1-frac1) * buffer_2[kr_prev1] + frac1 * buffer_2[kr_next1]
        buffer_1[kw1] = x0
        buffer_2[kw1] = x1


        kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f0 * n / RATE )
            
        if kr1 >= BUFFER_LEN:
        	kr1 = kr1 - BUFFER_LEN
   
        kw1 = kw1 + 1
        if kw1 == BUFFER_LEN:
        	kw1 = 0


        kr_prev2 = int(math.floor(kr2))
        frac2 = kr2 - kr_prev2    # 0 <= frac < 1
        kr_next2 = kr_prev2 + 1
        if kr_next2 == BUFFER_LEN:
        	kr_next2 = 0
        y2= (1-frac2) * buffer_3[kr_prev2] + frac1 * buffer_3[kr_next2]
        y3 = (1-frac2) * buffer_4[kr_prev2] + frac1 * buffer_4[kr_next2]
        buffer_3[kw2] = x0
        buffer_4[kw2] = x1


        kr2 = kr2 + 1 + W2 * math.sin( 2 * math.pi * f0 * n / RATE )
            
        if kr2 >= BUFFER_LEN:
            kr2 = kr2 - BUFFER_LEN
   
        kw2 = kw2 + 1
        if kw2 == BUFFER_LEN:
        	kw2 = 0

        output_bytes = struct.pack('hh', int(clip16(x0*l+y0*g1+y2*g2)),int(clip16(x1+y2*g1+y3*g2)))
        stream.write(output_bytes)
    print('* Finished')
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
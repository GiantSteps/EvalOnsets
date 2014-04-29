'''
Created on Apr 28, 2014

@author: mhermant
'''
import numpy as np
import conf

import essentia
from essentia.standard import *



from bisect import bisect_left


import matplotlib.pyplot as pl


opts = {"name" : "FreqMedian",
        "ratio":0.08
        
        }



opts_r = {"ratio":[.1,.9,0.1],}




def compute(audio):
    """
    filters out maxs values corresponding to harmonic part
    """
    audio = essentia.array(audio)
    sampleRate  = int(conf.opts['sampleRate'])
    frameSize   = int(conf.opts['frameSize'])
    hopSize     = frameSize/4
    zeroPadding = int(conf.opts['zeroPadding'])
    windowType  = conf.opts['windowType']

    frameRate = float(sampleRate)/float(hopSize)


    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    window  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType)
    fft = FFT()
    ifft = IFFT()
    cartesian2polar = CartesianToPolar()
    polar2cartesian = PolarToCartesian()
    audioout=np.zeros(len(audio))
    
    
    
    total_frames = frames.num_frames()
    n_frames = 0
    start_of_frame =0
    
    for frame in frames:

        windowed_frame = window(frame)
        complex_fft = fft(windowed_frame)
        (spectrum,phase) = cartesian2polar(complex_fft)
        sortedS = np.sort(spectrum)
        minFloor = sortedS[int(len(sortedS)*(1.-opts["ratio"]))]
 
        spectrum = essentia.array([0 if x>minFloor else x for x in spectrum ])


        complex_fft=polar2cartesian(spectrum,phase)
        outf = ifft(complex_fft)*.5*hopSize
        if start_of_frame+frameSize < len(audio) and start_of_frame>0:
            audioout[start_of_frame:start_of_frame+frameSize]+=window(outf)
    
        n_frames += 1
        start_of_frame += hopSize
        
    return essentia.array(audioout)



def test():
    
    loader=MonoLoader(filename=conf.PathToData+"sine.wav")

    audio = loader()
    

    a = compute(audio)
    
    pl.plot(audio[:5000])
    pl.plot(a[:5000])
    pl.show()
    MonoWriter(filename = conf.PathToData+"out.wav",format="wav")(a)

    return a


if __name__=="__main__":
    print bisect_left([0, 1, 2],0.1)
    print test()
    
'''
Created on Apr 29, 2014

@author: mhermant
'''

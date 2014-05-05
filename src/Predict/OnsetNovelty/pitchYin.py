
import sys

from essentia import INFO
import essentia
from essentia.standard import *
import numpy as np
import conf


opts={'name' : 'pitch',
      'maxFreq':2000,
      'minFreq':100,
      "confThresh":0.01,
      "smoothTime":1}

    
def compute(audio):
    audio = essentia.array(audio)
    sampleRate  = int(conf.opts['sampleRate'])
    frameSize   = int(conf.opts['frameSize'])
    hopSize     = int(conf.opts['hopSize'])
    zeroPadding = int(conf.opts['zeroPadding'])
    windowType  = conf.opts['windowType']

    frameRate = float(sampleRate)/float(hopSize)


    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    window  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType)
    spectrumf = Spectrum()
    yinf = PitchYinFFT(frameSize = frameSize,minFrequency = opts["minFreq"],maxFrequency = opts["maxFreq"])
    avgf = MovingAverage(size=int(opts["smoothTime"]*frameRate))

    total_frames = frames.num_frames()
    n_frames = 0
    start_of_frame = -frameSize*0.5

    resp,resc = [0],[0]

    
    for frame in frames:

        windowed_frame = window(frame)
        sp = spectrumf(windowed_frame)
        pitch,confi = yinf(sp)
        k=0
        if n_frames:
            """
            here is legato
            """
            if confi>opts["confThresh"] and resc[-1]>opts["confThresh"] :
                if resp[-1]>0:
                    while(True):
                        if pitch*pow(2,k)>2.*resp[-1]:
                            k-=1
                        elif pitch*pow(2,k)<resp[-1]/2.:
                            k+=1
                        else:
                            
                            break
            
                """
                here is attack
                """
            else :
                pitch = 0
            resc+=[confi]
            resp += [pitch*pow(2,k)]
        
        n_frames += 1
        start_of_frame += hopSize
        

    # The onset rate is defined as the number of onsets per seconds

    resp = np.diff(resp)*1000./frameRate

    res = np.zeros(n_frames)
    res[2:] = abs(np.diff(resp))*1000./frameRate
    res = avgf(essentia.array(res))


    return res



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import essentia.standard
    
    path = '/Users/mhermant/Documents/Work/Datasets/jku/onsets/audio/flac/gs_mix2_0dB.wav'
    l = essentia.standard.MonoLoader(filename = path)
    ons = compute(l())
    print ons
    
    plt.plot(ons)
    plt.show()

    
    
    
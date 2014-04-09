
import sys

from essentia import INFO
import essentia
from essentia.progress import Progress
from essentia.standard import *
import numpy as np


opts={}

    
def compute(audio, options):

    sampleRate  = options['sampleRate']
    frameSize   = options['frameSize']
    hopSize     = options['hopSize']
    zeroPadding = options['zeroPadding']
    windowType  = options['windowType']

    frameRate = float(sampleRate)/float(hopSize)

    INFO('Computing Ess Detection...')

    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    window  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType)
    fft = FFT()
    cartesian2polar = CartesianToPolar()
    onsetdetectionHFC = OnsetDetection(method = "hfc", sampleRate = sampleRate)
    onsetdetectionComplex = OnsetDetection(method = "complex", sampleRate = sampleRate)
    

    total_frames = frames.num_frames()
    n_frames = 0
    start_of_frame = -frameSize*0.5

    hfc = []
    complex = []

    progress = Progress(total = total_frames)
    maxhfc=0 
    
    for frame in frames:

        windowed_frame = window(frame)
        complex_fft = fft(windowed_frame)
        (spectrum,phase) = cartesian2polar(complex_fft)
        hfc.append(onsetdetectionHFC(spectrum,phase))
        maxhfc = max(hfc[-1],maxhfc)
        complex.append(onsetdetectionComplex(spectrum,phase))

        # display of progress report
        progress.update(n_frames)

        n_frames += 1
        start_of_frame += hopSize

    # The onset rate is defined as the number of onsets per seconds
    res = [[x/maxhfc for x in hfc]]
    res +=[complex]
   
    return np.array(res)





    
    
    
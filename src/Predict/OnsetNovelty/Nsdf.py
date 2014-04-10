'''
Created on Apr 1, 2014

@author: mhermant
'''
import sys

from essentia import INFO
import essentia
from essentia.progress import Progress
from essentia.standard import *

import matplotlib.pyplot as plt
import numpy as np 
import scipy.signal as signal
import conf


opts = {"name":"Nsdf","minthresh" : 0.0000001}









def compute(audio):
    audio = essentia.array(audio)
    sampleRate  = int(conf.opts['sampleRate'])
    frameSize   = int(conf.opts['frameSize'])
    hopSize     = int(conf.opts['hopSize'])
    zeroPadding = int(conf.opts['zeroPadding'])
    windowType  = conf.opts['windowType']

    frameRate = float(sampleRate)/float(hopSize)

    INFO('Computing Onset Detection...')

    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    window  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType)
    nsdff = Nsdf()
    fftf = Spectrum()
    crestf = Crest()
    instPowf = InstantPower()
    
    total_frames = frames.num_frames()
    n_frames = 0
    start_of_frame = -frameSize*0.5


    progress = Progress(total = total_frames)
    cr = []
    env = []
    for frame in frames:

        windowed_frame = window(frame)
        nsdf = nsdff(frame)
        fftn = fftf(nsdf)
        cr += [crestf(fftn)]
        pow = instPowf(frame)
        
        if len(cr)>2 and pow<opts["minthresh"]:
            
            cr[-1]=cr[-2]
        

        n_frames += 1
        start_of_frame += hopSize

    
    cr = np.array(cr)
#     w = signal.gaussian(3,1)
#     area = np.sum(w)
#     cr =np.convolve(cr,w , 'same')
#     cr = cr/(100.*area)
    return cr
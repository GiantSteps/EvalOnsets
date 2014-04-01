'''
Created on Mar 28, 2014

@author: mhermant
'''
from essentia.standard import *
import essentia
import numpy as np 
import sys
from essentia import INFO
from essentia.progress import Progress
import matplotlib.pyplot as plt
import scipy.signal as signal




def onsetEss(features,opt):
    frameRate = opt['sampleRate']/opt['hopSize']
    onsets = Onsets(frameRate = frameRate)
    if isinstance(features[0],list):
        weights =  essentia.array([1 for x in range(len(features))])
        time_onsets = list(onsets(essentia.array(features),weights))
    else:
        time_onsets = list(onsets(essentia.array([features]),essentia.array([1])))

    return time_onsets






 
    
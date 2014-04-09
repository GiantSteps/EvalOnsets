'''
Created on Mar 28, 2014

@author: mhermant
'''



import essentia
import numpy as np
from essentia.standard import *

opts={}
def compute(features,opt):
    frameRate = opt['sampleRate']/opt['hopSize']
    onsets = Onsets(frameRate = frameRate)
    if isinstance(features[0],list) or isinstance(features[0],np.ndarray):
        weights =  essentia.array([1 for x in range(len(features))])
        time_onsets = list(onsets(essentia.array(features),weights))
    else:
        time_onsets = list(onsets(essentia.array([features]),essentia.array([1])))

    return time_onsets






 
    
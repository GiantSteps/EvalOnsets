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


def compute(features,opt):
    
    frameRate = opt['sampleRate']*1./opt['hopSize']
    t_ons=[]
    print type(features) 
    if any(isinstance(el, list) for el in features) or (isinstance(features,np.ndarray) and features.shape[1]>1):
        t_ons = []
        for l in features:
            t_ons += signal.find_peaks_cwt(l,np.arange(1,15))

    else:
        t_ons = signal.find_peaks_cwt(features,np.arange(1,15))
            
            


    t_ons=[x*1./frameRate for x in t_ons]
    
    return t_ons

    
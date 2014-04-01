'''
Created on Apr 1, 2014

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


def peakcwt(features,opt):
    
    frameRate = opt['sampleRate']*1./opt['hopSize']
    t_ons=[]
    
    if any(isinstance(el, list) for el in features):
        t_ons = []
        for l in features:
            t_ons += signal.find_peaks_cwt(l,np.arange(1,105))

    else:
        t_ons = signal.find_peaks_cwt(features,np.arange(1,105))
            
            


    t_ons=[x*1./frameRate for x in t_ons]
    
    return t_ons

    
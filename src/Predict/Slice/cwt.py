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



opt = {"rmin":1,
       "rmax":15}

opt_ranges = {"rmin":[1,4],
              "rmax":[10,20]}

name = "peak_cwt"

def compute(features,optc):
    global opt
    
    frameRate = optc['sampleRate']*1./optc['hopSize']
    t_ons=[]
     
    if any(isinstance(el, list) for el in features) or (isinstance(features,np.ndarray) and features.shape[1]>1):
        t_ons = []
        for l in features:
            t_ons += signal.find_peaks_cwt(l,np.arange(opt["rmin"],opt["rmax"]))

    else:
        t_ons = signal.find_peaks_cwt(features,np.arange(opt["rmin"],opt["rmax"]))
            
            


    t_ons=[x*1./frameRate for x in t_ons]
    
    return t_ons

    
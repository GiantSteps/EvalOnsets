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

    


if __name__ == "__main__":
    curdic = {'sampleRate':10,'hopSize':10}
    tstarr = np.array([[2,3,4],[5,6,7]])
    peakcwt(tstarr,curdic)
 
    
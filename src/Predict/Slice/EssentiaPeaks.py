'''
Created on Mar 28, 2014

@author: mhermant
'''



import essentia
import numpy as np
from essentia.standard import *
import conf

opts={"name":"EssentiaPeaks",
      "alpha":.2,
      "silenceThresh":0.05
      
      }
def compute(features,opt):
    frameRate = opt['sampleRate']/opt['hopSize']

        
    delay = int(conf.opts["doubleOnsetT"]/2.*frameRate)
    onsets = Onsets(frameRate = frameRate,alpha=opts["alpha"],delay=delay,silenceThreshold=opts["silenceThresh"])
    if isinstance(features[0],list) or isinstance(features[0],np.ndarray):
        weights =  essentia.array([1 for x in range(len(features))])
        time_onsets = list(onsets(essentia.array(features),weights))
    else:
        time_onsets = list(onsets(essentia.array([features]),essentia.array([1])))

    return time_onsets






 
    
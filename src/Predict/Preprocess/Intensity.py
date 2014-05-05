'''
Created on Apr 2, 2014

@author: mhermant
'''
import numpy as np
# import Utils.Configurable as confM

# confM.getNamespace("att")

opts = {"name" : "Intensity",
        "normalize" :0,
        "att":0}
opts_r = {"at":[0,5,1]}




def compute(audio):
    """
    normalize / attenuate signal by "att"(dB)
    """
    if opts["normalize"]:
        audio = audio / np.max(audio)
    
    if opts["att"]:
        att = np.power(np.sqrt(10.), opts['att'] / 10.)
        audio = np.asarray(audio / att, dtype=audio.dtype)
    
    return audio

'''
Created on Mar 27, 2014

@author: mhermant
'''

from essentia import *
from essentia.standard import *

from Eval.Distance import *
from fileMgmt import *
from Predict.OnsetNovelty.OnsetEssentia import *
from Slice import Slice as sl
import matplotlib.pyplot as plt

comonOpt = {
            "sampleRate":44100,
            "frameSize":512,
            "hopSize":512,
            "zeroPadding":0,
            "windowType":"hann"
            }


def removeDoubles(time_onsets,threshold=0.08):
    t = 1
    time_onsets = sorted(time_onsets)
    while t < len(time_onsets):
        if time_onsets[t] - time_onsets[t-1] < threshold: time_onsets.pop(t)
        else: t += 1
        
def compute(path):
#     pool = fileMgmt.pool
    loader = MonoLoader(filename=path)
    audio = loader()
        
        
    novelty = computeEss(audio,comonOpt)
        
    if any(isinstance(el, list) for el in novelty):           
        num=0
        for l in novelty: 
            pool.set("novelty."+str(num),l)
                
            num+=1
    else:
        pool.set("novelty.0",essentia.array(novelty))
            
        
        
    t_ons = sl.onsetEss(novelty,comonOpt)
        
        
        
    removeDoubles(t_ons)
            
    pool.setEvt("pred",essentia.array(t_ons))
        

def computeAll():
    fns = crawlfn()
    
    for fn in fns:
        path = fns[fn]
        
        pool.setPool(fn,comonOpt)
        compute(path)
    print "---------endcomputation--------"
    

if __name__=="__main__":
    computeAll()
    pool.writePool()
    pool.writePred()
    


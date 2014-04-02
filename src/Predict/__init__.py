'''
Created on Mar 27, 2014

@author: mhermant
'''

from essentia import *
from essentia.standard import *



import Predict.OnsetNovelty as oN
import Predict.Slice as sl
from Utils.fileMgmt import *
import matplotlib.pyplot as plt

import conf


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
        
        
    novelty = oN.compute(audio,conf.comonOpt)
        
    if any(isinstance(el, list) for el in novelty):           
        num=0
        for l in novelty: 
            pool.set("novelty."+str(num),l)
            num+=1
    else:
        pool.set("novelty.0",essentia.array(novelty))
            
        
        
    t_ons = sl.compute(novelty,conf.comonOpt)
        
        
        
    removeDoubles(t_ons)
            
    pool.setEvt("pred",essentia.array(t_ons))
        

def computeAll():
    fns = crawlpaths()
    
    for fn in fns:
        path = fns[fn]
        if conf.fromFile or ( conf.skipComputed and isInPool(fn) ):
    #         pred = getonsets(Path.ODBPredicted+fn+".txt")
            print "reading from pool for" + fn
            pool.readPool(fn)
        else:
            pool.setPool(fn,conf.comonOpt)
            compute(path)
            pred = pool.getn("pred")
            pool.writePool()
            pool.writePred()
            
    print "---------endcomputation--------"
    

if __name__=="__main__":
    computeAll()
    pool.writePool()
    pool.writePred()
    


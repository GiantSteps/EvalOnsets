'''
Created on Mar 27, 2014

@author: mhermant
'''

from essentia import *
from essentia.standard import *


import Predict.Preprocess as pp
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
    print path
    #SuperFlux wants to use scipy for its audio, let it
    if 'SELF_AUDIO' in dir(oN.curalgo):
        audio = path
    else:
        loader = MonoLoader(filename=path)
        audio = loader()
        
        
        
    novelty = oN.compute(audio,conf.opts)
        
    if len(novelty) and (isinstance(novelty[0], list) or isinstance(novelty[0],np.ndarray)):           
        num=0
        for l in novelty: 
            pool.set("novelty."+str(num),essentia.array(l))
            num+=1
    else:
        pool.set("novelty.0",essentia.array(novelty))
            
        
        
    t_ons = sl.compute(novelty,conf.opts)
        
        
        
    removeDoubles(t_ons)
            
    pool.setEvt("pred",essentia.array(t_ons))
        

def computeAll():
    fns = crawlpaths()
    confM.saveconf(conf.ODBStats+"/config.conf") 
    for fn in fns:
        
        path = fns[fn]
        if conf.fromFile or ( conf.skipComputed and isInPool(fn) ):
    #         pred = getonsets(Path.ODBPredicted+fn+".txt")
            print "reading from pool for" + fn
            pool.readPool(fn)
        else:
            pool.setPool(fn,conf.opts)
            compute(path)
            pred = pool.getn("pred")
            pool.writePool()
            pool.writePred()
    
    print "---------endcomputation--------"
    

if __name__=="__main__":
    import sys
    import cStringIO
    import argparse
    #import Utils
    import Utils.Configurable as confM
    # define parser
#     p = argparse.ArgumentParser(
#         formatter_class=argparse.RawDescriptionHelpFormatter, description="")
#     p.add_argument('-t', dest='nodebug', action='store_true', default=False,
#                    help='active console output')
#     p.add_argument('-conf')
#     args = p.parse_args()
#     
#     if args.conf:
#         print args.conf
#         conf.opts["configName"]=args.conf
#     if args.nodebug:
#         sys.stdout = cStringIO.StringIO()
    
    conf.initconf()
    
    Utils.fileMgmt.init()
    
    confM.linkparams(conf)
    
    pp.registerparams()
    confM.linkparams(oN.curalgo)
    confM.linkparams(sl.curalgo)
    
    print confM.params.descriptorNames()
    computeAll()

    


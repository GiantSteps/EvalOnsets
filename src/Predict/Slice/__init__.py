

import cwt
import EssentiaOnsets
import SuperFluxPeaks
import conf


curalgo = globals()[conf.opts["SliceName"]]#cwt

def compute(features,opt):
    global curalgo
    return curalgo.compute(features, opt)

def getName():
    return curalgo.name

def getOptions():
    return curalgo.opt



if __name__ == "__main__":
    
    import numpy as np
    
    curdic = {'sampleRate':10,'hopSize':10}
    tstarr = np.array([[2,3,4],[5,6,7]])
    print curalgo.compute(tstarr,curdic)
#     EssentiaOnsets.compute(tstarr, curdic)
    
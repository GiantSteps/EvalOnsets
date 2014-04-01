

import cwt
import EssentiaOnsets


curalgo = cwt

def compute(features,opt):
    global curalgo
    return curalgo.compute(features, opt)

def getName():
    return curalgo.name

def getOptions():
    return curalgo.opt



if __name__ == "__main__":
    
    import numpy as np
    curalgo2 = cwt
    curdic = {'sampleRate':10,'hopSize':10}
    tstarr = np.array([[2,3,4],[5,6,7]])
    curalgo2.compute(tstarr,curdic)
    EssentiaOnsets.compute(tstarr, curdic)
    
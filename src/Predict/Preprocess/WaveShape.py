'''
Created on Apr 2, 2014

@author: mhermant

compresser expander 

-> linear symetric waveshaper with one control point


        |        ____
gain    |     x
        |   /
        | /
        _____________
              |
            threshold

'''
import numpy as np

import essentia.standard
opts = {"name" : "WaveShape",
        "type":"cube",
        "thresh" : 0.25,
        "gain":.15
        
        }



opts_r = {"thresh":[0,5,1],"ratio":[.0,2,0.25],}




def compute(audio):
    """
    compress/expand
    """
    #audio = np.array([np.copysign(opts['thresh'] + (abs(x)-opts['thresh'])*opts['ratio'],x)  if abs(x)>opts['thresh'] else x for x in audio ])
    
    if opts["type"]=="cube":
        return cube(audio)
    else:
        return bpf(audio)


def bpf(audio):
    gain1 = opts["gain"]/opts["thresh"]
    gain2 = (1-opts["gain"])/(1-opts["thresh"])
    audio = np.array([ np.copysign(opts['gain'] + (abs(x)-opts['thresh'])*gain2,x)  if abs(x)>opts['thresh'] 
                      else  np.copysign(abs(x)*gain1,x) 
                      for x in audio ])
    
    return audio
    
def cube(audio):
    f  = essentia.standard.UnaryOperator(type="cube")
    audio = f(essentia.array(audio))
    return audio

def test():
    import time
    
    a=np.linspace(-1,1,num=1000000)
    print a
    t= time.clock()
    a1 = compute(a)
    print time.clock()-t
    t= time.clock()
    global opts
    opts["type"]=""
    a2=compute(a)
    print time.clock()-t
    return a1-a2


if __name__=="__main__":

    print np.mean(test())


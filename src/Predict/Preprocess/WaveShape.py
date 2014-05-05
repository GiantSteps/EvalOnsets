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

from essentia.standard import *
import essentia
opts = {"name" : "WaveShape",
        
        "LUTx"   :[0,.2,.4,.5,.9,1],
        "LUTy"   :[0,.1,.3,.5,.8,1],
        
        "normalize":0,
        "spline":1
        
        }



opts_r = {"thresh":[0,5,1],"ratio":[.0,2,0.25],}




def compute(audio):
    """
    compress/expand
    """
    f = waveshaper(xPoints=essentia.array(opts["LUTx"]),
                   yPoints=essentia.array(opts["LUTy"]),
                   normalize = True if opts["normalize"] else False,
                   spline = True if opts["spline"] else False,
                       )
    
    audio = f(essentia.array(audio))
    return audio
        
#audio = np.array([np.copysign(opts['thresh'] + (abs(x)-opts['thresh'])*opts['ratio'],x)  if abs(x)>opts['thresh'] else x for x in audio ])
    
    
    
#     if opts["type"]=="cube":
#         return cube(audio)
#     else:
#         return bpf(audio)


# def bpf(audio):
#     gain1 = opts["gain"]/opts["thresh"]
#     gain2 = (1-opts["gain"])/(1-opts["thresh"])
#     audio = np.array([ np.copysign(opts['gain'] + (abs(x)-opts['thresh'])*gain2,x)  if abs(x)>opts['thresh'] 
#                       else  np.copysign(abs(x)*gain1,x) 
#                       for x in audio ])
#     
#     return audio
#     
# def cube(audio):
#     f  = essentia.standard.UnaryOperator(type="cube")
#     audio = f(essentia.array(audio))
#     return audio

def test():
    import time
    import matplotlib.pyplot as plt
    a=np.linspace(-1.5,1.5,num=1000000)

    t= time.clock()
    a1 = compute(a)
    plt.plot(a)
    plt.plot(a1)
    plt.show()
    print time.clock()-t
    return a1


if __name__=="__main__":

    print test()


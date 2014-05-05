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
        
        "p1x" : 0,
        "p1y" : 0,
        "p2x" : 0.25,
        "p2y" : 0,
        "p3x" : 0.8,
        "p3y" : 0.8,
        "p4x" : 1,
        "p4y" : 1,
        "normalize":True,
        
        
        }



opts_r = {"thresh":[0,5,1],"ratio":[.0,2,0.25],}




def compute(audio):
    """
    compress/expand
    """
    f = waveshaper(p1x=opts["p1x"],
                       p1y=opts["p1y"],
                       p2x=opts["p2x"],
                       p2y=opts["p2y"],
                       p3x=opts["p3x"],
                       p3y=opts["p3y"],
                       p4x=opts["p4x"],
                       p4y=opts["p4y"],
                       normalize = opts["normalize"]
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
    
    a=np.linspace(-1.5,1.5,num=1000000)
    print a
    t= time.clock()
    a1 = compute(a)
    print time.clock()-t
    t= time.clock()
    global opts
    opts["type"]=""
    a2=compute(a)
    print time.clock()-t
    return a1


if __name__=="__main__":

    print test()


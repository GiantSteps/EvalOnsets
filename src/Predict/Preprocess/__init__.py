
from Predict.Preprocess import Intensity, WaveShape
from Predict.Preprocess import anHarmonic

import conf


opts={
      'name' : "preprocess",
      'algo' : dict((an,globals()[an].opts)for an in conf.opts['preprocess'])
      }


def initopts():
    opts['algo'] = dict((an,globals()[an].opts)for an in conf.opts['preprocess'])

def loadFromConf():
    for a in opts['algo']:
        return 0
#         globals()[a].opts = confM
        
    
def compute(audio):
    
    import time
    
    curt = time.clock()
    for a in opts['algo']:
        alg = globals()[a]
        audio = alg.compute(audio)
    
    print time.clock() - curt
    
    return audio
    

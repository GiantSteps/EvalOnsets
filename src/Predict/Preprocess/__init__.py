
from Predict.Preprocess import Intensity
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
    for a in opts['algo']:
        alg = globals()[a]
        audio = alg.compute(audio)
    return audio


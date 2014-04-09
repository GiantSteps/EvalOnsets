
from Predict.Preprocess import Intensity
import conf
import Utils.Configurable as confM

opts={
      'name' : "preprocess",
      'algo' : dict((an,globals()[an].opts)for an in conf.opts['preprocess'])
      }


def initopts():
    opts['algo'] = dict((an,globals()[an].opts)for an in conf.opts['preprocess'])

def loadFromConf():
    for a in opts['algo']:
        globals()[a].opts = confM
        

def compute(audio):
    for a in opts['algo']:
        alg = globals()[a]
        alg.compute(audio)


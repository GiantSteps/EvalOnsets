
from Predict.Preprocess import Intensity
import conf
import Utils.Configurable as confM

opts={
      'algo' : conf.opts['preprocess']
      }


def compute(audio):
    for a in opts['algo']:
        alg = globals()[a]
        alg.compute(audio)

def registerparams():
    for a in opts['algo']:
        confM.linkparams(globals()[a])
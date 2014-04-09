import Predict.Preprocess as pp
import Predict.OnsetNovelty as oN
import Predict.Slice as sL


import conf
import Utils
from Utils.fileMgmt import *
import Utils.Configurable as confM
from essentia.standard import  *

from essentia import *

def execute(conf):
    return 0
    
    
def loadConf(fn):
    pool = Pool()
    pool = YamlInput(filename=fn)()
    desc = [x.split('.')[0] for x in pool.descriptorNames()]
    entities = set(desc)
    entities.remove('metadata')
    entities.remove('globalSettings')
    glob = getNameSpace(pool,'globalSettings',False)
    conf.opts = glob
    conf.initconf()
    
    Utils.fileMgmt.init()
    
    oN.loadFromConf()
    sL.loadFromConf()
    
    
    confM.linkparams(conf)
    confM.linkparams(pp)
    confM.linkparams(oN.curalgo)
    confM.linkparams(sL.curalgo)
    print glob
    for x in entities:
        
        
    
    return pool


def saveConf():
    return 0



if __name__ == "__main__":
    loadConf(conf.ODBStats+"config.conf")
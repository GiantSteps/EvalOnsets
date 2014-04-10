'''
warper for onset novelty functions
an onset novelty function has to return a list of novelty functions

'''


import essOnsetFunc
import Nsdf
import SuperFluxOnsets
import conf
import ModalOnsets
# import Utils.Configurable as confM

curalgo = globals()[conf.opts["NoveltyName"]]#essOnsetFunc

def loadFromConf():
    global curalgo
    curalgo = globals()[conf.opts["NoveltyName"]]#essOnsetFunc
#     curalgo.opts = confM.getNamespace(conf.opts["NoveltyName"])



def compute(audio):
    
    global curalgo
    
    return curalgo.compute(audio)



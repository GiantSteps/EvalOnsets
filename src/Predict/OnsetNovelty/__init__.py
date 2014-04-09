'''
warper for onset novelty functions
an onset novelty function has to return a list of novelty functions

'''


import essOnsetFunc
import Nsdf
import SuperFluxOnsets
import conf
import Utils.Configurable as confM



curalgo = globals()[conf.opts["NoveltyName"]]#essOnsetFunc




def compute(audio,opt):
    
    global curalgo
    
    return curalgo.compute(audio, opt)



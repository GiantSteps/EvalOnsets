'''
warper for onset novelty functions
an onset novelty function has to return a list of novelty functions

'''


import essOnsetFunc
import Nsdf
import SuperFluxOnsets
import conf

curalgo = globals()[conf.NoveltyName]#essOnsetFunc



def compute(audio,opt):
    
    global curalgo
    return curalgo.compute(audio, opt)
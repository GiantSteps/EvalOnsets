'''
Created on Mar 27, 2014

@author: mhermant
'''
# import essentia
import essentia.extractor.onsetdetection as extron
# import essentia.essentia_extractor



def essOnset(audio,comonopt):
#     pool  = essentia.Pool()
    pool=0
    extron.compute(audio,pool,comonopt)
    return pool["rythm.onset_times"]
    
    
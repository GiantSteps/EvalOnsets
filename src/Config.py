'''
Created on Apr 1, 2014

@author: mhermant
'''

'''
path for 
- sound files
- ground truth (read only)
- essentia pool cache
- onset text files prediction to write out
'''


ODBMedias = '/Users/mhermant/Documents/Work/Datasets/ODB/sounds'
ODBgroundtruth = '/Users/mhermant/Documents/Work/Datasets/ODB/ground-truth'
ODBPool =  '/Users/mhermant/Documents/Work/Datasets/ODB/pool'
ODBPredicted = ODBPool+'/predicted'



'''
Option for Onset Prediction
'''

comonOpt = {
                "sampleRate":44100,
                "frameSize":512,
                "hopSize":512,
                "zeroPadding":0,
                "windowType":"hann"
                }


'''
specific options
'''


fromFile = False;
isPlot = False;
onlyOne = False;
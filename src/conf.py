'''
Created on Apr 1, 2014

@author: mhermant
'''

import os

'''
specific options
'''


fromFile = False;
skipComputed = False;
isPlot = False;
onlyNRandomFiles = 0;

'''
file Options

Take care that Giants steps repo is mounted!
choose the data sets directories you want


'''


ODBdirs = {"name":"ODB",
           "medias":"ODB/sounds/",
          "gt":"ODB/ground-truth/"
          }

JKUdirs = {"name":"JKU",
           "medias":"jku/onsets/audio/",
           "gt":"jku/onsets/annotations/onsets/"}

'''
config for dataset used and user defined name of configuration 
'''
# curdirectories = ODBdirs
curdirectories = JKUdirs
configName = "_default"

NoveltyName= "Nsdf"
SliceName = "EssentiaOnsets"



dir = os.path.dirname(__file__)
PathToLocal = os.path.realpath('../cache/')#os.path.join(dir, '../cache')
PathToLocal+='/'
# print PathToLocal



# PathToLocal = '/Users/mhermant/Documents/Work/Datasets/ODB/'
PathToData = '/Volumes/GiantSteps-Share/datasets/'
# PathToData = PathToLocal


'''
path for 
- sound files
- ground truth (read only)
- essentia pool cache
- onset text files prediction to write out
'''
ODBMedias = PathToData+curdirectories["medias"]
ODBgroundtruth = PathToData+curdirectories["gt"]
ODBPool =  PathToLocal+curdirectories["name"]+"/"+configName+"/pool/"
ODBPredicted = PathToLocal+curdirectories["name"]+"/"+configName+'/predicted/'
ODBStats = PathToLocal+curdirectories["name"]+"/"+configName+'/stats/'



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




onsetsufix = ['.txt','.onsets','.onset']


'''
create cache folders
'''
if not os.path.exists(ODBPool):
    os.makedirs(ODBPool)
if not os.path.exists(ODBPredicted):
    os.makedirs(ODBPredicted) 
if not os.path.exists(ODBStats):
    os.makedirs(ODBStats)
    

def initconf():
    global ODBMedias,ODBPool,ODBgroundtruth,ODBPredicted,ODBStats
    ODBMedias = PathToData+curdirectories["medias"]
    ODBgroundtruth = PathToData+curdirectories["gt"]
    ODBPool =  PathToLocal+curdirectories["name"]+configName+"/pool/"
    ODBPredicted = PathToLocal+curdirectories["name"]+configName+'/predicted/'
    ODBStats = PathToLocal+curdirectories["name"]+configName+'/stats/'
    
    if not os.path.exists(ODBPool):
        os.makedirs(ODBPool)
    if not os.path.exists(ODBPredicted):
        os.makedirs(ODBPredicted) 
    if not os.path.exists(ODBStats):
        os.makedirs(ODBStats)
    
    
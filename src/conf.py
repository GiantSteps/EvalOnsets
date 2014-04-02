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
config for dataset used and user defined name of configuration 

Option for Onset Prediction

merged into one dict for configuration management
'''

opts = {   "name":"globalSettings",
                # curdirectories = ODBdirs
                "curdirectories" : "JKU",
                "configName" : "_default",

                "NoveltyName": "Nsdf",
                "SliceName" : "EssentiaOnsets",

                "sampleRate":44100,
                "frameSize":512,
                "hopSize":512,
                "zeroPadding":0,
                "windowType":"hann"
                }
'''
file Options

Take care that Giants steps repo is mounted!
choose the data sets directories you want


'''


dirlist = {
               "ODB":{
                      "medias":"ODB/sounds/",
                      "gt":"ODB/ground-truth/"
                      },
           
                "JKU":{
                       "medias":"jku/onsets/audio/",
                       "gt":"jku/onsets/annotations/onsets/"
                       }
           
           }





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
ODBMedias = PathToData+dirlist[opts['curdirectories']]["medias"]
ODBgroundtruth = PathToData+dirlist[opts['curdirectories']]["gt"]
ODBPool =  PathToLocal+opts['curdirectories']+"/"+opts['configName']+"/pool/"
ODBPredicted = PathToLocal+opts['curdirectories']+"/"+opts['configName']+'/predicted/'
ODBStats = PathToLocal+opts['curdirectories']+"/"+opts['configName']+'/stats/'








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
 
 
 
def updateconf():
     confM.update(opts)
    

def initconf():
    import Utils.Configurable as confM
    confM.linkparams(globals())
    
    
    
    global ODBMedias,ODBPool,ODBgroundtruth,ODBPredicted,ODBStats
    ODBMedias = PathToData+dirlist[opts['curdirectories']]["medias"]
    ODBgroundtruth = PathToData+dirlist[opts['curdirectories']]["gt"]
    ODBPool =  PathToLocal+dirlist[opts['curdirectories']]["name"]+opts['configName']+"/pool/"
    ODBPredicted = PathToLocal+dirlist[opts['curdirectories']]["name"]+opts['configName']+'/predicted/'
    ODBStats = PathToLocal+dirlist[opts['curdirectories']]["name"]+opts['configName']+'/stats/'
    
    if not os.path.exists(ODBPool):
        os.makedirs(ODBPool)
    if not os.path.exists(ODBPredicted):
        os.makedirs(ODBPredicted) 
    if not os.path.exists(ODBStats):
        os.makedirs(ODBStats)
    
    
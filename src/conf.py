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
isPlot = True;
onlyNRandomFiles = 1;


'''
config for dataset used and user defined name of configuration 

Option for Onset Prediction

merged into one dict for configuration management
'''

opts = {   "name":"globalSettings",
                # curdataset = ODBdirs
                'preprocess' : ["Intensity"],
                "curdataset" : "JKU",
                "configName" : "_default",

                "NoveltyName": "essOnsetFunc",
                "SliceName" : "EssentiaPeaks",

                "sampleRate":44100,
                "frameSize":512,
                "hopSize":512,
                "zeroPadding":0,
                "windowType":"hann",
                
                "doubleOnsetT" : 0.8
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
PathToLocal = ''.join(dir.split('/src')[:-1])+'/cache/'

# print PathToLocal



#PathToData = '/Users/mhermant/Documents/Work/Datasets/'
PathToData = '/Volumes/GiantSteps-Share/datasets/'
# PathToData = PathToLocal


'''
path for 
- sound files
- ground truth (read only)
- essentia pool cache
- onset text files prediction to write out
'''
ODBMedias = PathToData+dirlist[opts['curdataset']]["medias"]
ODBgroundtruth = PathToData+dirlist[opts['curdataset']]["gt"]
ODBPool =  PathToLocal+opts['curdataset']+"/"+opts['configName']+"/pool/"
ODBPredicted = PathToLocal+opts['curdataset']+"/"+opts['configName']+'/predicted/'
ODBStats = PathToLocal+opts['curdataset']+"/"+opts['configName']+'/stats/'








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
    
    
    
    
    
    global ODBMedias,ODBPool,ODBgroundtruth,ODBPredicted,ODBStats
    ODBMedias = PathToData+dirlist[opts['curdataset']]["medias"]
    ODBgroundtruth = PathToData+dirlist[opts['curdataset']]["gt"]
    ODBPool =  PathToLocal+opts['curdataset']+"/"+opts['configName']+"/pool/"
    ODBPredicted = PathToLocal+opts['curdataset']+"/"+opts['configName']+'/predicted/'
    ODBStats = PathToLocal+opts['curdataset']+"/"+opts['configName']+'/stats/'
    
    print ODBPredicted
    if not os.path.exists(ODBPool):
        os.makedirs(ODBPool)
    if not os.path.exists(ODBPredicted):
        os.makedirs(ODBPredicted) 
    if not os.path.exists(ODBStats):
        os.makedirs(ODBStats)
    
initconf()
    

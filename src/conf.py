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
onlyNRandomFiles = 4;


'''
config for dataset used and user defined name of configuration 

Option for Onset Prediction

merged into one dict for configuration management
'''

'''
Set the root path for your dataset here
'''

#Carthach
PathToData = '/Users/carthach/GiantSteps-Share/datasets/'

#Martin
PathToData = '/Users/mhermant/Documents/Work/Datasets/'

PathToData = '/Volumes/GiantSteps-Share/datasets/'
# PathToData = PathToLocal

opts = {   "name":"globalSettings",
                # curdataset = ODBdirs
                'preprocess' : ["Intensity"],
                "curdataset" : "JKU",
                "configName" : "_default",

                "NoveltyName": "SuperFluxOnsets",
                "SliceName" : "EssentiaPeaks",

                "sampleRate":44100,
                "frameSize":512,
                "hopSize":512,
                "zeroPadding":0,
                "windowType":"hann",
                
                "doubleOnsetT" : 0.1
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

               "ENST-1":{
                      "medias":"ENST/drummer_1/audio",
                      "gt":"ENST/drummer_1/annotation"
                      },

               "ENST-2":{
                      "medias":"ENST/drummer_2/audio",
                      "gt":"ENST/drummer_2/annotation"
                      },

               "ENST-3":{
                      "medias":"ENST/drummer_3/audio",
                      "gt":"ENST/drummer_3/annotation"
                      },                                 
           
                "JKU":{
                       "medias":"jku/onsets/audio/flac/",
                       "gt":"jku/onsets/annotations/onsets/"
                       },
           
                "Leveau":{
                       "medias":"Leveau/audio/",
                       "gt":"Leveau/annotations/"
                       },
           
                "Modal":{
                       "medias":"Modal/audio/",
                       "gt":"Modal/annotations/"
                       },
                      
           }



dir = os.path.dirname(__file__)
PathToLocal = ''.join(dir.split('/src')[:-1])+'/cache/'
# print PathToLocal





########DEFAULT INSTANCE STUFF########
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

MARTIN - this is a dupe of initconf no? Should delete...
'''

if not os.path.exists(ODBPool):
    os.makedirs(ODBPool)
if not os.path.exists(ODBPredicted):
    os.makedirs(ODBPredicted) 
if not os.path.exists(ODBStats):
    os.makedirs(ODBStats)
    
################
 

    
#This sets all the paths
def initconf():    
    global ODBMedias,ODBPool,ODBgroundtruth,ODBPredicted,ODBStats
    
    #Check if the dataset paths exist and report otherwise
    if os.path.exists(PathToData+dirlist[opts['curdataset']]["medias"]):
        ODBMedias = PathToData+dirlist[opts['curdataset']]["medias"]
    else:
        print "WARNING: Dataset audio path doesn't exist"
    if os.path.exists(PathToData+dirlist[opts['curdataset']]["gt"]):
        ODBgroundtruth = PathToData+dirlist[opts['curdataset']]["gt"]
    else:
        print "WARNING: Dataset ground truth path doesn't exist"
        
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

def loadDict(d):
    opts = d
    initconf()
#When this is imported run the initconf method to set the variables    
initconf()



import os
# trick to import modules when launching from command line
if __name__ == "__main__":
    import sys, inspect
    dir = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    PathToLocal = ''.join(dir.split('/src')[:-1])+'/src/'

    sys.path.insert(0, PathToLocal)
    




import Predict
import Eval
# 
# 
import conf
# import Utils
# from Utils.fileMgmt import *
import Utils.Configurable as confM
from essentia.standard import  *

from essentia import *



    
    #for x in entities:
        



             
            

def execute(fn):
    confM.loadconf(fn)
    conf.isPlot=False
    Predict.main();
    Eval.main()
    
    
    return 0


def batch(fn):
    import subprocess
    import os
    import time
    
    processes = set()
    max_processes = 5

        
    dir = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))+"/__init__.py"
#     print dir
    
    for (dirpath, dirnames, filenames) in os.walk(fn):
        confs = [dirpath+x for x in filenames if '.conf' in x]
        for n in confs:
            processes.add(subprocess.Popen(['python',dir, '-fi',n]))
        if len(processes) >= max_processes:
            os.wait()
            processes.difference_update([
                p for p in processes if p.poll() is not None])
            
        break 
#         


if __name__ == "__main__":

    
#     import argparse

        
        
        
    

    import argparse
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
    process onset Detections following a given configuration file or folder
 
    """)
    

     
    p.add_argument('-fi', dest='filename', action='store',default='',
               help='filename ')
    p.add_argument('-fo', dest='folder', action='store',default='',
               help='foldername ')
    
     
    args = p.parse_args()

    if args.filename : 
        execute(args.filename)
    else :
        if not args.folder:
            args.folder = conf.ODBStats
        batch(args.folder)

    
        
# 
#     
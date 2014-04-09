# import Predict.Preprocess as pp
# import Predict.OnsetNovelty as oN
# import Predict.Slice as sL
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
        


# def generateConfBatch(conf,range,var):
#     confM.loadconf(conf)
#     confM.loadconfrange(range)
#     batchname = ''
#     print
#     if var in confM.ranges.descriptorNames():
#         return 0
#             
            

def execute(fn):
    confM.loadconf(fn)
    Predict.main();
    Eval.main()
    
    
    return 0
    




if __name__ == "__main__":
    import argparse
    
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
    process onset Detections following a given configuration file

    """)

    execute(conf.ODBStats+"config.conf")
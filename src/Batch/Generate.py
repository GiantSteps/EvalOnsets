import Predict
import Eval
# 
# 
import conf

import Utils.Configurable as confM



'''
Helper to generate multple conf file to be reqd by __init.py__
'''


def generateConfBatch(confin='',range='',var=[''],output = ''):
    if not output : 
        output = conf.PathToLocal+'/Batch'
    if confin : 
        confM.loadconf(confin)
        
    
    
    
    confM.loadconfrange(range)
    batchname = ''
    
    print
    if var in confM.ranges.descriptorNames():
        return 0
    
    
if __name__=="__main__":
    
    
    generateConfBatch
    
    
    return 0

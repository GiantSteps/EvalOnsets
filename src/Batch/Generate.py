import Predict
import Eval
import os
import conf

import Utils.Configurable as confM
import numpy as np


'''
Helper to generate multple conf file to be reqd by __init.py__
'''

# TODO: multi dimensionnal grid generation
def generateConfBatch(var={},name='default',output = '',confin=''):
    if not output : 
        output = conf.PathToLocal+'Batch'
    if confin : 
        confM.loadconf(confin)
    else :
        confM.crawlParams()
    
    output+="/"+name+"/"
    if not os.path.exists(output):
        os.makedirs(output)     
    
    print confM.params.descriptorNames()
    for n,v in var.iteritems():
        if n in confM.params.descriptorNames():
            init = confM.params[n]
            for val in v:
                curname =str(n)+str(val)
                confM.params.set(n,val)
                confM.params.set("globalSettings.configName",curname)
                confM.saveconf(output+curname+".conf")
                print "write conf :" +output+curname+".conf"
            confM.params.set(n,init)
    
    
if __name__=="__main__":

    
    var   = {'globalSettings.sampleRate':[44100,22050]}
    generateConfBatch(var)
    
    
    

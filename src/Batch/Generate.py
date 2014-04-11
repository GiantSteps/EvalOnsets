import Predict
import Eval
import os
import conf
import itertools as it
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
    
    varNames = sorted(var)
    combinations = [dict(zip(varNames, prod)) for prod in it.product(*(var[varName] for varName in varNames))]
    
    if any(v not in confM.params.descriptorNames() for v in var.iterkeys()): return 0
    
    init = confM.getDict(var)
    for curd in combinations:
        curname =dictToStr(curd)
        confM.setDict(curd)
        confM.params.set("globalSettings.configName",curname)
        confM.saveconf(output+curname+".conf")
        print "write conf :" +output+curname+".conf"
    
    confM.setDict(init)
    

def dictToStr(d):
    res = ''
    for n,v in d.iteritems():
        res+= str(n.split('.')[-1])+'.'+str(v)+'_'
    res = res[:-1]
    return res
 
if __name__=="__main__":

    
    var   = {'globalSettings.NoveltyName':['SuperFluxOnsets','essOnsetFunc','ModalOnsets'],'globalSettings.SliceName':['EssentiaPeaks','SuperFluxPeaks','ModalPeaks'], 'globalSettings.frameSize':[512,1024,2056]}
    
    generateConfBatch(var,'tst')
    
    
    

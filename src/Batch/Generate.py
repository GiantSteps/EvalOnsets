import Predict
import Eval
import os
import conf
import itertools as it
import Utils.Configurable as confM
import numpy as np
from numpy.core.defchararray import startswith


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
    
    f = open(output+"generated.txt",'w')
    f.write(str(var))
    f.close()
    
    varNames = sorted(var)
    
    
    combinations = [dict(zip(varNames, prod)) for prod in it.product(*(var[varName] for varName in varNames))]
    
    
#     presumedmod  = {}
#     for k,v in var.iteritems():
#         if isinstance(v,list):
#             for y in v:
#                 if isinstance(y,str):
#                     presumedmod[k]=v
#     for co in it.product(*(presumedmod[n] for n in presumedmod)):
#         print dict(zip(presumedmod, co))
#     #combination2 =             
#     for k in combinations:
#         wrong = False
#         for n in presumedmod.iterkeys():
#             wrongkeys = n
#             wrongkeys.remove(k[n])
#             for j in k.iterkeys():
#                 if any(j.startswith(x+'.')for x in wrongkeys):
#                     wrong=True
#                     break
#             if wrong : break
#         
#         if not wrong :
#             #combination2+=[k]    
#     
    if any(v not in confM.params.descriptorNames() for v in var.iterkeys()):
        print 'wrong configuration'
        return 0
    
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

    
    var   = {'globalSettings.NoveltyName':['SuperFluxOnsets','essOnsetFunc'],
             'globalSettings.SliceName':['EssentiaPeaks','SuperFluxPeaks'],
             'globalSettings.curdataset':['JKU'],
             'globalSettings.frameSize':[512,1024,2048],
             
             #'preprocess.algo.FreqMedian.ratio':[0,0.05,0.1],
             
             'preprocess.algo.WaveShape.pts':[.1,.2,.3],
             'preprocess.algo.WaveShape.thresh':[.01,.1,.2]
             }
    
    #var   = {'globalSettings.NoveltyName':['SuperFluxOnsets','globalSettings.SliceName':['EssentiaPeaks','SuperFluxPeaks','ModalPeaks'], 'globalSettings.frameSize':[512,1024,2048]}
    generateConfBatch(var,'JKU.')
    
    
    

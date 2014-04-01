'''
Created on Mar 27, 2014

@author: mhermant
'''
from essentia import *
from essentia.standard import *

from Eval.Distance import *

from fileMgmt import *

import Predict
import time

import os

fromFile = False;
isPlot = False;
onlyOne = False;


exectime = time.clock()
print exectime




fns = crawlfn()
gt = crawlgt()
meas=[]
for fn in fns:
    path = fns[fn]
    if fromFile:
#         pred = getonsets(Path.ODBPredicted+"/"+fn+".txt")
        pool.readPool(fn)
    else:
        pool.setPool(fn,Predict.comonOpt)
        Predict.compute(path)
        pred = pool.getn("pred")
        pool.writePool()
        pool.writePred()
    
    print  pool.pool.descriptorNames()
    pred = pool.getn("pred")
    plt.subplot(211)
    
    meas+=[analyze(pred,gt[fn],0.08)]
    plt.title(str(fn)+"/"+str(meas[-1]),loc= 'left')
    if isPlot :
        
        nl =  pool.getNames("novelty")
        print nl
        for n in nl:
            plt.plot([x*1./pool.getn(n,True) for x in range(len(pool.getn(n)))],pool.getn(n))
            
        plt.show()
    

meas = np.array(meas)
print meas
# print np.mean(meas)

print time.clock()-exectime
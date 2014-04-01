'''
Created on Mar 27, 2014

@author: mhermant
'''


from essentia import *
from essentia.standard import *

from Eval.Distance import *
import Predict
from fileMgmt import *











def eval(fn):
    path = fns[fn]
    if conf.fromFile:
#         pred = getonsets(Path.ODBPredicted+"/"+fn+".txt")
        pool.readPool(fn)
    else:
        pool.setPool(fn,conf.comonOpt)
        Predict.compute(path)
        pred = pool.getn("pred")
        pool.writePool()
        pool.writePred()
    
    
    pred = pool.getn("pred")

        
        
    return analyze(pred,gt[fn],0.08)




def plot():
    plt.subplot(211)
    
    
    plt.title(str(fn)+"/"+str(meas[-1]),loc= 'left')
    
        
    nl =  pool.getNames("novelty")
    
    for n in nl:
        plt.plot([x*1./pool.getn(n,True) for x in range(len(pool.getn(n)))],pool.getn(n))
            
    plt.show()
    
    
    
    
    
if __name__ == "__main__":
    import time
    import Config as conf
    
    
    exectime = time.clock()
    
    fns = crawlfn()
    gt = crawlgt()
    meas=[]
    for fn in fns:
        meas+=[eval(fn)]
        if conf.isPlot: plot()
    meas = np.array(meas)
    print meas
    # print np.mean(meas)
    
    print "execution time : "+str(time.clock()-exectime)
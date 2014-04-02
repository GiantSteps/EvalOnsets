'''
Created on Mar 27, 2014

@author: mhermant
'''


from essentia import *
from essentia.standard import *

from Eval.Distance import *
import Predict
from Utils.fileMgmt import *











def eval(fn):


#     pred = pool.getn("pred")
        
    return analyze(fn[0],fn[1],0.08)




def plot():
    plt.subplot(211)
    
    
    plt.title(str(fn)+"/"+str(meas[-1]),loc= 'left')
    
        
    nl =  pool.getNames("novelty")
    
    for n in nl:
        plt.plot([x*1./pool.getn(n,True) for x in range(len(pool.getn(n)))],pool.getn(n))
            
    plt.show()
    
    
    
    
    
if __name__ == "__main__":
    import time
    import conf
    
    
    exectime = time.clock()
    crawlpaths()
    pgts = crawlpgt()

    meas=[]
    for fn in pgts:
        meas+=[eval(pgts[fn])]
        if conf.isPlot: plot()
    writeStats(meas)
    meas = np.array(meas)
    print meas
    # print np.mean(meas)
    
    print "execution time : "+str(time.clock()-exectime)
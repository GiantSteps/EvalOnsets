'''
Created on Mar 27, 2014

@author: mhermant
'''


from essentia import *
from essentia.standard import *

from Eval.Distance import *
import Predict
from Utils.fileMgmt import *











def eval(predGt):


#     pred = pool.getn("pred")
        
    return analyze(predGt[0],predGt[1])




def plot(fn,meas):
    plt.subplot(211)
    
    
    
    if pool.readPool(fn):
        plt.title(pool.poolName+"/"+str({k:round(v,2) if isinstance(v,float) else v for k,v in meas.iteritems()}),loc= 'left')
        nl =  pool.getNames("novelty")
        for n in nl:
            curn = pool.getn(n)
            plt.plot([x*1./pool.getn(n,True) for x in range(len(pool.getn(n)))],pool.getn(n))
    

    plt.tight_layout(pad=0);   
            
    plt.show()
    
    
    
    
def plotstats(meas):
    fields = {}
    for l in meas:
        for f,v in l.iteritems():
            if not f in fields.keys():
                fields[f] = [v]
            else : fields[f]+=[v]
    
    numplots = len(fields)
    i = 1
    for l,v in fields.iteritems():
        
        plt.subplot(numplots,1,i)
        plt.bar(range(len(v)), v, align='center')
        
        plt.xlim((-1,plt.xlim()[1]))
        plt.ylim((0.5,1))
        plt.title(l)
        i+=1
        
    plt.xticks(range(len(v)), curFiles.keys(), size='small',rotation=90)
    plt.tight_layout();
    plt.savefig(conf.ODBStats+"stats.png")
    plt.show()
     
     
     
     
     
     
     
     
     
            
def main():
    
    
    
    import time
    

    

    
    exectime = time.clock()
    
    crawlpaths()
    pgts = crawlpgt()

    meas=[]
    i = 0
    for fn in pgts:
        
        meas+=[eval(pgts[fn])]
        if conf.isPlot: plot(fn,meas[-1])
        i+=1
    writeStats(meas)
    meas = np.array(meas)
    if conf.isPlot: plotstats(meas)
    print meas
    # print np.mean(meas)
    
    print "execution time : "+str(time.clock()-exectime)  
    
    
if __name__ == "__main__":
    import Utils.Configurable
    Utils.Configurable.crawlParams()
    
    main()
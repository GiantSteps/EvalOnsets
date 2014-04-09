from os import walk
import os

from essentia import *
from essentia.standard import *
import random
import numpy as np
import conf



def getonsets(fn):
    f = open(fn, 'r')
    s = f.readline()
    res = []
    
    while s:
        res+=[float(s)]
        s= f.readline()

    return res

    
def crawlgt():
    if curFiles:
        res = dict((x,getGt(x)) for x in curFiles)
    else:
        for (dirpath, dirnames, filenames) in walk(conf.ODBgroundtruth):
            res = dict((os.path.splitext(x)[0],getonsets(dirpath+"/"+x)) for x in filenames if any(x.endswith(y) for y in conf.onsetsufix))
    return res

def getGt(fn):
    curpath = next((conf.ODBgroundtruth+fn+x for x in conf.onsetsufix if os.path.exists(conf.ODBgroundtruth+fn+x)),"")
    if curpath:
        f=open(curpath,'r')
        res= f.readlines()
        res = [float(x) for x in res]
        f.close()
        return res
    else:
        print fn+" not found"
    

def crawlpaths():
    res = []
    for (dirpath, dirnames, filenames) in walk(conf.ODBMedias):
        if conf.onlyNRandomFiles>0:
            filenames2=[]
            for i in range(conf.onlyNRandomFiles):
                cur=random.choice(filenames)
                filenames2+=[cur]
            filenames = filenames2
            
            
        res = dict((os.path.splitext(x)[0],dirpath+x) for x in filenames if any(x.endswith(y) for y in ['.wav','.flac']) )
        
    if not res: 
        print "no file found"
        return

    global curFiles
    curFiles = res
    return res

def crawlpred():
    if curFiles:
        res = dict((x,getPred(x)) for x in curFiles)
    else:
        for (dirpath, dirnames, filenames) in walk(conf.ODBPredicted):
            res = dict((os.path.splitext(x)[0],getonsets(dirpath+"/"+x)) for x in filenames if any(x.endswith(y) for y in conf.onsetsufix))
    return res

def getPred(fn):
    curpath = next((conf.ODBPredicted+fn+x for x in conf.onsetsufix if os.path.exists(conf.ODBPredicted+fn+x)),"")
    if curpath:
        f=open(conf.ODBPredicted+fn+".txt",'r')
        res= f.readlines()
        res = [float(x) for x in res]
        f.close()
        return res
    else:
        print fn+" not found"
    
    
def crawlpgt():
    preds = crawlpred()
    gts = crawlgt()
    res = {}
    for x in gts:
        if x in preds.keys():
            res[x]=[gts[x],preds[x]]
        else:
            print "groundtruth not found for : "+x.key
    return res






def isInPool(fn):
    """
    check if already computed
    """
    res=False
    for (dirpath, dirnames, filenames) in walk(conf.ODBPool):
        res = any(os.path.splitext(x)[0]==fn for x in filenames)
    
    
    return res
 
 
   





def writeStats(l):
    recallavg = 0
    fmeasavg=0
    precavg = 0
    
    for i in l:
        recallavg+=i['recall']
        fmeasavg+=i['f-measure']
        precavg+=i['precision']
    recallavg/=len(l)
    fmeasavg/=len(l)
    precavg/=len(l)
    
    f=open(conf.ODBStats+"statsavg.txt",'w')
    f.writelines([
                  "average recall : "+str(recallavg)+"\n",
                  "average f-measure : "+str(fmeasavg)+"\n",
                  "average precision : "+str(precavg)+"\n"
                  ])
    f.close()
    




class PoolM:
    def __init__(self):
        self.pool = Pool()
        self.poolHead = ""
        self.curOpt =conf.opts
        self.poolName = ""
        self.poolDir =conf.ODBPool
        self.poolPath = ""
    
    def readPool(self,fn=""):
        if fn : self.poolName=fn
        self.poolPath = self.poolDir+fn+".pool"
        if os.path.exists(self.poolPath):
            self.pool=YamlInput(filename = self.poolPath)()
            return True
        else : 
            print "pool not loaded"
            return False
        
    def setPool(self,fn,opt={}):
        self.pool.clear()
        self.poolDir =conf.ODBPool
        self.poolName = fn
        self.poolPath = self.poolDir+fn+".pool"
        if opt : self.curOpt=opt
        
        
    def writePool(self,fn=""):
        YamlOutput(filename = self.poolPath)(self.pool)
    
    def writePred(self):
        f=open(conf.ODBPredicted+self.poolName+".txt",'w')
        f.writelines([str(x)+'\n' for x in self.pool["pred.data"]])
        f.close()
        
    def writeRes(self,res):
        f=open(conf.ODBPredicted+"res.txt",'w')
        f.write(res)
        f.close()
        

        
    def setPoolHead(self,nm,opt={}):
        self.poolHead = nm+"."
     
    
    def add(self,name,data):
        self.pool.set(self.poolHead+name+".frameRate",self.curOpt["sampleRate"]*1./self.curOpt["hopSize"])
        self.pool.add(self.poolHead+name+".data",data)
    
    def addEvt(self,name,data):
        self.pool.set(self.poolHead+name+".frameRate",0)
        self.pool.add(self.poolHead+name+".data",data)
        
    def set(self,name,data):
        self.pool.set(self.poolHead+name+".frameRate",self.curOpt["sampleRate"]*1./self.curOpt["hopSize"])
        self.pool.set(self.poolHead+name+".data",data)
    
    def setEvt(self,name,data,opt={}):
        self.pool.set(self.poolHead+name+".frameRate",0)
        self.pool.set(self.poolHead+name+".data",data)
        
    def getn(self,name,fR=False):
        if fR : return self.pool[name+".frameRate"]
        return self.pool[name+".data"]
    def getNames(self,name):
        return [x.split('.data')[0] for x in self.pool.descriptorNames(name) if "data" in x]





'''
init
instanciate pool manager
crawl among audio file paths following configuration file
'''
pool = PoolM()
   
curFiles = {}

crawlpaths()


def init():
    global pool
    pool = PoolM()
    crawlpaths()




if __name__ == "__main__":
#     print getGt("lolo")
    
    print crawlpaths()
    print len(crawlpgt())
#     




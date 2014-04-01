from os import walk

from essentia import *
from essentia.standard import *

import numpy as np
import Config as conf



def getonsets(fn):
    f = open(fn, 'r')
    s = f.readline()
    res = []
    
    while s:
        res+=[float(s)]
        s= f.readline()

    return res

    
def crawlgt():
    for (dirpath, dirnames, filenames) in walk(conf.ODBfiles):
    
        res = dict((x.split('.')[0],getonsets(dirpath+"/"+x)) for x in filenames if 'txt' in x)
    
    return res

def crawlfn():
    for (dirpath, dirnames, filenames) in walk(conf.ODBMedias):
        res = dict((x.split('.')[0],dirpath+"/"+x) for x in filenames if 'wav' in x)
    return res




class PoolM:
    pool = Pool()
    poolHead = ""
    curOpt ={"v":1}
    poolName = ""
    poolDir =conf.ODBPool
    poolPath = ""
    
    def readPool(self,fn=poolName):
        self.poolName=fn
        self.poolPath = self.poolDir+"/"+fn+".pool"
        self.pool=YamlInput(filename = self.poolPath)()
        
    def setPool(self,fn,opt=curOpt):
        self.poolName = fn
        self.poolPath = self.poolDir+"/"+fn+".pool"
        self.curOpt=opt
        
        
    def writePool(self,fn=poolName):
        YamlOutput(filename = self.poolPath)(self.pool)
    
    def writePred(self):
        f=open(conf.ODBPredicted+"/"+self.poolName+".txt",'w')
        f.writelines([str(x)+'\n' for x in self.pool["pred.data"]])
        f.close()
        
    def setPoolHead(self,nm,opt=curOpt):
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
    
    def setEvt(self,name,data,opt=curOpt):
        self.pool.set(self.poolHead+name+".frameRate",0)
        self.pool.set(self.poolHead+name+".data",data)
        
    def getn(self,name,fR=False):
        if fR : return self.pool[name+".frameRate"]
        return self.pool[name+".data"]
    def getNames(self,name):
        return [x.split('.data')[0] for x in self.pool.descriptorNames(name) if "data" in x]



pool = PoolM()


if __name__ == "__main__":
    print crawlgt()
    print crawlfn()
    




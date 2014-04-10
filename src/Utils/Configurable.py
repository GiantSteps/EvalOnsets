'''
Created on Apr 2, 2014

@author: mhermant
'''
from essentia import *
from essentia.standard import *


import Predict.Preprocess as pp
import Predict.OnsetNovelty as oN
import Predict.Slice as sL
import Predict
import Eval


import conf
import Utils


params = Pool()
ranges = Pool()

params.clear()

curHead = ""



 

def crawlParams():
    '''
    get all curent parameters
    '''
    params.clear()
    linkparams(conf)
    linkparams(pp)
    print params.descriptorNames()
    linkparams(oN.curalgo)
    print params.descriptorNames()
    linkparams(sL.curalgo)
    print params.descriptorNames()


def setConfig():
    '''
    set all current parameters
    
    '''
    
    conf.opts = getNamespace('globalSettings')
    
    conf.initconf()

    Utils.fileMgmt.init()
        
    pp.opts['algo'] = getNamespace('preprocess.algo',True)
    oN.loadFromConf()
    sL.loadFromConf()
    



def linkparams(algo):
    '''
    dynamicly link a paramwhen algo is instanciated
    '''
    
    if 'opts_r' in dir(algo): v_r = algo.opts_r
    else : v_r={}
    dict = algo.opts
    if dict :
        setparams(dict,v_r)
        print "linked conf : "+str(algo)
    else : print 'no opts to link for : '+str(algo)


  
    
def setparams(dictin,rangedict={}):
    '''
    register all values from opts dict
    '''
    name = dictin['name']
    if not name in params.descriptorNames():
        global params
        for x,val in dictin.iteritems():
            
            '''adding list of string'''
            if(isinstance(val,list) and isinstance(val[0],str)): 
                for s in val:
                    params.add(name+'.'+x,s)
                
                '''adding dict (TODO recursive method)'''
            elif isinstance(val,dict): 
                for s,v in val.iteritems():
                    if isinstance(v,dict) :
                        for s2,v2 in v.iteritems():
                            params.set(name+'.'+x+'.'+s+'.'+s2,v2)
                    else :
                        params.set(name+'.'+x+'.'+s,v)
                    
                '''normal'''
            else :
                print x + " " + str(val) 
                params.set(name+'.'+x,val)
        
        for x,val in rangedict.iteritems():
            ranges.set(name+'.'+x,val)
            
    else : print "already added to conf pool"
    
    
    
    
def getNamespace(name,isDict = False):
    '''
    get dictionary according to the asked namespace
    '''
    global params
    print params.descriptorNames(name)
    prune = len(name.split('.'))
    res = dict(('.'.join(x.split('.')[prune:]),params[x]) for x in params.descriptorNames(name))
    if not res : print "no namespace for "+name
    if isDict:
        prune+=1
        ent = set([x.split(".")[0] for x in res.keys()])
        res2 = {}
        for g in ent :
            res2[g] =  dict(('.'.join(x.split('.')[prune:]),params[x]) for x in params.descriptorNames(name+'.'+g))
        res = res2         
    return res
    

def setDict(di):
    for k,v in di.iteritems():
        params.set(k,v)
        
def getDict(di):
    res = {}
    for k in di.iterkeys():
            res[k] = params[k]
    return res

    
def saveconf(fn):
    global params
    YamlOutput(filename = fn)(params)



def saveconfrange(fn):
    global ranges
    YamlOutput(filename = fn)(ranges)

def loadconfrange(fn):
    global ranges
    ranges = YamlOutput(filename = fn)()

def loadconf(fn):
    global params
    params = YamlInput(filename = fn)()
    setConfig()


if __name__ == '__main__':
    crawlParams()
    saveconf(conf.ODBStats +'tst.conf')
    saveconfrange(conf.ODBStats + 'tst.range.conf')

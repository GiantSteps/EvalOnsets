'''
Created on Apr 2, 2014

@author: mhermant
'''
from essentia import *
from essentia.standard import *


params = Pool()
ranges = Pool()

params.clear()

curHead = ""

def linkparams(algo):
    if 'opts_r' in dir(algo): v_r = algo.opts_r
    else : v_r={}
    dict = algo.opts
    if dict :
        setparams(dict,v_r)
        print "linked conf : "+str(algo)
    else : print 'no opts to link for : '+str(algo)


def update(dictin):
    dictin = getNamespace(dictin["name"])    
    
def setparams(dict,rangedict={}):
    name = dict['name']
    if not name in params.descriptorNames():
        global params
        for x,val in dict.iteritems():
            if(isinstance(val,list) and isinstance(val[0],str)): 
                for s in val:
                    params.add(name+'.'+x,s)
                    
            else : params.set(name+'.'+x,val)
        for x,val in rangedict.iteritems():
            ranges.set(name+'.'+x,val)
    else : print "already added to conf pool"
    
def getNamespace(name):
    global params
    res = dict(('.'.join(x.split('.')[1:]),params[x]) for x in params.descriptorNames())
    return res
    
    
def saveconf(fn):
    global params
    YamlOutput(filename = fn)(params)

def saveconfrange(fn):
    global ranges
    YamlOutput(filename = fn)(ranges)

def loadconf(fn):
    global params
    params = YamlInput(filename = fn)()
    
# curHead = 'lala.'
# setparams("lolo",5)
# print params.descriptorNames()
# print getNamespace("lala")
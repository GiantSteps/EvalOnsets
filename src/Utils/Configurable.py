'''
Created on Apr 2, 2014

@author: mhermant
'''
from essentia import *
from essentia.standard import *


params = Pool()
params.clear()

curHead = ""

def linkparams(dict):
    if 'opts_r' in dict.keys() : v_r = dict['opts_r']
    else : v_r={}
    
    setparams(dict['opts']["name"],dict["opts"],v_r)


def update(dictin):
    dictin = getNamespace(dictin["name"])    
    
def setparams(name,dict,rangedict={}):
    if not name in params.descriptorNames():
        global params
        for x,val in dict.iteritems():
            params.set(name+'.'+x+".value",val)
            if x in rangedict.keys():range = rangedict[x]
            else : range = [0]
            params.set(name+'.'+x+".range",range)
    else : print "already added to conf pool"
    
def getNamespace(name):
    global params
    res = dict(('.'.join(x.split('.')[1:-1]),params[x]) for x in params.descriptorNames() if ".value" in x)
    return res
    
    
def saveconf(fn):
    global params
   
    YamlOutput(filename = fn)(params)

def loadconf(fn):
    global params
    params = YamlInput(filename = fn)()
    
# curHead = 'lala.'
# setparams("lolo",5)
# print params.descriptorNames()
# print getNamespace("lala")
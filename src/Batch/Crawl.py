'''
Created on Apr 10, 2014

@author: mhermant

Helper for crawling results made by batch
'''

import os
import Utils.fileMgmt as fi
import conf
def getResults(path):
    res = {}
    for (dirpath,dirnames,filenames) in os.walk(path):
        for n in filenames:
            if "statsavg" in n:
                name = '.'.join(dirpath.split('/')[-3:])
                res[name] = fi.getStats(dirpath+'/'+n)
    
    return res

def getnBests(num,di):
    res = {}
    for name in di[di.keys()[0]].keys():
        new = sorted(di.iteritems(), key=lambda k: k[1][name], reverse=True)
        res[name] = [[x[0],x[1][name]] for x in new[:num]]
    return res

        
    

if __name__=="__main__":
    
    stats = getResults(conf.PathToLocal)
    print getnBests(3,stats)
    
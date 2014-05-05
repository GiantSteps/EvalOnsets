'''
Created on Apr 10, 2014

@author: mhermant

Helper for crawling results made by batch
'''

import os
import Utils.fileMgmt as fi
import conf
import numpy as np
import itertools as it
import Eval.Distance as dist

def removeDoubles(time_onsets,threshold=0.08):
    t = 1
    time_onsets = sorted(time_onsets)
    while t < len(time_onsets):
        if time_onsets[t] - time_onsets[t-1] < threshold: time_onsets.pop(t)
        else: t += 1
    return time_onsets

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



def crawlPreds(path):
    res = {}
    stats = {}
    for (dirpath,dirnames,filenames) in os.walk(path):
        if dirpath.endswith("predicted"):
            tmp = {}
            for n in filenames:
                if any(n.endswith(y) for y in conf.onsetsufix):
                    name = '.'.join(dirpath.split('/')[-3:])
                    tmp[os.path.splitext(n)[0]] = fi.getonsets(dirpath+'/'+n)
                    
            if tmp:
                stats[name] = fi.getStats('/'.join(dirpath.split('/')[:-1]+["stats/statsavg.txt"]))
                res[name]=tmp
    
    return res,stats


    
    
def getComplementarity(pred1,pred2,GT,statName):
    res = 0
    n = 0
    for i in pred1.iterkeys():
        predT = np.sort(pred1[i]+pred2[i])
        predT = removeDoubles(predT,conf.opts["doubleOnsetT"])
        res += dist.analyze(predT, GT[i])[statName]
        n+=1
        
    res/=n
    
    
    return res

def CrawlComplementarity(path):
    
    preds,stats = crawlPreds(path)
    gts = fi.crawlgt()
    
    #print preds
    res ={}
    statName = "f-measure"
    totaliter = len(preds.keys())
    totaliter*=(totaliter-1)/2
    curiter = 0
    for x in it.combinations( preds.iterkeys(),2):
        
        print str(curiter*100./totaliter)+"% computing : "+str(x)
        if stats[x[0]] and stats[x[1]] :
            combinedStats = getComplementarity(preds[x[0]],preds[x[1]], gts,statName)
            
            preStats = max(stats[x[0]][statName],stats[x[1]][statName] )
            if combinedStats-preStats>0:
                res[str(x)]=[combinedStats-preStats]
        curiter+=1
    
    return sorted(res.iteritems(), key=operator.itemgetter(1))
    
    #print [x for x in it.product(*[y for y in dic.iterkeys()])]

 
def main():
    path = conf.PathToLocal+'JKU'
    stats = getResults(path)
    res = getnBests(15,stats)
    f = open(conf.PathToLocal+'bestRes.txt','w')
    
    f.writelines([str(k)+"\n"+str(v)+"\n" for k,v in res.iteritems()])
    f.close()    

if __name__=="__main__":
    import operator
    path = conf.PathToLocal+'JKU'
    #main()
    print CrawlComplementarity(path)
        
    
    #main()
    
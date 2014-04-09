'''
Created on Mar 26, 2014

@author: mhermant
'''
from sklearn.metrics import *

# import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import conf


def toClass(pred,tru):
    pos = []
    mis = []
    neg = []
    for i in tru:
        found = False
        for j in pred:
            if (len(pos)==0 or j>pos[-1][0]) and abs(i - j) < threshold:
                pos+=[[j,abs(i-j)]]
                found = True
                break
            if j>i+threshold : break
        if not found :
            mis+= [i,0]
    
            
    neg = [[y,0] for y in pred if not (y in [x[0] for x in pos] or  y in [x[0] for x in mis])]
    
    return pos,mis,neg


def preRec(pred,true):
    threshold = conf.opts['doubleOnsetT']
    pos,mis,neg = toClass(pred,true,threshold)
    print pos,mis,neg
    pre = len(pos)*1./(len(pos)+len(neg))
    recall = len(pos)*1./(len(pos)+len(mis))
    return pre,recall

def toBinPT(pred,tru,isBin=False):
    threshold = conf.opts['doubleOnsetT']
    res=[]
    trub=[]
    endi = endj= False
    i = 0;
    j = 0;
    while (not endj or not endi):
        if (not endj and not endi):
            if(abs(pred[i]-tru[j])<threshold):
                if isBin :res+=[1]
                else:res+=[1-abs(pred[i]-tru[j])/threshold]
                trub+=[1]
                i+=1;
                j+=1;
            elif pred[i]< tru[j]:
                i+=1
                trub+=[0]
                res+=[1]
            else :
                j+=1
                res+=[0]
                trub+=[1]
        else :
            if endj :
                res+=[1]
                trub+=[0]
                i+=1
            if endi:
                res+=[0]
                trub+=[1]
                j+=1
        if ( j == len(tru)) : endj = True
        if ( i == len(pred)) : endi = True
        
    
    return np.array(res),np.array(trub)



            
            
def analyze(pred,t):
        
        

        predb,tb =  toBinPT(pred,t,True)
        
        
        if conf.isPlot : plot(t,pred,tb,predb)
        

#         return np.mean(tb-predb);
        pre,rec,f,dumb = precision_recall_fscore_support(tb,predb)
        
        classtrue = 1
        if len(f) < 2:
            if predb[0]==1:
                classtrue = 0
            else :
                print"what?"
        return {"f-measure": f[classtrue],
                "precision": pre[classtrue],
                "recall":rec[classtrue]
                
                }       
        

def plot(t,p,tb,pb):  
    
    plt.scatter([x for x in range(len(tb))],tb,marker = "o",s=200/1,c="red")
    plt.scatter([x for x in range(len(pb))],pb,marker = "o",s=200/2,c="blue")
    
    plt.xlim(0,plt.xlim()[1])
    
    plt.subplot(212)

    plt.scatter(t,[1 for x in range(len(t))],c="red",marker = "^",s=100)
    plt.scatter(p,[0 for x in range(len(p))],c="blue",marker = "^",s=100)
    
    plt.xlim(0,plt.xlim()[1])
            
# def distEMD(a,p):
#     cv.calc
#     cv.CalcEMD2
        # Convert from numpy array to CV_32FC1 Mat
#     a64 = cv.fromarray(a)
#     a32 = cv.CreateMat(a64.rows, a64.cols, cv.CV_32FC1)
#     cv.Convert(a64, a32)
#     
#     b64 = cv.fromarray(p)
#     b32 = cv.CreateMat(b64.rows, b64.cols, cv.CV_32FC1)
#     cv.Convert(b64, b32)
#     
#     # Calculate Earth Mover's
#     print cv.CalcEMD2(a32,b32,cv.CV_DIST_L2)
    
if __name__ == "__main__":  
    pred=[1,3, 6,6.1,6.4,8, 9]
    t=[0, 2,5,6,10]
    print analyze(pred,t)
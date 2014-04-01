'''
Created on Mar 26, 2014

@author: mhermant
'''
import cv2 as cv

import numpy as np
from sklearn.metrics import *

import matplotlib.pyplot as plt


def toClass(pred,tru,threshold):
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


def preRec(pred,true,threshold):
    
    pos,mis,neg = toClass(pred,true,threshold)
    print pos,mis,neg
    pre = len(pos)*1./(len(pos)+len(neg))
    recall = len(pos)*1./(len(pos)+len(mis))
    return pre,recall

def toBinPT(pred,tru,threshold,isBin=False):
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



            
            
def analyze(pred,t,threshold):
        
        

        predb,tb =  toBinPT(pred,t,2,True)
        
        
        plotbin(tb,1)
        plotbin(predb,2,"blue")
        xm,xmm  = plt.xlim()
        plt.xlim(0,xmm)
        plt.subplot(212)
        
        plotons(pred,1,"blue")
        plotons(t,0)
        xm,xmm  = plt.xlim()
        plt.xlim(0,xmm)
#         return np.mean(tb-predb);
        return classification_report(tb,predb);       
        

def plotons(ons,num,color="red"):
    plt.scatter(ons,[num for x in range(len(ons))],c=color,marker = "^",s=100)
    
def plotbin(onsb,num,color="red"):
    plt.scatter([x for x in range(len(onsb))],onsb,marker = "o",s=200/num,c=color)
            
# def distEMD(a,b):
#     cv.calc
#     cv.CalcEMD2
        # Convert from numpy array to CV_32FC1 Mat
#     a64 = cv.fromarray(a)
#     a32 = cv.CreateMat(a64.rows, a64.cols, cv.CV_32FC1)
#     cv.Convert(a64, a32)
#     
#     b64 = cv.fromarray(b)
#     b32 = cv.CreateMat(b64.rows, b64.cols, cv.CV_32FC1)
#     cv.Convert(b64, b32)
#     
#     # Calculate Earth Mover's
#     print cv.CalcEMD2(a32,b32,cv.CV_DIST_L2)
    
if __name__ == "__main__":  
    pred=[1,3, 6,6.1,6.4,8, 9]
    t=[0, 2,5,6,10]
    print analyze(pred,t,2)
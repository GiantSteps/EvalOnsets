
import cv2 as cv
import numpy as np
from numpy.matlib import rand
import random

import matplotlib.pyplot as plt
from numpy import arange
 
colors1 = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1],[1, 0.5, 0],[0, 0.5, 1],[0.5, 1, 0]])

def calcNoiseCircle(noise):

    l = 100
    a = [[1,0]]
    xs = [1]
    ys = [0]
    for i in range(l):
        r = 1 + noise*random.random()
        xs+=[r*np.cos(2*np.pi*i/l)]
        ys+=[r*np.sin(2*np.pi*i/l)];
#     print a
    xs = np.array(xs)
    xi = [a*1./len(xs) for a in range(len(xs))]
    ds= [x/1400. for x in range(1400)]   
#     
    xs=np.interp(ds,xi,xs)
    ys=np.interp(ds,xi,ys)
    b=zip(xs,ys)
    b=np.array(b)
    return b;
    

def calcNoiseSpiral(noise):

    l = 100

    xs = [1]
    ys = [0]
    for i in range(l):
        r = 1 + noise*random.random()
        xs+=[r*10*i/l*np.cos(2*np.pi*i/l)]
        ys+=[r*np.sin(2*np.pi*i/l)];
#     print a
    xs = np.array(xs)
    
    xi = [a*1./len(xs) for a in range(len(xs))]
    ds= [x/1400. for x in range(1400)]
    
    xs=np.interp(ds,xi,xs)
    ys=np.interp(ds,xi,ys)
    b=zip(xs,ys)
    b=np.array(b)

    return b;
    

def calcNoiseSquare(noise):

    l = 100

    xs = [1]
    ys = [0]
    for i in range(l):
        r = 1 + noise*random.random()
        if i<l/4. : 
            cx = -r/2.;
            cy = i*4./l*r-r/2.;
        elif i<l/2.: 
            cx = (i-l/4)*4./l*r -r/2.;
            cy = r/2.;
        elif i<l*3./4 : 
            cx = r/2.;
            cy = r/2.-(i-l/2)*4./l*r;
        else: 
            cx = r/2.-(i-3*l/4)*4./l*r;
            cy = -r/2.;    
        xs+=[cx]
        ys+=[cy]
        print cy
#     print a


    xs = np.array(xs)
    
    xi = [a*1./len(xs) for a in range(len(xs))]
    ds= [x/1400. for x in range(1400)]
    
    xs=np.interp(ds,xi,xs)
    ys=np.interp(ds,xi,ys)
    b=zip(xs,ys)
    b=np.array(b)

    return b;
    
    

Hu=[]
Hu2 = []
test = [calcNoiseCircle(0)]
for i in range(10):
    a = calcNoiseCircle(1)

    x,y =zip(*a)
    plt.plot(x,y,c=colors1[1])
    test+=a
    Mom = cv.moments(a,False)
    Hu += [cv.HuMoments(Mom)]

for i in range(10):
    a = calcNoiseSpiral(1)
    x,y =zip(*a)
    plt.plot(x,y,c=colors1[1])
#     test+=a
    
    Mom = cv.moments(a,False)
    Hu2 += [cv.HuMoments(Mom)]




# print a

def printo(m):
   
    print str(np.mean(m))+ " +-" +str(np.std(m)) + " ; " + str(np.std(m)*1./np.mean(m))
    
    
    
m1,m2,m3,m4,m5,m6,m7 = zip(*Hu)
print m1
printo(m1)
printo(m2)
printo(m3)
printo(m4)
printo(m5)
printo(m6)
printo(m7)



print "spi"
m1,m2,m3,m4,m5,m6,m7 = zip(*Hu2)

printo(m1)
printo(m2)
printo(m3)
printo(m4)
printo(m5)
printo(m6)
printo(m7)

plt.show()



    
# 
# def readMIR(intput):
#     open(input)
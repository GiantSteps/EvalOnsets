'''
Created on Apr 29, 2014

@author: mhermant
'''
import unittest
import time
from Predict.Preprocess.anHarmonic import  *
import matplotlib.pyplot as plt


class Test(unittest.TestCase):


    def test(self):
        loader=MonoLoader(filename=conf.PathToData+"sine.wav")
    
        audio = loader()
        
        t= time.clock()
        a = compute(audio)
        print time.clock()-t
        plt.plot(audio[:5000])
        plt.plot(a[:5000])
        #plt.show()
        MonoWriter(filename = conf.PathToData+"out.wav",format="wav")(a)
    
        return a


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
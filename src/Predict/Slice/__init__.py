
from Predict.Slice import *


if __name__ == "__main__":
    
    import numpy as np
    
    curdic = {'sampleRate':10,'hopSize':10}
    tstarr = np.array([[2,3,4],[5,6,7]])
    cwt.compute(tstarr,curdic)
    EssentiaOnsets.compute(tstarr, curdic)
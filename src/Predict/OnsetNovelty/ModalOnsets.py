import sys
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import modal
import modal.onsetdetection as od
import modal.ui.plot as trplot
import conf

#Need to have this for some reason
opts = {}


#Load wav file and create the onset detection function      
def compute(audio):
#    file_name = audio
#    sampling_rate, audio = wavfile.read(file_name)
#    audio = np.asarray(audio, dtype=np.double)
#    audio /= np.max(audio)
    sampling_rate = int(conf.opts["sampleRate"])
    frame_size = int(conf.opts["frameSize"])#2048
    hop_size = int(conf.opts["hopSize"])#512
    
    odf = modal.ComplexODF()
    odf.set_hop_size(hop_size)
    odf.set_frame_size(frame_size)
    odf.set_sampling_rate(sampling_rate)
    odf_values = np.zeros(len(audio) / hop_size, dtype=np.double)
    odf.process(audio, odf_values)
    
    return odf_values
    
    

import sys
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import modal
import modal.onsetdetection as od
import modal.ui.plot as trplot

#Need to have this for some reason
opts = {}

SELF_AUDIO = True

#Load wav file and create the onset detection function      
def compute(audio):
    file_name = audio
    sampling_rate, audio = wavfile.read(file_name)
    audio = np.asarray(audio, dtype=np.double)
    audio /= np.max(audio)
    
    frame_size = 2048
    hop_size = 512
    
    odf = modal.ComplexODF()
    odf.set_hop_size(hop_size)
    odf.set_frame_size(frame_size)
    odf.set_sampling_rate(sampling_rate)
    odf_values = np.zeros(len(audio) / hop_size, dtype=np.double)
    odf.process(audio, odf_values)
    
    return odf_values
    
    

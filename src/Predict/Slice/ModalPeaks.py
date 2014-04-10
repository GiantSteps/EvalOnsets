import sys
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import modal
import modal.onsetdetection as od
import modal.ui.plot as trplot
import conf

#Load wav file and create the onset detection function      
def compute(features, opt):
    onset_det = od.OnsetDetection()
    onset_det.peak_size = 3
    onsets = onset_det.find_onsets(features) * conf.opts["hopSize"]
    

def plot():
    # plot onset detection results
    fig = plt.figure(1, figsize=(12, 12))
    plt.subplot(3, 1, 1)
    plt.title('Onset detection with ' + odf.__class__.__name__)
    plt.plot(audio, '0.4')
    plt.subplot(3, 1, 2)
    trplot.plot_detection_function(onset_det.odf, hop_size)
    trplot.plot_detection_function(onset_det.threshold, hop_size, "green")
    plt.subplot(3, 1, 3)
    trplot.plot_onsets(onsets, 1.0)
    plt.plot(audio, '0.4')
    plt.show()
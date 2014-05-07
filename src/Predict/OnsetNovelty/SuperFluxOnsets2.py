#!/usr/bin/env python
# encoding: utf-8
"""
Copyright (c) 2012 - 2014 Sebastian Böck <sebastian.boeck@jku.at>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

"""
Please note that this program released together with the paper

"Maximum Filter Vibrato Suppression for Onset Detection"
by Sebastian Böck and Gerhard Widmer
in Proceedings of the 16th International Conference on Digital Audio Effects
(DAFx-13), Maynooth, Ireland, September 2013

is not tuned in any way for speed/memory efficiency. However, it can be used
as a reference implementation for the described onset detection with a maximum
filter for vibrato suppression.

If you use this software, please cite the above paper.

Please send any comments, enhancements, errata, etc. to the main author.

"""

import numpy as np
import scipy.fftpack as fft
from scipy.io import wavfile
from scipy.ndimage.filters import (maximum_filter, maximum_filter1d,
                                   uniform_filter1d)
import conf

from essentia.standard import *
import essentia

#SELF_AUDIO = False
opts = {}


def frequenciesComp(bands, fmin, fmax,ffts,sampleRate=44100,a=440):
        """
        Returns a list of frequencies aligned on a logarithmic scale.

        :param bands: number of filter bands per octave
        :param fmin:  the minimum frequency [Hz]
        :param fmax:  the maximum frequency [Hz]
        :param a:     frequency of A0 [Hz]
        :returns:     a list of frequencies

        Using 12 bands per octave and a=440 corresponding to the MIDI notes.

        """
        
        if fmax > sampleRate / 2:
            fmax = sampleRate / 2
        

        
        

        # factor 2 frequencies are apart
        factor = 2.0 ** (1.0 / bands)
        # start with A0
        freq = a
        frequencies = [freq]
        # go upwards till fmax
        while freq <= fmax:
            # multiply once more, since the included frequency is a frequency
            # which is only used as the right corner of a (triangular) filter
            freq *= factor
            frequencies.append(freq)
        # restart with a and go downwards till fmin
        freq = a
        while freq >= fmin:

            freq /= factor
            frequencies.append(freq)
        # sort frequencies
        frequencies.sort()
        # return the list
        
        # conversion factor for mapping of frequencies to spectrogram bins
        factor = (sampleRate / 2.0) / ffts
        # map the frequencies to the spectrogram bins
        frequencies = np.round(np.asarray(frequencies) / factor).astype(int)
        # only keep unique bins
        frequencies = np.unique(frequencies)
        # filter out all frequencies outside the valid range
        frequencies = [f*factor for f in frequencies if f < ffts]

        return essentia.array(frequencies)
def compute(audio):
    audio = essentia.array(audio)
    sampleRate  = int(conf.opts['sampleRate'])
    frameSize   = int(conf.opts['frameSize'])
    hopSize     = int(conf.opts['hopSize'])
    zeroPadding = int(conf.opts['zeroPadding'])
    windowType  = conf.opts['windowType']

    frameRate = float(sampleRate)/float(hopSize)



    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    windowf  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType,zeroPhase=False)
    specf = Spectrum()


    trifreqs = frequenciesComp(24, 27.5, 16000,frameSize/2,sampleRate,a=440)
    
    triangf = Triangularbands(sampleRate = sampleRate,frequencyBands = trifreqs)
    
    dilateDifff = DilateDiff(frameWidth=2,binWidth=3) 
    bandsF = []

    import time
    t=time.clock()
    for frame in frames:
        #avoid normalisation of windows made by essentia
        wframe = frameSize*0.25*windowf(frame)
        spec = specf(wframe)

        bandsF += [np.log10(1+triangf(spec))]
        

        
    d,tst = dilateDifff(bandsF)
    print time.clock()-t
    return d





if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import essentia.standard
    
    path = '/Users/mhermant/Documents/Work/Datasets/ODB/sounds/2-uncle_mean.wav'
    l = essentia.standard.MonoLoader(filename = path)

    superf = compute(l())

    
    plt.plot(superf)
    plt.show()
    
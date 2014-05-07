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


def frequenciesComp(bands, fmin, fmax,ffts=1024,sampleRate=44100,a=440):
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

        return np.array(frequencies)
def compute(audio):
    audio = essentia.array(audio)
    sampleRate  = int(conf.opts['sampleRate'])
    frameSize   = int(conf.opts['frameSize'])
    hopSize     = int(conf.opts['hopSize'])
    zeroPadding = int(conf.opts['zeroPadding'])
    windowType  = conf.opts['windowType']

    frameRate = float(sampleRate)/float(hopSize)



    frames  = FrameGenerator(audio = audio, frameSize = frameSize, hopSize = hopSize)
    window  = Windowing(size = frameSize, zeroPadding = zeroPadding, type = windowType)
    fft = FFT()


    trifreqs = frequenciesComp(24, 27.5, 16000,conf.opts["frameSize"]/2,conf.opts['sampleRate'],a=440)
    triangf = essentia.standard.Triangularbands(sampleRate = self.wav.samplerate,frequencybands = trifreqs)
    


        filtered_spec2 += [triangf(essentia.array(spec[it]))]
    

    




class SpectralODF(object):
    """
    The SpectralODF class implements most of the common onset detection
    function based on the magnitude or phase information of a spectrogram.

    """
    def __init__(self, spectrogram, ratio=0.5, max_bins=3, diff_frames=None):
        """
        Creates a new ODF object instance.

        :param spectrogram: a Spectrogram object on which the detection
                            functions operate
        :param ratio:       calculate the difference to the frame which has the
                            given magnitude ratio
        :param max_bins:    number of bins for the maximum filter
        :param diff_frames: calculate the difference to the N-th previous frame

        If no diff_frames are given, they are calculated automatically based on
        the given ratio.

        """
        self.s = spectrogram
        # determine the number off diff frames
        if diff_frames is None:
            # get the first sample with a higher magnitude than given ratio
            sample = np.argmax(self.s.window > ratio)
            diff_samples = self.s.window.size / 2 - sample
            # convert to frames
            diff_frames = int(round(diff_samples / self.s.hop_size))
            # set the minimum to 1
            if diff_frames < 1:
                diff_frames = 1
        self.diff_frames = diff_frames
        # number of bins used for the maximum filter
        self.max_bins = max_bins

    def diff(self, spec, pos=False, diff_frames=None, max_bins=None):
        """
        Calculates the difference of the magnitude spectrogram.

        :param spec:        the magnitude spectrogram
        :param pos:         only keep positive values
        :param diff_frames: calculate the difference to the N-th previous frame
        :param max_bins:    number of bins over which the maximum is searched

        Note: If 'max_bins' is greater than 0, a maximum filter of this size
              is applied in the frequency deirection. The difference of the
              k-th frequency bin of the magnitude spectrogram is then
              calculated relative to the maximum over m bins of the N-th
              previous frame (e.g. m=3: k-1, k, k+1).

              This method works only properly if the number of bands for the
              filterbank is chosen carefully. A values of 24 (i.e. quarter-tone
              resolution) usually yields good results.

        """
        # init diff matrix
        diff = np.zeros_like(spec)
        if diff_frames is None:
            diff_frames = self.diff_frames
        assert diff_frames >= 1, 'number of diff_frames must be >= 1'
        # apply the maximum filter if needed
        if max_bins > 0:
            max_spec = maximum_filter(spec, size=[1, max_bins])
        else:
            max_spec = spec
        # calculate the diff
        diff[diff_frames:] = spec[diff_frames:] - max_spec[0:-diff_frames]
        # keep only positive values
        if pos:
            diff *= (diff > 0)
        return diff

    # Onset Detection Functions
    def superflux(self):
        """
        SuperFlux with a maximum filter trajectory tracking stage.

        "Maximum Filter Vibrato Suppression for Onset Detection"
        Sebastian Böck, and Gerhard Widmer
        Proceedings of the 16th International Conferenceon Digital Audio
        Effects (DAFx-13), Maynooth, Ireland, September 2013

        """
        return np.sum(self.diff(self.s.spec, pos=True, max_bins=self.max_bins),
                      axis=1)



def parser():
    """
    Parses the command line arguments.

    """
    import argparse
    # define parser
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
    If invoked without any parameters, the software detects all onsets in
    the given files in online mode according to the method proposed in:

    "Maximum Filter Vibrato Suppression for Onset Detection"
    by Sebastian Böck and Gerhard Widmer
    Proceedings of the 16th International Conference on Digital Audio Effects
    (DAFx-13), Maynooth, Ireland, September 2013

    """)
    # general options
#     p.add_argument('files', metavar='files', nargs='+',
#                    help='files to be processed')
    p.add_argument('-v', dest='verbose', action='store_true',
                   help='be verbose')
    p.add_argument('-s', dest='save', action='store_true', default=False,
                   help='save the activations of the onset detection function')
    p.add_argument('-l', dest='load', action='store_true', default=False,
                   help='load the activations of the onset detection function')
    p.add_argument('--sep', action='store', default='',
                   help='separater for saving/loading the onset detection '
                        'function [default=numpy binary]')
    # online / offline mode
    p.add_argument('--offline', dest='online', action='store_false',
                   default=True, help='operate in offline mode')
    # wav options
    wav = p.add_argument_group('audio arguments')
    wav.add_argument('--norm', action='store_true', default=True,
                     help='normalize the audio (switches to offline mode)')
    wav.add_argument('--att', action='store', type=float, default=None,
                     help='attenuate the audio by ATT dB')
    # spectrogram options
    spec = p.add_argument_group('spectrogram arguments')
    spec.add_argument('--fps', action='store', default=200, type=int,
                      help='frames per second [default=%(default)s]')
    spec.add_argument('--frame_size', action='store', type=int, default=2048,
                      help='frame size [samples, default=%(default)s]')
    spec.add_argument('--ratio', action='store', type=float, default=0.5,
                      help='window magnitude ratio to calc number of diff '
                           'frames [default=%(default)s]')
    spec.add_argument('--diff_frames', action='store', type=int, default=None,
                      help='diff frames')
    spec.add_argument('--max_bins', action='store', type=int, default=3,
                      help='bins used for maximum filtering '
                           '[default=%(default)s]')
    # spec-processing
    pre = p.add_argument_group('pre-processing arguments')
    # filter
    pre.add_argument('--no_filter', dest='filter', action='store_false',
                     default=True, help='do not filter the magnitude '
                                        'spectrogram with a filterbank')
    pre.add_argument('--fmin', action='store', default=27.5, type=float,
                     help='minimum frequency of filter '
                          '[Hz, default=%(default)s]')
    pre.add_argument('--fmax', action='store', default=16000, type=float,
                     help='maximum frequency of filter '
                          '[Hz, default=%(default)s]')
    pre.add_argument('--bands', action='store', type=int, default=24,
                     help='number of bands per octave [default=%(default)s]')
    pre.add_argument('--equal', action='store_true', default=False,
                     help='equalize triangular windows to have equal area')
    pre.add_argument('--block_size', action='store', default=2048, type=int,
                     help='perform filtering in blocks of N frames '
                          '[default=%(default)s]')
    # logarithm
    pre.add_argument('--no_log', dest='log', action='store_false',
                     default=True, help='use linear magnitude scale')
    pre.add_argument('--mul', action='store', default=1, type=float,
                     help='multiplier (before taking the log) '
                          '[default=%(default)s]')
    pre.add_argument('--add', action='store', default=1, type=float,
                     help='value added (before taking the log) '
                          '[default=%(default)s]')
    # onset detection
    onset = p.add_argument_group('onset detection arguments')
    
    onset.add_argument('-t', dest='threshold', action='store', type=float,
                       default=1.25, help='detection threshold '
                                          '[default=%(default)s]')
    onset.add_argument('--combine', action='store', type=float, default=30,
                       help='combine onsets within N miliseconds '
                            '[default=%(default)s]')
    onset.add_argument('--pre_avg', action='store', type=float, default=100,
                       help='build average over N previous miliseconds '
                            '[default=%(default)s]')
    onset.add_argument('--pre_max', action='store', type=float, default=30,
                       help='search maximum over N previous miliseconds '
                            '[default=%(default)s]')
    onset.add_argument('--post_avg', action='store', type=float, default=70,
                       help='build average over N following miliseconds '
                            '[default=%(default)s]')
    onset.add_argument('--post_max', action='store', type=float, default=30,
                       help='search maximum over N following miliseconds '
                            '[default=%(default)s]')
    onset.add_argument('--delay', action='store', type=float, default=0,
                       help='report the onsets N miliseconds delayed '
                            '[default=%(default)s]')
    # version
    p.add_argument('--version', action='version',
                   version='%(prog)spec 1.01 (2014-03-30)')
    # parse arguments
    args = p.parse_args()
    # print arguments
    if args.verbose:
        print args
    # return args
    return args



#Don't use the argument parser because it throws an error if you're not using the command line
def linkArgs(args):


    args.samplerate = int(conf.opts['sampleRate'])
    
    args.norm = ''
    args.fps = int(conf.opts['sampleRate'])/int(conf.opts['hopSize'])
    args.frame_size = int(conf.opts['frameSize'])#2048

    
    return args

#Load wav file and create the onset detection function      
def compute(audio):

    args = parser()
    #link to current framework
    args = linkArgs(args)
    
    
    filt = None
    filterbank = None

    # open the wav file
    w = Wav(np.array(audio),args.samplerate)
    
    
    # create filterbank if needed
    if args.filter:
        # (re-)create filterbank if the samplerate of the audio changes
        if filt is None or filt.fs != args.samplerate:
            filt = Filter(args.frame_size / 2, args.samplerate,
                          args.bands, args.fmin, args.fmax, args.equal)
            filterbank = filt.filterbank
    # spectrogram
    s = Spectrogram(w, args.frame_size, args.fps, filterbank, args.log,
                    args.mul, args.add, args.online, args.block_size)
    # use the spectrogram to create an SpectralODF object
    sodf = SpectralODF(s, args.ratio, args.max_bins, args.diff_frames)
    # perform detection function on the object
    act = sodf.superflux()

    return act


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import essentia.standard
    
    path = '/Users/mhermant/Documents/Work/Datasets/ODB/sounds/2-uncle_mean.wav'
    l = essentia.standard.MonoLoader(filename = path)
    superf = compute(l())
    print superf
    
    plt.plot(superf)
    plt.show()
    
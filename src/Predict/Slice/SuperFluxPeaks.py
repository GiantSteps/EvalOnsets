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

opts = {"name":"SuperFluxPeaks",
        }



class Onset(object):
    """
    Onset Class.

    """
    def __init__(self, activations, fps, online=True, sep=''):
        """
        Creates a new Onset object instance with the given activations of the
        ODF (OnsetDetectionFunction). The activations can be read from a file.

        :param activations: an array containing the activations of the ODF
        :param fps:         frame rate of the activations
        :param online:      work in online mode (i.e. use only past
                            information)

        """
        self.activations = None     # activations of the ODF
        self.fps = fps              # framerate of the activation function
        self.online = online        # online peak-picking
        self.detections = []        # list of detected onsets (in seconds)
        # set / load activations
        if isinstance(activations, np.ndarray):
            # activations are given as an array
            self.activations = activations
        else:
            # read in the activations from a file
            self.load(activations, sep)

    def detect(self, threshold, combine=30, pre_avg=100, pre_max=30,
               post_avg=30, post_max=70, delay=0):
        """
        Detects the onsets.

        :param threshold: threshold for peak-picking
        :param combine:   only report 1 onset for N miliseconds
        :param pre_avg:   use N miliseconds past information for moving average
        :param pre_max:   use N miliseconds past information for moving maximum
        :param post_avg:  use N miliseconds future information for mov. average
        :param post_max:  use N miliseconds future information for mov. maximum
        :param delay:     report the onset N miliseconds delayed

        In online mode, post_avg and post_max are set to 0.

        Implements the peak-picking method described in:

        "Evaluating the Online Capabilities of Onset Detection Methods"
        Sebastian Böck, Florian Krebs and Markus Schedl
        Proceedings of the 13th International Society for Music Information
        Retrieval Conference (ISMIR), 2012

        """
        # online mode?
        if self.online:
            post_max = 0
            post_avg = 0
        # convert timing information to frames
        pre_avg = int(round(self.fps * pre_avg / 1000.))
        pre_max = int(round(self.fps * pre_max / 1000.))
        post_max = int(round(self.fps * post_max / 1000.))
        post_avg = int(round(self.fps * post_avg / 1000.))
        # convert to seconds
        combine /= 1000.
        delay /= 1000.
        # init detections
        self.detections = []
        # moving maximum
        max_length = pre_max + post_max + 1
        max_origin = int(np.floor((pre_max - post_max) / 2))
        mov_max = maximum_filter1d(self.activations, max_length,
                                   mode='constant', origin=max_origin)
        # moving average
        avg_length = pre_avg + post_avg + 1
        avg_origin = int(np.floor((pre_avg - post_avg) / 2))
        mov_avg = uniform_filter1d(self.activations, avg_length,
                                   mode='constant', origin=avg_origin)
        # detections are activation equal to the maximum
        detections = self.activations * (self.activations == mov_max)
        
        # detections must be greater or equal than the mov. average + threshold
        detections = detections * (detections >= mov_avg + threshold)
        # convert detected onsets to a list of timestamps
        last_onset = 0
        for i in np.nonzero(detections)[0]:
            onset = float(i) / float(self.fps) + delay
            # only report an onset if the last N miliseconds none was reported
            if onset > last_onset + combine:
                self.detections.append(onset)
                # save last reported onset
                last_onset = onset

    def write(self, filename):
        """
        Write the detected onsets to the given file.

        :param filename: the target file name

        Only useful if detect() was invoked before.

        """
        with open(filename, 'w') as f:
            for pos in self.detections:
                f.write(str(pos) + '\n')

    def save(self, filename, sep):
        """
        Save the onset activations to the given file.

        :param filename: the target file name
        :param sep: separator between activation values

        Note: using an empty separator ('') results in a binary numpy array.

        """
        print filename, sep
        self.activations.tofile(filename, sep=sep)

    def load(self, filename, sep):
        """
        Load the onset activations from the given file.

        :param filename: the target file name
        :param sep: separator between activation values

        Note: using an empty separator ('') results in a binary numpy array.

        """
        self.activations = np.fromfile(filename, sep=sep)


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
    wav.add_argument('--norm', action='store_true', default=None,
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



        
######################## MTG STUFF ###################
#Don't use the argument parser because it throws an error if you're not using the command line
def linkArgs(args):

    
    args.samplerate = int(conf.opts['sampleRate'])
    

    args.fps = args.samplerate/int(conf.opts['hopSize'])
    args.frame_size = int(conf.opts['frameSize'])#2048

    return args

#Create a SuperFlux onset object with the onset functions previously computed then detect the onsets
def compute(features,opt):
    
#     args = staticArgs(opt) 
    args = parser()
    args=linkArgs(args)
    if(isinstance(features[0],list) or isinstance(features[0],np.ndarray)):
        features = np.mean(features,axis=0)
    o = Onset(features, args.fps, args.online)
        
    o.detect(args.threshold, args.combine, args.pre_avg, args.pre_max, args.post_avg, args.post_max, args.delay)

    return o.detections



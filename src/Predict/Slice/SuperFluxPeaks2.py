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

from essentia.standard import *
import conf

opts = {"name":"SuperFluxPeaks2"
        }




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
    
    sfP = SuperFluxPeaks(threshold =args.threshold, combine = args.combine, pre_avg = args.pre_avg, pre_max = args.pre_max, frameRate =args.fps)
    detections = sfP(essentia.array(features))
    
        
    

    return detections



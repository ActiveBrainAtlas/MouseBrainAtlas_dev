#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
parser.add_argument("rotation_type", type=str, help="transpose, transverse, rotate90, rotate270, flip, or flop")
parser.add_argument("resolution", type=str, help="raw or thumbnail", default='raw')
parser.add_argument("version", type=str, help="None, Ntb, NtbNormalized, NtbNormalizedAdaptiveInvertedGamma, gray, grayJpeg", default=None)
parser.add_argument("prep_id", type=str, help="None, aligned, padded, wholeslice, or brainstem", default=None)
args = parser.parse_args()
stack = args.stack
stain = args.stain
rotation_type = args.rotation_type
resolution = args.resolution
version = args.version
prep_id = args.prep_id

import os
import subprocess
import numpy as np
import sys
import json
import time
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from metadata import *
from preprocess_utilities import *
from data_manager import DataManager
from a_driver_utilities import *

# rotates CLOCKWISE
# http://www.imagemagick.org/Usage/warping/#flip

make_rotation_ini(stack, prep_id, prep_id, rotation_type)
        
create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id=prep_id, version=version, resol=resolution)
command = ['python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', 'rotate_transverse', '--init_rotate', 'x']
#command = ['python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op', 'rotate','rotate90', '--init_rotate', '90']
completion_message = ''
call_and_time( command, completion_message=completion_message)

#['rotate270', 'rotate90', 'transpose', 'transverse']
# python a_script_rotate.py DK17 NTB rotate270 thumbnail NtbNormalized None

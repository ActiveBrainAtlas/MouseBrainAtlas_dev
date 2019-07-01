#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Runs the entirety of the processing pipeline. Assumes prep2 images have been generated and all necessary files are downloaded from S3.')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
parser.add_argument('--win_id', default=7, type=int)
args = parser.parse_args()
stack = args.stack
stain = args.stain
win_id = args.win_id

# Import other modules and packages
import os
import subprocess
import numpy as np
import sys
import json
import time
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from metadata import *
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from data_manager import DataManager
from a_driver_utilities import *


if stain.lower() == 'ntb':
    img_version = 'NtbNormalizedAdaptiveInvertedGamma'
if stain.lower() == 'thionin':
    img_version = 'gray'
    

# Compute patch features
create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                           prep_id='alignedBrainstemCrop', \
                           version=img_version,\
                           resol='raw')
command = [ 'python', 'demo_compute_features_v2.py', 'input_spec.ini','--win_id', win_id]
completion_message = 'Finished generating patch features.'
call_and_time( command, completion_message=completion_message)
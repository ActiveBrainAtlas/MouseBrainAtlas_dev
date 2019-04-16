#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Generates intensity volume, then obtains simple global alignment using manually inputted 12N and 3N_R center coordinates.')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
args = parser.parse_args()
stack = args.stack
stain = args.stain
x_12N, y_12N, x_3N, y_3N, z_midline = args.list

# Import other modules and packages
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

make_manual_anchor_points( stack, x_12N=x_12N, y_12N=y_12N, x_3N=x_3N, y_3N=y_3N, z_midline=z_midline)

if stain == 'NTB':
    tb_version = 'NtbNormalizedAdaptiveInvertedGamma'
if stain == 'Thionin':
    tb_version = 'gray'
    
# Compute intensity volumes
script_fp =  os.path.join( os.environ['REPO_DIR'], 'reconstruct', 'construct_intensity_volume.py')
command = [ 'python', script_fp, stack, '--tb_version', tb_version, '--tb_resol', 'thumbnail']
completion_message = 'Finished constructing intensity volume.'
call_and_time( command, completion_message=completion_message)

# Run simple global alignment
manual_anchor_fp =  os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration', stack+'_manual_anchor_points.ini' )
script_fp =  os.path.join( os.environ['REPO_DIR'], 'registration', 'compute_simple_global_registration.py')
command = [ 'python', script_fp, stack, manual_anchor_fp]
completion_message = 'Finished simple global alignment of the atlas using 3N and 12N.'
call_and_time( command, completion_message=completion_message)
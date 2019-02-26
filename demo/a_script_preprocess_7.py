#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Generates intensity volume, then obtains simple global alignment using manually inputted 12N and 3N_R center coordinates.')

parser.add_argument("stack", type=str, help="The name of the stack")
args = parser.parse_args()
stack = args.stack

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


# For Ntb
#! python ../src/reconstruct/construct_intensity_volume.py UCSD001 --tb_version NtbNormalizedAdaptiveInvertedGamma --tb_resol thumbnail
# For Thionin
#! python ../src/reconstruct/construct_intensity_volume.py MD585 --tb_version gray --tb_resol thumbnail
if True:
    tb_version = 'NtbNormalizedAdaptiveInvertedGamma'
else:
    tb_version = 'gray'
# Compute intensity volumes
command = [ 'python', '../src/reconstruct/construct_intensity_volume.py', stack, '--tb_version', 'NtbNormalizedAdaptiveInvertedGamma', '--tb_resol', 'thumbnail']
completion_message = 'Finished constructing intensity volume.'
call_and_time( command, completion_message=completion_message)


# Run simple global alignment
manual_anchor_fp =  os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration', stack+'_manual_anchor_points.ini' )
command = [ 'python', '../src/registration/compute_simple_global_registration.py', stack, manual_anchor_fp]
completion_message = 'Finished simple global alignment of the atlas using 3N and 12N.'
call_and_time( command, completion_message=completion_message)
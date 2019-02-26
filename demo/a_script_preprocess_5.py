#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='INSERT DESCRIPTION')

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


create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
            prep_id='None', version='NtbNormalizedAdaptiveInvertedGamma', resol='raw')
fp = os.path.join(DATA_ROOTDIR, 'CSHL_data_processed',stack, 'operation_configs', 'from_none_to_wholeslice')
command = [ 'python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', fp]
completion_message = 'Finished transformed images into wholeslice format (prep5).'
call_and_time( command, completion_message=completion_message)


create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
            prep_id='alignedWithMargin', version='NtbNormalizedAdaptiveInvertedGamma', resol='raw')
command = [ 'python', 'rescale.py', 'input_spec.ini', 'thumbnail', '-f', '0.03125']
completion_message = 'Finished rescaling images into thumbnail format.'
call_and_time( command, completion_message=completion_message)

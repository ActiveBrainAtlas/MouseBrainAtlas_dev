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
            prep_id='alignedPadded', version='NtbNormalized', resol='thumbnail')
fp = os.path.join(os.environ['DATA_ROOTDIR'],'CSHL_data_processed',stack,\
                  stack+'_prep1_thumbnail_initSnakeContours.pkl')
command = [ 'python', 'masking.py', 'input_spec.ini', fp]
completion_message = 'Automatic mask creation finished.'
call_and_time( command, completion_message=completion_message)


print('\nMask generation finished, check using the following command:\n')
print('`python ../src/gui/mask_editing_tool_v4.py $stack NtbNormalized`')

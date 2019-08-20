#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Generates binary masks for every image to segment the pixels containing the brain.')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
args = parser.parse_args()
stack = args.stack
stain = args.stain

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

if stain == 'NTB':
    ### Next 2 commands rerun script 2 alignments
    create_input_spec_ini_all( name='input_spec.ini', \
            stack=stack, prep_id='None', version='NtbNormalized', resol='thumbnail')
    command = ['python', 'align_compose.py', 'input_spec.ini', '--op', 'from_none_to_aligned']
    completion_message = 'Finished preliminary alignment.'
    call_and_time( command, completion_message=completion_message)
    
    command = ['python', 'warp_crop_v3.py','--input_spec', 'input_spec.ini', '--op_id', 'from_none_to_padded','--njobs','8','--pad_color','black']
    completion_message = 'Finished transformation to padded (prep1).'
    call_and_time( command, completion_message=completion_message)
    
    
    # Generate masks
    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedPadded', version='NtbNormalized', resol='thumbnail')
    fp = os.path.join(os.environ['DATA_ROOTDIR'],'CSHL_data_processed',stack,\
                      stack+'_prep1_thumbnail_initSnakeContours.pkl')
    command = [ 'python', 'masking.py', 'input_spec.ini', fp]
    completion_message = 'Automatic mask creation finished.'
    call_and_time( command, completion_message=completion_message)

if stain == 'Thionin':
    ### Next 2 commands rerun script 2 alignments
    create_input_spec_ini_all( name='input_spec.ini', \
            stack=stack, prep_id='None', version='gray', resol='thumbnail')
    command = ['python', 'align_compose.py', 'input_spec.ini', '--op', 'from_none_to_aligned']
    completion_message = 'Finished preliminary alignment.'
    call_and_time( command, completion_message=completion_message)
    
    command = ['python', 'warp_crop_v3.py','--input_spec', 'input_spec.ini', '--op_id', 'from_none_to_padded','--njobs','8','--pad_color','white']
    completion_message = 'Finished transformation to padded (prep1).'
    call_and_time( command, completion_message=completion_message)
    
    
    # Generate masks
    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedPadded', version='gray', resol='thumbnail')
    fp = os.path.join(os.environ['DATA_ROOTDIR'],'CSHL_data_processed',stack,\
                      stack+'_prep1_thumbnail_initSnakeContours.pkl')
    command = [ 'python', 'masking.py', 'input_spec.ini', fp]
    completion_message = 'Automatic mask creation finished.'
    call_and_time( command, completion_message=completion_message)

print('\nMask generation finished, check using the following command:\n')
print('`python ../src/gui/mask_editing_tool_v4.py $stack NtbNormalized`')

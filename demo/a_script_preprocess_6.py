#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

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
    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedWithMargin', version='NtbNormalizedAdaptiveInvertedGamma', resol='raw')
    fp =  os.path.join(DATA_ROOTDIR, 'CSHL_data_processed',stack, 'operation_configs', 'from_wholeslice_to_brainstem')
    command = [ 'python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', fp]
    completion_message = 'Finished creating brainstem crop of preprocessed image.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedBrainstemCrop', version='NtbNormalizedAdaptiveInvertedGamma', resol='raw')
    command = [ 'python', 'rescale.py', 'input_spec.ini', 'thumbnail', '-f', '0.03125']
    completion_message = 'Finished generating thumbnails for final preprocessed images.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedBrainstemCrop', version='NtbNormalizedAdaptiveInvertedGamma', resol='raw')
    command = [ 'python', 'compress_jpeg.py', 'input_spec.ini']
    completion_message = 'Finished compressing preprocessed images into jpegs.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, 
                prep_id='alignedPadded', version='mask', resol='thumbnail')
    # Create prep2 thumbnail masks
    fp =  os.path.join(DATA_ROOTDIR, 'CSHL_data_processed', stack, 'operation_configs', 'from_padded_to_brainstem')
    command = [ 'python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', fp]
    completion_message = 'Finished creating prep2 thumbnail masks.'
    call_and_time( command, completion_message=completion_message)

if stain == 'Thionin':
    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedWithMargin', version='gray', resol='raw')
    fp =  os.path.join(DATA_ROOTDIR, 'CSHL_data_processed',stack, 'operation_configs', 'from_wholeslice_to_brainstem')
    command = [ 'python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', fp]
    completion_message = 'Finished creating brainstem crop of preprocessed image.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedBrainstemCrop', version='gray', resol='raw')
    command = [ 'python', 'rescale.py', 'input_spec.ini', 'thumbnail', '-f', '0.03125']
    completion_message = 'Finished generating thumbnails for final preprocessed images.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                prep_id='alignedBrainstemCrop', version='gray', resol='raw')
    command = [ 'python', 'compress_jpeg.py', 'input_spec.ini']
    completion_message = 'Finished compressing preprocessed images into jpegs.'
    call_and_time( command, completion_message=completion_message)

    create_input_spec_ini_all( name='input_spec.ini', stack=stack, 
                prep_id='alignedPadded', version='mask', resol='thumbnail')
    # Create prep2 thumbnail masks
    fp =  os.path.join(DATA_ROOTDIR, 'CSHL_data_processed', stack, 'operation_configs', 'from_padded_to_brainstem')
    command = [ 'python', 'warp_crop_v3.py', '--input_spec', 'input_spec.ini', '--op_id', fp]
    completion_message = 'Finished creating prep2 thumbnail masks.'
    call_and_time( command, completion_message=completion_message)
    
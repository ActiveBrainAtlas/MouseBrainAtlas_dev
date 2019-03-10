#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Runs the entirety of the processing pipeline. Assumes prep2 images have been generated and all necessary files are downloaded from S3.')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
parser.add_argument("id_detector", type=str, help="A number indicating the detector settings you want.")
args = parser.parse_args()
stack = args.stack
stain = args.stain
id_detector = args.id_detector

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


if stain == 'NTB':
    img_version = 'NtbNormalizedAdaptiveInvertedGamma'
if stain == 'Thionin':
    img_version = 'gray'
    

# Compute patch features
create_input_spec_ini_all( name='input_spec.ini', stack=stack, \
                           prep_id='alignedBrainstemCrop', \
                           version=img_version,\
                           resol='raw')
command = [ 'python', 'demo_compute_features_v2.py', 'input_spec.ini']
completion_message = 'Finished generating patch features.'
call_and_time( command, completion_message=completion_message)


# Generate Probability Volumes
command = [ 'python', 'generate_prob_volumes.py', stack, id_detector, img_version]
#command = [ 'python', 'generate_prob_volumes.py', stack, id_detector, img_version, '-s', "[\"12N\"]"]
completion_message = 'Finished generating probability volumes.'
call_and_time( command, completion_message=completion_message)


# Registration script ran on each structure individually
for structure in structures_sided_sorted_by_size:
    # Make input specifications for the registration script, saved into json files
    fn_fixed, fn_moving = make_structure_fixed_and_moving_brain_specs( stack, id_detector, structure)
    command = [ 'python', 'register_brains_demo.py', fn_fixed, fn_moving, '-g']
    completion_message = 'Finished registration.'
    call_and_time( command, completion_message=completion_message)


# Registration visualization ran on each structure individually
for structure in structures_sided_sorted_by_size:
    # Make input specifications for the registration visualization script, saved into json files
    fn_vis_structures, fn_vis_global = make_registration_visualization_input_specs( stack, id_detector, structure)
    command = [ 'python', 'visualize_registration.py', img_version+'Jpeg', fn_vis_structures, '-g', fn_vis_global]
    completion_message = 'Finished registration visualization.'
    call_and_time( command, completion_message=completion_message)
    
    
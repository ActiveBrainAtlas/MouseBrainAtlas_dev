#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Converts image format to tiff, extracts different channels')

parser.add_argument("stack", type=str, help="The name of the stack")
args = parser.parse_args()
stack = args.stack

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

# Make sure ROOT_DIR/CSHL_data_processed/STACK/STACK_raw/SLICE_raw.tif files all exist, otherwise can't continue
sorted_fns = get_fn_list_from_sorted_filenames( stack )
for fn in sorted_fns:
    fp_tif = ROOT_DIR+'/CSHL_data_processed/'+stack+'/'+stack+'_raw/'+fn+'_raw.tif'
    if not os.path.isfile(fp_tif):
        print 'Raw files not located. Need to be stored as `ROOT_DIR/CSHL_data_processed/STACK/STACK_raw/SLICE_raw.tif`'

# Extract the BLUE channel, for NTB brains
start = time.time()
create_input_spec_ini_all( name='input_spec.ini', stack=stack, prep_id='None', version='None', resol='raw')
subprocess.call(["python", "extract_channel.py", "input_spec.ini", "2", "Ntb"])
end = time.time()
print('Extracted BLUE channel. Took ',end - start,' seconds')

# Create Thumbnails of eachraw image
start = time.time()
create_input_spec_ini( name='input_spec.ini', stack=stack, prep_id='None', version='Ntb', resol='raw')
subprocess.call(["python", "rescale.py", "input_spec.ini", "thumbnail", "-f", "0.03125"])
end = time.time()
print('Generated thumbnails. Took ',end - start,' seconds')

# Normalize intensity using thumbnails
start = time.time()
create_input_spec_ini( name='input_spec.ini', stack=stack, prep_id='None', version='Ntb', resol='thumbnail')
subprocess.call(["python", "rescale.py", "input_spec.ini", "NtbNormalized"])
end = time.time()
print('Normalized intensity. Took ',end - start,' seconds')
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


def create_from_none_to_aligned_file(  ):
    DATA_ROOTDIR = os.environ['DATA_ROOTDIR'] # THUMBNAIL_DATA_DIR

    # Creating 'from_none_to_aligned.ini'
    #none_to_aligned_fp = os.path.join(DATA_ROOTDIR, 'CSHL_data_processed', \
    #                stack, 'operation_configs', 'from_none_to_aligned.ini')
    none_to_aligned_fp = os.path.join(DATA_ROOTDIR,'CSHL_data_processed',stack, 'operation_configs', 'from_none_to_aligned.ini')

    from_none_to_aligned_content = '[DEFAULT]\n\
type=warp\n\
\n\
base_prep_id=None\n\
dest_prep_id=aligned\n\
\n\
# For align\n\
elastix_parameter_fp='+REPO_DIR+'/preprocess/parameters/Parameters_Rigid_MutualInfo_\
noNumberOfSpatialSamples_4000Iters.txt\n\
elastix_output_dir='+DATA_ROOTDIR+'CSHL_data_processed\
/'+stack+'/'+stack+'_elastix_output\n\
custom_output_dir='+DATA_ROOTDIR+'CSHL_data_processed\
/'+stack+'/'+stack+'_custom_output\n\
\n\
# For compose\n\
anchor_image_name='+anchor_fn+'\n\
transforms_csv='+DATA_ROOTDIR+'CSHL_data_processed/'+stack+'\
/'+stack+'_transforms_to_anchor.csv\n\
#transforms_csv='+DATA_ROOTDIR+'CSHL_data_processed/'+stack+'\
/'+stack+'_transformsTo_'+anchor_fn+'.csv\n\
resolution=thumbnail'

    if not os.path.exists(os.path.dirname(none_to_aligned_fp)):
        os.makedirs(os.path.dirname(none_to_aligned_fp))

    f = open( none_to_aligned_fp , "w")
    f.write( from_none_to_aligned_content ) 
    f.close()
    
def create_anchor_file( anchor_fn='auto' ):
    DATA_ROOTDIR = os.environ['DATA_ROOTDIR'] # THUMBNAIL_DATA_DIR
    
    if anchor_fn=='auto':
        fn_list = get_fn_list_from_sorted_filenames(stack)
        anchor_fn = fn_list[ int(len(fn_list)/2) ]

    # First designate an anchor to use
    anchor_text_fp = os.path.join(DATA_ROOTDIR, 'CSHL_data_processed', \
                    stack, stack+'_anchor.txt')

    f = open( anchor_text_fp , "w")
    f.write( anchor_fn ) 
    f.close()
    
    return anchor_fn
    
# Create 2 files necessary for running the following 2 scripts
anchor_fn = create_anchor_file()
create_from_none_to_aligned_file()


create_input_spec_ini_all( name='input_spec.ini', \
        stack=stack, prep_id='None', version='NtbNormalized', resol='thumbnail')
command = ['python', 'align_compose.py', 'input_spec.ini', '--op', 'from_none_to_aligned']
completion_message = 'Finished preliminary alignment.'
call_and_time( command, completion_message=completion_message)

command = ['python', 'warp_crop.py','--input_spec', 'input_spec.ini', '--op_id', 'from_none_to_padded','--njobs','8','--pad_color','black']
completion_message = 'Finished transformation to padded (prep1).'
call_and_time( command, completion_message=completion_message)

print('\nNow manually fix any incorrect alignments. Custom GUI available with the following command:\n')
print('`python ../src/gui/preprocess_tool_v3.py UCSD001 --tb_version NtbNormalized/gray`')
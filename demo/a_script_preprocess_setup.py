#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Downloads all relevant files from S3.')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
args = parser.parse_args()
stack = args.stack
stain = args.stain

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

if stain=="NTB":
    id_detector = 799
elif stain=="Thionin":
    id_detector = 19

def create_folder_if_nonexistant( directory ):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Download operation config files
s3_fp = 's3://mousebrainatlas-data/operation_configs/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_data_processed', stack, 'operation_configs/' )
create_folder_if_nonexistant( local_fp )
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request',s3_fp, local_fp]
subprocess.call( command )


id_classifier = detector_settings.loc[id_detector]['feature_classifier_id']
    
# Download mxnet files
s3_fp = 's3://mousebrainatlas-data/mxnet_models/inception-bn-blue/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'mxnet_models', 'inception-bn-blue/')
create_folder_if_nonexistant( local_fp )
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )
    
# Download AtlasV7 volume files
s3_fp = 's3://mousebrainatlas-data/CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume/score_volumes/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_volumes', 'atlasV7', 'atlasV7_10.0um_scoreVolume', 'score_volumes/')
create_folder_if_nonexistant( local_fp )
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )

# Download pre-trained classifiers for a particular setting
s3_fp = 's3://mousebrainatlas-data/CSHL_classifiers/setting_'+str(id_classifier)+'/classifiers/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_classifiers', 'setting_'+str(id_classifier), 'classifiers/')
create_folder_if_nonexistant( local_fp )
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )

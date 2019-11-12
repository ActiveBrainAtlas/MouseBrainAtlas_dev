#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
parser.add_argument("id_detector", type=str, help="A number indicating the detector settings you want.")
args = parser.parse_args()
stack = args.stack
stain = args.stain
id_detector = int( args.id_detector )

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
from data_manager_v2 import DataManager
from a_driver_utilities import *

id_classifier = detector_settings.loc[id_detector]['feature_classifier_id']
    
# Download mxnet files
s3_fp = 's3://mousebrainatlas-data/mxnet_models/inception-bn-blue/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'mxnet_models', 'inception-bn-blue/')
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )
    
# Download AtlasV7 volume files
s3_fp = 's3://mousebrainatlas-data/CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume/score_volumes/'
#local_fp = os.path.join( os.environ['ROOT_DIR'], 'atlas_volumes', 'atlasV7', 'atlasV7_10.0um_scoreVolume', 'score_volumes/')
local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_volumes', 'atlasV7', 'atlasV7_10.0um_scoreVolume', 'score_volumes/')
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )

# Download pre-trained classifiers for a particular setting
s3_fp = 's3://mousebrainatlas-data/CSHL_classifiers/setting_'+str(id_classifier)+'/classifiers/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'classifiers', 'setting_'+str(id_classifier), 'classifiers/')
command = ["aws", "s3", "cp", '--recursive', '--no-sign-request', s3_fp, local_fp]
subprocess.call( command )

#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Downloads all relevant files from S3.')

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
from a_driver_utilities import *


s3_fp = 's3://mousebrainatlas-data/operation_configs/'
local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_data_processed', stack, 'operation_configs' )
command = ["aws", "s3", "cp", '--recursive', s3_fp, local_fp]
subprocess.call( command )
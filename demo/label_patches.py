#! /usr/bin/env python

import sys
import os
import time

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg') # https://stackoverflow.com/a/3054314
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from metadata import *
from data_manager import *
from learning_utilities import *

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("brain_name", type=str, help="Brain name")
parser.add_argument("--win_id", type=int, help="Window id")
args = parser.parse_args()

stack = args.brain_name
win_id = args.win_id

grid_index_class_lookup, latest_timestamp = \
generate_annotation_to_grid_indices_lookup_v2(stack, win_id=win_id, by_human=True, 
                                              stack_m='atlasV7',
                                             suffix='contours', timestamp='latest',
                                             surround_margins=[200, 500],
                                            return_timestamp=True)

# If is human created
grid_index_class_lookup_fp = \
DataManager.get_annotation_to_grid_indices_lookup_filepath(stack=stack, win_id=win_id, 
                                                           by_human=True, timestamp=latest_timestamp)

save_hdf_v2(grid_index_class_lookup, grid_index_class_lookup_fp)
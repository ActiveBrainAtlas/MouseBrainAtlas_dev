import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("win_id", type=int, help="The window ID you'd like to use. Changes size of window and spacing between windows.")
args = parser.parse_args()
stack = args.stack
win_id = args.win_id

import sys
import os
import time

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *
from learning_utilities import *


for stack in [stack]:
    # Loads human-annotation files, generates grid indices lookup table
    grid_index_class_lookup, latest_timestamp = \
    generate_annotation_to_grid_indices_lookup_v2(stack, win_id=win_id, \
                                                  by_human=True, 
                                                  stack_m='atlasV7',
                                                  suffix='contours', \
                                                  timestamp='latest',
                                                  surround_margins=[200, 500],
                                                  return_timestamp=True,
                                                  change_to_prep2_frame=False)
    # Everything past here just saved results
    grid_index_class_lookup_fp = \
    DataManager.get_annotation_to_grid_indices_lookup_filepath(stack=stack, win_id=win_id, 
                                                               by_human=True, timestamp=latest_timestamp)
    # grid_index_class_lookup_fp = ROOT_DIR+'/CSHL_labelings_v3/<STACK>/<STACK>_annotation_win<WIN#>_<TIMESTAMP>_grid_indices_lookup.hdf'
    save_hdf_v2(grid_index_class_lookup, grid_index_class_lookup_fp)
    #upload_to_s3(grid_index_class_lookup_fp)
    

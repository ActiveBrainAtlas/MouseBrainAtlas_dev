import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Converts image format to tiff, extracts different channels')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument("win_id", type=int, help="The window ID you'd like to use. Changes size of window and spacing between windows.")
parser.add_argument("annotation_type", type=str, choices=['human_annotated', 'atlas_aligned', 'atlas_aligned_corrected'], \
                    help="Can be equal to one of the following: human_annotated, atlas_aligned, atlas_aligned_corrected")
parser.add_argument("--detector_id", type=int, help="Detector ID required if not human annotation", default=-1)
args = parser.parse_args()
stack = args.stack
win_id = args.win_id
annotation_type = args.annotation_type
detector_id = args.detector_id

import sys
import os
import time

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *
from learning_utilities import *


if annotation_type!='human_annotated' and detector_id==-1:
    print('Must add a valid detector_id value as follows:')
    print('python identify_patch_class_based_on_labeling_v3.py STACK WIN_ID ANNOTATION_TYPE --detector_id ID')
    sys.exit()

# Human Annotated
if annotation_type=='human_annotated':
    for stack in [stack]:
        grid_index_class_lookup, latest_timestamp = \
        generate_annotation_to_grid_indices_lookup_v2(stack, win_id=win_id, by_human=True, 
                                                      stack_m='atlasV7',
                                                     suffix='contours', timestamp='latest',
                                                     surround_margins=[200, 500],
                                                    return_timestamp=True)

        # Everything past here just saved results
        grid_index_class_lookup_fp = \
        DataManager.get_annotation_to_grid_indices_lookup_filepath(stack=stack, win_id=win_id, 
                                                                   by_human=True, timestamp=latest_timestamp)

        # grid_index_class_lookup_fp = ROOT_DIR+'/CSHL_labelings_v3/<STACK>/<STACK>_annotation_win<WIN#>_<TIMESTAMP>_grid_indices_lookup.hdf'
        save_hdf_v2(grid_index_class_lookup, grid_index_class_lookup_fp)
        #upload_to_s3(grid_index_class_lookup_fp)
    sys.exit()
    

# Atlas Aligned
elif annotation_type=='atlas_aligned': # UNTESTED
    for stack in [stack]:
        grid_index_class_lookup = generate_annotation_to_grid_indices_lookup(stack=stack, win_id=win_id, by_human=False, 
                                                                                        detector_id_f=detector_id,
                                                                            surround_margins=[200],
                                                                            positive_level=0.8, negative_level=0.1)
        grid_index_class_lookup_fp = \
    DataManager.get_annotation_to_grid_indices_lookup_filepath(stack=stack, win_id=win_id, by_human=False, 
                                                               stack_m='atlasV7', 
                                                               detector_id_f=detector_id,
                                                               timestamp='now')
        # fp = ROOT_DIR+'/CSHL_labelings_v3/<STACK>/\
        #      <STACK>_annotation_atlasV7_down32_scoreVolume_warp17_<STACK>_prep2_detector<DET#>_down32_scoreVolume_win<WIN#>_<TIMESTAMP>_grid_indices_lookup.hdf'
        save_hdf_v2(grid_index_class_lookup, grid_index_class_lookup_fp)
        #upload_to_s3(grid_index_class_lookup_fp)
    sys.exit()
    
# Atlas Aligned Corrected
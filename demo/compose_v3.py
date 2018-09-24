#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""Generate a csv file that stores a dict. Keys are image names and values are flattened (3,3)-matrices.
Usage 1: compose.py --input_spec in.ini --op_id from_none_to_aligned
Usage 2: compose.py --input_spec input_spec.ini --elastix_output_dir DEMO998_elastix_output --custom_output_dir DEMO998_custom_output --anchor_img_name "MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250" --out DEMO998_transformsTo_anchor.csv"
""")

# parser.add_argument("stack", type=str, help="stack")
parser.add_argument("input_spec", type=str, help="Input specifier. ini.")
parser.add_argument("--op", type=str, help="Op id of warp")
parser.add_argument("--prep_id", type=str, help="Prep ID of the warp")
parser.add_argument("--elastix_output_dir", type=str, help="Elastix-generated pairwise transform output dir")
parser.add_argument("--custom_output_dir", type=str, help="User-corrected pairwise transform output dir")
parser.add_argument("--anchor_img_name", type=str, help="Anchor image name")
parser.add_argument("--out", type=str, help="csv, composed transforms for each image to anchor")

args = parser.parse_args()

import os
import numpy as np
import sys
import cPickle as pickle
import json

sys.path.append(os.environ['REPO_DIR'] + '/utilities/')
from metadata import *
from preprocess_utilities import *
from data_manager import DataManager

op = load_ini(os.path.join(DATA_ROOTDIR, 'operation_configs', args.op + '.ini'))
assert op['type'] == 'warp', "Op type  must be warp."

elastix_output_dir = op['elastix_output_dir']
custom_output_dir = op['custom_output_dir']
toanchor_transforms_fp = op['transforms_csv']
anchor_img_name = op['anchor_image_name']
base_prep_id = op['base_prep_id']

input_spec = load_ini(args.input_spec)
image_name_list = input_spec['sorted_image_name_list']

assert op['base_prep_id'] == input_spec['prep_id'], "Op requires %s, but input has prep %s." % (op['base_prep_id'], input_spec['prep_id'])

#################################################

anchor_idx = image_name_list.index(anchor_img_name)

transformation_to_previous_sec = {}

for i in range(1, len(image_name_list)):
    
    transformation_to_previous_sec[i] = DataManager.load_consecutive_section_transform(moving_fn=image_name_list[i], fixed_fn=image_name_list[i-1], elastix_output_dir=elastix_output_dir, custom_output_dir=custom_output_dir)

transformation_to_anchor_sec = {}

for moving_idx in range(len(image_name_list)):

    if moving_idx == anchor_idx:
        # transformation_to_anchor_sec[moving_idx] = np.eye(3)
        transformation_to_anchor_sec[image_name_list[moving_idx]] = np.eye(3)

    elif moving_idx < anchor_idx:
        T_composed = np.eye(3)
        for i in range(anchor_idx, moving_idx, -1):
            T_composed = np.dot(np.linalg.inv(transformation_to_previous_sec[i]), T_composed)
        # transformation_to_anchor_sec[moving_idx] = T_composed
        transformation_to_anchor_sec[image_name_list[moving_idx]] = T_composed

    else:
        T_composed = np.eye(3)
        for i in range(anchor_idx+1, moving_idx+1):
            T_composed = np.dot(transformation_to_previous_sec[i], T_composed)
        # transformation_to_anchor_sec[moving_idx] = T_composed
        transformation_to_anchor_sec[image_name_list[moving_idx]] = T_composed
        
    print moving_idx, image_name_list[moving_idx], transformation_to_anchor_sec[image_name_list[moving_idx]]

#################################################
dict_to_csv(transformation_to_anchor_sec, toanchor_transforms_fp)

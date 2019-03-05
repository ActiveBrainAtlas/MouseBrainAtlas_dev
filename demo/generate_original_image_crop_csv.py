#! /usr/bin/env python

import sys
import os

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from data_manager import *
from metadata import *
from distributed_utilities import *
import pandas as pd

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Generate original_image_crop.csv')

parser.add_argument("input_spec", type=str, help="Input image specification")
args = parser.parse_args()

input_spec = load_ini(args.input_spec)

stack = input_spec['stack']
prep_id = input_spec['prep_id']
if prep_id == 'None':
    prep_id = None
resol = input_spec['resol']
version = input_spec['version']
if version == 'None':
    version = None

image_name_list = input_spec['image_name_list']
if image_name_list == 'all':
    image_name_list = DataManager.load_sorted_filenames(stack=stack)[0].keys()

# x,y,w,h
d = {img_name: \
 (0,0) + DataManager.load_image_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=img_name).shape[::-1]
 for img_name in image_name_list}

df = pd.DataFrame.from_dict({k: np.array(v).flatten() for k, v in d.iteritems()}, orient='index')
df.to_csv(os.path.join(DATA_ROOTDIR, 'CSHL_data_processed', stack, stack + '_original_image_crop.csv'), header=False)

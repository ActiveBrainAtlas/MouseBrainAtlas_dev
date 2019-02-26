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
import pyplot

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from metadata import *
from preprocess_utilities import *
from data_manager import DataManager
from a_driver_utilities import *

sorted_fns = get_fn_list_from_sorted_filenames( stack )
img_fps = []
for fn in sorted_fns:
    img_fp = DataManager.get_image_filepath_v2(stack=stack, resol='thumbnail', \
                        prep_id=None, version='NtbNormalized', fn=fn)
    img_fps.append(img_fp)

img_fp = img_fps[2]
cerebellum_fp = '/home/alexn/Desktop/custom/cerebellum.tif'

img =  imread(img_fp)
cerebellum = imread(cerebellum_fp)

imshow(cerebellum)

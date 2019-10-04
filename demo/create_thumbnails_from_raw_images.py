#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("stack", type=str, help="The name of the stack")
#parser.add_argument("stain", type=str, help="Either \'NTB\' or \'Thionin\'.")
args = parser.parse_args()
stack = args.stack
#stain = args.stain

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
from data_manager_v2 import DataManager
from a_driver_utilities import *


## Downsample and normalize images in the "_raw" folder
raw_folder = DataManager.setup_get_raw_fp( stack )
for img_name in os.listdir( raw_folder ):
    input_fp = os.path.join( raw_folder, img_name)
    output_fp = os.path.join( DataManager.setup_get_thumbnail_fp(stack), img_name )
    
    # Create output directory if it doesn't exist
    try:
        os.makedirs( DataManager.setup_get_thumbnail_fp(stack) )
    except:
        pass
    # Create thumbnails
    execute_command("convert \""+input_fp+"\" -resize 4% -auto-level -normalize \
                    -compress lzw \""+output_fp+"\"")
    
## Downsample and normalize all secondary-channel images in the "_raw_C#" folders
for channel_i in range(0,8):
    raw_folder = DataManager.setup_get_raw_fp_secondary_channel(stack, channel_i)
    
    # Break out if a channel doesn't exist.
    if not os.path.exists( raw_folder ):
        print(raw_folder+' does not exist, skipping secondary channels.')
        break
    
    for img_name in os.listdir( raw_folder ):
        input_fp = os.path.join( raw_folder, img_name)
        output_fp = os.path.join( DataManager.setup_get_thumbnail_fp_secondary_channel(
                                        stack, channel_i), img_name )
        # Create output directory if it doesn't exist
        try:
            os.makedirs( DataManager.setup_get_thumbnail_fp_secondary_channel(stack, channel_i) )
        except:
            pass
        # Create thumbnails for secondary channels
        execute_command("convert \""+input_fp+"\" -resize 4% -auto-level -normalize \
                    -compress lzw \""+output_fp+"\"")
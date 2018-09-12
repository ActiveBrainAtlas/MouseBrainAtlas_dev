#! /usr/bin/env python

import os
import argparse
import sys
import time

import numpy as np
from multiprocess import Pool

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from metadata import *
from data_manager import *
from learning_utilities import *

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Specify either (stck, resol, version, image_names) or filelist.')

parser.add_argument("--stack", type=str, help="Brain name")
parser.add_argument("--resol", type=str, help="Resolution", default='thumbnail')
parser.add_argument("--version", type=str, help="Image version")
parser.add_argument("--image_names", type=str, help="txt file. Each row is an imageName. Corresponding file paths are determined by data manager.")
parser.add_argument("--filelist", type=str, help="csv file. Each row is imageName,filePath .")
parser.add_argument("--anchor", type=str, help="Anchor image name")
parser.add_argument("--elastix_output_dir", type=str, help="Folder for pairwise transforms computed by Elastix")
parser.add_argument("--custom_output_dir", type=str, help="Folder for pairwise transforms provided by human")


args = parser.parse_args()

if hasattr(args, 'stack') and hasattr(args, 'image_names') and hasattr(args, 'version') and hasattr(args, 'resol'):
    image_names = load_txt(args.image_names)
    filelist = [(imgName, DataManager.get_image_filepath_v2(stack=args.stack, fn=imgName, resol=args.resol, version=args.version)) 
                 for imgName in image_names]
elif hasattr(args, 'filelist'):
    filelist = load_csv(args.filelist)
else:
    raise Exception('Must provide filelist or (resol, version, image_list).')

    
# Step 1: Compute pairwise transforms.
    
t = time.time()
print 'Align...'

run_distributed("%(script)s \"%(input_dir)s\" \"%(output_dir)s\" \'%%(kwargs_str)s\' %(fmt)s -p %(param_fp)s -r" % \
                {'script': os.path.join(REPO_DIR, 'preprocess', 'align.py'),
                'output_dir': args.elastix_output_dir,
                 'param_fp': '/home/yuncong/Brain/preprocess/parameters/Parameters_Rigid_MutualInfo_noNumberOfSpatialSamples_4000Iters.txt'
                },
                kwargs_list=[{'prev_img_name': filelist[i-1][0],
                              'curr_img_name': filelist[i][0],
                              'prev_fp': filelist[i-1][1],
                              'curr_fp': filelist[i][1],
                             } 
                            for i in range(1, len(filelist))],
                argument_type='list',
                jobs_per_node=8,
               local_only=True)

# wait_qsub_complete()

print 'done in', time.time() - t, 'seconds' # 2252 seconds full stack

# Step 2: Compose pairwise transforms to get each image's transform to the anchor image.

if hasattr(args, 'anchor'):
    anchor_img_name = args.anchor
else:
    assert hasattr(args, 'stack')
    anchor_img_name = DataManager.load_anchor_filename(stack=args.stack)

img_name_list = [img_name for img_name, _ in filelist]

toanchor_transforms_fp = os.path.join(DATA_DIR, stack, '%(stack)s_transformsTo_%(anchor_img_name)s.pkl' % \
                         dict(stack=stack, anchor_img_name=anchor_img_name))

t = time.time()
print 'Composing transform...'

cmd = "%(script)s --elastix_output_dir \"%(elastix_output_dir)s\" --custom_output_dir \"%(custom_output_dir)s\" --image_name_list \"%(image_name_list)s\" --anchor_img_name \"%(anchor_img_name)s\" --toanchor_transforms_fp \"%(toanchor_transforms_fp)s\"" % \
            {
                # 'stack': stack,
            'script': os.path.join(REPO_DIR, 'preprocess', 'compose.py'),
            'elastix_output_dir': args.elastix_output_dir,
            'custom_output_dir': args.custom_output_dir,
             'image_name_list': image_name_list,
             'anchor_img_name': anchor_img_name,
            'toanchor_transforms_fp': toanchor_transforms_fp}

execute_command(cmd)
        
print 'done in', time.time() - t, 'seconds' # 20 seconds

# Step 3: transform all images according to computed transformations.

pad_bg_color = 'black'
prep_id = 'alignedPadded'
version = 'NtbNormalized'

input_dir = DataManager.get_image_dir_v2(stack=stack, prep_id=None, version=version, resol='thumbnail')
out_dir = DataManager.get_image_dir_v2(stack=stack, prep_id=prep_id, resol='thumbnail', version=version)
print 'out_dir:', out_dir
script = os.path.join(REPO_DIR, 'preprocess', 'warp_crop.py')

execute_command("rm -rf %s" % out_dir)

t = time.time()
print 'Warping...'

transforms_to_anchor = DataManager.load_transforms(stack=stack, downsample_factor=32, use_inverse=False, anchor_fn=anchor_fn)

if pad_bg_color == 'auto': # useful for alternatively stained stacks where bg varies depending on stain on each section
    run_distributed('%(script)s %(stack)s \"%%(input_fp)s\" \"%%(output_fp)s\" %%(transform)s thumbnail 0 0 2000 1500 %%(pad_bg_color)s' % \
                    {'script': script,
                    'stack': stack,
                    },
                    kwargs_list=[{'transform': ','.join(map(str, transforms_to_anchor[fn].flatten())),
                                'input_fp': DataManager.get_image_filepath_v2(stack=stack, fn=fn, prep_id=None, version=version, resol='thumbnail'),
                                  'output_fp': DataManager.get_image_filepath_v2(stack=stack, fn=fn, prep_id=prep_id, version=version, resol='thumbnail'),
                                'pad_bg_color': 'black' if fn.split('-')[1][0] == 'F' else 'white'}
                                for fn in valid_filenames],
                    argument_type='single',
                   jobs_per_node=8,
                   local_only=True)
else:
    run_distributed('%(script)s %(stack)s \"%%(input_fp)s\" \"%%(output_fp)s\" %%(transform)s thumbnail 0 0 2000 1500 %(pad_bg_color)s' % \
                    {'script': script,
                    'stack': stack,
                    'pad_bg_color': pad_bg_color},
                    kwargs_list=[{'transform': ','.join(map(str, transforms_to_anchor[fn].flatten())),
                                'input_fp': DataManager.get_image_filepath_v2(stack=stack, fn=fn, prep_id=None, version=version, resol='thumbnail'),
                                  'output_fp': DataManager.get_image_filepath_v2(stack=stack, fn=fn, prep_id=prep_id, version=version, resol='thumbnail'),
                                 }
                                for fn in valid_filenames],
                    argument_type='single',
                   jobs_per_node=8,
                   local_only=True)

# wait_qsub_complete()
    
print 'done in', time.time() - t, 'seconds' # 300 seconds.


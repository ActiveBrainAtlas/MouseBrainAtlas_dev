#! /usr/bin/env python

import sys
import os
import numpy as np
import json

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import execute_command, create_parent_dir_if_not_exists
from metadata import orientation_argparse_str_to_imagemagick_str

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Warp and crop images.')

parser.add_argument("input_spec", type=str, help="json")
parser.add_argument("out_prep_id", type=str, help="")
parser.add_argument("--warp", type=str, help="pkl for multiple images or csv_str for one image")
parser.add_argument("--crop", type=str, help="json or box_xywh_str")
parser.add_argument("--njobs", type=int, help="number of parallel jobs", default=8)
parser.add_argument("--pad_bg_color", type=str, help="background color (black or white)", default='auto')
parser.add_argument("-r", "--init_rotate", type=str, help="escaped imagemagick convert option string for initial flipping and rotation", default='')
args = parser.parse_args()

njobs = args.njobs
out_prep_id = args.out_prep_id
init_rotate = args.init_rotate
warp = args.warp
crop = args.crop

input_spec = load_json(args.input_spec)

image_name_list = input_spec['image_name_list']
stack = input_spec['stack']
prep_id = input_spec['prep_id']
version = input_spec['version']
resol = input_spec['resol']

if crop.endswith('.json'):
    cropbox = load_json(crop)
    cropbox_str = ','.join(map(str, [cropbox['rostral_limit'], cropbox['dorsal_limit'], cropbox['caudal_limit'] -  cropbox['rostral_limit'] + 1, cropbox['ventral_limit'] -  cropbox['dorsal_limit'] + 1]))
elif isinstance(crop, str):
    cropbox_str = crop
    raise

if len(image_name_list) > 1 and njobs > 1:

    assert warp.endswith('.pkl')
    transforms_to_anchor = load_pickle(warp)

    run_distributed('%(script)s \"%%(input_fp)s\" \"%%(output_fp)s\" --warp %%(transform_str)s --crop %%(box_xywh_str)s --pad_color %%(pad_bg_color)s' % \
                {'script': os.path.join(REPO_DIR, 'preprocess', 'warp_crop.py'),
                'stack': stack,
                },
                kwargs_list=[{'transform_str': ','.join(map(str, transforms_to_anchor[img_name].flatten())),
                              'box_xywh_str': cropbox_str,
                            'input_fp': DataManager.get_image_filepath_v2(stack=stack, fn=img_name, prep_id=None, version=version, resol=resol),
                            'output_fp': DataManager.get_image_filepath_v2(stack=stack, fn=img_name, prep_id=out_prep_id, version=version, resol=resol),
                            'pad_bg_color': ('black' if img_name.split('-')[1][0] == 'F' else 'white') if pad_bg_color == 'auto' else pad_bg_color}
                            for img_name in image_name_list],
                argument_type='single',
               jobs_per_node=njobs,
            local_only=True)

else:

    if init_rotate == '':
        init_rotate = ''
    else:
        init_rotate = orientation_argparse_str_to_imagemagick_str[init_rotate]

    assert isinstance(warp, str)
    transform_str = warp
    transform = np.reshape(map(np.float, transform_str.split(',')), (3,3))

    x, y, w, h = map(int, cropbox_str.split(','))
    cropbox_resol = 'thumbnail'

    transforms_scale_factor = convert_resolution_string_to_um(stack=stack, resolution=transforms_resol) / convert_resolution_string_to_um(stack=stack, resolution=resol) 
    cropbox_scale_factor = convert_resolution_string_to_um(stack=stack, resolution=cropbox_resol) / convert_resolution_string_to_um(stack=stack, resolution=resol)

    T2 = transform.copy()
    T2[:2,2] = transform[:2, 2] * transforms_scale_factor
    T = np.linalg.inv(T2)

    x = x * cropbox_scale_factor
    y = y * cropbox_scale_factor
    w = w * cropbox_scale_factor
    h = h * cropbox_scale_factor

    execute_command("convert \"%(input_fp)s\" %(init_rotate)s +repage -virtual-pixel background -background %(bg_color)s +distort AffineProjection '%(sx)f,%(rx)f,%(ry)f,%(sy)f,%(tx)f,%(ty)f' -crop %(w)sx%(h)s%(x)s%(y)s\! -flatten -compress lzw \"%(output_fp)s\"" % \
                {'init_rotate':init_rotate,
                    'sx':T[0,0],
     'sy':T[1,1],
     'rx':T[1,0],
    'ry':T[0,1],
     'tx':T[0,2],
     'ty':T[1,2],
     'input_fp': input_fp,
     'output_fp': output_fp,
     'x': '+' + str(x) if int(x) >= 0 else str(x),
     'y': '+' + str(y) if int(y) >= 0 else str(y),
     'w': str(w),
     'h': str(h),
     'bg_color': pad_bg_color
}

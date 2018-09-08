#!/usr/bin/env python

import os
import numpy as np
import sys
import cPickle as pickle
import json

sys.path.append(os.environ['REPO_DIR'] + '/utilities/')
from metadata import *
from preprocess_utilities import *
from data_manager import DataManager

stack = sys.argv[1]
elastix_output_dir = sys.argv[2]
filenames = json.loads(sys.argv[3])[0]['filenames']
anchor_idx = int(sys.argv[4])
output_fn = sys.argv[5]

#################################################

transformation_to_previous_sec = {}

for i in range(1, len(filenames)):

    transformation_to_previous_sec[i] = DataManager.load_consecutive_section_transform(\
    stack=stack, moving_fn=filenames[i], fixed_fn=filenames[i-1], elastix_output_dir=elastix_output_dir)

#     custom_tf_fn = os.path.join(DATA_DIR, stack, stack + '_custom_transforms', filenames[i] + '_to_' +\
# filenames[i-1], filenames[i] + '_to_' + filenames[i-1] + '_customTransform.txt')
#     custom_tf_fn2 = os.path.join(DATA_DIR, stack, stack + '_custom_transforms', filenames[i] + '_to_' +\
# filenames[i-1], 'TransformParameters.0.txt')
#     if os.path.exists(custom_tf_fn):
#         # if custom transform is provided
#         sys.stderr.write('Load custom transform: %s\n' % custom_tf_fn)
#         with open(custom_tf_fn, 'r') as f:
#             t11, t12, t13, t21, t22, t23 = map(float, f.readline().split())
#         # transformation_to_previous_sec[i] = np.array([[t11, t12, t13], [t21, t22, t23], [0,0,1]])
#         transformation_to_previous_sec[i] = np.linalg.inv(np.array([[t11, t12, t13], [t21, t22, t23], [0,0,1]]))

#     elif os.path.exists(custom_tf_fn2):
#         sys.stderr.write('Load custom transform: %s\n' % custom_tf_fn2)
#         transformation_to_previous_sec[i] = parse_elastix_parameter_file(custom_tf_fn2)
#     else:
#         # otherwise, load elastix output
#         sys.stderr.write('Load elastix-computed transform: %s\n' % custom_tf_fn2)
#         param_fn = os.path.join(elastix_output_dir, filenames[i] + '_to_' + filenames[i-1], 'TransformParameters.0.txt')
#         if not os.path.exists(param_fn):
#             raise Exception('Transform file does not exist: %s to %s, %s' % (filenames[i], filenames[i-1], param_fn))
#         transformation_to_previous_sec[i] = parse_elastix_parameter_file(param_fn)

#         print filenames[i] + '_to_' + filenames[i-1], transformation_to_previous_sec[i]

#     sys.stderr.write('%s\n' % transformation_to_previous_sec[i])

#################################################

transformation_to_anchor_sec = {}

for moving_idx in range(len(filenames)):

    if moving_idx == anchor_idx:
        # transformation_to_anchor_sec[moving_idx] = np.eye(3)
        transformation_to_anchor_sec[filenames[moving_idx]] = np.eye(3)

    elif moving_idx < anchor_idx:
        T_composed = np.eye(3)
        for i in range(anchor_idx, moving_idx, -1):
            T_composed = np.dot(np.linalg.inv(transformation_to_previous_sec[i]), T_composed)
        # transformation_to_anchor_sec[moving_idx] = T_composed
        transformation_to_anchor_sec[filenames[moving_idx]] = T_composed

    else:
        T_composed = np.eye(3)
        for i in range(anchor_idx+1, moving_idx+1):
            T_composed = np.dot(transformation_to_previous_sec[i], T_composed)
        # transformation_to_anchor_sec[moving_idx] = T_composed
        transformation_to_anchor_sec[filenames[moving_idx]] = T_composed

    print moving_idx, filenames[moving_idx], transformation_to_anchor_sec[filenames[moving_idx]]

#################################################

with open(output_fn, 'w') as f:
    pickle.dump(transformation_to_anchor_sec, f)
    # Note that the index starts at 0, BUT the .._renamed folder index starts at 1.

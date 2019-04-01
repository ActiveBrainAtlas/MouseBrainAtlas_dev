import sys
import os
import time

import numpy as np
try:
    import mxnet as mx
except:
    sys.stderr.write("Cannot import mxnet.\n")
#import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity
from skimage.transform import rotate

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *
from learning_utilities import *
from distributed_utilities import *
from visualization_utilities import *



from sklearn.externals import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier

sys.path.append('/home/yuncong/csd395/xgboost/python-package')
try:
    from xgboost.sklearn import XGBClassifier
except:
    sys.stderr.write('xgboost is not loaded.')


win_id = 7
train_stacks = ['MD585']
test_stacks = ['MD585']
stack_stain = {'MD585': 'N'}



batch_size = 256
model_dir_name = 'inception-bn-blue'
model_name = 'inception-bn-blue'
model, mean_img = load_mxnet_model(model_dir_name=model_dir_name, model_name=model_name,
                                   num_gpus=1, batch_size=batch_size)


# Number of sections on which to sample examples from.
stack_section_number = defaultdict(dict)

for name_u in all_known_structures:
    for st in train_stacks:
        stack_section_number[st][name_u] = 10
#         if name_u == '4N' or name_u == '10N':
#             stack_section_number[st][name_u] = 20
#         else:
#             stack_section_number[st][name_u] = 10
    for st in test_stacks:
        stack_section_number[st][name_u] = 10
stack_section_number.default_factory = None


grid_indices_lookup_allStacks = {}
# Saves pandas lookup table of all patches for all structures
for stack in set(train_stacks + test_stacks):
    grid_indices_lookup_allStacks[stack] = \
    DataManager.load_annotation_to_grid_indices_lookup(stack=stack, win_id=win_id,
                                                       by_human=True, timestamp='latest',
                                                      return_locations=True)
# Extracts a list of the columns. ex: '12N', '12N_negative', '12N_surround_200um_10N'
from itertools import chain
all_labels = sorted(list(set(chain.from_iterable(set(grid_indices_lookup_allStacks[st].columns.tolist())
                                                 for st in train_stacks + test_stacks))))

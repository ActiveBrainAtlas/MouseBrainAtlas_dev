#! /usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from metadata import *
from data_manager import *

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='This script downloads input data for demo.')

parser.add_argument("-d", "--demo_data_dir", type=str, help="Directory to store demo input data", default='demo_data')
args = parser.parse_args()

# demo_data_dir = '/home/yuncong/Brain/demo_data/'

def download_to_demo(fp):
    demo_data_dir = args.demo_data_dir
    s3_http_prefix = 'https://s3-us-west-1.amazonaws.com/mousebrainatlas-data/'
    url = s3_http_prefix + fp
    demo_fp = os.path.join(demo_data_dir, fp)
    execute_command('wget -N -P \"%s\" \"%s\"' % (os.path.dirname(demo_fp), url))
    return demo_fp

# For scoring and construct 3-d probability map.

stack = 'DEMO999'
prep_id = 'alignedBrainstemCrop'
win_id = 7
normalization_scheme = 'none'
model_name = 'inception-bn-blue'
timestamp = None

#for sec in range(85, 357):
for sec in range(220, 223):
    # Download features
    fp = DataManager.get_dnn_features_filepath_v2(stack=stack, sec=sec, prep_id=prep_id, win_id=win_id,
                          normalization_scheme=normalization_scheme,
                                         model_name=model_name, what='features', timestamp=timestamp)
    fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
    download_to_demo(fp)

    fp = DataManager.get_dnn_features_filepath_v2(stack=stack, sec=sec, prep_id=prep_id, win_id=win_id,
                          normalization_scheme=normalization_scheme,
                                         model_name=model_name, what='locations', timestamp=timestamp)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
    download_to_demo(rel_fp)

download_to_demo(os.path.join('CSHL_simple_global_registration', 'DEMO999_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json'))

classifier_id = 899
for name_u in ['3N', '4N', '12N']:
    fp = DataManager.get_classifier_filepath(structure=name_u, classifier_id=classifier_id)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)	
    download_to_demo(rel_fp)


# For drawing score map background 
for sec in range(220, 222):
    fp = DataManager.get_image_filepath_v2(stack='DEMO999', prep_id=2, resol='raw', version='NtbNormalizedAdaptiveInvertedGammaJpeg', section=sec)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
    download_to_demo(rel_fp)


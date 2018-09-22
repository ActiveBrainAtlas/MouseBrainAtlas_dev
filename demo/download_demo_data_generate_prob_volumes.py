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

stack = 'DEMO998'
prep_id = 'alignedBrainstemCrop'
win_id = 7
normalization_scheme = 'none'
model_name = 'inception-bn-blue'
timestamp = None

#for sec in range(220, 223):
#for sec in []:
    # Download features
#    fp = DataManager.get_dnn_features_filepath_v2(stack=stack, sec=sec, prep_id=prep_id, win_id=win_id,
#                          normalization_scheme=normalization_scheme,
#                                         model_name=model_name, what='features', timestamp=timestamp)
#    fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
#    download_to_demo(fp)

#    fp = DataManager.get_dnn_features_filepath_v2(stack=stack, sec=sec, prep_id=prep_id, win_id=win_id,
#                          normalization_scheme=normalization_scheme,
#                                         model_name=model_name, what='locations', timestamp=timestamp)
#    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
#    download_to_demo(rel_fp)


# Download the bounding boxes for different structures that are inferred from SIMPLE global alignment.
download_to_demo(os.path.join('CSHL_simple_global_registration', 'DEMO998_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json'))

# Download pre-trained logistic regression classifiers.
classifier_id = 899
for name_u in ['3N', '4N', '12N']:
    fp = DataManager.get_classifier_filepath(structure=name_u, classifier_id=classifier_id)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)	
    download_to_demo(rel_fp)


# Download background images on top of which to draw score maps.
#for sec in [225, 235]:
#    fp = DataManager.get_image_filepath_v2(stack='DEMO998', prep_id=2, resol='raw', version='NtbNormalizedAdaptiveInvertedGammaJpeg', section=sec)
#    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
#    download_to_demo(rel_fp)

# Download atlas
for name_s in ['3N_R', '4N_R', '3N_R_surround_200um', '4N_R_surround_200um','12N', '12N_surround_200um']:

    fp = DataManager.get_score_volume_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s)
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)

    fp = DataManager.get_score_volume_origin_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s, wrt='canonicalAtlasSpace')
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)


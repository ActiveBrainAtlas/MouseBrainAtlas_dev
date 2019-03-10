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

#parser.add_argument("-d", "--demo_data_dir", type=str, help="Directory to store demo input data", default='demo_data')
#args = parser.parse_args()

# demo_data_dir = '/home/yuncong/Brain/demo_data/'

demo_data_dir = DATA_ROOTDIR

def download_to_demo(fp):
    #demo_data_dir = args.demo_data_dir
    s3_http_prefix = 'https://s3-us-west-1.amazonaws.com/v0.2-required-data/'
    url = s3_http_prefix + fp
    demo_fp = os.path.join(demo_data_dir, fp)
    execute_command('wget -N -P \"%s\" \"%s\"' % (os.path.dirname(demo_fp), url))
    return demo_fp

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


# Download pre-trained logistic regression classifiers.
classifier_id = 899
#for name_u in ['3N', '4N', '12N']:
for name_u in all_known_structures:
    fp = DataManager.get_classifier_filepath(structure=name_u, classifier_id=classifier_id)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)	
    download_to_demo(rel_fp)


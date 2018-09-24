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

##### For registration demo. #####

fp = DataManager.get_sorted_filenames_filename(stack='DEMO999')
rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
download_to_demo(rel_fp)

fp = DataManager.get_anchor_filename_filename(stack='DEMO999')
rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
anchor_fp_demo = download_to_demo(rel_fp)

anchor_fn = DataManager.load_data(anchor_fp_demo, filetype='anchor')

fp = DataManager.get_section_limits_filename_v2(stack='DEMO999', anchor_fn=anchor_fn)
rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
download_to_demo(rel_fp)

fp = DataManager.get_cropbox_filename_v2(stack='DEMO999', prep_id=2, anchor_fn=anchor_fn)
rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
download_to_demo(rel_fp)

download_to_demo(os.path.join('CSHL_simple_global_registration', 'DEMO999_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.bp'))

# Download subject detection maps
for name_s in ['3N_R', '4N_R', '12N']:

    fp = DataManager.get_score_volume_filepath_v3(stack_spec={'name':'DEMO999', 'detector_id':799, 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s)
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)

    fp = DataManager.get_score_volume_origin_filepath_v3(stack_spec={'name':'DEMO999', 'detector_id':799, 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s, wrt='wholebrain')
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)

# Download atlas
for name_s in ['3N_R', '4N_R', '3N_R_surround_200um', '4N_R_surround_200um','12N', '12N_surround_200um']:

    fp = DataManager.get_score_volume_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s)
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)

    fp = DataManager.get_score_volume_origin_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s, wrt='canonicalAtlasSpace')
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)

##### For visualization demo. #####

# Download images
for sec in range(221, 238):
    fp = DataManager.get_image_filepath_v2(stack='DEMO999', prep_id=2, resol='raw', version='NtbNormalizedAdaptiveInvertedGammaJpeg', section=sec)
    rel_fp = relative_to_local(fp, local_root=DATA_ROOTDIR)
    download_to_demo(rel_fp)

fp = DataManager.get_original_volume_filepath_v2(stack_spec={'name':'DEMO999', 'resolution':'10.0um', 'vol_type':'intensity', 'prep_id':'wholebrainWithMargin'}, structure=None)
rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
download_to_demo(rel_fp)

fp = DataManager.get_original_volume_origin_filepath_v3(stack_spec={'name':'DEMO999', 'resolution':'10.0um', 'vol_type':'intensity', 'prep_id':'wholebrainWithMargin'}, structure=None)
rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
download_to_demo(rel_fp)

download_to_demo(os.path.join('CSHL_simple_global_registration', 'DEMO999_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json'))

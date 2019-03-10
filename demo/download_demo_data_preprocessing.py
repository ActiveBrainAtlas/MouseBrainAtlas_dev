#! /usr/bin/env python

import sys, os
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import execute_command, create_if_not_exists
from metadata import *
from data_manager import relative_to_local

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='This script downloads input data for demo.')

parser.add_argument("-d", "--demo_data_dir", type=str, help="Directory to store demo input data")
args = parser.parse_args()

if args.demo_data_dir is None:
    demo_data_dir = DATA_ROOTDIR
else:
    demo_data_dir = args.demo_data_dir

def download_to_demo(fp):
    """
    Args:
	fp (str): file path relative to data root.
    """
    create_if_not_exists(demo_data_dir)
    s3_http_prefix = 'https://s3-us-west-1.amazonaws.com/v0.2-required-data/'
    url = s3_http_prefix + fp
    demo_fp = os.path.join(demo_data_dir, fp)
    execute_command('wget -N -P \"%s\" \"%s\"' % (os.path.dirname(demo_fp), url))
    return demo_fp


# Download raw JPEG2000 images

print("Download raw JPEG2000 images")
for img_name in [
'MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242',
'MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250',
'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
]:

    download_to_demo(os.path.join('jp2_files', 'DEMO998', img_name + '_lossless.jp2'))
    #pass

# Download mxnet model

print("Download mxnet model")

model_dir_name = 'inception-bn-blue'

fp = os.path.join(MXNET_MODEL_ROOTDIR, model_dir_name, 'inception-bn-blue-0000.params')
download_to_demo(relative_to_local(fp, local_root=DATA_ROOTDIR))

fp = os.path.join(MXNET_MODEL_ROOTDIR, model_dir_name, 'inception-bn-blue-symbol.json')
download_to_demo(relative_to_local(fp, local_root=DATA_ROOTDIR))

fp = os.path.join(MXNET_MODEL_ROOTDIR, model_dir_name, 'mean_224.npy')
download_to_demo(relative_to_local(fp, local_root=DATA_ROOTDIR))

# Download warp/crop operation configs.

print("Download warp/crop operation configs")

for fn in [
'crop_orig_template',
'from_aligned_to_none',
'from_aligned_to_padded',
'from_none_to_aligned_template',
'from_none_to_padded',
'from_none_to_wholeslice',
'from_padded_to_brainstem_template',
'from_padded_to_wholeslice_template',
'from_padded_to_none',
'from_wholeslice_to_brainstem'
]:
    download_to_demo(os.path.join('operation_configs', fn + '.ini'))

# Download brain meta data
print("Download brain DEMO998 meta data")
download_to_demo(os.path.join('brains_info', 'DEMO998.ini'))

download_to_demo(os.path.join('CSHL_data_processed', 'DEMO998', 'DEMO998_sorted_filenames.txt'))
download_to_demo(os.path.join('CSHL_data_processed', 'DEMO998', 'DEMO998_prep2_sectionLimits.ini'))

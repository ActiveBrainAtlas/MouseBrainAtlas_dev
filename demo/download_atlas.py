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

parser.add_argument("-d", "--demo_data_dir", type=str, help="Directory to store demo input data")
parser.add_argument("-s", "--structure_list", type=str, help="Json-encoded list of structures (sided) (Default: all known structures)")
args = parser.parse_args()

import json
if hasattr(args, 'structure_list') and args.structure_list is not None:
    structure_list = json.loads(args.structure_list)
else:
    structure_list = all_known_structures_sided
    print(structure_list)

if args.demo_data_dir is None:
    demo_data_dir = DATA_ROOTDIR
else:
    demo_data_dir = args.demo_data_dir

def download_to_demo(fp):
    s3_http_prefix = 'https://s3-us-west-1.amazonaws.com/v0.2-required-data/'     
    url = s3_http_prefix + fp    
    demo_fp = os.path.join(demo_data_dir, fp)
    execute_command('wget -N -P \"%s\" \"%s\"' % (os.path.dirname(demo_fp), url))
    return demo_fp


#for name_s in ['3N_R', '4N_R', '3N_R_surround_200um', '4N_R_surround_200um','12N', '12N_surround_200um']:
for name_s in structure_list + [compose_label(name_s, surround_margin='200um') for name_s in structure_list]:

    fp = DataManager.get_score_volume_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s)
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)
 
    fp = DataManager.get_score_volume_origin_filepath_v3(stack_spec={'name':'atlasV7', 'resolution':'10.0um', 'vol_type':'score'}, structure=name_s, wrt='canonicalAtlasSpace')
    rel_fp = relative_to_local(fp, local_root=ROOT_DIR)
    download_to_demo(rel_fp)


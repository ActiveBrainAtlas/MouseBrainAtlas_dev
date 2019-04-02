import xgboost

import mxnet

import argparse

import sys
import os
sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *

parser = argparse.ArgumentParser(description="")
parser.add_argument('--test_stacks', default='MD589', type=str)
parser.add_argument('--train_stacks', default='MD589', type=str)
parser.add_argument('--win_id', default=7, type=int)
parser.add_argument('--structures', default='all', type=str)

args = parser.parse_args()
test_stacks = args.test_stacks.replace('[','').replace(']','').replace(' ','').split(',')
train_stacks = args.train_stacks.replace('[','').replace(']','').replace(' ','').split(',')
win_id = args.win_id
if args.structures == 'all':
    structures = structures_sided_sorted_by_size
else:
    structures = args.structures.replace('[','').replace(']','').replace(' ','').split(',')

for stack in test_stacks:
    print stack
    
for stack in train_stacks:
    print stack
    
for str in structures:
    print str
#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')

parser.add_argument("stack", type=str, help="The name of the stack")
parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
args = parser.parse_args()
list = args.list

print list


import sys
import os
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
# from utilities2015 import *
# from registration_utilities import *
# from annotation_utilities import *
# from metadata import *
from data_manager import *

import vtk
from PyQt4.QtCore import *
print('IMPORTS DONE')

# Testing mmetadata cache is good (importing marching cubes)


# Works with sudo
# Empty with no sudo (cannot import name marching_cubes, no vtk)
print metadata_cache['valid_sections']


# Testing mxnet import

# Fails with sudo (OSError: libcudart.so.9.0: cannot open shared object file: No such file or directory)
# works with no sudo
try:
    import mxnet
except Exception as e:
    print("******************************")
    print("No mxnet")
    print(e)
    print("******************************")

try:
    from vis3d_utilities import *
except Exception as e:
    print("******************************")
    print("No vtk")
    print(e)
    print("******************************")

import skimage
# skimage.measure.marching_cubes_classic(g)
# skimage.measure.marching_cubes()
from vis3d_utilities import *
try:
    from skimage.measure import marching_cubes_classic, correct_mesh_orientation, mesh_surface_area
except Exception as e:
    print("******************************")
    print("No skimage")
    print(e)
    print("******************************")

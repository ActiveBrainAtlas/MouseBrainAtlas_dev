import sys
import os
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from metadata import *
from data_manager import *

# Testing mmetadata cache is good (importing marching cubes)


# Works with sudo
# Empty with no sudo (cannot import name marching_cubes, no vtk)
print metadata_cache['valid_sections']


# Testing mxnet import

# Fails with sudo (OSError: libcudart.so.9.0: cannot open shared object file: No such file or directory)
# works with no sudo
import mxnet
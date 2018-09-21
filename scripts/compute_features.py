#! /usr/bin/env python

import sys
import os
import time

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg') # https://stackoverflow.com/a/3054314
import matplotlib.pyplot as plt
import numpy as np

#os.environ['REPO_DIR'] = '/home/alexn/brainDev/src'
sys.path.append(os.path.join(os.environ['REPO_DIR'],'utilities'))
print os.environ['REPO_DIR']
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from metadata import *
from data_manager import *
from learning_utilities import *


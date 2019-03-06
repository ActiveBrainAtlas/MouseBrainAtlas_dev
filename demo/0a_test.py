#!/usr/bin/env python

import os
import sys
import subprocess
import time

#os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH']+':/usr/local/cuda-9.0'

import mxnet as mx
print mx.__file__
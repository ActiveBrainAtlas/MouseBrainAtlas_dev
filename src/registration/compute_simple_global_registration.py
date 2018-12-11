#! /usr/bin/env python

# Adapted from notebook registration/registration_v7_atlasV7_simpleGlobal.ipynb

import sys
import os
import time

from multiprocess import Pool
import numpy as np

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *

from registration_utilities import *

def align_anchors(pm1, pm2, pf1, pf2):
    """
    Align the vector (pm1, pm2) and vector (pf1, pf2), and align the two middle points. 
    """
    
    t = ((pf1 + pf2) / 2. - (pm1 + pm2) / 2.)
    
    subject_d = pf1 - pf2
    atlas_d = pm1 - pm2

    subject_d_n = subject_d / np.linalg.norm(subject_d)
    atlas_d_n = atlas_d / np.linalg.norm(atlas_d)

    R = R_align_two_vectors(atlas_d_n, subject_d_n)
    
    T = np.zeros((3,4))
    T[:3, :3] = R
#     T[:3, 3] = np.dot(R, t)
    T[:3, 3] = t
    
    return T

# https://www.lfd.uci.edu/~gohlke/code/transformations.py.html

def quaternion_about_axis(angle, axis):
    """Return quaternion for rotation about axis.

    >>> q = quaternion_about_axis(0.123, [1, 0, 0])
    >>> numpy.allclose(q, [0.99810947, 0.06146124, 0, 0])
    True

    """
    q = np.array([0.0, axis[0], axis[1], axis[2]])
    qlen = np.linalg.norm(q)
    q *= np.sin(angle/2.0) / qlen
    q[0] = np.cos(angle/2.0)
    return q


def quaternion_matrix(quaternion):
    """Return homogeneous rotation matrix from quaternion.

    >>> M = quaternion_matrix([0.99810947, 0.06146124, 0, 0])
    >>> numpy.allclose(M, rotation_matrix(0.123, [1, 0, 0]))
    True
    >>> M = quaternion_matrix([1, 0, 0, 0])
    >>> numpy.allclose(M, numpy.identity(4))
    True
    >>> M = quaternion_matrix([0, 1, 0, 0])
    >>> numpy.allclose(M, numpy.diag([1, -1, -1, 1]))
    True

    """
    q = np.array(quaternion, dtype=np.float64, copy=True)
    n = np.dot(q, q)
    q *= np.sqrt(2.0 / n)
    q = np.outer(q, q)
    return np.array([
        [1.0-q[2, 2]-q[3, 3],     q[1, 2]-q[3, 0],     q[1, 3]+q[2, 0], 0.0],
        [    q[1, 2]+q[3, 0], 1.0-q[1, 1]-q[3, 3],     q[2, 3]-q[1, 0], 0.0],
        [    q[1, 3]-q[2, 0],     q[2, 3]+q[1, 0], 1.0-q[1, 1]-q[2, 2], 0.0],
        [                0.0,                 0.0,                 0.0, 1.0]])


import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Compute the global transform based on two manually designated anchor points.')
parser.add_argument("stack", type=str, help="brain name")
parser.add_argument("manual_anchors", type=str, help="an ini specifying the manually designated anchor points")
args = parser.parse_args()

stack = args.stack
manual_points = load_ini(args.manual_anchors)
print("Manually selected anchor points", manual_points)
x_12N = manual_points['x_12N']
y_12N = manual_points['y_12N']
x_3N = manual_points['x_3N']
y_3N = manual_points['y_3N']
mid_z_wrt_wholebrainWithMargin = manual_points['z_midline']

atlas_spec = dict(name='atlasV7',
                   vol_type='score'    ,               
                    resolution='10.0um'
                   )

atlas_structures_wrt_canonicalAtlasSpace_atlasResol = \
DataManager.load_original_volume_all_known_structures_v3(atlas_spec, in_bbox_wrt='canonicalAtlasSpace',
                                                        out_bbox_wrt='canonicalAtlasSpace')

atlas_structure_centroids_wrt_canonicalAtlasSpace_atlasResol = get_structure_centroids(vol_origin_dict=atlas_structures_wrt_canonicalAtlasSpace_atlasResol)

atlas_anchor1_wrt_canonicalAtlasSpace_atlasResol = \
np.r_[atlas_structure_centroids_wrt_canonicalAtlasSpace_atlasResol['12N'][:2], 0]
atlas_anchor2_wrt_canonicalAtlasSpace_atlasResol = \
np.r_[atlas_structure_centroids_wrt_canonicalAtlasSpace_atlasResol['3N_R'][:2], 0]

intensity_volume_spec = dict(name=stack, resolution='10.0um', prep_id='wholebrainWithMargin', vol_type='intensity')

_, wholebrainWithMargin_origin_wrt_wholebrain_dataResol = \
DataManager.load_original_volume_v2(intensity_volume_spec, return_origin_instead_of_bbox=True)

wholebrainWithMargin_origin_wrt_wholebrain_dataResol_x, \
    wholebrainWithMargin_origin_wrt_wholebrain_dataResol_y, \
    wholebrainWithMargin_origin_wrt_wholebrain_dataResol_z = \
wholebrainWithMargin_origin_wrt_wholebrain_dataResol

subject_anchor1_wrt_wholebrain_atlasResol = np.array([wholebrainWithMargin_origin_wrt_wholebrain_dataResol_x * 10. + x_12N * 20., 
                                                      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_y * 10. + y_12N * 20., 
                                                      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_z*10. + mid_z_wrt_wholebrainWithMargin*20.]) / 10.
subject_anchor2_wrt_wholebrain_atlasResol = np.array([wholebrainWithMargin_origin_wrt_wholebrain_dataResol_x * 10. + x_3N * 20., 
                                                      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_y * 10. + y_3N * 20., 
                                                      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_z*10. + mid_z_wrt_wholebrainWithMargin*20.]) / 10.

wholebrainWithMargin_origin_wrt_wholebrain_dataResol = \
np.r_[wholebrainWithMargin_origin_wrt_wholebrain_dataResol_x,
      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_y,
      wholebrainWithMargin_origin_wrt_wholebrain_dataResol_z]

T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol = \
align_anchors(atlas_anchor1_wrt_canonicalAtlasSpace_atlasResol, atlas_anchor2_wrt_canonicalAtlasSpace_atlasResol,
             subject_anchor1_wrt_wholebrain_atlasResol, subject_anchor2_wrt_wholebrain_atlasResol)

print T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol


#rand_vec = np.random.uniform(size=3)
#rand_vec = rand_vec / np.linalg.norm(rand_vec)
#rand_rot_amount = np.random.uniform(high=np.deg2rad(5))
#perturb_rot = quaternion_matrix(quaternion_about_axis(rand_rot_amount, rand_vec))

#np.random.seed(0)
#perturb_xyz = np.random.choice(np.arange(-30, 30), 3)

#T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol = \
#np.dot(T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol, perturb_rot)
#T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol[:3, 3] += perturb_xyz

print T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol

fp = os.path.join(DATA_ROOTDIR, 'CSHL_simple_global_registration', stack + '_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.txt')
create_parent_dir_if_not_exists(fp)
np.savetxt(fp, T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol)

######################################################################
## Identify 3-d bounding box of each simpleGlobal aligned structure ##
######################################################################

atlas_structures_wrt_canonicalAtlasSpace_atlasResol = \
DataManager.load_original_volume_all_known_structures_v3(atlas_spec, in_bbox_wrt='canonicalAtlasSpace',
                                                        out_bbox_wrt='canonicalAtlasSpace')

T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol = \
np.loadtxt(os.path.join(DATA_ROOTDIR, 'CSHL_simple_global_registration', stack + '_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.txt'))

registered_atlas_structures_wrt_wholebrain_atlasResol = \
{name_s: transform_volume_v4(volume=vo, transform=T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol, 
                             return_origin_instead_of_bbox=True)
for name_s, vo in atlas_structures_wrt_canonicalAtlasSpace_atlasResol.iteritems()}

registered_atlas_structures_bbox_wrt_wholebrain_atlasResol = \
{name_s: (o[0], o[0] + v.shape[1] - 1, o[1], o[1] + v.shape[0] - 1, o[2], o[2] + v.shape[2] - 1)
 for name_s, (v, o) in registered_atlas_structures_wrt_wholebrain_atlasResol.iteritems()}

registered_atlas_structures_xyzTwoCorners_wrt_wholebrain_atlasResol = \
{name_s: ((o[0], o[2], o[4]), (o[1], o[3], o[5]))
for name_s, o in registered_atlas_structures_bbox_wrt_wholebrain_atlasResol.iteritems()}

#     registered_atlas_structures_xyzCorners_wrt_wholebrainWithMargin_atlasResol = \
#     {name_s: ((o[0], o[2], o[4]), (o[0], o[2], o[5]), (o[0], o[3], o[4]), (o[0], o[3], o[5]), \
#              (o[1], o[2], o[4]), (o[1], o[2], o[5]), (o[1], o[3], o[4]), (o[1], o[3], o[5]))
#     for name_s, o in registered_atlas_structures_bbox_wrt_wholebrainWithMargin_atlasResol.iteritems()}

atlas_resol = atlas_spec['resolution']

from data_manager import CoordinatesConverter

converter = CoordinatesConverter(stack=stack)

registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners_raw = {}

for name_s, corners_xyz in registered_atlas_structures_xyzTwoCorners_wrt_wholebrain_atlasResol.iteritems():
#     print name_s
    registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners_raw[name_s] = \
    converter.convert_frame_and_resolution(p=corners_xyz, 
                                       in_wrt=('wholebrain', 'sagittal'),
                                      in_resolution=atlas_resol,
                                      out_wrt=('wholebrainXYcropped', 'sagittal'),
                                      out_resolution='raw_raw_section').astype(np.int)

save_json(registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners_raw, 
      os.path.join(DATA_ROOTDIR, 'CSHL_simple_global_registration', stack + '_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json'))

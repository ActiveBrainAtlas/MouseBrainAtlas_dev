#!/usr/bin/env python

import os
import sys
import subprocess
import time
import json

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
#from utilities2015 import *
#from data_manager import *
#from distributed_utilities import *
from metadata import *

def create_input_spec_ini( name, image_name_list, stack, prep_id, version, resol  ):
    f = open(name, "w")
    
    f.write('[DEFAULT]\n')
    f.write('image_name_list = '+image_name_list[0]+'\n')
    for i in range ( 1 , len(image_name_list) ):
        f.write('    '+image_name_list[i]+'\n')
    f.write('stack = '+stack+'\n')
    f.write('prep_id = '+prep_id+'\n')
    f.write('version = '+version+'\n')
    f.write('resol = '+resol+'\n')
    
def create_input_spec_ini_all( name, stack, prep_id, version, resol  ):
    f = open(name, "w")
    
    f.write('[DEFAULT]\n')
    f.write('image_name_list = all\n')
    f.write('stack = '+stack+'\n')
    f.write('prep_id = '+prep_id+'\n')
    f.write('version = '+version+'\n')
    f.write('resol = '+resol+'\n')
    
def get_fn_list_from_sorted_filenames( stack ):
    '''
        get_fn_list_from_sorted_filenames( stack ) returns a list of all the valid
        filenames for the current stack.
    '''
    fp = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_data_processed', stack+'/')
    fn = stack+'_sorted_filenames.txt'
    
    try:
        file0 = open( fp+fn, 'r')
    except:
        print('_________________________________________________________________________________')
        print('_________________________________________________________________________________')
        print('\"'+fp+fn+'\" not found!')
        print('')
        print('This file must be present for the pipeline to continue. Add the file and rerun the script.')
        print('_________________________________________________________________________________')
        print('_________________________________________________________________________________')
        sys.exit()
        
    section_names = []

    for line in file0: 
        if 'Placeholder' in line:
            #print line
            continue
        else:
            space_index = line.index(" ")
            section_name = line[ 0 : space_index ]
            section_number = line[ space_index+1 : ]
            section_names.append( section_name )
    return section_names

def make_from_x_to_y_ini(stack,x,y,rostral_limit,caudal_limit,dorsal_limit,ventral_limit):
    '''
    Creates operation configuration files that specify the cropping boxes for either the whole brain, or the brainstem.
    '''
    base_prep_id=''
    dest_prep_id=''
    if x=='aligned':
        base_prep_id = 'aligned'
    elif x=='padded':
        base_prep_id = 'alignedPadded'
    if y=='wholeslice':
        dest_prep_id = 'alignedWithMargin'
    elif y=='brainstem':
        dest_prep_id = 'alignedBrainstemCrop'
    
    fn = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_data_processed', stack, 'operation_configs', 'from_'+x+'_to_'+y+'.ini' )
    f = open(fn, "w")
    f.write('[DEFAULT]\n')
    f.write('type = crop\n\n')
    f.write('base_prep_id = '+base_prep_id+'\n')
    f.write('dest_prep_id = '+dest_prep_id+'\n\n')
    f.write('rostral_limit = '+str(rostral_limit)+'\n')
    f.write('caudal_limit = '+str(caudal_limit)+'\n')
    f.write('dorsal_limit = '+str(dorsal_limit)+'\n')
    f.write('ventral_limit = '+str(ventral_limit)+'\n')
    f.write('resolution = thumbnail')
    f.close()
    
def make_manual_anchor_points( stack, x_12N, y_12N, x_3N, y_3N, z_midline):
    if not os.path.exists( os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration') ):
        os.mkdir( os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration') )
    
    fn = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration', stack+'_manual_anchor_points.ini' )
    f = open(fn, "w")
    f.write('[DEFAULT]\n')
    f.write('x_12N = '+str(x_12N)+'\n')
    f.write('y_12N = '+str(y_12N)+'\n')
    f.write('x_3N = '+str(x_3N)+'\n')
    f.write('y_3N = '+str(y_3N)+'\n')
    f.write('z_midline = '+str(z_midline))
    f.close()
    
def make_rotation_ini(stack, base_prep_id, dest_prep_id, rotation_type):
    '''
    Creates operation configuration files that specify the kind of rotation / flipping to apply to images (Clockwise rotations).
    
    http://www.imagemagick.org/Usage/warping/#flip
    '''
    assert rotation_type in orientation_argparse_str_to_imagemagick_str.keys()
    
    # Defined in metadata
    base_prep_id = prep_id_short_str_to_full[ base_prep_id ]
    dest_prep_id = prep_id_short_str_to_full[ dest_prep_id ]
    
    fn = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_data_processed', stack, 'operation_configs', 'rotate_transverse.ini' )
    f = open(fn, "w")
    f.write('[DEFAULT]\n')
    f.write('type = rotate\n')
    f.write('how = '+rotation_type+'\n\n')
    f.write('base_prep_id = '+base_prep_id+'\n')
    f.write('dest_prep_id = '+dest_prep_id+'\n\n')
    f.close()
    
def make_structure_fixed_and_moving_brain_specs( stack, id_detector, structure):
    '''
    Creates the input specification file for the registration script.
    '''
    if type(structure)==list:
        fixed_brain_spec_data = {"name":stack,
                            "vol_type": "score", 
                            "resolution":"10.0um",
                            "detector_id":id_detector,
                            "structure":structure
                            }
        moving_brain_spec_data = {"name":"atlasV7",
                            "vol_type": "score", 
                            "resolution":"10.0um",
                            "structure":structure
                            }
    elif type(structure)==str:
        fixed_brain_spec_data = {"name":stack,
                                "vol_type": "score", 
                                "resolution":"10.0um",
                                "detector_id":id_detector,
                                "structure":[structure]
                                }
        moving_brain_spec_data = {"name":"atlasV7",
                                "vol_type": "score", 
                                "resolution":"10.0um",
                                "structure":[structure]
                                }

    fn_fixed = stack+'_fixed_brain_spec.json'
    fn_moving = stack+'_moving_brain_spec.json'
    
    fp = os.path.join( os.environ['REPO_DIR'], '..', 'demo/')

    with open(fp+fn_fixed, 'w') as outfile:
        json.dump(fixed_brain_spec_data, outfile)
    with open(fp+fn_moving, 'w') as outfile:
        json.dump(moving_brain_spec_data, outfile)
        
    return fp+fn_fixed, fp+fn_moving

def make_registration_visualization_input_specs( stack, id_detector, structure):
    '''
    Creates the input specification file for the registration visualization script.
    '''
    fp = os.path.join( os.environ['REPO_DIR'], '..', 'demo/')
    
    fn_global = stack+'_visualization_global_alignment_spec.json'
    data = {}
    data["stack_m"] ={
            "name":"atlasV7",
            "vol_type": "score",
            "resolution":"10.0um"
            }
    data["stack_f"] ={
        "name":stack, 
        "vol_type": "score", 
        "resolution":"10.0um",
        "detector_id":id_detector
        }
    data["warp_setting"] = 0

    with open(fp+fn_global, 'w') as outfile:
        json.dump(data, outfile)
        
    fn_structures = stack+'_visualization_per_structure_alignment_spec.json'
    data = {}        
    data[structure] ={
        "stack_m": 
            {
            "name":"atlasV7", 
            "vol_type": "score", 
            "structure": [structure],
            "resolution":"10.0um"
            },
        "stack_f":
            {
                    "name":stack,
                    "vol_type": "score",
                    "structure":[structure],
                    "resolution":"10.0um",
                    "detector_id":id_detector
                    },
        "warp_setting": 7
        }
    with open(fp+fn_structures, 'w') as outfile:
        json.dump(data, outfile)
        
    return fn_structures, fn_global

def create_prep2_section_limits( stack, lower_lim, upper_lim):
    fn = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_data_processed', stack, stack+'_prep2_sectionLimits.ini' )
    f = open(fn, "w")
    f.write('[DEFAULT]\n')
    f.write('left_section_limit = '+str(lower_lim)+'\n')
    f.write('right_section_limit = '+str(upper_lim)+'\n')
    f.close()
    
def call_and_time( command_list, completion_message='' ):
    start_t = time.time()
    subprocess.call( command_list )
    end_t = time.time()
    
    if command_list[0]=='python':
        print('**************************************************************************************************')
        print '\nScript '+command_list[1]+' completed. Took ',round(end_t - start_t,1),' seconds'
        print completion_message +'\n'
        print('**************************************************************************************************')
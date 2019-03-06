#!/usr/bin/env python

import os
import sys
import subprocess
import time


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
    
    file0 = open( fp+fn, 'r')
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
    fn = os.path.join( os.environ['DATA_ROOTDIR'], 'CSHL_simple_global_registration', stack+'_manual_anchor_points.ini' )
    f = open(fn, "w")
    f.write('[DEFAULT]\n')
    f.write('x_12N = '+str(x_12N)+'\n')
    f.write('y_12N = '+str(y_12N)+'\n')
    f.write('x_3N = '+str(x_3N)+'\n')
    f.write('y_3N = '+str(y_3N)+'\n')
    f.write('z_midline = '+str(z_midline))
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
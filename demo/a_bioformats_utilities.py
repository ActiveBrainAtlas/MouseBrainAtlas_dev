#%matplotlib inline
#import matplotlib.pyplot as plt
import time
import numpy as np
import subprocess
import os, sys
import cv2

def get_czi_metadata( czi_fp, get_full_metadata=False ):
    command = ['showinf', '-nopix', czi_fp ]
    # "showinf -nopix" will return the metadata of a CZI file
    czi_metadata_full = subprocess.check_output( command )
    
    if get_full_metadata:
        return czi_metadata_full
    
    # I seperate the metadata into 3 seperate sections
    czi_metadata_header = czi_metadata_full[
        0:czi_metadata_full.index('\nSeries #0')]
    czi_metadata_series = czi_metadata_full[
        0:czi_metadata_full.index('\nReading global metadata')]
    czi_metadata_global = czi_metadata_full[
        czi_metadata_full.index('\nReading global metadata'):]

    # This extracts the 'series' count.
    # Each series is a tissue sample at a certain resolution
    #  or an erroneous thingy
    series_count = int( czi_metadata_header[
        czi_metadata_header.index('Series count = ')+15:] )

    # Series #0 should be the first tissue sample at full resolution.
    # Series #1 tends to be this same tissue sample at half the resolution.
    # This continues halving resolution 5-6 times in succession. We only
    # want the full resolution tissue series so we ignore those with dimensions
    # that are much smaller than expected.
    expected_min_width = 9000
    expected_min_height = 9000

    metadata_dict = {}

    for series_i in range(series_count):
        search_str = 'Series #'

        # If the last series, extract to end of file
        if series_i == series_count-1:
            czi_metadata_series_i = czi_metadata_series[
                czi_metadata_series.index('Series #'+str(series_i)) : ]
        # Otherwise extract metadata from Series(#) to Series(#+1)
        else:
            czi_metadata_series_i = czi_metadata_series[
                czi_metadata_series.index('Series #'+str(series_i)) : 
                czi_metadata_series.index('Series #'+str(series_i+1))]

        # Extract width and height
        width_height_data = czi_metadata_series_i[ czi_metadata_series_i.index('Width'):
                                                   czi_metadata_series_i.index('\n\tSizeZ')]
        width, height = width_height_data.replace('Width = ','').replace('Height = ','').split('\n\t')

        metadata_dict[series_i] = {}
        metadata_dict[series_i]['width'] = width
        metadata_dict[series_i]['height'] = height
        
        # Extract number of channels
        channel_count_index = czi_metadata_series_i.index('SizeC = ')+8
        channel_count = int( czi_metadata_series_i[ channel_count_index: channel_count_index+1] )
        
        metadata_dict[series_i]['channels'] = channel_count
        
        # Extract channel names
        str_to_search = 'Information|Image|Channel|Name #'+str(series_i+1)+': '
        channel_name = czi_metadata_global[czi_metadata_global.index(str_to_search)]
        
    return metadata_dict

def get_fullres_series_indices( metadata_dict ):
    fullres_series_indices = []
    
    last_series_i = max(metadata_dict.keys())
    
    series_0_width = int( metadata_dict[0]['width'] )
    series_0_height = int( metadata_dict[0]['height'] )
    
    for series_curr in metadata_dict.keys():
        # Series 0 is currently assumed to be real, fullres tissue
        if series_curr != 0:
            series_curr_width = int( metadata_dict[series_curr]['width'] )
            series_prev_width = int( metadata_dict[series_curr-1]['width'] )
            
            series_prev_width_halved = series_prev_width/2
            
            # If the curr series is about half the size of the previous series
            # this indicates that it is not a new tissue sample, just a 
            # downsampled version of the previous series.
            if abs( series_curr_width-series_prev_width_halved ) < 5:
                continue
            # If this series is suspisciously small, it is not likely to be fullres
            # Currently this assumed that series#0 is fullres 
            if series_curr_width < series_0_width*0.5:
                continue
                
        # We ignore the last two series.
        # 2nd last should be "label image"
        # last should be "macro image"
        if series_curr >= last_series_i-2:
            continue
                
        fullres_series_indices.append( series_curr )
        
    return fullres_series_indices

def get_list_of_czis_in_folder( folder ):
    command = ['ls', folder]

    possible_czi_files = subprocess.check_output( command ).split( '\n' )
    possible_czi_files.remove('')
    
    czi_files = []

    for file_to_check in czi_files:
        if '.czi' not in file_to_check:
            continue
            #czi_files.remove(file_to_check)
        else:
            czi_files.append(file_to_check)
            
            
    czi_files = []
    
    for possible_czi in os.listdir( folder ):
        if '.czi' in possible_czi:
            czi_files.append(possible_czi)
            
    return czi_files

def print_stars():
    print '********************************'

def extract_tiff_from_czi_all_channels( fn_czi, tiff_target_folder, series_i ):
    # The name of the tiff file
    # %t is time, %z is z height, %s is series #, %c is channel #
    target_tiff_fn = os.path.join( tiff_target_folder, '%n_C%c_W%w.tif' )
    
    command = ['bfconvert', '-bigtiff', '-compression', 'LZW', '-separate', 
               '-series', str(series_i), fn_czi, target_tiff_fn]
    
    subprocess.call( command )


def extract_tiff_from_czi( fn_czi, tiff_target_folder, series_i, channel ):
    # The name of the tiff file
    # %t is time, %z is z height, %s is series #, %c is channel #
    target_tiff_fn = os.path.join( tiff_target_folder, '%n_S%s_C%c_%w.tiff' )
    
    #command = ['bfconvert', '-bigtiff', '-compression', 'LZW', '-separate', 
    #           '-series', str(series_i), '-channel', str(channel), fn_czi, target_tiff_fn]
    
    command = ['bfconvert', '-compression', 'LZW', '-separate', 
               '-series', str(series_i), '-channel', str(channel), fn_czi, target_tiff_fn]
    
    subprocess.call( command )
    
    clean_up_tiff_directory( tiff_target_folder )
    
def clean_up_tiff_directory( tiff_target_folder ):
    # Create path if it doesn't exist
    if not os.path.exists(tiff_target_folder):
        os.makedirs(tiff_target_folder)
    
    for tiff_fn in os.listdir(tiff_target_folder):
        # Do nothing if expected patterns don't show up in the file
        if (not '.czi' in tiff_fn and not '.ndpi' in tiff_fn) or not '.tiff' in tiff_fn:
            continue
            
        old_fn = os.path.join(tiff_target_folder, tiff_fn)
        # Remove unwanted symbols and whatnot
        new_fn = old_fn.replace('.czi #','_S')
        # Read the image we just extracted
        img = cv2.imread( old_fn )
        try:
            # Save the image in its proper format
            cv2.imwrite(new_fn, img[:,:,0] )
            del img
            os.remove( old_fn )
        except Exception as e:
            print old_fn
            print e
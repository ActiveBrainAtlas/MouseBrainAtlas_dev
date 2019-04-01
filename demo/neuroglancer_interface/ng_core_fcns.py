import os
import sys

from ng_utilities import *

sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
from metadata import *
from data_manager import *

import matplotlib.pyplot as plt

import neuroglancer
import cv2

NEUROGLANCER_ROOT = '/media/alexn/BstemAtlasDataBackup/neuroglancer_volumes/'

# For current MD585 stack on neuroglancer
MD585_ng_section_min = 83
MD585_ng_section_max = 352
MD585_ng_total_sections = 268

MD585_s3_offset_from_local_MD585_x = -42
MD585_s3_offset_from_local_MD585_y = 25

# Tranforms volume data to contours
def image_contour_generator( stack, detector_id, structure, use_local_alignment = True, image_prep = 2, threshold=0.5):
    """
    Loads volumes generated from running through the atlas pipeline, transforms them into a set of contours.
    
    Returns the first and last section spanned from the contours, as well as the contour itself which is stored as a dictionary.
    """
    fn_vis_global,fn_vis_structures = create_alignment_specs(stack, detector_id)
    
    if use_local_alignment:
        # Load local transformed volumes
        str_alignment_spec = load_json(fn_vis_structures)[structure]
        vol = DataManager.load_transformed_volume_v2(alignment_spec = str_alignment_spec, 
                                                     return_origin_instead_of_bbox = True,
                                                     structure = structure)
    else:
        # Load simple global volumes
        str_alignment_spec = load_json(fn_vis_global)
        vol = DataManager.load_transformed_volume_v2(alignment_spec = global_alignment_spec, 
                                                                    return_origin_instead_of_bbox = True,
                                                                    structure = structure)


    # Load collection of bounding boxes for every structure
    registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners = \
            load_json(os.path.join(ROOT_DIR, 'CSHL_simple_global_registration', \
                                    stack + '_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json'))
    # Load cropping box for structure. Only need the valid min and max sections though
    (_, _, secmin), (_, _, secmax) = registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners[structure]
    # Load range of sections for particular structure
    valid_secmin = 1
    valid_secmax = 999
    section_margin = 50 # 1000um margin / 20um per slice
    atlas_structures_wrt_wholebrainWithMargin_sections = \
        range(max(secmin - section_margin, valid_secmin), min(secmax + 1 + section_margin, valid_secmax))

    # Choose thresholds for probability volumes
    levels = [threshold]


    # LOAD CONTOURS FROM VOLUME
    str_contour = get_structure_contours_from_structure_volumes_v3(volumes={structure: vol}, stack=stack, 
                                                         sections=atlas_structures_wrt_wholebrainWithMargin_sections,
                                                        resolution='10.0um', level=levels, sample_every=5)

    # Check number sections that the contours are present on 
    str_keys = str_contour.keys()
    valid_sections = []

    for key in str_keys:
        if isinstance(key,int) and key>1:
            valid_sections.append(key)
            # Need to check individual "levels" are on this section as well. 
            #    (0.1 threshold spans more slices than 0.9)
    valid_sections.sort()
    print 'Number of valid sections:'
    num_valid_sections = len(valid_sections)
    print num_valid_sections
    first_sec = valid_sections[0]
    last_sec = valid_sections[len(valid_sections)-1]
    print 'First valid section:',first_sec
    print 'Last valid section:',last_sec
    print 'num_valid_sections:',num_valid_sections
    print '\n\n'

    #print str_contour[ valid_sections[0] ][structure][ levels[0] ]
    
    # LOAD prep5->prep2 cropbox
    if image_prep==5:
        # wholeslice_to_brainstem = -from_padded_to_wholeslice, from_padded_to_brainstem
        ini_fp = os.environ['DATA_ROOTDIR']+'CSHL_data_processed/'+stack+'/operation_configs/from_padded_to_brainstem.ini'
        with open(ini_fp,'r') as fn:
            contents_list = fn.read().split('\n')
        for line in contents_list:
            if 'rostral_limit' in line:
                rostral_limit = int( line.split(' ')[2] )
            if 'dorsal_limit' in line:
                dorsal_limit = int( line.split(' ')[2] )
        ini_fp = os.environ['DATA_ROOTDIR']+'CSHL_data_processed/'+stack+'/operation_configs/from_padded_to_wholeslice.ini'
        with open(ini_fp,'r') as fn:
            contents_list = fn.read().split('\n')
        for line in contents_list:
            if 'rostral_limit' in line:
                rostral_limit = rostral_limit - int( line.split(' ')[2] )
            if 'dorsal_limit' in line:
                dorsal_limit = dorsal_limit - int( line.split(' ')[2] )
        # DONE LOADING PREP5 OFFSETS
    elif image_prep==2:
        rostral_limit = 0
        dorsal_limit = 0

    # PLOT Contours
    contour_str = str_contour[ valid_sections[num_valid_sections/2] ][structure][ levels[0] ]
    # Downsample
    y_len, x_len = np.shape(contour_str)
    x_list = []
    y_list = []
    for y in range(y_len):
        x_list.append(rostral_limit + contour_str[y][0]/32)
        y_list.append(dorsal_limit + contour_str[y][1]/32)

    # PLOT Structure overlayed on thumbnail image
    sorted_fns = DataManager.load_sorted_filenames(stack=stack)[0].keys()
    # fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=5, resol='thumbnail', version='gray', fn=sorted_fns[int(len(sorted_fns)/2)])
    img_fn = metadata_cache['sections_to_filenames'][stack][last_sec-num_valid_sections/2]
    fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=image_prep, resol='thumbnail', version='gray', fn=img_fn)
    
#     img = imread(fp)
#     plt.imshow( img, cmap='gray' )
#     plt.scatter(x_list,y_list,s=1, color='r')
#     plt.show()
    
    return str_contour, first_sec, last_sec



def add_structure_to_neuroglancer( viewer, str_contour, structure, stack, first_sec, last_sec, color_radius=4, xy_ng_resolution_um=10, threshold=0.5, color=1, solid_volume=False, no_offset_big_volume=False, save_results=False, return_with_offsets=False, add_to_ng=True, human_annotation=False ):
    """
    Takes in the contours of a structure as well as the name, sections spanned by the structure, and a list of
    parameters that dictate how it is rendered.
    
    Returns the binary structure volume.
    """
    xy_ng_resolution_um = xy_ng_resolution_um # X and Y voxel length in microns
    color_radius = color_radius*(10.0/xy_ng_resolution_um)**0.5

    # Max and Min X/Y Values given random initial values that will be replaced
    # X and Y resolution will be specified by the user in microns (xy_ng_resolution_umx by y_ng_resolution_um)
    max_x = 0
    max_y = 0
    min_x = 9999999
    min_y = 9999999
    # 'min_z' is the relative starting section (if the prep2 sections start at slice 100, and the structure starts at slice 110, min_z is 10 )
    # Z resolution is 20um for simple 1-1 correspondance with section thickness
    if stack=='MD585':
        max_z = (last_sec-MD585_ng_section_min)
        min_z = (first_sec-MD585_ng_section_min)

        if max_z>MD585_ng_section_max:
            max_z = MD585_ng_section_min
        if min_z<0:
            min_z = 0
    # Scaling factor is (0.46/X). Scaling from resolution of 0.46 microns to X microns. 
    scale_xy = 0.46/xy_ng_resolution_um

    # X,Y are 10um voxels. Z is 20um voxels. 
    # str_contour_ng_resolution is the previous contour data rescaled to neuroglancer resolution
    str_contour_ng_resolution = {}

    for section in str_contour:
        # Load (X,Y) coordinates on this contour
        section_contours = str_contour[ section ][structure][ threshold ]
        # (X,Y) coordinates will be rescaled to the new resolution and placed here
        # str_contour_ng_resolution starts at z=0 for simplicity, must provide section offset later on
        str_contour_ng_resolution[section-first_sec] = []
        # Number of (X,Y) coordinates
        num_contours = len( section_contours )
        # Cycle through each coordinate pair
        for coordinate_pair in range(num_contours):

            curr_coors = section_contours[ coordinate_pair ]
            # Rescale coordinate pair and add to new contour dictionary
            str_contour_ng_resolution[section-first_sec].append( [scale_xy*curr_coors[0],scale_xy*curr_coors[1]] )
            # Replace Min/Max X/Y values with new extremes
            min_x = min( scale_xy*curr_coors[0], min_x)
            min_y = min( scale_xy*curr_coors[1], min_y)
            max_x = max( scale_xy*curr_coors[0], max_x)
            max_y = max( scale_xy*curr_coors[1], max_y)


    # Cast max and min values to int as they are used to build 3D numpy matrix
    max_x = int( np.ceil(max_x) ) 
    max_y = int( np.ceil(max_y) )
    min_x = int( np.floor(min_x) )
    min_y = int( np.floor(min_y) )

    # Create empty 'structure_volume' using min and max values found earlier. Acts as a bounding box for now
    structure_volume = np.zeros( (max_z-min_z, max_y-min_y, max_x-min_x), dtype = np.uint8 )
    z_voxels, y_voxels, x_voxels =  np.shape(structure_volume)
    print  np.shape(structure_volume)

    # Go through every slice. For every slice color in the voxels corrosponding to the contour's coordinate pair
    for slice in range(z_voxels):
        # For Human Annotated files, sometimes there is a missing set of contours for a slice
        try:
            slice_contour = np.asarray( str_contour_ng_resolution[slice] )
        except:
            continue

        for xy_pair in slice_contour:
            x_voxel = int(xy_pair[0])-min_x
            y_voxel = int(xy_pair[1])-min_y
            
            structure_volume[slice,y_voxel,x_voxel] = color

            # Instead of coloring a single voxel, color all in a specified radius from this voxel!
            lower_bnd_offset = int( np.floor(1-color_radius) )
            upper_bnd_offset = int( np.ceil(color_radius) )
            for x_coor_color_radius in range( lower_bnd_offset, upper_bnd_offset):
                for y_coor_color_radius in range( lower_bnd_offset, upper_bnd_offset):

                    x_displaced_voxel = x_voxel + x_coor_color_radius
                    y_displaced_voxel = y_voxel + y_coor_color_radius
                    distance = ( (y_voxel-y_displaced_voxel)**2 + (x_voxel-x_displaced_voxel)**2 )**0.5
                    # If the temporary coordinate is within the specified radius AND inside the 3D matrix
                    if distance<color_radius and \
                    x_displaced_voxel<x_voxels and \
                    y_displaced_voxel<y_voxels and \
                    x_displaced_voxel>0 and \
                    y_displaced_voxel>0:
                        try:
                            # Set temporary coordinate to be visible
                            structure_volume[slice,y_displaced_voxel,x_displaced_voxel] = color
                        except:
                            pass
                        
        if solid_volume:
            structure_volume[slice,:,:] = fill_in_structure( structure_volume[slice,:,:], color )

    # structure_volume

    display_name = structure+'_'+str(threshold)+'_'+str(color)
    
    if stack=='MD585':
        hc_x_offset = MD585_s3_offset_from_local_MD585_x*10/xy_ng_resolution_um
        hc_y_offset = MD585_s3_offset_from_local_MD585_y*10/xy_ng_resolution_um
    true_ng_x_offset = min_x+hc_x_offset
    true_ng_y_offset = min_y+hc_y_offset
    xyz_str_offsets = [true_ng_x_offset, true_ng_y_offset, min_z]
    
    # If instead of a small volume and an offset, we want no offset and an extremely large+sparse volume
    if no_offset_big_volume:
        big_sparse_structure_volume = np.zeros((z_voxels+min_z, y_voxels+true_ng_y_offset, x_voxels+true_ng_x_offset), dtype=np.uint8)
        
        big_sparse_structure_volume[-z_voxels:,-y_voxels:,-x_voxels:] = structure_volume
        
        #big_sparse_structure_volume = np.ones((z_voxels, (y_voxels+true_ng_y_offset)/20, (x_voxels+true_ng_x_offset)/20))
        
        #del structure_volume
        structure_volume = big_sparse_structure_volume
        true_ng_x_offset = 0
        true_ng_y_offset = 0
        min_z = 0
            
            
    if add_to_ng:
        with viewer.txn() as s:
            s.layers[ display_name ] = neuroglancer.SegmentationLayer(
                source = neuroglancer.LocalVolume(
                    data=structure_volume, # Z,Y,X
                    voxel_size=[ xy_ng_resolution_um*1000, xy_ng_resolution_um*1000,20000], # X Y Z
                    voxel_offset = [ true_ng_x_offset, true_ng_y_offset, min_z] # X Y Z
                ),
                segments = [color]
        )
        
    if save_results:
        fp_volume_root = '/media/alexn/BstemAtlasDataBackup/neuroglancer_volumes/'+stack+'/'
        
        if human_annotation:
            fp_volume_root += 'human_annotation/'
        else:
            fp_volume_root += 'registration/'
        if no_offset_big_volume:
            fp_volume_root += 'structure_volumes_'+str(xy_ng_resolution_um)+'um/'
            if not os.path.exists( fp_volume_root ):
                os.makedirs(fp_volume_root)
            np.save( fp_volume_root+structure+'_volume.npy',structure_volume)
        else:
            fp_volume_root += 'structure_volumes_offsets_'+str(xy_ng_resolution_um)+'um/'
            if not os.path.exists( fp_volume_root ):
                os.makedirs(fp_volume_root)
            np.save( fp_volume_root+structure+'_volume.npy',structure_volume)
            # Save offsets
            with open(fp_volume_root+structure+'_offsets.txt', 'w') as offset_file:
                insert_str =  str(min_x+hc_x_offset)+" "+str(min_y+hc_y_offset)+" "+str(min_z)
                offset_file.write(  insert_str )
            offset_file.close()
    
    if return_with_offsets:
        return structure_volume, xyz_str_offsets
    return structure_volume


def fill_in_structure( voxel_sheet, color ):
    contour_coordinates = []
    y_len, x_len = np.shape(voxel_sheet )
    
    for y in range(y_len):
        for x in range(x_len):
            # If this pixel is colored in
            if not voxel_sheet[y,x] == 0:
                contour_coordinates.append( [y,x] )
    
    for y in range(y_len):
        for x in range(x_len):
            has_lr, has_ur, has_ll, has_ul = [False,False,False,False]
            
            for coordinate in contour_coordinates:
                coor_y = coordinate[0]
                coor_x = coordinate[1]
                
                if coor_y < y and coor_x < x:
                    has_ll = True
                if coor_y < y and coor_x > x:
                    has_lr = True
                if coor_y > y and coor_x < x:
                    has_ul = True
                if coor_y > y and coor_x > x:
                    has_ur = True
                    
            if has_lr==True and has_ur==True and has_ll==True and has_ul==True:
                voxel_sheet[y,x] = color
    return voxel_sheet
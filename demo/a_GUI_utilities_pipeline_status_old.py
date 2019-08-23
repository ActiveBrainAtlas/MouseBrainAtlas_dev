import os
import subprocess
from a_driver_utilities import *
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from utilities2015 import *
from registration_utilities import *
from annotation_utilities import *
# from metadata import *
from data_manager import DataManager
from a_driver_utilities import *

import sys
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

necessary_image_files_by_script_ntb = {}

necessary_image_files_by_script_ntb['  initial setup gui'] = {'image_set_1': {'prep_id':'None', 'version':'None', 'resol':'raw'}}

necessary_image_files_by_script_ntb[' a_script_preprocess_setup'] = {'output_file_1':'setup_files'}

necessary_image_files_by_script_ntb['a_script_preprocess_1'] = {'image_set_1': {'prep_id':'None', 'version':'Ntb', 'resol':'raw'},
                                              'image_set_2': {'prep_id':'None', 'version':'Ntb', 'resol':'thumbnail'},
                                              'image_set_3': {'prep_id':'None', 'version':'NtbNormalized', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_2'] = {'image_set_1': {'prep_id':1, 'version':'NtbNormalized', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_3'] = {'image_set_1': 'autoSubmasks'}

necessary_image_files_by_script_ntb['a_script_preprocess_4'] = {'image_set_1': {'prep_id':'None', 'version':'mask', 'resol':'thumbnail'},
                                                               'image_set_2': 'floatHistogram',
                                                               'image_set_3': {'prep_id':'None', 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'}}

necessary_image_files_by_script_ntb['a_script_preprocess_5'] = {'image_set_1': {'prep_id':5, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'},
                                                               'image_set_2': {'prep_id':5, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_6'] = {'image_set_1': {'prep_id':2, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'raw'},
                                                               'image_set_2': {'prep_id':2, 'version':'NtbNormalizedAdaptiveInvertedGamma', 'resol':'thumbnail'},
                                                               'image_set_3': {'prep_id':2, 'version':'mask', 'resol':'thumbnail'}}

necessary_image_files_by_script_ntb['a_script_preprocess_7'] = {'output_file_1': 'atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol',
                                                               'output_file_2': 'registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners'}

necessary_image_files_by_script_ntb['a_script_processing_setup'] = {'output_file_1': 'classifier_setup_files'}
necessary_image_files_by_script_ntb['a_script_processing`'] = {'output_file_1': 'x'}

script_name_to_full_command = { '  initial setup gui': 'Please rerun the new brain setup by rerunning this GUI',
                              ' a_script_preprocess_setup': 'python a_script_preprocess_setup.py $stack $stain',
                              'a_script_preprocess_1': 'python a_script_preprocess_1.py $stack $stain',
                              'a_script_preprocess_2': 'python a_script_preprocess_2.py $stack $stain',
                              'a_script_preprocess_3': 'python a_script_preprocess_3.py $stack $stain',
                              'a_script_preprocess_4': 'python a_script_preprocess_4.py $stack $stain',
                              'a_script_preprocess_5': 'python a_script_preprocess_5.py $stack $stain -l $rostral_limit $caudal_limit $dorsal_limit $ventral_limit',
                              'a_script_preprocess_6': 'python a_script_preprocess_6.py $stack $stain -l $rostral_limit_2 $caudal_limit_2 $dorsal_limit_2 $ventral_limit_2 $prep2_section_min $prep2_section_max',
                              'a_script_preprocess_7': 'python a_script_preprocess_7.py $stack $stain -l $x_12N $y_12N $x_3N $y_3N $z_midline',
                              'a_script_processing_setup': 'python a_script_processing_setup.py $stack $stain $detector_id',
                              'a_script_processing`': 'python a_script_processing.py $stack $stain $detector_id'}

script_name_to_prev_manual_command = { '  initial setup gui': 'Please rerun the new brain setup by rerunning this GUI',
                              ' a_script_preprocess_setup': '',
                              'a_script_preprocess_1': 'python a_script_rotate.py $stack $stain rotate90 raw None None (please confirm rotation type prior to running this, likely wont even be necessary)',
                              'a_script_preprocess_2': '(Check image orientations with outside program)',
                              'a_script_preprocess_3': 'cmd 1:   python $REPO_DIR/gui/preprocess_tool_v3.py $stack --tb_version $img_version_1     cmd 2:   python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1',
                              'a_script_preprocess_4': 'python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1',
                              'a_script_preprocess_5': '(write down the whole brain crop cropbox values, GIMP makes this easy)',
                              'a_script_preprocess_6': '(write down the brainstem crop cropbox values, write down the first and last image numbers that contain the brainstem, GIMP makes the first part easy)',
                              'a_script_preprocess_7': 'python $REPO_DIR/gui/brain_labeling_gui_v28.py $stack --img_version $img_version_2',
                              'a_script_processing_setup': '',
                              'a_script_processing`': ''}

def all_img_files_valid( stack, prep_id='None', version='Ntb', resol='thumbnail' ):
    all_files_valid = True
    corrupted_files = []

    filenames_list = DataManager.load_sorted_filenames(stack)[0].keys()
    for img_name in filenames_list:
        img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=img_name)

        try:
            img = cv2.imread(img_fp)
            # If length of the image size is zero, it's corrupted
            if len(np.shape(img))==0:
                all_files_valid = False
                corrupted_files.append(img_name)
                continue
        except Exception as e:
            all_files_valid = False
            print(e)
            corrupted_files.append(img_name)

    return all_files_valid, corrupted_files

def all_img_files_present( stack, prep_id='None', version='Ntb', resol='thumbnail' ):
    all_files_present = True
    missing_files = []

    filenames_list = DataManager.load_sorted_filenames(stack)[0].keys()
    for img_name in filenames_list:
        img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=img_name)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_name)

    return all_files_present, missing_files

def all_autoSubmasks_present( stack ):
    all_files_present = True
    missing_files = []
    for fn in metadata_cache['filenames_to_sections'][stack].keys():
        sec = metadata_cache['filenames_to_sections'][stack][fn]
        img_fp = DataManager.get_auto_submask_filepath(stack=stack, what='submask', submask_ind=0,
                                                      fn=fn, sec=sec)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_fp)
    return all_files_present, missing_files

def all_adaptive_intensity_floatHistograms_present( stack ):
    all_files_present = True
    missing_files = []
    for fn in metadata_cache['filenames_to_sections'][stack].keys():
        sec = metadata_cache['filenames_to_sections'][stack][fn]
        img_fp = DataManager.get_intensity_normalization_result_filepath(what='float_histogram_png', stack=stack,
                                                                         fn=fn, section=sec)
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_fp)
    return all_files_present, missing_files

def all_setupFiles_present( stack ):
    all_files_present = True
    missing_files = []

    # Check atlas is downloaded
    for struct in all_known_structures_sided:
        img_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_volumes', 'atlasV7',
                              'atlasV7_10.0um_scoreVolume', 'score_volumes', 'atlasV7_10.0um_scoreVolume_'+struct+'.bp' )
        if not os.path.isfile( img_fp ):
            all_files_present = False
            missing_files.append(img_fp)
            
    # Check operation configs
    op_config_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_data_processed', stack, 'operation_configs' )
    for op_config_name in ['from_aligned_to_none.ini', 'from_aligned_to_padded.ini', 'from_none_to_aligned.ini', 
                           'from_none_to_brainstem.ini', 'from_wholeslice_to_brainstem.ini', 'from_padded_to_wholeslice.ini', 
                           'from_padded_to_none.ini', 'from_padded_to_brainstem.ini', 'from_none_to_wholeslice.ini']:
        if not os.path.isfile( os.path.join( op_config_fp, op_config_name) ):
            all_files_present = False
            missing_files.append( os.path.join( op_config_fp, op_config_name) )
            
    return all_files_present, missing_files

def all_setupFiles_present_classifier( stack ):
    all_files_present = True
    missing_files = []
    
    # check for mxnet files
    
    # check for classifier files
    #local_fp = os.path.join( os.environ['ROOT_DIR'], 'CSHL_classifiers', 'setting_'+str(id_classifier), 'classifiers/')
            
    return all_files_present, missing_files

def check_for_file( file_to_check, stack ):
    all_files_present = True
    missing_files = []

    if file_to_check=='atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol':
        fp = os.path.join(os.environ['ROOT_DIR'], 'CSHL_simple_global_registration',
            stack + '_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.txt')
        if not os.path.isfile( fp ):
            all_files_present = False
            missing_files.append(fp)
    elif file_to_check=='registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners':
        fp = os.path.join(os.environ['ROOT_DIR'], 'CSHL_simple_global_registration',
            stack + '_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json')
        if not os.path.isfile( fp ):
            all_files_present = False
            missing_files.append(fp)
    return all_files_present, missing_files

def get_text_of_pipeline_status( stack, stain ):
    text = ""
    all_correct = True

    for script_name in sorted(necessary_image_files_by_script_ntb.keys()):

        for image_set in necessary_image_files_by_script_ntb[script_name].keys():

            contents = necessary_image_files_by_script_ntb[script_name][image_set]

            if type(contents)==str:
                if contents=='setup_files':
                    all_files_present, missing_files = all_setupFiles_present( stack )
                elif contents=='autoSubmasks':
                    all_files_present, missing_files = all_autoSubmasks_present( stack )
                elif contents=='floatHistogram':
                    all_files_present, missing_files = all_adaptive_intensity_floatHistograms_present( stack )
                elif contents=='atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol':
                    all_files_present, missing_files = check_for_file( contents, stack )
                elif contents=='registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners':
                    all_files_present, missing_files = check_for_file( contents, stack )
                elif contents=='classifier_setup_files':
                    all_files_present, missing_files = all_setupFiles_present_classifier( stack )
            else:
                prep_id = contents['prep_id']
                version = contents['version']
                resol = contents['resol']
                if version=='None':
                    version = None
                all_files_present, missing_files = all_img_files_present( \
                                         stack, prep_id=prep_id, version=version, resol=resol )

            if all_files_present:
                #text += script_name + " " + image_set + " has been run successfully!\n"
                pass
            else:
                num_missing_files = len(missing_files)
                num_total_files = len(DataManager.load_sorted_filenames(stack)[0].keys())
                if num_missing_files == num_total_files:
                    text += "" + script_name + " is the next script you need to run.\n"
                    all_correct = False
                    break

                for fn in missing_files[0]:
                    img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=fn)
                    img_root_fp = img_fp[0:img_fp.rfind('/')+1]
                #text += "\n"+script_name + " " + image_set + " is missing files:\n\n"
                text += "\n" + script_name + " did not run properly and has missing files:\n"
                text += "(" + str(num_missing_files) + " missing out of "+str(num_total_files)+")\n\n"
                text += "Missing Directory:   "+img_root_fp+"\n\n"
                #text += "`" + img_root_fp + "` is the image directory in which there are the following missing files:\n\n"
                text += "Missing Files:\n"
                missing_files.sort()
                for fn in missing_files:
                    img_fp = DataManager.get_image_filepath_v2(stack=stack, prep_id=prep_id, resol=resol, version=version, fn=fn)
                    text += fn+"\n"
                all_correct = False
                break
        if not all_correct:
            break
        elif all_correct:
            if script_name=='a_script_processing`':
                text += script_name + " runs the brain through the classifiers and fits the atlas to the images. Ready to run!"
            else:
                text += script_name + " has been run successfully!\n\n"

    return text, script_name

def get_script_command( curr_script_name, stack, stain, detector_id, script_or_manual ):
    if script_or_manual=='script':
        script_str = script_name_to_full_command[curr_script_name]
    elif script_or_manual=='manual':
        script_str = script_name_to_prev_manual_command[curr_script_name]
        resolution = stack_metadata[stack]['resolution']
        if curr_script_name == 'a_script_preprocess_7' and float(resolution) != 0.46:
            script_str = script_str + ' --resolution 1um'
    
    script_str = script_str.replace('$stack', stack)
    script_str = script_str.replace('$stain', stain)
    script_str = script_str.replace('$detector_id', detector_id)
    
    if stain.lower()=='thionin':
        img_version_1 = 'gray'
        img_version_2 = 'gray'
    if stain.lower()=='ntb':
        img_version_1 = 'NtbNormalized'
        img_version_2 = 'NtbNormalizedAdaptiveInvertedGamma'

    script_str = script_str.replace('$img_version_1', img_version_1)
    script_str = script_str.replace('$img_version_2', img_version_2)
    
    script_str = script_str.replace('$REPO_DIR', os.environ['REPO_DIR'])
    script_str = script_str.replace('$ROOT_DIR', os.environ['ROOT_DIR'])
    
    script_str = script_str.replace('//', '/')
    
    return script_str
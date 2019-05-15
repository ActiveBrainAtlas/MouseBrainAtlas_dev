import sys, os
import argparse
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'utilities'))
from data_manager import *
from a_driver_utilities import *

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='')
parser.add_argument("stack", type=str, help="The name of the stack")
args = parser.parse_args()
stack = args.stack

# Prompt for copying all files over
def prompt_for_choice( prompt_message, list_of_choices):
    answer = None
    while answer not in list_of_choices:
        answer = raw_input( prompt_message ).lower()

        if answer in list_of_choices:
            break
        else:
            print('Please choose a response from the given options.')
    return answer
def get_selected_fp( initialdir=os.environ['ROOT_DIR'], default_filetype=("jp2 files","*.jp2") ):
    # Use tkinter to ask user for filepath to jp2 images
    from tkinter import filedialog
    from tkinter import *
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = initialdir,\
                                                title = "Select file",\
                                                filetypes = (default_filetype,("all files","*.*")))
    fn = root.filename
    root.destroy()
    return fn

# Create the CSHL_data_processed/<STACK>/<STACK>_raw/ directory
try:
    raw_stack_dir = DataManager.get_image_filepath_v2(stack, None, version=None, resol="raw", fn=fn)
    os.makedirs( raw_stack_dir[0:max(loc for loc, val in enumerate(raw_stack_dir) if val == '/')] )
except:
    pass

# Prompt for moving sorted_filenames.txt
sorted_fns_fp = DataManager.get_sorted_filenames_filename(stack)
try:
    with open( sorted_fns_fp, 'r') as file:
        sorted_fns = file.read()
except:
    print('')
    print('_________________________________________________________________________________')
    print('_________________________________________________________________________________')
    print('Sorted filenames not found at proper location.')
    print('Ensure that the following file exists: '+sorted_fns_fp)
    print('_________________________________________________________________________________')
    print('_________________________________________________________________________________')
    print('\n********** copying sorted_fns **********')
    yes_no_choices = ['yes', 'no']
    answer = prompt_for_choice( "Do you want to copy sorted_filenames over? (yes/no) : ", yes_no_choices)
    if answer=='yes':
        print('\nPlease navigate to the sorted_filenames.txt .\n')    
        sorted_fns_current_loc = get_selected_fp( initialdir = os.environ['ROOT_DIR'], default_filetype=("txt files","*.txt") )
        
        try:
            true_fp = sorted_fns_fp[0:max(loc for loc, val in enumerate(sorted_fns_fp) if val == '/')+1]
            os.makedirs( true_fp )
        except Exception as e:
            print(e)
            pass
    
        command = ["cp", sorted_fns_current_loc, sorted_fns_fp]
        completion_message = 'Successfully copied sorted_filenames.txt over.'
        call_and_time( command, completion_message=completion_message)
    elif answer=='no':
        sys.exit()



print('\n********** jp2 -> tiff **********')
yes_no_choices = ['yes', 'no']
answer = prompt_for_choice( "Do you need to convert raw jp2 images to tiff? (yes/no) : ", yes_no_choices)
if answer=='yes':
    # Prompt user to navigate to the filepath containing the jp2 images
    print('\nPlease navigate to the filepath containing all jp2 images and click any arbitrary image.\n')    
    
    fn = get_selected_fp( initialdir=os.environ['ROOT_DIR'], default_filetype=("jp2 files","*.jp2") )
    jp2_fp = fn[0:max(loc for loc, val in enumerate(fn) if val == '/')]
    
    # Use name of jp2 image to find how the resolution is encoded
    if 'raw' in fn:
        resolution = '_raw'
    elif 'lossless' in fn:
        resolution = '_lossless'
    else:
        resolution = ''
    
    # CONVERT *.jp2 to *.tif
    json_fn = stack+'_raw_input_spec.json'
    
    json_data = [{"version": None, \
                 "resolution": "raw", \
                 "data_dirs": jp2_fp, \
                 "filepath_to_imageName_mapping": jp2_fp+"/(.*?)"+resolution+".jp2", \
                 "imageName_to_filepath_mapping": jp2_fp+"/%s"+resolution+".jp2"}]
    with open( json_fn, 'w') as outfile:
        json.dump( json_data, outfile)
    command = ["python", "jp2_to_tiff.py", stack, json_fn]
    completion_message = 'Completed converting jp2 to tiff for all files in folder.'
    call_and_time( command, completion_message=completion_message)
    
elif answer=='no':
    print('\n********** copy and rename raw tiffs **********')
    yes_no_choices = ['yes', 'no']
    answer = prompt_for_choice( "Do you want to copy and rename a set of raw tiff files? (yes/no) : ", yes_no_choices)
    
    if answer=='yes':
        # Prompt user to select a tiff file in the proper fodler
        fn = get_selected_fp( initialdir=os.environ['ROOT_DIR'], default_filetype=("tiff files","*.tif*") )
        #raw_tiff_sample_fn = fn[max(loc for loc, val in enumerate(fn) if val == '/')+1:len(fn)]
        raw_tiff_input_fp = fn[0:max(loc for loc, val in enumerate(fn) if val == '/')]
        raw_tiff_input_fns = os.listdir( raw_tiff_input_fp )

        filenames_list = DataManager.load_sorted_filenames(stack)[0].keys()
        # Rename and copy over all tiff files in the selected folder
        for fn in filenames_list:
            for raw_tiff_input_fn in raw_tiff_input_fns:
                if fn in raw_tiff_input_fn:
                    old_fp = os.path.join( raw_tiff_input_fp, raw_tiff_input_fn )
                    new_fp = DataManager.get_image_filepath_v2(stack, None, version=None, resol="raw", fn=fn)
                    command = ["cp", old_fp, new_fp]
                    completion_message = 'Finished copying and renaming all tiff files into the proper location.'
                    call_and_time( command, completion_message=completion_message)
        
    elif answer=='no':
        pass
    
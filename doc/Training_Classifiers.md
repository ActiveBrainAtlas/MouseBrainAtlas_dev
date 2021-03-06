## Classifier Training

Training the NN classifiers requires having all prep2 (preprocessed and brainstem cropped) images downloaded for all testing and training stacks. Classifiers are typically trained on and for specific stains, the two most used being NTB and Thionin stains. In addition to the images themselves, files containing segmented regions of interest must be supplied. Square patches are extracted from these regions and are used to train the classifier. Finally a "windowing_id" must be supplied, which dictates the size of the square patches as well as their seperations.

There are two major scripts outlined below, they are driven by a notebook located at `src/learning/a_learning_driver.ipynb`. Before running anything, ensure that the virtual environment is setup by running `$ source setup/config.sh`

### identify_patch_class_based_on_labeling_v3_human_annotations
Script Location: `/src/learning/identify_patch_class_based_on_labeling_v3_human_annotations.py`

Required Files:
- `ROOT_DIR/CSHL_data_processed/<STACK>/<STACK>_prep2_thumbnail_mask/*_prep2_thumbnail_mask.png`
- `ROOT_DIR/CSHL_data_processed/<STACK>/<STACK>_prep2_raw_gray/*_prep2_raw_gray.tif`
- `ROOT_DIR/CSHL_labelings_v3/<STACK>/<STACK>_annotation_contours_<TIMESTAMP>.hdf`
  - Contains professional annotation indices which are converted to grid points
Outputs
- Output: `ROOT_DIR/CSHL_labelings_v3/<STACK>/<STACK>_annotation_win<WIN_ID>_<TIMESTAMP>_grid_indices_lookup.hdf`

This script will create a table that takes in a structure and a slice, and returns a list of grid indices. The grid indices each correspond to a patch image foubnd on a slice. Prep2 masks are loaded in for the stack to only use grid indices that are located on the brain and not the background. These grid indices now let you easily load patches for each structure to be used by the CNN for training and testing.

### a_train_and_test_classifier_performance_v4
Script Location: `/src/learning/a_train_and_test_classifier_performance_v4.py`

Note: this is intended to be replaced with the newer and more robust "v5", however this will take some time.

Required Files:
- Same dependencies as previous scripts, with some additional dependencies
- `ROOT_DIR/CSHL_patch_features/inception-bn-blue/<STACK>/<STACK>_prep2_none_win8/*_prep2_none_win8_inception-bn-blue_features.bp`
- `ROOT_DIR/CSHL_patch_features/inception-bn-blue/<STACK>/<STACK>_prep2_none_win8/*_prep2_none_win8_inception-bn-blue_locations.bp`

Results:
- Output: `$ROOT_DIR/assessment_results_v3/assessment_result_<ID>.pkl`

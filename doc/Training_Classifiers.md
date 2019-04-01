## Classifier Training

Training the NN classifiers requires having all prep2 (preprocessed and brainstem cropped) images downloaded for all testing and training stacks. Classifiers are typically trained on and for specific stains, the two most used being NTB and Thionin stains. In addition to the images themselves, files containing segmented regions of interest must be supplied. Square patches are extracted from these regions and are used to train the classifier. Finally a "windowing_id" must be supplied, which dictates the size of the square patches as well as their seperations.

Required scripts:
  - `/src/learning/identify_patch_class_based_on_labeling_v3_human_annotations.py`
    - Loads human annotation contours, and image files
      - Required: `ROOT_DIR/CSHL_data_processed/<STACK>/<STACK>_prep2_thumbnail_mask/*_prep2_thumbnail_mask.png`
      - Required: `ROOT_DIR/CSHL_data_processed/<STACK>/<STACK>_prep2_raw_gray/*_prep2_raw_gray.tif`
      - Required: `ROOT_DIR/CSHL_labelings_v3/<STACK>/<STACK>_annotation_contours_<TIMESTAMP>.hdf`
    - Outputs grid indices lookup table
      - Output: `ROOT_DIR/CSHL_labelings_v3/<STACK>/<STACK>_annotation_win<WIN_ID>_<TIMESTAMP>_grid_indices_lookup.hdf`
  - `/src/learning/a_train_and_test_classifier_performance_v5.py`


`src/learning/train_and_test_classifier_performance_v5.ipynb`, [Link](http://132.239.73.85:8888/notebooks/src/learning/train_and_test_classifier_performance_v5.ipynb).

The code is general but we only have the annotations for 3 brains to train from.

Run the first two cells. The next cell loads the pre-trained inception network

Requires human annotation files, got from `/ROOT_DIR/CSHL_labelings_v3/MD585/`. Only need the latest .hdf file (contains "contours" string).

Now we generate another necessary file:
Go to `src/learning/identify_patch_class_based_on_labeling_v3.ipynb`, [Link](http://132.239.73.85:8888/notebooks/src/learning/identify_patch_class_based_on_labeling_v3.ipynb).

Run the "# Based on contour annotation" part. Change stack to only MD585 and uncomment the bottom part of the main cell

Need to add brain in metadata.py, add brain info (change resolutiion to 0.46)

Once the cell finishes running, inspect grid_index_class_lookup. `grid_index_class_lookup['10N'][179]`, using pandas. Code should save it as an hdf.

Go back to `src/learning/train_and_test_classifier_performance_v5.ipynb`. You will need to make the following changes to train and test from the same brain:
- train_stacks = ['MD585']
- test_stacks  = ['MD585']
- win_id must be the same as before

Inspecting the result:
It is basically a dict {stack: the dataframe like before}
If we have more train_brains or test_brains it will have more keys


## Update atlas

`src/registration/update_atlas.ipynb`

We used detector 799 and classifier 899

## Detector

Detector settings are encoded in a number according to [Detector_settings.csv](https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/learning/detector_settings.csv)

These are the relevant fields: 
- detector_id
- input_version
- windowing_id
- feature_network
- feature_classifier_id

Known classifiers: One used for Ntb (899), one for Thionin. The Ntb classifier can be used on Thionin brains after intensity normalization, but will not work quite as well. The other classifier was trained on 3 thionin brains: MD585/MD589/MD594, but does not exist on any server (may have been deleted entirely).


Detector/classifier settings are read in [metadata line 509](https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/utilities/metadata.py#L535)

`window_id`: It defines a particular mapping between location and gridpoint index. For example, say windowing_id =7, then patch_size_um = 103.04 for 0.46um/pixel images correspond to patch size of 224 pixel. The grid point with index 0 will be at coordinate (112, 112), spacing is 30 um which translates to 65 pixels, so the grid point with index 1 will be at coordinate (112 + 65, 112) .... Each grid point is associated a square image patch and the point is the center of the patch. Each index maps to a feature vector, as a result of "feature extraction".

### Inception-bn-blue feature vectors

Located in `/CSHL_patch_features/inception-bn-blue/STACK/STACK_prep2_none_win#/`

Open any location.bp (They should be txt, for some reason was named bp and stuck)

Row number is the grid point index. The two values are x and y pixel coordinates. Only the grid points that are ON the binary masks are listed here. Each row directly matches the same row in `features.bp` (if you read it in notebook, it is a  n x 1024 matrix). Now back to detector setting 

`feature_classifier_id`: Specifies any machine learning decision model that takes a feature vector and output a score. This can be SVM, can be decision tree, logistic regression, or boosting classifier: any f for y = f(x).

In /CSHL_classifiers there are serialized sklearn.logistic_regression objects. You can load them as you load any sklearn model.

## Classifier

The classifier settings encode a "model", or "trained classifier".


Now return to src/learning
Open [Classifier_settings.csv](https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/learning/classifier_settings.csv)

Classifier 899 is not in it as classifier_settings.csv became documentation. The pipeline is not reading anything from it.

### Classifier Training

`src/learning/train_and_test_classifier_performance_v5.ipynb`, [Link](http://132.239.73.85:8888/notebooks/src/learning/train_and_test_classifier_performance_v5.ipynb).

The code is general but we only have the annotations for 3 brains to train from.

Run the first two cells. The next cell loads the pre-trained inception network

Requires human annotation files, got from `/ROOT_DIR/CSHL_labelings_v3/MD585/`. Only need the latest .hdf file ("The contours one").

Now we generate another necessary file:
Go to `src/learning/identify_patch_class_based_on_labeling_v3.ipynb`, [Link](http://132.239.73.85:8888/notebooks/src/learning/identify_patch_class_based_on_labeling_v3.ipynb).

Run the "# Based on contour annotation" part. Change stack to only MD585 and uncomment the bottom part of the main cell

Need to add brain in metadata.py, add brain info (change resolutiion to 0.46)

Create a symbolic link in CSHL_Data_processed called MD585 and point it to Yuncong's HDD. Following command works:
`ln -s /media/yuncong/BstemAtlasData/atlas_data/CSHL_data_processed/MD585 <your_path>/CSHL_data_processed/MD585`


Once the cell finishes running, inspect grid_index_class_lookup. `grid_index_class_lookup['10N'][179]`, uses pandas, need to know how to index into DataFrame. Code should save it as an hdf.

Go back to `src/learning/train_and_test_classifier_performance_v5.ipynb`. You will need to make the following changes to train and test from the same brain:
- train_stacks = ['MD585]
- test_stacks  = ['MD585]
- win_id must be the same as before

Inspecting the result:
It is basically a dict {stack: the dataframe like before}
If we have more train_brains or test_brains it will have more keys


## Update atlas

`src/registration/update_atlas.ipynb`

## Detector

Detector settings are encoded in a number according to [Detector_settings.csv](https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/learning/detector_settings.csv)

These are the relevant fields: 
- detector_id
- input_version
- windowing_id
- feature_network
- feature_classifier_id

| detector_id	|	input_version |	windowing_id |	feature_network |	feature_classifier_id |	comments	|
|-------------|---------------|------------|------------------|-----------------------|-----------|
|15 |	gray |	5 |	inception-bn-blue |	73 |	NaN |
|19 |	gray |	7 |	inception-bn-blue |	73 |	NaN |
|799 |	NtbNormalizedAdaptiveInvertedGamma |	7 |	inception-bn-blue |	899 |	NaN |
|998 |	normalized_-1_5 |	7 |	inception-bn-blue |	998 |	trained using normalized MD589/MD594/MD585 wit... |
|999 |	normalized_-1_5 |	7 |	inception-bn-blue |	999 |	trained from auto-aligned MD661/MD662 before c... |

There are separate classifiers for Ntb and Thionin brains. The Ntb classifier can be used on Thionin brains after intensity normalization, but will not work quite as well.
  - Detector 799, used for Ntb, uses classifier 899
  - Detector 19, used for Thionin, uses classifier 73
    - Trained on brains MD585/MD589/MD594

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


## Update atlas

`src/registration/update_atlas.ipynb`

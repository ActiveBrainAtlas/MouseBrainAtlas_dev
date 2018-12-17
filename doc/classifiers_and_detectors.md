We used detector 799 and classifier 899

## Detector

"We settled on using two sets of classifiers. One for thionin, one for Ntb."

"The MD585 results  I obtained look OK for 3N/4N/12N but I actually used the Ntb classifier on it
So it is not optimal, may or may not work well for other structures
We had another set of classifiers trained using 3 thionin brains MD585/MD589/MD594
but due to the accidental data loss a while back (remember?), they are gone and need to be re-generated
We can take this opportunity to teach you how to deal with the classifier related stuff (mainly training)
We also have yet to talk about how to initialize structure shapes, initialize positions, and update positions.
You have read the paper, so you should have some ideas about which aspects of this pipeline we never touched upon, right?
I suggest you think big for this moment, and lay out all things you would like me to teach you
I can then work with you to prioritize things
I think the best strategy is for you to have at least an superficial understanding of all things, rather than deep understanding of a few things and zero on others."


"If you go to 'src/learning/'
there are two files "detector_settings" and "classifier_settings"
They are CSV files"

Where detector/classifier settings are read: https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/yuncong_demo/src/utilities/metadata.py#L535

"window_id: It defines a particular mapping between location and gridpoint index
 a particular mapping between x-y coordinates and gridpoint index
"

"For example, say windowing_id =7, then 
side note: 7 is the one used in the paper right?
patch_size_um = 103.04 for 0.46um/pixel images correspond to patch size of 224 pixel
The grid point with index 0 will be at coordinate (112, 112)
spacing is 30 um which translates to 65 pixels, so the grid point with index 1 will be at coordinate (112 + 65, 112) ....
Each grid point is associated a square image patch
The point is the center of the patch

Each index maps to a feature vector, as a result of "detection"
sorry, as a result of "feature extraction" "

Detector_settings: https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/learning/detector_settings.csv 



"
Now go to /media/yuncong/BstemAtlasData/atlas_data/CSHL_patch_features

Go into the model "inception-bn-blue"
Go to UCSD001
Go to bottom level
Open any location.bp
(They should be txt, for some reason was named bp and stuck)
Row number is the grid point index
The two values are x and y pixel coordinates
Only the grid points that are ON the binary masks are listed here
Each row directly matches the same row in `features.bp` (if you read it in notebook, it is a  n x 1024 matrix)
Now return to detector setting 
"

"
Now "feature_classifier_id"
This is the "classifier"
as opposed to "detector"
This specifies any machine learning decision model that takes a feature vector and output a score
This can be SVM, can be decision tree, logistic regression, or boosting classifier
any f for y = f(x)
"

"
Now go to /media/yuncong/BstemAtlasData/atlas_data/CSHL_classifiers
You now should understand what are in it
They are serialized sklearn.logistic_regression objects
You can load them as you load any sklearn model
OK. Now you have fully understood detector_settings.csv
"

## Classifier

"
Basically, it is a "model" as we  call it in machine learning
or a "classifier"
"TRAINED classifier"

Now return to src/learning
Open "classifier_settings.csv"

hmm, why was 899 not in it...I am confused...
OK, I think classifier_settings.csv eventually became just a documentation. The pipeline is not reading anything from it.
IGNORE classifier_settings.csv
"

Classifier_settings: https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/master/src/learning/classifier_settings.csv


### Classifier Training

"
Go to src/learning/train_and_test_classifier_performance_v5.ipynb
The code is general but we only have the annotations for 3 brains 

Run the first two cells
The next cell loads the pre-trained inception network

>I was missing human annotation files, got from /home/yuncong/CSHL_labelings_v3/MD585<

I think you only need the latest hdf
The contours one

Now we generate another necessary file:
Go to src/learning/identify_patch_class_based_on_labeling_v3.ipynb

Run the "# Based on contour annotation" part
CHange stack  to only MD585
Uncomment the bottom part of the main cell

Need to add brain in metadata.py, add brain info (change resolutiion to 0.46)

Create a symbolic link in CSHL_Data_processed
called MD585 and point it to mine
ln -s /media/yuncong/BstemAtlasData/atlas_data/CSHL_data_processed/MD585 <your_path>/CSHL_data_processed/MD585


Wait for it to finish
Then inspect grid_index_class_lookup

You ever used pandas befoer?
know howto index into DataFrame?
grid_index_class_lookup['10N'][179]

Code should save it as an hdf.

Now go to "train_and_test_classifier_performance_v5"
You will need to make train_stacks = ['MD585]
test_stacks  = ['MD585]
basically train and test using the same one brain for now

win_id must be the same as before

OK, inspect the result
It is basically a dict {stack: the dataframe like before}
If we have more train_brains or test_brains it will have more keys
"




## Update atlas

src/registration/update_atlas.ipynb

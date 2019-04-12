Note: Script names may change when the code is officially released. The current names are iterative using the order the scripts are meant to be run. The prepended `a_script_preprocess` is simply to organize the scripts together while in development.

These scripts assume the stack has been given a name (example stack="MD585"), and the associated stain for each set of images has been defined (stain="NTB" or stain="Thionin" are the two current options). As a shorthand when referring to these stains, I will define T = Thionin and NTB = Neurotrace Blue.


# Preprocessing Scripts

The single setup script and seven preprocessing scripts are spaced with user intervention steps such that the first script is run, the user is required to perform some step by hand, then the second script is run, etc... For every script there is listed the command to run it, a brief description of what the script does, and the manual step for the user after completion.

- if stain=='Thionin':
    - img_version_1 = 'gray'
    - img_version_2 = 'gray'
- if stain=='NTB':
    - img_version_1 = 'NtbNormalized'
    - img_version_2 = 'NtbNormalizedAdaptiveInvertedGamma'


### Setup Script
---
__Command__: `python a_script_preprocess_setup.py $stack`

__Description__: 


### Script 1
---
__Command__: `python a_script_preprocessing_1.py $stack $stain`

__Description__: Converts images from .jp2 format to .tiff format. Extracts the blue channel for slides stained with T or NTB. NTB slides are intensity normalized. 32x downsampled thumbnails are generated for every image.

__User step__: Check slice orientations with GIMP/ImageJ/Photoshop/etc.. All slices must be cut sagittally, roughly oriented with the rostral side on the left, and slices must begin on the left hemisphere of the brain.


### Script 2
---
__Command__: `python a_script_preprocessing_2.py $stack $stain --anchor_fn $anchor_image_filename`

__Description__: Generates image translation and rotation alignment parameters, one "anchor" file is chosen which all other images are aligned to. User can choose to pass an images filename in to be the anchor image, otherwise the anchor image will be chosen automatically. Image alignment parameters are applied and the new aligned image stack is saved as so called "prep1" images. The background is padded white for T stain and black for NTB stain.

__User step__: Manually fix incorrect alignments. The image alignment scripts is imperfect and has an error rate of 5-10%. The incorrectly aligned slides must be aligned and saved by hand. The built in GUI can be run using `python $REPO_DIR/gui/preprocess_tool_v3.py $stack --tb_version $img_version_1`. Gui guide link (incomplete).

__User step 2__: Create initial segmentation outlines of the brain for every slice with the following command, `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`. Gui guide link (incomplete).


### Script 3
---
__Command__: `python a_script_preprocessing_3.py $stack $stain`

__Description__: Generates binary masks for every image to segment the pixels containing the brain using the user's initial segmentation outline for assistance.

__User step__: Manually correct the generated masks with the following command, `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1` and save these prep1 thumbnail image masks. Gui guide link (incomplete).


### Script 4
---
__Command__: `python a_script_preprocessing_4.py $stack $stain`

__Description__: Creates "original_image_crop.csv" file which contains the dimensions of every thumbnail (32x downsampled) image. Applies reverse prep1 transforms on all masks and saves these unaligned masks in the original orientation of the images. Applies a local adaptive intensity normalization on NTB images.

__User step__: User specifies prep5 cropping box.


### Script 5
---
__Command__: `python a_script_preprocessing_5.py $stack $stain`

__Description__: 

__User step__: User specifies prep2 cropping box.


### Script 6
---
__Command__: `python a_script_preprocessing_6.py $stack $stain`

__Description__: 

__User step__: Record X/Y/Z coordinates for midpoint of 12N, 3N_R on midplane.


### Script 7
---
__Command__: `python a_script_preprocessing_7.py $stack $stain`

__Description__: 


# Structure Registration Scripts

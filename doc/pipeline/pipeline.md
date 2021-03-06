Note: Script names may change when the code is officially released. The current names are iterative using the order the scripts are meant to be run. The prepended `a_script_preprocess` is simply to organize the scripts together while in development.

These scripts assume the stack has been given a name (example stack="MD585"), and the associated stain for each set of images has been defined (stain="NTB" or stain="Thionin" are the two current options). As a shorthand when referring to these stains, I will define T = Thionin and NTB = Neurotrace Blue. When `$stain` is used, this should be replaced by the name of your stack, this also goes for `$stain` and every other variable that starts with a dollar sign `$`.


# Preprocessing Scripts
---------------------------

## Description

The single setup script and seven preprocessing scripts are spaced with user intervention steps such that the first script is run, the user is required to perform some step by hand, then the second script is run, etc... For every script there is listed the command to run it, a brief description of what the script does, and the manual step for the user after completion.

## Variable Glossary

- if stain=='Thionin':
    - `$img_version_1` = 'gray'
    - `$img_version_2` = 'gray'
- if stain=='NTB':
    - `$img_version_1` = 'NtbNormalized'
    - `$img_version_2` = 'NtbNormalizedAdaptiveInvertedGamma'
- `$REPO_DIR` = '/home/alexn/brainDev'
- `$ROOT_DIR` = '/media/alexn/Data_2/Atlas_Root_Dirs/Duke_Brains'
    
## Scripts

---------------------------
### Setup Script
---------------------------
__Command__: `python a_script_preprocess_setup.py $stack $stain`

__Description__: Downloads the following files from S3: operation configs, mxnet files, atlas version 7 volume, classifier settings.

---------------------------
### Prepare Images
---------------------------
__Rotation__: Some images will need to be rotated such that they are oriented with the rostral side on the left, caudal on the right, for sagittal sections. Images should be rotated as needed to make this true. The below command will rotate (clockwise, always) every single image by 90 degrees. the rotation options are: `rotate90`, `rotate180`, and `rotate270`. `python a_script_rotate.py $stack $stain rotate90 raw None None` (~40 seconds per image)

__Flipping__: Run the following command to mirror each image acroos a vertical line drawn down the center of the image.
    - `python a_script_rotate.py $stack $stain flip raw None None` (~40 seconds per image)

---------------------------
### Script 1
---------------------------
__Command__: `python a_script_preprocess_1.py $stack $stain`

__Description__: Extracts the blue channel for slides stained with T or NTB. NTB slides are intensity normalized. 32x downsampled thumbnails are generated for every image.

__Expected script duration__: 

---------------------------
#### User Step 2
---------------------------

__User step__: Check slice orientations with GIMP/ImageJ/Photoshop/etc.. All slices must be cut sagittally, roughly oriented with the rostral side on the left, and slices must begin on the left hemisphere of the brain.


---------------------------
### Script 2
---------------------------
__Command__: `python a_script_preprocess_2.py $stack $stain`

__Command (optional alternative)__: `python a_script_preprocess_2.py $stack $stain --anchor_fn $anchor_image_filename`

__Description__: Generates image translation and rotation alignment parameters, one "anchor" file is chosen which all other images are aligned to. User can choose to pass an images filename in to be the anchor image, otherwise the anchor image will be chosen automatically. Image alignment parameters are applied and the new aligned image stack is saved as so called "prep1" images. The background is padded white for T stain and black for NTB stain.

__Expected script duration__: 

---------------------------
#### User Step 3
---------------------------

__User step__: Manually fix incorrect alignments. The image alignment scripts is imperfect and has an error rate of 5-10%. The incorrectly aligned slides must be aligned and saved by hand. The built in GUI can be run using `python $REPO_DIR/gui/preprocess_tool_v3.py $stack --tb_version $img_version_1`. [Link to GUI guide](GUI_guides.md#alignment-gui)

__User step 2__: Create initial segmentation outlines of the brain for every slice with the following command, `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`. [Link to GUI guide](GUI_guides.md#masking-gui-initial-manual-mask-contours)


---------------------------
### Script 3
---------------------------
__Command__: `python a_script_preprocess_3.py $stack $stain`

__Description__: Generates binary masks for every image to segment the pixels containing the brain using the user's initial segmentation outline for assistance.

__Expected script duration__: 

---------------------------
#### User Step 4
---------------------------

__User step__: Manually correct the generated masks with the following command, `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1` and save these prep1 thumbnail image masks. [Link to GUI guide](GUI_guides.md#masking-gui-correct-auto-generated-masks)


---------------------------
### Script 4
---------------------------
__Command__: `python a_script_preprocess_4.py $stack $stain`

__Description__: Creates "original_image_crop.csv" file which contains the dimensions of every thumbnail (32x downsampled) image. Applies reverse prep1 transforms on all masks and saves these unaligned masks in the original orientation of the images. Applies a local adaptive intensity normalization algorithm on NTB images.

- __Algorithm descriptions [inc]__
    - local adaptive intensity normalization algorithm: [inc]

__Expected script duration__: upwards of 12-18 hours

---------------------------
#### User Step 5 [OBSOLETE]
---------------------------

__User step__: User specifies a cropping box for the entire brain (called prep5 crop). Using the *prep1 thumbnail images*, the user must open one of the larger slices near the middle of the stack (where the slice's size would be maximized) and must find the vertices of a rectangle that encloses the brain tissue, such that all the brain tissue on every image is enclosed in this space. Record this cropping box in the following fomat: (rostral_limit, caudal_limit, dorsal_limit, ventral_limit). For convenience this is equivalent to: (x_min, x_max, y_min, y_max).
 

---------------------------
### Script 5
---------------------------
__Command__: `python a_script_preprocess_5.py $stack $stain -l $rostral_limit $caudal_limit $dorsal_limit $ventral_limit`

__Description__: Using the user specified whole brain cropbox, cropped images are generated and saved as raw "prep5" images. Thumbnails are then generated.

__Expected script duration__: 


---------------------------
#### User Step 6
---------------------------

__User step__: Similar to the last user step, the user specifies a cropping box for the brainstem region (called prep2 crop). Using the __prep1__ thumbnail images, the user should open one of the larger slices near the middle of the stack (where the brainstem region's size would be maximized) and must find the vertices of a rectangle that encloses the brainstem region. Record this cropping box in the following fomat: (rostral_limit, caudal_limit, dorsal_limit, ventral_limit). For convenience this is equivalent to: (x_min, x_max, y_min, y_max). "_2" is appended to the limits when referenced in Script 6 to differentiate from the previous limits.

__User step 2__: Record (prep2_section_min, prep2_section_max). These are the slice numbers in which the brainstem region is enclosed. Typical values might be (90, 370).


---------------------------
### Script 6
---------------------------
__Command__: `python a_script_preprocess_6.py $stack $stain -l $rostral_limit_2 $caudal_limit_2 $dorsal_limit_2 $ventral_limit_2 $prep2_section_min $prep2_section_max`

__Description__: Using the user specified brainstem cropbox, cropped images are generated and saved as raw "prep2" images. Thumbnails are then generated. Raw prep2 images are compressed into jpeg format. Finally the masks are cropped to match the prep2 images. These raw prep2 images are finished being processed, they are the images that will be used throughout the rest of the pipeline. Finally, intensity volume is generated for the brain.

__Expected script duration__: 

---------------------------
#### User Step 7
---------------------------

__User step__: Record X/Y/Z coordinates for midpoint of 12N, 3N_R on midplane, the following gui can be used to assist: `$REPO_DIR/gui/brain_labeling_gui_v28.py $stack --img_version $img_version_2`. If resolution of the images is NOT _0.46um_: set --resolution flag to 'thumbnail' or '1um' as follows: `--resolution 1um`. [Link to GUI guide](GUI_guides.md#annotation-gui)


---------------------------
### Script 7
---------------------------
__Command__: `python a_script_preprocess_7.py $stack $stain -l $x_12N $y_12N $x_3N $y_3N $z_midline`

__Description__: Obtains simple global alignment of the atlas using manually inputted 12N and 3N_R center coordinates.

- __Algorithm descriptions__
    - Intensity volume generation algorithm:
        - Creates a 3D voxel-based representation of the brain at a resolution of 10um x 10um x 20um by default. Placeholder slices are filled with copies of the previous slice. The end product is a every image downsampled and stitched together with the area outside of each mask being set to 0. This allows for a quick analysis of the shape, orientation, and varied intensity of this brain relative to others. 
    - Simple global alignment algorithm:
        - Affine transformations are applied to the atlas so that the midpoints of 3N_R and 12N coincide with the midpoints of the current stack as entered by the user. These two structures were chosen as they both lay on the midline and are relatively far apart from one another. Mapping the atlas this way gives a good starting transformation which is improved in future scripts.

__Expected script duration__: 

# Structure Registration Scripts

---------------------------
## Processing Script
---------------------------
- __Description__: This processing script calls four other scripts that compose the processing pipeline. These are listed below.
    - Compute Patch Features
    - Generate Probability Volumes
    - Structure Registration
    - Generate visualizations of registered structures and patch features

__Command__: `python a_script_processing.py $stack $stain $detector_id`

- __Patch Features Algorithm__: 
    - Computing patch features requires a CNN model (uses mxnet model inception-bn-blue), a windowing id (which dictates the spacing and x-y dimensions of the patches used, default=7), and a normalization scheme (default is None). First the patches and locations need to be generated. Using the specified windowing id patch origin locations will be generated for every image, these patches will span the mask of the prep2 image. The patches are individually fed into the inception-bn-blue pre-trained neural network and the output layer, of length 1024, is returned and assigned to that patch. Each patch location will have this associated 1024-length patch feature.

- __Probability Volumes Algorithm__: 
    - Generating probability volumes (as well as the scoremaps) involves loading in the current atlas (v7 as of the April 2019 paper). First bounding boxes are loaded from the simple global alignment output, and a large ROI is generated for each structure that encapsulates the volume that the structure may occupy with a margin of 2000um in the sagittal plane and 300um between sections. This constrains the computation to be done on this ROI bounding box rather than the entire sample. Then score volumes are generated, a heatmap-like representation of the likelyhood of a structure occupying a certain region. For each patch location, the associated feature vector is fed into a neural network and a probability score is returned representing the percent chance that this patch is located inside of a particular structure. For every structure, this must be done for every slice it might possibly span. The end result is a set of scoremaps for every structure, these are combined into a single volume and saved as well as their offsets from the origin. Finally, gradients are computed for the volumetric data and are saved in a similar format.

- __Registration Algorithm__: 
    - Inputs: The final step in the pipeline involves properly aligning the current atlas to a given brain, assisted by the simple global registration parameters and scoremaps generated earlier. This script takes in a "fixed_brain_spec" and a "moving_brain_spec", which are specifications of the two brain volumes (the moving brain will be transformed to overlay the fixed brain), as well as a registration_setting, the encodings of which can be found in `src/registration/registration_settings.csv`.
    - An "Aligner" object is created that is initially set to the simple global transformation.

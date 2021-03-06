## Table of Contents
The preprocessing stage of the code can be broken down into the following 7-8 steps.

### Preprocessing (Local)

1) [Preprocess Setup](#preprocess-setup)
2) [Global Intensity Normalization](#global-intensity-normalization)
3) [Intra-Stack Alignment](#intra-stack-align)
4) [Create Masks](#create-masks)
5) [Local Adaptive Intensity Normalization](#local-adaptive-intensity-normalization)
6) [While-Slice Brain Crop](#whole-slice-crop)
7) [Brainstem Crop](#brainstem-crop)

### Processing (Local or Butt)
0) [Simple Global Alignment](#optional-obtain-a-simple-global-alignment)
1) [Generate intensity volume](#generate-intensity-volume)
2) [Compute Patch Features](#compute-patch-features)
3) [Generate Probability Volumes](#generate-probability-volumes)
4) [Registration](#registration)
5) [Visualize Registration Results](#visualize-registration-results)

### Abbreviations

Throughout this document there are a few shorthand representations for various elements.
- List of abbreviations:
	- `STACK`: The name of the stack you are running through the pipeline.
		- example: 'MD585'
	- `SECTION`: The name of an individual slice in the stack. Varies 
		- example: 'slide074_2018_09_04-S3'
	- `STR`: The name of any one of the 28 structures in the brainstem.
		- example: '5N'
	- `STR-RL`: The name of any one of the 51 landmarks. Some centerline structures are landmarks, structures that appear in the right and left hemispheres are considered two landmarks and are appended with an 'R' or an 'L'.
		- example: '5N_R'

# Scripts

Each demo shows one of the essential steps of the pipeline:
- preprocess jpeg2000 images (e.g. convert to tif and intra-stack align)
- extract features using a convolutional neural network
- generate probability maps using pre-trained classifiers
- register 12N (hypoglossal nucleus) to the atlas.
- register 3N_R (occulomotor nucleus, right) and 4N_R (trochlear nucleus, right) to the atlas as a group.
- visualize the aligned atlas overlaid on original images

Associated with each step are one download script and one work script.
At each step, the work script generates **a subset** of the full outputs expected of that step.
A download script is then used to download from S3 the full set of outputs that are **pre-computed**. They are then used by the work script of the next step.

------------------------------------------------------


## Preprocess

### Preprocess Setup
- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** create `STACK.ini` and put it under `demo_data/brains_info/`
	- Example:
	```
	[DEFAULT]
	planar_resolution_um = 0.46
	section_thickness_um = 20
	```
- Create `STACK_input_spec.json`. `python jp2_to_tiff.py STACK STACK_raw_input_spec.json`.
- Create `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`
- Create `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

### Global intensity normalization
- Create `input_spec.ini` as (None,Ntb,thumbnail). `python normalize_intensity.py input_spec.ini NtbNormalized`
	- Output:
	```
	DATA_ROOTDIR/
        └── STACK_thumbnail_NtbNormalized
            └── SECTION_thumbnail_NtbNormalized.tif
	```

### Intra-stack align
- **(HUMAN)** Browse thumbnails to verify orientations are all correct.
- **(HUMAN)** Create `from_none_to_aligned.ini` to describe intra-stack alignment operation.
- Create `input_spec.ini` as (None,NtbNormalized,thumbnail). `python align_compose.py input_spec.ini --op from_none_to_aligned`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		├── STACK_elastix_output
		│   └── SECTION1_to_SECTION2
		│       ├── elastix.log
		│       ├── IterationInfo.0.R0.txt
		│       ├── IterationInfo.0.R1.txt
		│       ├── IterationInfo.0.R2.txt
		│       ├── IterationInfo.0.R3.txt
		│       ├── IterationInfo.0.R4.txt
		│       ├── IterationInfo.0.R5.txt
		│       ├── result.0.tif
		│       └── TransformParameters.0.txt
		└── STACK_transforms_to_anchor.csv
	```
- `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_padded --njobs 8`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_NtbNormalized
		    └── SECTION_prep1_thumbnail_NtbNormalized.tif
	```
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_tool_v3.py`, correct pairwise transforms and check each image's order in stack. `python preprocess_tool_v3.py STACK --tb_version NtbNormalized`

### Create masks
- **(HUMAN)** On a machine with monitor, launch the maskingGUI. `DATA_ROOTDIR=/media/yuncong/brainstem/home/yuncong/MouseBrainAtlas/demo/demo_data python mask_editing_tool_v4.py STACK`.
Draw initial snake contours.
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
	    	├── STACK_prep1_thumbnail_initSnakeContours.pkl
		└── STACK_prep1_thumbnail_anchorInitSnakeContours.pkl
	```
- Create `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini demo_data/CSHL_data_processed/STACK/STACK_prep1_thumbnail_initSnakeContours.pkl`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_autoSubmasks
		    └── SECTION
			├── SECTION_prep1_thumbnail_autoSubmask_0.png
			└── SECTION_prep1_thumbnail_autoSubmaskDecisions.csv
	```
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
	- Output after correcting masks & exporting as PNG:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_userModifiedSubmasks
		    └── SECTION
			├── SECTION_prep1_thumbnail_userModifiedParameters.json
			├── SECTION_prep1_thumbnail_userModifiedSubmask_0.png
			├── SECTION_prep1_thumbnail_userModifiedSubmaskContourVertices.pkl
			└── SECTION_prep1_thumbnail_userModifiedSubmaskDecisions.csv
	```
- Create `input_spec.ini` as (None,NtbNormalized,thumbnail). `python generate_original_image_crop_csv.py --input_spec input_spec.ini`. This creates `DEMO998_original_image_crop.csv` under data dir. In this file each row is x,y,width,height in thumbnail resolution.
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_masks
		    └── SECTION
			└── SECTION_prep1_thumbnail_mask.png
	```
- Create `input_spec.ini` as (alignedPadded,mask,thumbnail). Copy template `from_padded_to_none.ini`. Copy and modify operation `crop_orig.ini`. `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_thumbnail_mask
		    └── SECTION_thumbnail_mask.png
	```
 
### Local adaptive intensity normalization
- Create `input_spec.ini` as (None,Ntb,raw). `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_intensity_normalization_results
		    ├── floatHistogram
		    │   └── SECTION_raw_floatHistogram.png
		    ├── meanMap
		    │   └── SECTION_raw_meanMap.bp
		    ├── meanStdAllRegions
		    │   └── SECTION_raw_meanStdAllRegions.bp
		    ├── normalizedFloatMap
		    │   └── SECTION_raw_normalizedFloatMap.bp
		    ├── regionCenters
		    │   └── SECTION_raw_regionCenters.bp
		    └── stdMap
			└── SECTION_raw_stdMap.bp
	```

### Whole-slice crop
- **(HUMAN)** Create `from_aligned_to_wholeslice.ini`. Copy `from_none_to_wholeslide.ini`. In this file specify the cropbox for the domain `alignedWithMargin ` based on `alignedPadded` images. This cropbox can also be automatically inferred as padding 20 thumbnail-resolution pixels surrounding the `alignedPadded` masks.
	- Output:
	```
	```
- Create `input_spec.ini` as (None,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_wholeslice`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep5_raw_NtbNormalizedAdaptiveInvertedGamma
		    └── SECTION_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma
		    └── SECTION_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
	```

### Brainstem crop
- **(HUMAN)** Create `from_wholeslice_to_brainstem.ini`. Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin or alignedPadded thumbnails.
	- File contents:
	```
	[DEFAULT]
	operation_sequence = -from_padded_to_wholeslice
	from_padded_to_brainstem
	```
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGamma
		    └── SECTION_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma
		    └── SECTION_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
		    └── SECTION_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
	```

## Generate intensity volume
- `python construct_intensity_volume.py DEMO998 --tb_version NtbNormalizedAdaptiveInvertedGamma`
	- Output:
	```
	ROOT_DIR/
	└── CSHL_volumes
		└── STACK
			└── STACK_wholebrainWithMargin_10.0um_intensityVolume
				└── STACK_prep2_none_win7 # Possibly incorrect, may not exist
					├── STACK_wholebrainWithMargin_10.0um_intensityVolume.bp
					└── STACK_wholebrainWithMargin_10.0um_intensityVolume_origin_wrt_wholebrain.txt
	```

## Obtain a simple global alignment
---
Description: The user inputs the center of the `12N` and `3N_R` structures. These structures are fairly far apart and are located on the sagittal centerline. An affine transformation is made on the Atlas, aligned the `12N` and `3N_R` of the Atlas to the target brain. This gives a simple, fast alignment along the centerline and is used as a basis for the structure-specific alignment in the registration step.

Once this mid-sagittal, simple global alignment has finished, rough bounding boxes are computed for every structure. These bounding boxes give a generous rectangular field in which each structure can be located. The boxes are wide enough to never cut off any region where the structure might be, and reduce computational time for future steps.

This can serve two purposes:
1. It allows us to estimate a probable region of the brain volume for each structure. We can compute features only on these regions to save computation. 
2. It can be used as a starting point for the structure-specific registration later.
---

#### Notes
- Pick the center of 12N and of 3N at sagittal midline.
	- Command: `python src/gui/brain_labeling_gui_v28.py <STACK> --img_version NtbNormalizedAdaptiveInvertedGammaJpeg`
	- Record X, Y, Z positions in midsaggital plane for 12N (ovalar on right) and 3N (circular on left)
- Input the centers into `ROOT_DIR/CSHL_simple_global_registration/STACK_manual_anchor_points.ini` and then run `src/registration/compute_simple_global_registration.py` to compute the simple global transform.
	- Output:
	```
	ROOT_DIR/
	└── CSHL_simple_global_registration
		├── STACK_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.txt
		└── STACK_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.bp
	```
- The second part of this script will identify 3-d bounding boxes of each simpleGlobal aligned structure, to generating structure ROIs.
	- Output:
	```
	ROOT_DIR/
	└── CSHL_simple_global_registration
		└── STACK_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json
	```

- Temporary notes on this part of the pipeline can be found [here](global_alignment_notes.md)
- `src/learning/from_images_to_score_volume.ipynb` will NOT run unless `src/utilities/learning_utilities.py`, Line __844__, is correct for this particular stack. NEEDS TO BE CHANGED  

## Compute patch features
- ~ 5 minutes
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python demo_compute_features_v2.py DEMO998_input_spec.ini`
	-If using GPU, the demo for each section should finish in about 1 minute. If using CPU, this takes about 1 hour.
	- Output:
	```
	ROOT_DIR/
	└── CSHL_patch_features
		└── inception-bn-blue
			└── STACK
				└── STACK_prep2_none_win7
					├── SECTION_prep2_none_win7_inception-bn-blue_features.bp
					└── SECTION_prep2_none_win7_inception-bn-blue_locations.bp
	```

## Generate probability volumes
- ~ 8 hours
- Create `DEMO998_prep2_sectionLimits.ini`. In this file specify the indices of the first and last sections that include the brainstem.
- Download detectors. `python download_demo_data_generate_prob_volumes.py`
- `python demo_generate_prob_volumes.py DEMO998 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"`
	- Don't include the 'structure_list' arg to do all structures
	- Output:
	```
	ROOT_DIR/
	├── CSHL_scoremaps
	│	└── 10.0um
	│		└── STACK
	│			└── STACK_prep2_10.0um_detector799
	│				└── STACK_SECTION_prep2_10.0um_detector799
	│					└── STACK_SECTION_prep2_10.0um_detector799_STR_scoremap.bp
	└── CSHL_scoremap_Viz
		└── 10.0um
			└── STR
				└── STACK
					└── detector799
						└── prep2
							└── STACK_SECTION_prep2_10.0um_STR_detector799_STR_scoremapViz.jpg
	```
	- Output:
	```
	ROOT_DIR/
	└── CSHL_volumes/
		└── STACK
		    └── STACK_detector799_10.0um_scoreVolume
			├── score_volume_gradients
			│   ├── STACK_detector799_10.0um_scoreVolume_STR-RL_gradients.bp
			│   └── STACK_detector799_10.0um_scoreVolume_STR-RL_origin_wrt_wholebrain.txt
			└── score_volumes
			    ├── STACK_detector799_10.0um_scoreVolume_STR-RL.bp
			    └── STACK_detector799_10.0um_scoreVolume_STR-RL_origin_wrt_wholebrain.txt
	```


## Registration
- ~ 12 hours
- Output:
```
ROOT_DIR/
└── CSHL_volumes/
	└── atlasV7
		└── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um
			└── score_volumes
				├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um_STR-RL.bp
				├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um_STR-RL_origin_wrt_fixedWholebrain.txt
				├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um_STR-RL_surround_200um.bp
				└── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um_STR-RL_surround_200um_origin_wrt_fixedWholebrain.txt
				
ROOT_DIR/
└── CSHL_registration_parameters/
	└── atlasV7
		└── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL
			├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_parameters.json
			├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_scoreEvolution.png
			├── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_scoreHistory.bp
			└── atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_trajectory.bp
```

### Register 12N individually
- `$ python register_brains_demo_12N.py --use_simple_global`
  - Expected runtime of about 8 minutes
  - Output displays 1000 iterations of gradient descent

### Register 3N_R and 4N_R as a group
- `$ python register_brains_demo_3N_R_4N_R.py --use_simple_global`
  - Expected runtime of about 3 minutes
  - Output displays 1000 iterations of gradient descent

The outputs include the transform parameters and transformed atlas structures.

## Visualize registration results
- ~ 10 minutes

To visualize the multi-probability level structures of the aligned atlas overlaid on original images:
- `$ python visualize_registration_demo_3_structures.py`
  - Expected runtime of about 1 minute
  - "Image fails to load. Trying to convert from other resol/versions" is part of expected output

An [example output image](example_atlas_overlay.jpg) is included in this repo.
The background image is the intensity-normalized Neurotrace Blue-stained section.
White contours are the atlas after simple global registration.
Colored contours are the atlas after local registration. Different colors correspond to different probability levels. The  levels from outside in are 0.99, 0.75, 0.5, 0.25, 0.01.

The complete set of overlay images are under `CSHL_registration_visualization/DEMO999_atlas_aligned_multilevel_down16_all_structures/NtbNormalizedAdaptiveInvertedGammaJpeg/`. Note: They are 16X downsampled to allow for easy downloading and visualization.


Input and expected output will be downloaded from an open S3 bucket

-------------------------------------------

## Learn structure textures

- Generate annotation boundaries using `brain_labeling_gui_v28.py`.
- Assign class labels to image patches, according to manually annotated boundaries. `python label_patches.py DEMO998 --win_id 7`
- Train classifiers. `python train_classifiers.py DEMO998 --win_id 7 --classifier_id 898 --structure_list "[\"3N\"]"`

## Estimate structure shapes and positions


------------------------------------------

## Notes
### Prep IDs
As the preprocessing stage relies on a series of image manipulations, there is a coding system that caries information on what manipulations have ben applied to the given image. In the filename there will be the string 'prep#' where the number represents the stage it is at.

0) 'raw'
	- No changes except all slices have been rotated: rostral left, caudal right
1) 'alignedPadded'
2) 'alignedBrainstemCrop'
3) 'alignedThalamusCrop'
4) 'alignedNoMargin'
5) 'alignedWithMargin'
6) 'rawCropped'
7) 'rawBeforeRotation'
	- Unprocessed, unrotated. The very beginning for most stacks

Input_Spec shorthand:
- aligned: ?
- padded: prep1
- brainstem: prep2
- wholeslice: prep5

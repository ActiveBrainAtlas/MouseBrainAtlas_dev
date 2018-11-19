## Table of Contents
The preprocessing stage of the code can be broken down into the following 7-8 steps.

### Preprocessing

1) [Preprocess Setup](#preprocess-setup)
2) [Global Intensity Normalization](#global-intensity-normalization)
3) [Intra-Stack Alignment](#intra-stack-align)
4) [Create Masks](#create-masks)
5) [Local Adaptive Intensity Normalization](#local-adaptive-intensity-normalization)
6) [While-Slice Brain Crop](#whole-slice-crop)
7) [Brainstem Crop](#brainstem-crop)
8) [(Optional) Simple Global Alignment](#optional-obtain-a-simple-global-alignment)


### Processing

1) [Compute Patch Features](#compute-patch-features)
2) [Generate Probability Volumes](#generate-probability-volumes)
3) [Registration](#registration)
4) [Visualize Registration Results](#visualize-registration-results)


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
- **(HUMAN)** create `DEMO998.ini` and put it under `demo_data/brains_info/`
	- Example:
	```
	[DEFAULT]
	planar_resolution_um = 0.46
	section_thickness_um = 20
	```
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_raw_input_spec.json`.
- Create `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`
- Create `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

### Global intensity normalization
- Create `input_spec.ini` as (None,Ntb,thumbnail). `python normalize_intensity.py input_spec.ini NtbNormalized`
	- Output:
	```
	DATA_ROOTDIR/
        └── STACK_thumbnail_NtbNormalized
            └── SLICE_thumbnail_NtbNormalized.tif
	```
	- Output:
	```
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
		│   └── SLICE1_to_SLICE2
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
		    └── SLICE_prep1_thumbnail_NtbNormalized.tif
	```
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_tool_v3.py`, correct pairwise transforms and check each image's order in stack. `python preprocess_tool_v3.py DEMO998 --tb_version NtbNormalized`

### Create masks
- **(HUMAN)** On a machine with monitor, launch the maskingGUI. `DATA_ROOTDIR=/media/yuncong/brainstem/home/yuncong/MouseBrainAtlas/demo/demo_data python mask_editing_tool_v4.py DEMO998`.
Draw initial snake contours.
	- Output:
	```
	```
- Create `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_autoSubmasks
		    └── SLICE
			├── SLICE_prep1_thumbnail_autoSubmask_0.png
			└── SLICE_prep1_thumbnail_autoSubmaskDecisions.csv
	```
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
	- Output after correcting masks & exporting as PNG:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_userModifiedSubmasks
		    └── SLICE
			├── SLICE_prep1_thumbnail_userModifiedParameters.json
			├── SLICE_prep1_thumbnail_userModifiedSubmask_0.png
			├── SLICE_prep1_thumbnail_userModifiedSubmaskContourVertices.pkl
			└── SLICE_prep1_thumbnail_userModifiedSubmaskDecisions.csv
	```
- Create `input_spec.ini` as (None,NtbNormalized,thumbnail). `python generate_original_image_crop_csv.py --input_spec input_spec.ini`. This creates `DEMO998_original_image_crop.csv` under data dir. In this file each row is x,y,width,height in thumbnail resolution.
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_prep1_thumbnail_masks
		    └── SLICE
			└── SLICE_prep1_thumbnail_mask.png
	```
- Create `input_spec.ini` as (alignedPadded,mask,thumbnail). Copy template `from_padded_to_none.ini`. Copy and modify operation `crop_orig.ini`. `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
	    └── STACK
		└── STACK_thumbnail_mask
		    └── SLICE_thumbnail_mask.png
	```
 
### Local adaptive intensity normalization
- Create `input_spec.ini` as (None,Ntb,raw). `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_intensity_normalization_results
		    ├── floatHistogram
		    │   └── SLICE_raw_floatHistogram.png
		    ├── meanMap
		    │   └── SLICE_raw_meanMap.bp
		    ├── meanStdAllRegions
		    │   └── SLICE_raw_meanStdAllRegions.bp
		    ├── normalizedFloatMap
		    │   └── SLICE_raw_normalizedFloatMap.bp
		    ├── regionCenters
		    │   └── SLICE_raw_regionCenters.bp
		    └── stdMap
			└── SLICE_raw_stdMap.bp
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
		    └── SLICE_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma
		    └── SLICE_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
	```

### Brainstem crop
- **(HUMAN)** Create `from_wholeslice_to_brainstem.ini`. Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin or alignedPadded thumbnails.
	- Output:
	```
	```
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGamma
		    └── SLICE_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma
		    └── SLICE_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
	```
- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`
	- Output:
	```
	DATA_ROOTDIR/
	└── CSHL_data_processed
		└── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
		    └── SLICE_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
	```

## (Optional) Obtain a simple global alignment

This can serve two purposes:
1. It allows us to estimate a probable region of the brain volume for each structure. We can compute features only on these regions to save computation. 
2. It can be used as a starting point for the structure-specific registration later.

- Pick the center of 12N and of 3N at sagittal midline. Input them into `registration_v7_atlasV7_simpleGlobal.ipynb` to compute the simple global transform.
- Then run the `# Identify 3-d bounding box of each simpleGlobal aligned structure` part of `from_images_to_score_volume.ipynb` to generate structure ROIs.

## Compute patch features
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python demo_compute_features_v2.py DEMO998_input_spec.ini`
	-If using GPU, the demo for each section should finish in about 1 minute. If using CPU, this takes about 1 hour.
	- Output:
	```
	ROOT_DIR/
	└── CSHL_patch_features
		└── inception-bn-blue
			└── STACK
				└── STACK_prep2_none_win7
					├── SLICE_prep2_none_win7_inception-bn-blue_features.bp
					└── SLICE_prep2_none_win7_inception-bn-blue_locations.bp
	```

## Generate probability volumes

- Create `DEMO998_prep2_sectionLimits.ini`. In this file specify the indices of the first and last sections that include the brainstem.
- Download detectors. `python download_demo_data_generate_prob_volumes.py`
- `python demo_generate_prob_volumes.py DEMO998 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"`

## Registration

### Register 12N individually
- `$ python register_brains_demo_12N.py --use_simple_global`
  - Expected runtime of about 8 minutes
  - Output displays 1000 iterations of gradient descent

### Register 3N_R and 4N_R as a group
- `$ python register_brains_demo_3N_R_4N_R.py --use_simple_global`
  - Expected runtime of about 3 minutes
  - Output displays 1000 iterations of gradient descent

The outputs include the transform parameters and transformed atlas structures.

## Generate intensity volume
- `python construct_intensity_volume.py DEMO998 --tb_version NtbNormalizedAdaptiveInvertedGamma`

## Visualize registration results

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

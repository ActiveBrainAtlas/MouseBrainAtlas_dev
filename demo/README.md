# Demos

It is recommended to run the [walk-through](demo_tutorial.ipynb) (ipython notebook) interactively.

This demo suite shows how to align three structures (12N, 3N_R, 4N_R) in a subject brain (DEMO998) with the atlas (atlasV7). 

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

All generated and downloaded data are stored in `demo/demo_data/`.

---------------------------

## Installation

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas** and install necessary packages.
```
# Modify the first a few lines of config.sh according to your specific use case, then
source setup/config.sh
# Make sure we are now working under the mousebrainatlas python virtual environment, then
cd demo
```

- The demos are written in Python 2.7.2 and have been tested on a machine with Intel Xeon W5580 3.20GHz 16-core CPU, 128GB RAM and a Nvidia Titan X GPU, running Linux Ubuntu 16.04. 
- The default `requirements.txt` assumes CUDA version of 9.0. If your CUDA version (check using `nvcc -v` or `cat /usr/local/cuda/version.txt`) is 9.1, replace `mxnet-cu90` with `mxnet-cu91` in `requirements.txt`. If your machine does not have a GPU, replace `mxnet-cu90` with `mxnet`. Refer to [official mxnet page](https://mxnet.incubator.apache.org/install/index.html?platform=Linux&language=Python&processor=CPU) for available pips.

## Preprocess

Install ImageMagick 6.8.9.

Note that the `input_spec.ini` files for most steps are different and must be manually created according to the actual input. In the following instructions, "create `input_spec.ini` as (prep_id, version, resolution)" means using the same set of image names as `image_name_list` but set the `prep_id`, `version` and `resolution` accordingly.

To use GUIs, install PyQt4 into the virtualenv according to [this answer](https://stackoverflow.com/a/28850104).

- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** create `DEMO998.ini` and put it under `demo_data/brains_info/`
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_raw_input_spec.json`.
- Create `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`
- Create `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
### Global intensity normalization
- Create `input_spec.ini` as (None,Ntb,thumbnail). `python normalize_intensity.py input_spec.ini NtbNormalized`
### Intra-stack align
- **(HUMAN)** Browse thumbnails to verify orientations are all correct.
- **(HUMAN)** Create `from_none_to_aligned.ini` to describe intra-stack alignment operation.
- Create `input_spec.ini` as (None,NtbNormalized,thumbnail). `python align_compose.py input_spec.ini --op from_none_to_aligned`
- `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_padded`
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_gui.py`, correct pairwise transforms and check each image's order in stack.
### Create masks
- **(HUMAN)** On a machine with monitor, launch the maskingGUI. `DATA_ROOTDIR=/media/yuncong/brainstem/home/yuncong/MouseBrainAtlas/demo/demo_data python mask_editing_tool_v4.py DEMO998`.
Draw initial snake contours.
- Create `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
- **(HUMAN)** Create `DEMO998_original_image_crop.csv`. In this file each row is x,y,width,height in thumbnail resolution.
- Create `input_spec.ini` as (alignedPadded,mask,thumbnail). `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.
 
### Local adaptive intensity normalization
- Create `input_spec.ini` as (None,Ntb,raw). `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`

### Whole-slice crop
- **(HUMAN)** Create `from_none_to_wholeslice.ini`. In this file specify the cropbox for the domain `alignedWithMargin ` based on `alignedPadded` images. This cropbox can also be automatically inferred as padding 20 thumbnail-resolution pixels surrounding the `alignedPadded` masks.
- Create `input_spec.ini` as (None,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_wholeslice`
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

### Brainstem crop
- **(HUMAN)** Create `from_wholeslice_to_brainstem.ini`. Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin or alignedPadded thumbnails.
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`

## (Optional) Obtain a simple global alignment

This can serve two purposes:
1. It allows us to estimate a probable region of the brain volume for each structure. We can compute features only on these regions to save computation. 
2. It can be used as a starting point for the structure-specific registration later.

- Pick the center of 12N and of 3N at sagittal midline. Input them into `registration_v7_atlasV7_simpleGlobal.ipynb` to compute the simple global transform.
- Then run the `# Identify 3-d bounding box of each simpleGlobal aligned structure` part of `from_images_to_score_volume.ipynb` to generate structure ROIs.

## Compute patch features
```
python demo_compute_features.py DEMO998 --section 225 --version NtbNormalizedAdaptiveInvertedGamma
python demo_compute_features.py DEMO998 --section 230 --version NtbNormalizedAdaptiveInvertedGamma
python demo_compute_features.py DEMO998 --section 235 --version NtbNormalizedAdaptiveInvertedGamma
```

If using GPU, the demo for each section should finish in about 1 minute. If using CPU, this takes about 1 hour.

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

----------------

## Learn structure textures

- Generate annotation boundaries using `brain_labeling_gui_v28.py`.
- Assign class labels to image patches, according to manually annotated boundaries. `python label_patches.py DEMO998 --win_id 7`
- Train classifiers. `python train_classifiers.py DEMO998 --win_id 7 --classifier_id 898 --structure_list "[\"3N\"]"`

## Estimate structure shapes and positions

# Demos

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

For each step below that requires `input_spec.ini`, the ini file is a different one and must be manually created.

- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** Create meta data information for this brain
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_input_spec.json`.
- `python extract_channel.py input_spec.ini 2 Ntb`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- `python normalize_intensity.py input_spec.ini NtbNormalized`
- **(HUMAN)** browse thumbnails to verify orientations are all correct
- **(HUMAN)** Obtain a roughly correct sorted list of image names from the data provider.
- `python align.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_elastix_output ../src/preprocess/parameters/Parameters_Rigid_MutualInfo_noNumberOfSpatialSamples_4000Iters.txt`
- **(HUMAN)** select anchor image, using preprocessGUI `preprocess_gui.py`
- `python compose.py --elastix_output_dir "demo_data/CSHL_data_processed/DEMO998/DEMO998_elastix_output" \
--custom_output_dir "demo_data/CSHL_data_processed/DEMO998/DEMO998_custom_output" \
--input_spec input_spec.ini  \
--anchor "MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250" \
--out "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv"`
- **(HUMAN)** create `DEMO998.ini` and put it in `demo_data/brains_info/`
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --out_prep_id alignedPadded`
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_gui.py`, correct pairwise transforms and check each image's order in stack. Create `DEMO998_sorted_filenames.txt` based on the given roughly correct list.
- **(HUMAN)** draw initial snake contours for masking using maskingGUI. 
`python mask_editing_tool_v4.py DEMO998`
- `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks. 
`python mask_editing_tool_v4.py DEMO998`
- **(HUMAN)** Create `DEMO998_original_image_crop.csv`
- `python warp_crop.py --input_spec input_spec.ini \
 --inverse_warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_original_image_crop.csv" \
 --out_prep_id None`
- `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`
- **(HUMAN)** Manually specify the alignedWithMargin cropbox based on alignedPadded images, or automatically infer based on alignedPadded masks.
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_cropbox.ini" \
 --out_prep_id alignedWithMargin`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- **(HUMAN)** Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin thumbnails or alignedPadded thumbnails
- `python warp_crop.py --input_spec input_spec.ini \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_cropbox.ini" \
 --out_prep_id alignedBrainstemCrop`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- `python compress_jpeg.py input_spec.ini`

## Compute patch features
```
./download_demo_data_compute_features.py
# For 3N, do any two sections between 221-244, 4N 221-237, 12N 183-265.
./demo_compute_features.py DEMO998 --section 225 --version NtbNormalizedAdaptiveInvertedGamma
./demo_compute_features.py DEMO998 --section 235 --version NtbNormalizedAdaptiveInvertedGamma
```

If using GPU, the demo for each section should finish in about 1 minute. If using CPU, this takes about 1 hour.


## Generate probability volumes
```
./download_demo_data_generate_prob_volumes.py
./demo_generate_prob_volumes.py DEMO998 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"
```

## Registration
`$ ./download_demo_data_registration.py`
* This takes less than 1 minute.

### Register 12N individually
- `$ ./register_brains_demo_12N.py`
  - Expected runtime of about 8 minutes
  - Output displays 1000 iterations of gradient descent

### Register 3N_R and 4N_R as a group
- `$ ./register_brains_demo_3N_R_4N_R.py`
  - Expected runtime of about 3 minutes
  - Output displays 1000 iterations of gradient descent

The outputs include the transform parameters and transformed atlas structures.


## Visualize registration results

To visualize the multi-probability level structures of the aligned atlas overlaid on original images:
- `$ ./visualize_registration_demo_3_structures.py`
  - Expected runtime of about 1 minute
  - "Image fails to load. Trying to convert from other resol/versions" is part of expected output

An [example output image](example_atlas_overlay.jpg) is included in this repo.
The background image is the intensity-normalized Neurotrace Blue-stained section.
White contours are the atlas after simple global registration.
Colored contours are the atlas after local registration. Different colors correspond to different probability levels. The  levels from outside in are 0.99, 0.75, 0.5, 0.25, 0.01.

The complete set of overlay images are under `CSHL_registration_visualization/DEMO999_atlas_aligned_multilevel_down16_all_structures/NtbNormalizedAdaptiveInvertedGammaJpeg/`. Note: They are 16X downsampled to allow for easy downloading and visualization.


Input and expected output will be downloaded from an open S3 bucket

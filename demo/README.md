# Demos

This demo suite shows how to align a subject brain (DEMO999) with the atlas (atlasV7). 
Each demo shows one essential step of the pipeline:
- preprocess the jpeg2000 stack (e.g. convert to tif and intra-stack align)
- extract features using a convolutional neural network
- generate probability maps
- register 12N (hypoglossal nucleus) to the atlas individually.
- register 3N_R (occulomotor, right) and 4N_R (trochlear, right) to the atlas as a group.
- visualize the aligned atlas overlaid on original images

---------------------------

## Install packages, setup environment variables and download input data

The following has been tested on Linux Ubuntu 16.04 and might not work on other operating systems.

```
sudo apt-get install wget python-pip python-tk
cd setup
sudo pip install -r requirements.txt
source set_env_variables.sh
cd ../demo
```
* Pulling the Git repo takes 3-4 minutes with good Internet connection.

Each demo first download the necessary input data into `demo/demo_data/`, and then perform the task.


## Preprocess
- Run download_demo_data_preprocessing.py --step 1 to download an example JPEG2000 image.
- Run preprocess_demo.py --step 1
- Run download_demo_data_preprocessing.py --step 2
- `$ ./align.py DEMO999`

## Compute patch features
- `$ ./download_demo_data_compute_features.py`
- `$ ./compute_features_demo.py DEMO999 --section 152 --version NtbNormalizedAdaptiveInvertedGamma`

This demo is expected to finish in 1 minute.

## Generate probability volumes
- `$ ./download_demo_data_scoring.py`
- `$ ENABLE_UPLOAD_S3=0 ENABLE_DOWNLOAD_S3=0 ./from_images_to_score_volumes_demo.py DEMO999 799 --structure_list [\"3N, 4N, 12N\"]`

Note that the data needed to download for this demo is about 35G.

## Registration
`$ ./download_demo_data.py`
* Running `./download_demo_data.py` takes less than 1 minute.

### Register 12N individually
- `$ ./register_brains_demo_12N.py`
  - Expected runtime of about 8 minutes
  - Output displays 1000 iterations of gradient descent

### Register 3N_R and 4N_R as a group
- `$ ./register_brains_demo_3N_R_4N_R.py`
  - Expected runtime of about 3 minutes
  - Output displays 1000 iterations of gradient descent

The outputs are also generated in `demo_data/` folder. The outputs include the transform parameters and transformed atlas structures.


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

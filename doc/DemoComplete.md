# Demos

This demo suite shows how to align three structures (12N, 3N_R, 4N_R) in a subject brain (DEMO999) with the atlas (atlasV7). 
Each demo shows one essential step of the pipeline:
- preprocess the jpeg2000 stack (e.g. convert to tif and intra-stack align)
- extract features using a convolutional neural network
- generate probability maps using pre-trained classifiers
- register 12N (hypoglossal nucleus) to the atlas.
- register 3N_R (occulomotor nucleus, right) and 4N_R (trochlear nucleus, right) to the atlas as a group.
- visualize the aligned atlas overlaid on original images

Associated with each step are one download script and one work script.
At each step, the work script generates **a subset** of the full outputs expected of that step.
A download script is then used to download from S3 the full outputs that are **pre-computed**. They are then used by the work script of the next step.

All generated and downloaded data are stored in `demo/demo_data/`.

---------------------------

## Installation

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas** and install necessary packages.
```
cd setup
source config.sh
workon mousebrainatlas
cd ../demo
```

The following has been tested on Linux Ubuntu 16.04 and might not work on other operating systems. Pulling the Git repo takes 3-4 minutes with good Internet connection.

## Preprocess
- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** Create meta data information for this brain
- `python jp2_to_tiff.py DEMO998 {input_spec_json}`
- `python extract_channel.py input_spec.ini 2 Ntb`
- `python rescale.py input_spec.ini thumbnail -f {1./32}`
- `python normalize_intensity.py input_spec.ini NtbNormalized`

- **(HUMAN)** browse thumbnails to verify orientations are all correct
- **(HUMAN)** Obtain a roughly correct sorted list of image names from the data provider.
- `python align.py temp.ini {elastix_output_dir} {param_fp}`
- **(HUMAN)** select anchor image, using preprocessGUI `preprocess_gui.py`

- `python compose.py --elastix_output_dir "{elastix_output_dir}" \
--custom_output_dir "{custom_output_dir}" \
--input_spec input_spec.ini  \
--anchor "{anchor_img_name}" \
--out "{toanchor_transforms_fp}"`
- **(HUMAN)** set planar_resolution for DEMO998 in `metadata.py`

- `python warp_crop.py --input_spec input_spec.ini \
 --warp "/data/CSHL_data_processed/DEMO999/DEMO999_transformsTo_MD662&661-F102-2017.06.06-22.30.50_MD661_1_0304.csv" \
 --out_prep_id alignedPadded`

- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_gui.py`, correct pairwise transforms and check each image's order in stack. Create DEMO998_sorted_filenames.txt
- **(HUMAN)** draw initial snake contours for masking using maskingGUI `masking_gui.py`.
- `python masking.py input_spec.ini {DataManager.get_initial_snake_contours_filepath(stack=stack)}`
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
- `python warp_crop.py --input_spec input_spec.ini \
 --inverse_warp "{toanchor_transforms_fp}" \
 --crop "/data/CSHL_data_processed/DEMO998/DEMO998_original_image_crop.csv" \
 --out_prep_id None`
- `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`
- **(HUMAN)** Manually specify the alignedWithMargin cropbox based on alignedPadded images, or automatically infer based on alignedPadded masks.
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "{toanchor_transforms_fp}" \
 --crop "{DataManager.get_cropbox_filename_v2(stack=stack, anchor_fn=None, prep_id='alignedWithMargin')}" \
 --out_prep_id alignedWithMargin`
- `python rescale.py input_spec.ini thumbnail -f {1./32}`
- **(HUMAN)** Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin thumbnails or alignedPadded thumbnails
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "{toanchor_transforms_fp}" \
 --crop "{convert_cropbox_fmt(data=DataManager.load_cropbox_v2_relative(stack=stack, prep_id='alignedBrainstemCrop', \
                                     wrt_prep_id='alignedWithMargin', \
                                    out_resolution='thumbnail'), \
                    in_fmt='arr_xxyy', out_fmt='str_xywh', stack=stack)}" \
 --out_prep_id alignedBrainstemCrop`
- `python compress_jpeg.py input_spec.ini`

## Compute patch features
---
- `$ ./demo/download_demo_data_compute_features.py`
- `$ ./demo/compute_features_demo.py DEMO999 --section 230 --version NtbNormalizedAdaptiveInvertedGamma`
---

This demo is expected to finish in 1 minute.

#### Alex Running Notes
For `demo/download_demo_data_compute_features.py`:
- Set ALL environmental root path variables to be /media/alexn/BstemAtlasDataBackup/demo/, except REPO_DIIR. I'll call this path 'ROOT'
- Ran with `python demo/download_demo_data_compute_features.py --demo_data_dir /media/alexn/BstemAtlasDataBackup/demo/` to copy all files into the external hard drive. Only takes in 1 arg which is the download dir, otherwise defaults to ./demo_data. All files go into `[demo_data_dir]/CSHL_data_processed/DEMO999/`, Downloaded 4 files:
  - `DEMO999_sorted_filenames.txt`
  - `DEMO999_anchor.txt`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_sectionLimits.json`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_cropbox.json`
- After these are downloaded, a for loop is traversed to download the `*_prep1_thumbnail_mask.png` for every section. Following that, a single `*_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif` file is downloaded for one section (MD661_2_0155)
  - 272 `*_MD661_#_####_prep1_thumbnail_mask.png` files
  - `MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif`, denoted section 230
  
For COMPUTE FEATURE DEMO:
- Creates directory ROOT/mxnet_models_. The following 3 files should be inside:
      - `inception-bn-blue-0000.params.67eD5BCb`
      - `inception-bn-blue-symbol.json`
      - `mean_224.npy`
- Make sure that the demo downloads the same section you are computing features for. (Demo only gdoes 1 section, hard coded in the download script) Script can easily be changed to do every single section.
- OUTPUTS: (all saved to ROOT/CSHL_patch_features/inception-bn-blue/DEMO999/DEMO999_prep2_none_win7)
  - `MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_none_win7_inception-bn-blue_features.bp`
  - `MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_none_win7_inception-bn-blue_locations.bp`
  - To generalize, for every section two files are generated. Features and Locations, outputted as a bloscpack file.
 
## Generate probability volumes
---
- `$ ./demo/download_demo_data_scoring.py`
- `$ ./demo/from_images_to_score_volumes_demo.py DEMO999 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"`
---

Note that the data needed to download for this demo is about 35G.

#### Alex Running Notes
For `demo/download_demo_data_scoring.py`:
- Ran with `python demo/download_demo_data_scoring.py --demo_data_dir $ROOT_DIR`. Downloading the files takes at least 3-5 hours.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`

For `./demo/from_images_to_score_volumes_demo.py`

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

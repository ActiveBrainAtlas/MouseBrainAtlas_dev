This toolkit is written in Python 2.7.2 and have been tested on a machine with Intel Xeon W5580 3.20GHz 16-core CPU, 128GB RAM and a Nvidia Titan X GPU, running Linux Ubuntu 16.04. 

## Installation

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas-virtualenv** and install necessary packages.

- Change `REPO_DIR`, `ROOT_DIR`, `DATA_ROOTDIR`, `THUMBNAIL_DATA_ROOTDIR` in `setup/config.sh`
- The default `requirements.txt` assumes CUDA version of 9.0. If your CUDA version (check using `nvcc -V` or `cat /usr/local/cuda/version.txt`) is 9.1, replace `mxnet-cu90` with `mxnet-cu91` in `requirements.txt`. If your machine does not have a GPU, replace `mxnet-cu90` with `mxnet`. Refer to [official mxnet page](https://mxnet.incubator.apache.org/install/index.html?platform=Linux&language=Python&processor=CPU) for available pips.
- `source setup/config.sh`. Make sure we are now working under the mousebrainatlas python virtual environment.
- `cd demo`.

### Install non-python packages

- Install ImageMagick 6.8.9. `sudo apt-get install imagemagick`
- To use GUIs, install PyQt4 into the virtualenv according to [this answer](https://stackoverflow.com/a/28850104).
    - Install python-qt4 globaly: `sudo apt-get install python-qt4`
    - Create symbolic link of PyQt4 to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/PyQt4/ mousebrainatlas_virtualenv/lib/python2.7/site-packages/`
    - Create symbolic link of sip.so to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/sip.x86_64-linux-gnu.so mousebrainatlas_virtualenv/lib/python2.7/site-packages/`


## Preprocess

Note that the `input_spec.ini` files for most steps are different and must be manually created according to the actual input. In the following instructions, "create `input_spec.ini` as (prep_id, version, resolution)" means using the same set of image names as `image_name_list` but set the `prep_id`, `version` and `resolution` accordingly.

- Run `download_demo_data_preprocessing.py` to download necessary data. Make sure the folder content looks like:

```bash
├── brains_info
│   └── DEMO998.ini
├── jp2_files
│   └── DEMO998
│       ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_lossless.jp2
│       ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_lossless.jp2
│       └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_lossless.jp2
├── mxnet_models
│   └── inception-bn-blue
│       ├── inception-bn-blue-0000.params
│       ├── inception-bn-blue-symbol.json
│       └── mean_224.npy
└── operation_configs
    ├── crop_orig.ini
    ├── from_aligned_to_none.ini
    ├── from_aligned_to_padded.ini
    ├── from_aligned_to_wholeslice.ini
    ├── from_none_to_aligned.ini
    ├── from_none_to_brainstem.ini
    ├── from_none_to_padded.ini
    ├── from_none_to_wholeslice.ini
    ├── from_padded_to_brainstem.ini
    ├── from_padded_to_none.ini
    └── from_wholeslice_to_brainstem.ini
```
- **Convert raw images from JPEG2000 to tif**. Edit `DEMO998_raw_input_spec.json`. Set `data_dirs`, `filepath_to_imageName_mapping` and `imageName_to_filepath_mapping`. Run `python jp2_to_tiff.py DEMO998 DEMO998_raw_input_spec.json`.

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_raw
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw.tif
```

- **Extract Neurotrace-blue channel**. Modify `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       └── DEMO998_raw_Ntb
│           ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_Ntb.tif
│           ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_Ntb.tif
│           └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_Ntb.tif
```
- **Rescale to thumbnail**. Modify `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       └── DEMO998_thumbnail_Ntb
│           ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_Ntb.tif
│           ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_Ntb.tif
│           └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_Ntb.tif
```

- **Global intensity normalization**. Modify `input_spec.ini` as (None,Ntb,thumbnail). `python normalize_intensity.py input_spec.ini NtbNormalized`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       └── DEMO998_thumbnail_NtbNormalized
│           ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_NtbNormalized.tif
│           ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_NtbNormalized.tif
│           └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_NtbNormalized.tif
```

- Create `CSHL_data_processed/DEMO998/DEMO998_sorted_filenames.txt`.

- **Align images in this stack**. Modify `operation_configs/from_none_to_aligned.ini`. Modify `input_spec.ini` as (None,NtbNormalized,thumbnail). `python align_compose.py input_spec.ini --op from_none_to_aligned`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       └── DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv
│       ├── DEMO998_elastix_output
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_to_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
│       │   │   ├── elastix.log
│       │   │   ├── IterationInfo.0.R0.txt
│       │   │   ├── IterationInfo.0.R1.txt
│       │   │   ├── IterationInfo.0.R2.txt
│       │   │   ├── IterationInfo.0.R3.txt
│       │   │   ├── IterationInfo.0.R4.txt
│       │   │   ├── IterationInfo.0.R5.txt
│       │   │   ├── result.0.tif
│       │   │   └── TransformParameters.0.txt
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_to_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
│       │       ├── elastix.log
│       │       ├── IterationInfo.0.R0.txt
│       │       ├── IterationInfo.0.R1.txt
│       │       ├── IterationInfo.0.R2.txt
│       │       ├── IterationInfo.0.R3.txt
│       │       ├── IterationInfo.0.R4.txt
│       │       ├── IterationInfo.0.R5.txt
│       │       ├── result.0.tif
│       │       └── TransformParameters.0.txt
```

- **Transform images**. `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_padded --njobs 8`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep1_thumbnail_NtbNormalized
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_NtbNormalized.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_NtbNormalized.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_NtbNormalized.tif
```

- Modify `all_stacks` in `src/utilities/metadata.py` to include `DEMO_998`.

- On a machine with monitor, launch the maskingGUI. Run `DATA_ROOTDIR=/home/yuncong/brainstem/home/yuncong/demo_data ROOT_DIR=/home/yuncong/brainstem/home/yuncong/demo_data THUMBNAIL_DATA_ROOTDIR=/home/yuncong/brainstem/home/yuncong/demo_data python mask_editing_tool_v4.py DEMO998 NtbNormalized`. Generate initial masks.

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep1_thumbnail_anchorInitSnakeContours.pkl
│       ├── DEMO998_prep1_thumbnail_initSnakeContours.pkl
```

- Modify `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini /home/yuncong/demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep1_thumbnail_autoSubmasks
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
│       │   │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_autoSubmask_0.png
│       │   │   └── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_autoSubmaskDecisions.csv
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
│       │   │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_autoSubmask_0.png
│       │   │   └── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_autoSubmaskDecisions.csv
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257
│       │       ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_autoSubmask_0.png
│       │       └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_autoSubmaskDecisions.csv
```

- Re-launch masking GUI to inspect, correct the automatically generated masks, then export as PNGs.

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep1_thumbnail_mask
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_mask.png
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_mask.png
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_mask.png
```

- Modify `input_spec.ini` as (None,NtbNormalized,thumbnail). Run `generate_original_image_crop_csv.py`. 

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_original_image_crop.csv
```
- Modify `operation_configs/crop_orig.ini`. Modify `input_spec.ini` as (alignedPadded,mask,thumbnail). Run `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_thumbnail_mask
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_mask.png
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_mask.png
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_mask.png
```

- **Local adaptive intensity normalization**. Modify `input_spec.ini` as (None,Ntb,raw). `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_intensity_normalization_results
│       │   ├── floatHistogram
│       │   │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_floatHistogram.png
│       │   │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_floatHistogram.png
│       │   │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_floatHistogram.png
│       │   ├── meanMap
│       │   │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_meanMap.bp
│       │   │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_meanMap.bp
│       │   │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_meanMap.bp
│       │   ├── meanStdAllRegions
│       │   │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_meanStdAllRegions.bp
│       │   │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_meanStdAllRegions.bp
│       │   │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_meanStdAllRegions.bp
│       │   ├── normalizedFloatMap
│       │   │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_normalizedFloatMap.bp
│       │   │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_normalizedFloatMap.bp
│       │   │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_normalizedFloatMap.bp
│       │   ├── regionCenters
│       │   │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_regionCenters.bp
│       │   │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_regionCenters.bp
│       │   │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_regionCenters.bp
│       │   └── stdMap
│       │       ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_stdMap.bp
│       │       ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_stdMap.bp
│       │       └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_stdMap.bp
```

- **Whole-slice crop**. Modify `operation_configs/from_none_to_wholeslice.ini`. In this file specify the cropbox for the domain `alignedWithMargin ` based on `alignedPadded` images. Modify `input_spec.ini` as (None,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_wholeslice`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep5_raw_NtbNormalizedAdaptiveInvertedGamma
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
```

- Modify `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
```

- **Brainstem crop**. Modify `operation_configs/from_wholeslice_to_brainstem.ini`. Modify `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep2_raw_NtbNormalizedAdaptiveInvertedGamma
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
```

- Modify `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
```

- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`

```bash
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
```

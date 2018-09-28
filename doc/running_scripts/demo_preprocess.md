## Table of Contents
The preprocessing stage of the code can be broken down into the following 7-8 steps.

1) [Preprocess Setup](#preprocess-setup)
2) [Global Intensity Normalization](#global-intensity-normalization)
3) [Intra-Stack Alignment](#intra-stack-align)
4) [Create Masks](#create-masks)
5) [Local Adaptive Intensity Normalization](#local-adaptive-intensity-normalization)
6) [While-Slice Brain Crop](#whole-slice-crop)
7) [Brainstem Crop](#brainstem-crop)
8) [(Optional) Simple Global Alignment](#optional-obtain-a-simple-global-alignment)

## Changes

- Changed `warp_crop.py` line 91
    - op = load_ini( os.path.join( DATA_ROOTDIR, 'operation_configs', op_name + '.ini'))
- Changed `crop_orig.ini`line 7
    - cropboxes_csv = demo_data/CSHL_data_processed/DEMO998/DEMO998_original_image_crop.csv---[original line]
    - needs to be based off of environment variable, probably delete this line and change code in warp_crop.py
    - cropboxes_csv = /home/alexn/brainDev/demo/DEMO998_original_image_crop.csv---[New, temporary line]
- Changed `distributed_utilities.py` lines 304, 336, 337
    - temp_script = os.path.join( DATA_ROOTDIR, 'runall.sh' )
    - stdout_template = os.path.join( DATA_ROOTDIR, 'stdout_%d.log')
    - stderr_template = os.path.join( DATA_ROOTDIR, 'stderr_%d.log')

## Preprocess

Install ImageMagick 6.8.9.

Note that the `input_spec.ini` files for most steps are different and must be manually created according to the actual input. In the following instructions, "create `input_spec.ini` as (prep_id, version, resolution)" means using the same set of image names as `image_name_list` but set the `prep_id`, `version` and `resolution` accordingly.

To use GUIs, install PyQt4 into the virtualenv according to [this answer](https://stackoverflow.com/a/28850104).

- I used these commands successfully:
- Note, double check the names of `sip*.so` and `PyQt3/*`
```
sudo apt-get install python-qt4
sudo ln -s /usr/lib/python2.7/dist-packages/PyQt4/ /home/alexn/brainDev/mousebrainatlas_virtualenv/lib/python2.7/site-packages/
sudo ln -s /usr/lib/python2.7/dist-packages/sip.x86_64-linux-gnu.so /home/alexn/brainDev/mousebrainatlas_virtualenv/lib/python2.7/site-packages/
```

### Preprocess Setup
- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** create `DEMO998.ini` and put it under `demo_data/brains_info/`
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_input_spec.json`.
- Create `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`
- Create `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
Initial Notes, the first few steps have `` and `` being saved to the REPO_DIR/demo/ which I think is dumb. I'll change them to be saved to the DATA_ROOTDIR when I change this into a script.

- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
  - Downloads the following files
  - Note: The user must create `STACK.ini` themselves for actual script.
```
DATA_ROOTDIR/
│
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
- **(HUMAN)** create `DEMO998.ini` and put it under `demo_data/brains_info/`
  - The following is the contents of the file for this demo:
```
[DEFAULT]
planar_resolution_um = 0.46
section_thickness_um = 20
```
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_input_spec.json`.
  - Accomplished with the following:
    - Note that `data_dirs`, `filepath_to_imageName_mapping`, and `imageName_to_filepath_mapping` all must be changed by the user currently. I am trying to automate this
  - `jp2_to_tiff.py` file seems to also requires user to download `DATA_ROOTDIR/CSHL_data_processed/DEMO998/DEMO998_sorted_filenames.txt` ?
      - Errors found, around line 30. `vr` (version) is set to 'null' for no version but later None is used for this. Causes crash. Change kwargs list to be version='null'
      - distributed_utilities line 304 hard codes `/home/yuncong/runall.sh` as well as std_err and atd_out a few lines after 
- Below is an example .json file. Following that is the output of the command above.
        - This needs to be changed... input_spec.ini is used widely throughout making this very confusing later on..
```
Example DEMO998_input_spec.json:
[
    {"version": null, 
 "resolution": "raw", 
     "data_dirs": "/home/yuncong/MouseBrainAtlas/demo/demo_data/jp2_files/DEMO998/", 
     "filepath_to_imageName_mapping": "/home/yuncong/MouseBrainAtlas/demo/demo_data/jp2_files/DEMO998/(.*)?_lossless.jp2", 
     "imageName_to_filepath_mapping": "/home/yuncong/MouseBrainAtlas/demo/demo_data/jp2_files/DEMO998/%s_lossless.jp2"
    }
]
```
```
DATA_ROOTDIR/
|
├── CSHL_data_processed
│   └── DEMO998
│       ├── DEMO998_raw
│       │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw.tif
│       │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw.tif
│       │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw.tif
│       └── DEMO998_sorted_filenames.txt
├── runall.sh
├── stderr_0.log
└── stdout_0.log
```
- Create `input_spec.ini` as (None,None,raw). `python extract_channel.py input_spec.ini 2 Ntb`
```
Example input_spec.ini file:
[DEFAULT]
image_name_list = MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
    MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
    MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257
stack = DEMO998
prep_id = None
version = None
resol = raw
```
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
    └── DEMO998
        └── DEMO998_raw_Ntb
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_Ntb.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_Ntb.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_Ntb.tif
```
- Create `input_spec.ini` as (None,Ntb,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
```
[DEFAULT]
image_name_list = MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
    MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
    MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257
stack = DEMO998
prep_id = None
version = Ntb
resol = raw
```
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
    └── DEMO998
       └── DEMO998_thumbnail_Ntb
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_Ntb.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_Ntb.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_Ntb.tif
```

------------------------------------------------------------------------------------------------------------------------

### Global intensity normalization
- Create `input_spec.ini` as (None,Ntb,thumbnail). `python normalize_intensity.py input_spec.ini NtbNormalized`

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
- Output of `python normalize_intensity.py input_spec.ini NtbNormalized`
- From now on the `input_spec.ini` file contents that are used will remain in the notebook.
```
DATA_ROOTDIR/
        |
        └── DEMO998_thumbnail_NtbNormalized
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_NtbNormalized.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_NtbNormalized.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_NtbNormalized.tif
```

------------------------------------------------------------------------------------------------------------------------

### Intra-stack align
- **(HUMAN)** Browse thumbnails to verify orientations are all correct.
- **(HUMAN)** Create `from_none_to_aligned.ini` to describe intra-stack alignment operation.
- Create `input_spec.ini` as (None,NtbNormalized,thumbnail). Note that in this file specify `sorted_image_name_list` rather than `image_name_list`. `python align_compose.py input_spec.ini --op from_none_to_aligned`
- `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_padded`
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_gui.py`, correct pairwise transforms and check each image's order in stack.

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
Output from running `python align_compose.py input_spec.ini --op from_none_to_aligned`
  - NOTE: Some trouble on where to save .ini files. `input_spec.ini` always in repo's demo/ folder. `from_none_to_aligned_content.ini` will be ignored here, save to DATA_ROOTDIR.
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
    └── DEMO998
        ├── DEMO998_elastix_output
        │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_to_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
        │   │   ├── elastix.log
        │   │   ├── IterationInfo.0.R0.txt
        │   │   ├── IterationInfo.0.R1.txt
        │   │   ├── IterationInfo.0.R2.txt
        │   │   ├── IterationInfo.0.R3.txt
        │   │   ├── IterationInfo.0.R4.txt
        │   │   ├── IterationInfo.0.R5.txt
        │   │   ├── result.0.tif
        │   │   └── TransformParameters.0.txt
        │   └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_to_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
        │       ├── elastix.log
        │       ├── IterationInfo.0.R0.txt
        │       ├── IterationInfo.0.R1.txt
        │       ├── IterationInfo.0.R2.txt
        │       ├── IterationInfo.0.R3.txt
        │       ├── IterationInfo.0.R4.txt
        │       ├── IterationInfo.0.R5.txt
        │       ├── result.0.tif
        │       └── TransformParameters.0.txt
        └── DEMO998_transforms_to_anchor.csv
```
- Output running `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_padded`
    - Note: warp_crop.py line 92 changed to load_ini from `DATA_ROOTDIR + 'operation_configs/' + op_name + '.ini'`
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
    └── DEMO998
        └── DEMO998_prep1_thumbnail_NtbNormalized
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_NtbNormalized.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_NtbNormalized.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_NtbNormalized.tif

```
NOTE: By the end of GUI step a new STACK_sorted_filenames.txt will be generated, should replace the first and be more accurate. The GUI allows the user to correct files in the wrong order.

------------------------------------------------------------------------------------------------------------------------

### Create masks
- **(HUMAN)** On a machine with monitor, launch the maskingGUI. `DATA_ROOTDIR=/media/yuncong/brainstem/home/yuncong/MouseBrainAtlas/demo/demo_data python mask_editing_tool_v4.py DEMO998`.
Draw initial snake contours.
- Create `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
- **(HUMAN)** Create `DEMO998_original_image_crop.csv`. In this file each row is x,y,width,height in thumbnail resolution.
- Create `input_spec.ini` as (alignedPadded,mask,thumbnail). `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
- **(HUMAN)** On a machine with monitor, launch the maskingGUI. `DATA_ROOTDIR=/media/yuncong/brainstem/home/yuncong/MouseBrainAtlas/demo/demo_data python mask_editing_tool_v4.py DEMO998`.
Draw initial snake contours.
- Create `input_spec.ini` as (alignedPadded,NtbNormalized,thumbnail). `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep1_thumbnail_autoSubmasks
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_autoSubmask_0.png
            │   └── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_autoSubmaskDecisions.csv
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
            │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_autoSubmask_0.png
            │   └── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_autoSubmaskDecisions.csv
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_autoSubmask_0.png
                └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_autoSubmaskDecisions.csv
```
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks.
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep1_thumbnail_userModifiedSubmasks
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_userModifiedParameters.json
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_userModifiedSubmask_0.png
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_userModifiedSubmaskContourVertices.pkl
            │   └── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep1_thumbnail_userModifiedSubmaskDecisions.csv
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250
            │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_userModifiedParameters.json
            │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_userModifiedSubmask_0.png
            │   ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_userModifiedSubmaskContourVertices.pkl
            │   └── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep1_thumbnail_userModifiedSubmaskDecisions.csv
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_userModifiedParameters.json
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_userModifiedSubmask_0.png
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_userModifiedSubmaskContourVertices.pkl
                └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep1_thumbnail_userModifiedSubmaskDecisions.csv
```
- **(HUMAN)** Create `DEMO998_original_image_crop.csv`. In this file each row is x,y,width,height in thumbnail resolution.
        - DEMO998_original_image_crop.csv is annoying to make. Need to do this for every single slice??
```
MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242,77,86,1175,524
MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250,77,86,1175,524
MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257,77,86,1175,524
```
- Create `input_spec.ini` as (alignedPadded,mask,thumbnail). `python warp_crop.py --input_spec input_spec.ini --op_id from_padded_to_none`.
    - Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
    └── DEMO998
        └── DEMO998_thumbnail_mask
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_thumbnail_mask.png
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_thumbnail_mask.png
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_thumbnail_mask.png
```

------------------------------------------------------------------------------------------------------------------------
 
### Local adaptive intensity normalization
- Create `input_spec.ini` as (None,Ntb,raw). `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`

------------------------------------------------------------------------------------------------------------------------
##### Running Notes

```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_intensity_normalization_results
            ├── floatHistogram
            │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_floatHistogram.png
            │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_floatHistogram.png
            │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_floatHistogram.png
            ├── meanMap
            │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_meanMap.bp
            │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_meanMap.bp
            │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_meanMap.bp
            ├── meanStdAllRegions
            │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_meanStdAllRegions.bp
            │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_meanStdAllRegions.bp
            │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_meanStdAllRegions.bp
            ├── normalizedFloatMap
            │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_normalizedFloatMap.bp
            │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_normalizedFloatMap.bp
            │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_normalizedFloatMap.bp
            ├── regionCenters
            │   ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_regionCenters.bp
            │   ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_regionCenters.bp
            │   └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_regionCenters.bp
            └── stdMap
                ├── DEMO998_MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_raw_stdMap.bp
                ├── DEMO998_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_raw_stdMap.bp
                └── DEMO998_MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_raw_stdMap.bp
```
------------------------------------------------------------------------------------------------------------------------

### Whole-slice crop
- **(HUMAN)** Create `from_none_to_wholeslice.ini`. In this file specify the cropbox for the domain `alignedWithMargin ` based on `alignedPadded` images. This cropbox can also be automatically inferred as padding 20 thumbnail-resolution pixels surrounding the `alignedPadded` masks.
- Create `input_spec.ini` as (None,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_wholeslice`
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
- **(HUMAN)** Create `from_none_to_wholeslice.ini`. In this file specify the cropbox for the domain `alignedWithMargin ` based on `alignedPadded` images. This cropbox can also be automatically inferred as padding 20 thumbnail-resolution pixels surrounding the `alignedPadded` masks.
    - Below is the file contents I found from Yuncong's tests
```
[DEFAULT]
operation_sequence = from_none_to_aligned
	from_aligned_to_wholeslice
```
- Create `input_spec.ini` as (None,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_none_to_wholeslice`
    - Ran with: `python warp_crop.py --input_spec input_spec.ini --op_id /media/alexn/BstemAtlasDataBackup/demo_preprocess/operation_configs/from_none_to_wholeslice`
    - Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep5_raw_NtbNormalizedAdaptiveInvertedGamma
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep5_raw_NtbNormalizedAdaptiveInvertedGamma.tif
```
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
    - Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
```
------------------------------------------------------------------------------------------------------------------------

### Brainstem crop
- **(HUMAN)** Create `from_wholeslice_to_brainstem.ini`. Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin or alignedPadded thumbnails.
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`

------------------------------------------------------------------------------------------------------------------------
##### Running Notes
- **(HUMAN)** Create `from_wholeslice_to_brainstem.ini`. Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin or alignedPadded thumbnails.
	- It seems this file doesn't need to be changed..
	- `from_padded_to_wholeslice.ini` needs to be changed
		- Add rostral_limit, caudal_limit, dorsal_limit, ventral_limit information!
- Create `input_spec.ini` as (alignedWithMargin,NtbNormalizedAdaptiveInvertedGamma,raw). `python warp_crop.py --input_spec input_spec.ini --op_id from_wholeslice_to_brainstem`
	- Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep2_raw_NtbNormalizedAdaptiveInvertedGamma
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
```
- Create `input_spec.ini` as (alignedBrainstemCrop,NtbNormalizedAdaptiveInvertedGamma,raw). `python rescale.py input_spec.ini thumbnail -f 0.03125`
	- Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_thumbnail_NtbNormalizedAdaptiveInvertedGamma.tif
```
- Use the same `input_spec.ini` as previous step. `python compress_jpeg.py input_spec.ini`
	- Output below
```
DATA_ROOTDIR/
|
└── CSHL_data_processed
        └── DEMO998_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
            ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
```
------------------------------------------------------------------------------------------------------------------------

## (Optional) Obtain a simple global alignment

This can serve two purposes:
1. It allows us to estimate a probable region of the brain volume for each structure. We can compute features only on these regions to save computation. 
2. It can be used as a starting point for the structure-specific registration later.

- Pick the center of 12N and of 3N at sagittal midline. Input them into `registration_v7_atlasV7_simpleGlobal.ipynb` to compute the simple global transform.
- Then run the `# Identify 3-d bounding box of each simpleGlobal aligned structure` part of `from_images_to_score_volume.ipynb` to generate structure ROIs.


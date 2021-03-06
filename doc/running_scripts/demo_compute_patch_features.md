```
./demo/download_demo_data_compute_features.py
./demo_compute_features.py DEMO999 --section 225 --version NtbNormalizedAdaptiveInvertedGamma
./demo_compute_features.py DEMO999 --section 235 --version NtbNormalizedAdaptiveInvertedGamma
```

---
This demo is expected to finish in 1 minute.

## Summary
For the sake of generalization the following substitutions will be used.
- `STACK` = the name of the current brain stack, ex: 'MD662', 
- `SLICE` = the name of the current slice, this is typically long, ex: 'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
- `ANCHOR` = a particular SLICE, all other slices are aligned to this ANCHOR

This particular version of the script only computes features for two slices, I will denote them specially as `SLICECF`. For these files you only need the slices you need to compute features for. For the previously defined `SLICE`, all files in the `STACK` must be included no matter what.
- `SLICECF` = the slice you are computing features for. Stands for Slice Compute Features


#### INPUTS:

```
CSHL_data_processed/
└── STACK
    ├── STACK_alignedTo_ANCHOR_prep2_cropbox.json                 ??
    ├── STACK_alignedTo_ANCHOR_prep2_sectionLimits.json           ??
    ├── STACK_anchor.txt
    ├── STACK_sorted_filenames.txt
    ├── STACK_prep1_thumbnail_mask
    │   └── SLICE_prep1_thumbnail_mask.png      [for all 272 slices]
    └── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGamma
        ├── SLICECF_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
        └── SLICECF_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif
```

#### OUTPUTS:
Two files listed below. For every `SLICECF`, there will be these two files generated.

```
CSHL_patch_features/
└── inception-bn-blue
    └── STACK
        └── STACK_prep2_none_win7
            ├── SLICECF_prep2_none_win7_inception-bn-blue_features.bp
            └── SLICECF_prep2_none_win7_inception-bn-blue_locations.bp
```

#### INTERMEDIATE FILES:
For every `SLICECF` the .tiff files are converted to .jpg files. This should not be considered ouputs but an intermediate step.

```
CSHL_data_processed/
└── STACK
    └── STACK_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
        └── SLICECF_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
```

## Full Alex Running Notes

For the first command: `demo/download_demo_data_compute_features.py`:
- Downloads all necessary files.
- Ran with `python demo/download_demo_data_compute_features.py --demo_data_dir /media/alexn/BstemAtlasDataBackup/demo/` to copy all files into the external hard drive. Only takes in 1 arg which is the download dir, otherwise defaults to ./demo_data. All files go into `[demo_data_dir]/CSHL_data_processed/DEMO999/` from `s3://mousebrainatlas-data/CSHL_data_processed/DEMO999/`, Downloaded 4 files:
  - `DEMO999_sorted_filenames.txt`
  - `DEMO999_anchor.txt`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_sectionLimits.json`
    - `{"left_section_limit": 85, "right_section_limit": 356}`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_cropbox.json`
    - `{"rostral_limit": 468, "ventral_limit": 620, "caudal_limit": 1244, "dorsal_limit": 129}`
- After these are downloaded, a for loop is traversed to download the `*_prep1_thumbnail_mask.png` for every section downloading into `THUMBNAIL_DATA_ROOTDIR/CSHL_data_processed/DEMO999_prep1_thumbnail_mask/`. 
 - 272 `*_MD661_#_####_prep1_thumbnail_mask.png` files
- Following that, two `*_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif` files are downloaded into `THUMBNAIL_DATA_ROOTDIR/CSHL_data_processed/DEMO999_prep2_raw_NtbNormalizedAdaptiveInvertedGamma/`
  - `MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif`, denoted section 225
  - `MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGamma.tif`, denoted section 235
- Creates directory `DATA_ROOTDIR/mxnet_models/inception-bn-blue/`. The following 3 files should be inside:
      - `inception-bn-blue-0000.params`
      - `inception-bn-blue-symbol.json`
      - `mean_224.npy`
      
For the second command `compute_features_demo.py` for section 225:
- Make sure that the demo downloads the same section you are computing features for. (Demo only does 1 section, hard coded in the download script) Script can easily be changed to do every single section.
- OUTPUTS: (all saved to `DATA_ROOTDIR/CSHL_patch_features/inception-bn-blue/DEMO999/DEMO999_prep2_none_win7/`)
  - `MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_none_win7_inception-bn-blue_features.bp`
  - `MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_none_win7_inception-bn-blue_locations.bp`
  - To generalize, for every section two files are generated. Features and Locations, outputted as a bloscpack file. Features are a high dimensional vector that encodes properties of the images.
  
For the third command `compute_features_demo.py` for section 235:
- Make sure that the demo downloads the same section you are computing features for. (Demo only does 1 section, hard coded in the download script) Script can easily be changed to do every single section.
- OUTPUTS: (all saved to `DATA_ROOTDIR/CSHL_patch_features/inception-bn-blue/DEMO999/DEMO999_prep2_none_win7/`)
  - `MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_none_win7_inception-bn-blue_features.bp`
  - `MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_none_win7_inception-bn-blue_locations.bp`



## Description & Help

- NOTE: Script requires the following files to function: `STACK_cropbix.ini`, `STACK_anchor.txt`, `STACK_sorted_filenames.txt`, all located in `ROOT/CSHL_data_processed/`. These files are used to populate metadata_cache line 5438 of data_manager.py. The brains loaded into metadata_cache are set in metadata.py line 597.

- NOTE: Also requires the following user created file: `DATA_ROOTDIR/brain_info/STACK.ini`

Generating `STACK_cropbix.ini` is very easy. Open up a slice in Gimp, the highest and widest slice you can find, and make a box around the brainstem, there is a screenshot in my folder showing exactly how to do this. You need to generate 4 numbers (each one denotes a number of pixels). Xmin, Xmin, Ymin, Ymax.

### script download_demo_data_compute_features.py
---
description = 'This script downloads input data for demo.'

#### Args:
--demo_data_dir: type=str, help='Directory to store demo input data, must equal THUMBNAIL_DATA_ROOTDIR'

### script demo_compute_features.py
---
description = 'Computes features for specified sections, runs two orders of magnitude faster using a GPU.'

#### Args:
brain_name: type=str, help="Brain name"

--section: type=int, help="Section number. If specified, do detection on this one section; otherwise, use all valid sections."

--version": type=str, help="Image version"

--win_id": type=int, help="Window id (Default: %(default)s).", default=7

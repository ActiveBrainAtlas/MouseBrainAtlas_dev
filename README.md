This repo is in development as scripts are still being stitched together and code is being tested on new brains. A pipeline is being constructed, beginning with the preprocessing steps of which there are about 14. These preprocessing steps are outlined below as well as a compilation of useful documentation.

Notebooks that have been significantly altered from the original version:
  - preprocess_cshl_data_v2_neurotrace.ipynb
  - preprocess_ucsd_data_v2.ipynb
  - brightness_correction.ipynb
  - distributed_utilities.py
  - utilities2015.py

## Preprocessing details

For an in depth explanation of the code from the original developer look here at the [Original User Guide](doc/User%20Manuals/UserGuide.md). Inside is a link to `Preprocessing.md` which discusses the preprocessing steps in detail and the differences between different stain types. These files are intended to be replaced/altered in the coming weeks but remain the best reference for the code.

As of right now about 9 of the steps have been consolidated into `/preprocess_new/preprocess_cshl_ntb.ipynb` which specifically is geared toward brains stained with NeuroTrace blue. Minor changes will need to be made when a new brain stain type comes in.

### Preprocessing Steps:

1) raw (.jp2) -> raw_Ntb (.tif): extract_a single channel
2) raw_Ntb -> thumbnail_Ntb: rescale
3) thumbnail_Ntb -> thumbnail_NtbNormalized: normalize_intensity
4) Compute transforms using thumbnail_NtbNormalized: align + compose 
5) Supply prep1_thumbnail_mask :
  - use GUI with `prep1_thumbnail_normalized` images to check they are aligned properly
6) prep1_thumbnail_mask -> thumbnail_mask: warp
7) raw_Ntb -> raw_NtbNormalizedAdaptiveInvertedGamma: brightness_correction
8) Compute prep5 (alignedWithMargin) cropping box based on prep1_thumbnail_mask
9) raw_NtbNormalizedAdaptiveInvertedGamma -> prep5_raw_NtbNormalizedAdaptiveInvertedGamma: align + crop
10) thumbnail_NtbNormalized -> prep5_thumbnail_NtbNormalized: align + crop
11) prep5_raw_NtbNormalizedAdaptiveInvertedGamma -> prep5_thumbnail_NtbNormalizedAdaptiveInvertedGamma: rescale
12) Specify prep2 (alignedBrainstemCrop) cropping box
13) prep5_raw_NtbNormalizedAdaptiveInvertedGamma -> prep2_raw_NtbNormalizedAdaptiveInvertedGamma: crop
14) prep2_raw_NtbNormalizedAdaptiveInvertedGamma -> prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg: compress_jpeg

* Doc: documentation
* src: code

### Organizing Preprocessing

The previous 14 steps will be broken down even farthur into straightforward, easy to follow notebooks. These notebooks will in turn be broken down into executables but until then they work well organizing the code while being functional.

##### Steps 1-3
- raw files (CZI or JP2) are converted to raw tiff files and seperate the RGB channels. 
- The raw tiff files are then downsampled 32X into thumbnail files. 
- These thumbnail files are intensity normalized and then are reformatted from 16bit to 8bit
  - Final output is `*_thumbnail_NtbNormalized.tif` files

##### Steps 4-5
- Pairwise transforms (denoted prep1) are generated through a program called Elastix. 
  - Outputs saved in `~/Elastix_output/`
- A GUI is run that allows the user to double check and make sure each transformation is correct (typically 3% will fail)
  - Outputs saved in `~/custom_transform/` which will override the Elastix output transforms
- An anchor file is selected that other images transform relative to
  - `gui/preprocess_tool_v3.py` is run and `Anchor.txt` is created, only holding the name of the anchor file
- Transformation matrices are generated for each file
  - saved under `~/transformsTo_[ANCHOR]_.pkl`, stored as Python dictionary
- `*_prep1_thumnail_normalized.tif` files generated from the transformations
- The prep1 thumbnails are fed into the Active Contour Algorithm which generates prep1 thumbnail masks

### Buckets and Directories

 - `RAW`: All *\_raw.j2 are stored in Bucket mousebrainatlas-rawdata (as well *_lossy* files that are typically unused).
 - `DATA`: Bucket mousebrainatlas-data contains ALL other files.
 

Naming conventions are the each file has a unique filename, FILENAME. Every different transform of the file will have the naming convention FILE_SUFFIX where SUFFIX is an abbreviated description of the file's state.

`DATA` files will always be in *.tif form unless otherwise stated. One important exception is that the `RAW` files given to us are typically in the format *\_lossless.jp2.

Examples:
[FILENAME STEM] = `MD662&661-F1-2017.06.02-17.07.55_MD662_1_0001`
- raw_input = `MD662&661-F1-2017.06.02-17.07.55_MD662_1_0001_lossless.jp2`
- output_1 = `MD662&661-F1-2017.06.02-17.07.55_MD662_1_0001_raw_Ntb.tif`
- output_2 = `MD662&661-F1-2017.06.02-17.07.55_MD662_1_0001_thumbnail_Ntb.tif`

STACKNAME = the unique identifier for every stack. Example: MD662

folder naming conventions: STACKNAME_SUFFIX/

### File naming convensions

How different images are named can be found in [Image Naming Conventions](doc/User%20Manuals/user_guide_pages/imageNamingConventions.md)

Every slice has four major identifiers:
* image name: a string that uniquely identifies a physical section.
* prep id: a number or word that identifies the spatial adjustment operations applied.
* version: a word that specifies particular channel or appearance adjustment operations.
* resolution: a word that specifies the pixel resolution.

<br><br>

## Useful documentation files

## List of Guides
- [Alex User Guide](doc/RunningFiles.md)
  - Running Guide made by AlexN to assist with running the code [INC]
- **[Historical]** [Yuncong User Guide](doc/User%20Manuals/UserGuide.md)
  - User Guide made by Yuncong to assist with running the code

- **[Historical/Incomplete]** [Dev Guide](doc/DeveloperGuide.md)
  - Incomplete to-be guide of entire running process
- **[Historical]** [Registration Steps](doc/Analysis.md)
  - Guide for Registration with list of relevant scripts
- **[Historical]** [Old README](doc/old_readme.md)
  - Yuncong's old README

## Server Information
- [File Transfer](doc/TransferFiles.md)
  - Guide for transferring files to/from AWS S3 and Birdstore
- [AWS Instructions](doc/writeup/AWS_instruction.md)
  - AWS instruction manual

## File Organization
- **[Incomplete]** [S3 File Organization](doc/writeup/S3_file_organization.md)
  - Naming conventions in S3 storage [INC]
- [Stack Directories](doc/Brain_stack_directories.md)
  - Description of every stack, all relevant information

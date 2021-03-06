
## Definitions from `convert_frame_and_resolution`, data_manager.py line 440

- `wholebrain`: formed by stacking all sections of prep1 (aligned + padded) images
- `wholebrainWithMargin`: tightly wrap around brain tissue. The origin is the nearest corner of the bounding box of all images' prep1 masks.
- `wholebrainXYcropped`: formed by stacking all sections of prep2 images
- `brainstemXYfull`: formed by stacking sections of prep1 images that contain brainstem
- `brainstem`: formed by stacking brainstem sections of prep2 images
- `brainstemXYFullNoMargin`: formed by stacking brainstem sections of prep4 images


Build-in 2-D frames include:
- {0: `original`, 1: `alignedPadded`, 2: `alignedCroppedBrainstem`, 3: `alignedCroppedThalamus`, 4: `alignedNoMargin`, 5: `alignedWithMargin`, 6: `originalCropped`}


## Alignment file naming schema

Alignments are always with respect to a certain brain. Alignment files always contain the keywords `_wrt_<BRAIN_TYPE>` to indicate this. There are 4 major "brain types" that I list below.
  - canonicalAtlasSpace
  - wholebrain
  - wholebrainWithMargin
  - wholebrainXYcropped
  - fixedWholebrain

## Files containing alignment parameters

All filepaths given begin at the root of the "mousebrainatlas-data" bucket in S3.

#### Generating Intensity Volume

`CSHL_volumes/STACK/STACK_wholebrainWithMargin_10.0um_intensityVolume/STACK_prep2_none_win7/STACK_wholebrainWithMargin_10.0um_intensityVolume_origin_wrt_wholebrain.txt`
  - Aligns "wholebrainWithMargin" to "wholebrain"
  - X,Y,Z offsets
  
#### Simple Global Alignment
  
`CSHL_simple_global_registration/STACK_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.txt`
  - Aligns "canonicalAtlasSpace" to "wholebrain"_atlasResol
  - Parameters give global alignment of cononical atlas to current brain
  - 12 total parameters, unsure how they are oranized

`CSHL_simple_global_registration/STACK_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json`
  - Aligns registered atlas structures to "wholebrainXYcropped"
  - Contains bounding boxes for every structure? X1,Y1,Z1,X2,Y2,Z2
  
`CSHL_volumes/STACK/STACK_detector###_10.0um_scoreVolume/score_volumes/STACK_detector###_10.0um_scoreVolume_STR_origin_wrt_wholebrain.txt`
  - X,Y,Z offsets

#### Generating Probability Volumes
  - `CSHL_volumes/STACK/STACK_detector799_10.0um_scoreVolume/score_volumes/STACK_detector799_10.0um_scoreVolume_STR-RL_origin_wrt_wholebrain.txt`
  - X,Y,Z offsets

#### Registration
  - `CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um/score_volumes/atlasV7_10.0um_scoreVolume_STR-RL_warp7_STACK_detector799_10.0um_scoreVolume_STR-RL_10.0um_STR-RL_origin_wrt_fixedWholebrain.txt`
  - X,Y,Z offsets



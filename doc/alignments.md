## Alignment file naming schema

Alignments are always with respect to a certain brain. Alignment files always contain the keywords `_wrt_<BRAIN_TYPE>` to indicate this. There are 4 major "brain types" that I list below.
  - canonicalAtlasSpace
  - wholebrain
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

#### INC
  - 

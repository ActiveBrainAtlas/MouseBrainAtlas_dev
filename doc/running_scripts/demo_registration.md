
Commands:
```
./demo/download_demo_data_registration.py
./demo/register_brains_demo_12N.py
./demo/register_brains_demo_3N_R_4N_R.py
./demo/visualize_registration_demo_3_structures.py
```
The download takes less than 1 minute. The following 3 commands are detailed below:
- register 12N (hypoglossal nucleus) individually.
- register 3N_R (occulomotor, right) and 4N_R (trochlear, right) as a group.
- visualize the aligned atlas overlaid on original images

NOTE: The user must create `fixed_brain_spec_[STRUCTURE].json` and `moving_brain_spec_[STRUCTURE].json` files in the ROOT_DIR for registration to work properly. An example of this can be found in the next section.

---

## Example json file
`demo_fixed_brain_spec_12N.json` was used for the original demo which contained: 
```
{
"name":"DEMO999", 
"vol_type": "score", 
"resolution":"10.0um",
"detector_id":799,
"structure":["12N"]
}
```
- name: stack name
- vol_type: ?
- resolution: self explanitory
- detector_id: Sets detector settings (look below at detector settings link)
- structure: name of specific brain structure

[Classifier Settings](https://github.com/CodingDonky/MouseBrainAtlas/blob/master/learning/classifier_settings.csv)
[Detector Settings](https://github.com/CodingDonky/MouseBrainAtlas/blob/master/learning/detector_settings.csv)

## Summary
For the sake of generalization the following substitutions will be used.
- `STACK` = the name of the current brain stack, ex: 'MD662', 
- `SLICE` = the name of the current slice, this is typically long, ex: 'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
- `ANCHOR` = a particular SLICE, all other slices are aligned to this ANCHOR
- `SLICECF` = the slice you have computed features for. Must have run these slices through the last demo script fully (2 slices for the demo).

Folders already present:
`CSHL_classifiers,  CSHL_data_processed,  CSHL_patch_features,  CSHL_scoremaps,  CSHL_scoremap_viz,  CSHL_simple_global_registration,  CSHL_volumes,  mxnet_models`


#### INPUTS:
For Registration:
```
├── CSHL_data_processed
│   └── DEMO999
│       ├── DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_sectionLimits.json
│       ├── DEMO999_anchor.txt
│       └── DEMO999_sorted_filenames.txt
├── CSHL_simple_global_registration
│   └── DEMO999_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.bp
└── CSHL_volumes
    ├── atlasV7
    │   └── atlasV7_10.0um_scoreVolume
    │       └── score_volumes
    │           ├── atlasV7_10.0um_scoreVolume_12N.bp
    │           ├── atlasV7_10.0um_scoreVolume_12N_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_12N_surround_200um.bp
    │           ├── atlasV7_10.0um_scoreVolume_12N_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_3N_R.bp
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um.bp
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_4N_R.bp
    │           ├── atlasV7_10.0um_scoreVolume_4N_R_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_4N_R_surround_200um.bp
    │           └── atlasV7_10.0um_scoreVolume_4N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    └── DEMO999
        └── DEMO999_detector799_10.0um_scoreVolume
            └── score_volumes
                ├── DEMO999_detector799_10.0um_scoreVolume_12N.bp
                ├── DEMO999_detector799_10.0um_scoreVolume_12N_origin_wrt_wholebrain.txt
                ├── DEMO999_detector799_10.0um_scoreVolume_3N_R.bp
                ├── DEMO999_detector799_10.0um_scoreVolume_3N_R_origin_wrt_wholebrain.txt
                ├── DEMO999_detector799_10.0um_scoreVolume_4N_R.bp
                └── DEMO999_detector799_10.0um_scoreVolume_4N_R_origin_wrt_wholebrain.txt
```

For Visualization:
```
demo_data/
├── CSHL_data_processed
│   └── DEMO999
│       └── DEMO999_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg
│           ├── MD662&661-F79-2017.06.06-11.52.28_MD661_2_0236_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F80-2017.06.06-12.18.56_MD661_1_0238_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F80-2017.06.06-12.18.56_MD661_2_0239_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F81-2017.06.06-12.44.40_MD661_1_0241_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F82-2017.06.06-13.10.59_MD661_1_0244_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F82-2017.06.06-13.10.59_MD661_2_0245_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F83-2017.06.06-13.37.35_MD661_1_0247_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F83-2017.06.06-13.37.35_MD661_2_0248_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F84-2017.06.06-14.03.51_MD661_2_0251_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F85-2017.06.06-14.30.01_MD661_1_0253_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F85-2017.06.06-14.30.01_MD661_2_0254_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F86-2017.06.06-14.56.48_MD661_1_0256_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           ├── MD662&661-F87-2017.06.06-15.22.59_MD661_1_0259_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
│           └── MD662&661-F87-2017.06.06-15.22.59_MD661_2_0260_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg
├── CSHL_simple_global_registration
│   └── DEMO999_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json
└── CSHL_volumes
    ├── atlasV7
    │   └── atlasV7_10.0um_scoreVolume
    │       └── score_volumes
    │           ├── atlasV7_10.0um_scoreVolume_12N.bp
    │           ├── atlasV7_10.0um_scoreVolume_12N_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_12N_surround_200um.bp
    │           ├── atlasV7_10.0um_scoreVolume_12N_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_3N_R.bp
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um.bp
    │           ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_4N_R.bp
    │           ├── atlasV7_10.0um_scoreVolume_4N_R_origin_wrt_canonicalAtlasSpace.txt
    │           ├── atlasV7_10.0um_scoreVolume_4N_R_surround_200um.bp
    │           └── atlasV7_10.0um_scoreVolume_4N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
    └── DEMO999
        └── DEMO999_wholebrainWithMargin_10.0um_intensityVolume
            ├── DEMO999_wholebrainWithMargin_10.0um_intensityVolume.bp
            └── DEMO999_wholebrainWithMargin_10.0um_intensityVolume_origin_wrt_wholebrain.txt
```

#### OUTPUTS:
##### For command 2, `demo/register_brains_demo_12N.py`:
```
CSHL_registration_parameters/
└── atlasV7
    └── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N
        ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_parameters.json
        ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_scoreEvolution.png
        ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_scoreHistory.bp
        └── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_trajectory.bp
```

Note, everything under the folder `atlasV7` was simply downloaded from S3. This is the complete Atlas.
```
CSHL_volumes/          ?? maybe
└── DEMO999
    └── DEMO999_wholebrainWithMargin_10.0um_intensityVolume
        ├── DEMO999_wholebrainWithMargin_10.0um_intensityVolume.bp
        └── DEMO999_wholebrainWithMargin_10.0um_intensityVolume_origin_wrt_wholebrain.txt

```
```
CSHL_simple_global_registration/
└── DEMO999_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.bp
```
```
CSHL_volumes/
└── atlasV7
    ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_10.0um
    │   └── score_volumes
    │       ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_10.0um_12N.bp
    │       ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_10.0um_12N_origin_wrt_fixedWholebrain.txt
    │       ├── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_10.0um_12N_surround_200um.bp
    │       └── atlasV7_10.0um_scoreVolume_12N_warp7_DEMO999_detector799_10.0um_scoreVolume_12N_10.0um_12N_surround_200um_origin_wrt_fixedWholebrain.txt
    └── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um
        └── score_volumes
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_12N.bp
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_12N_origin_wrt_fixedWholebrain.txt
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_12N_surround_200um.bp
            └── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_12N_surround_200um_origin_wrt_fixedWholebrain.txt
```


##### For command 3, `demo/register_brains_demo_3N_R_4N_R.py`:
```
CSHL_registration_parameters/
└── atlasV7
    └── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R
        ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_parameters.json
        ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreEvolution.png
        ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreHistory.bp
        └── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_trajectory.bp
```

```
CSHL_volumes/
└── atlasV7
    ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um
    │   └── score_volumes
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R.bp
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R_origin_wrt_fixedWholebrain.txt
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R_surround_200um.bp
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R_surround_200um_origin_wrt_fixedWholebrain.txt
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_4N_R.bp
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_4N_R_origin_wrt_fixedWholebrain.txt
    │       ├── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_4N_R_surround_200um.bp
    │       └── atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_4N_R_surround_200um_origin_wrt_fixedWholebrain.txt
    └── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um
        └── score_volumes
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_3N_R.bp
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_3N_R_origin_wrt_fixedWholebrain.txt
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_3N_R_surround_200um.bp
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_3N_R_surround_200um_origin_wrt_fixedWholebrain.txt
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_4N_R.bp
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_4N_R_origin_wrt_fixedWholebrain.txt
            ├── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_4N_R_surround_200um.bp
            └── atlasV7_10.0um_scoreVolume_warp0_DEMO999_detector799_10.0um_scoreVolume_10.0um_4N_R_surround_200um_origin_wrt_fixedWholebrain.txt

```

##### For command 4, `demo/visualize_registration_demo_3_structures.py`:
```
CSHL_registration_visualization
 └── DEMO998_atlas_aligned_multilevel_down16_all_structures
     └── NtbNormalizedAdaptiveInvertedGammaJpeg
         ├── DEMO998_NtbNormalizedAdaptiveInvertedGammaJpeg_230.jpg
         └── DEMO998_NtbNormalizedAdaptiveInvertedGammaJpeg_235.jpg

```

##### Downloaded from S3 before any outputs generated:
```
CSHL_volumes/
    └── atlasV7
        └── atlasV7_10.0um_scoreVolume
            └── score_volumes
                ├── atlasV7_10.0um_scoreVolume_12N.bp
                ├── atlasV7_10.0um_scoreVolume_12N_origin_wrt_canonicalAtlasSpace.txt
                ├── atlasV7_10.0um_scoreVolume_12N_surround_200um.bp
                ├── atlasV7_10.0um_scoreVolume_12N_surround_200um_origin_wrt_canonicalAtlasSpace.txt
                ├── atlasV7_10.0um_scoreVolume_3N_R.bp
                ├── atlasV7_10.0um_scoreVolume_3N_R_origin_wrt_canonicalAtlasSpace.txt
                ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um.bp
                ├── atlasV7_10.0um_scoreVolume_3N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
                ├── atlasV7_10.0um_scoreVolume_4N_R.bp
                ├── atlasV7_10.0um_scoreVolume_4N_R_origin_wrt_canonicalAtlasSpace.txt
                ├── atlasV7_10.0um_scoreVolume_4N_R_surround_200um.bp
                └── atlasV7_10.0um_scoreVolume_4N_R_surround_200um_origin_wrt_canonicalAtlasSpace.txt
```


## Alex Running Notes

#### For running the first command `demo/download_demo_data_registration.py`:
***
- Ran with `./demo/download_demo_data_registration.py --demo_data_dir /media/alexn/BstemAtlasDataBackup/demo`.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`
***

#### For running the second command `demo/register_brains_demo_12N.py`:
- ran with `demo/register_brains_demo_12N.py -r 7 -g`. Requires adding filepath to json files in repo's dmeo folder.
- Outputs shown in summary, too many to list properly.

#### For running the second command `demo/register_brains_demo_3N_R_4N_R.py`:
- Outputs shown in summary, too many to list properly.

---
### PRE-VISUALIZATION
- This step currently missing from the pipeline!
- Run `python ../src/reconstruct/construct_intensity_volume.py STACK --tb_version NtbNormalizedAdaptiveInvertedGamma --tb_resol thumbnail --output_resol 10.0um`
    - Output below
```
└── CSHL_volumes
    └── DEMO998
        └── DEMO998_wholebrainWithMargin_10.0um_intensityVolume
            ├── DEMO998_wholebrainWithMargin_10.0um_intensityVolume.bp
            └── DEMO998_wholebrainWithMargin_10.0um_intensityVolume_origin_wrt_wholebrain.txt
```
---

### For running the third command `demo/visualize_registration_demo_3_structures.py`:
- Outputs shown in summary, too many to list properly.

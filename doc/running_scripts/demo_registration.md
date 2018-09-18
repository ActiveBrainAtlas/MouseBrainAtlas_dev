
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

---

## Summary
For the sake of generalization the following substitutions will be used.
- `STACK` = the name of the current brain stack, ex: 'MD662', 
- `SLICE` = the name of the current slice, this is typically long, ex: 'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
- `ANCHOR` = a particular SLICE, all other slices are aligned to this ANCHOR
- `SLICECF` = the slice you have computed features for. Must have run these slices through the last demo script fully (2 slices for the demo).

Folders already present:
`CSHL_classifiers,  CSHL_data_processed,  CSHL_patch_features,  CSHL_scoremaps,  CSHL_scoremap_viz,  CSHL_simple_global_registration,  CSHL_volumes,  mxnet_models`


#### INPUTS:

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
```
return code: 0
Traceback (most recent call last):
  File "./demo/download_demo_data_registration.py", line 76, in <module>
    fp = DataManager.get_image_filepath_v2(stack='DEMO999', prep_id=2, resol='raw', version='NtbNormalizedAdaptiveInvertedGammaJpeg', section=sec)
  File "/home/alexn/brainDev/setup/../src/utilities/data_manager.py", line 4767, in get_image_filepath_v2
    fn = metadata_cache['sections_to_filenames'][stack][section]
KeyError: 'DEMO999'
```

#### OUTPUTS:

```

```


## Alex Running Notes

#### For running the first command `demo/download_demo_data_registration.py`:
***
- Ran with `python demo/download_demo_data_generate_prob_volumes.py --demo_data_dir $ROOT_DIR`. Downloading the files takes at least 3-5 hours.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`
***

#### For running the second command `demo/register_brains_demo_12N.py`:
- Outputs shown in summary, too many to list properly.

#### For running the second command `demo/register_brains_demo_3N_R_4N_R.py`:
- Outputs shown in summary, too many to list properly.

### For running the third command `demo/visualize_registration_demo_3_structures.py`:
- Outputs shown in summary, too many to list properly.

Commands:
```
./demo/download_demo_data_scoring.py
./demo/from_images_to_score_volumes_demo.py DEMO999 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"
```

---

Note that the data needed to download for this demo is about 35G. It may take a few hours to download.

## Summary
For the sake of generalization the following substitutions will be used.
- `STACK` = the name of the current brain stack, ex: 'MD662', 
- `SLICE` = the name of the current slice, this is typically long, ex: 'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
- `ANCHOR` = a particular SLICE, all other slices are aligned to this ANCHOR
- `SLICECF` = the slice you have computed features for. Must have run these slices through the last demo script fully (2 slices for the demo).


#### INPUTS:

```
CSHL_patch_features/
└── inception-bn-blue
    └── STACK
        └── STACK_prep2_none_win7
            ├── SLICE_prep2_none_win7_inception-bn-blue_features.bp
            └── SLICE_prep2_none_win7_inception-bn-blue_locations.bp
```

#### OUTPUTS:
As this version of the scripts only acts on the structures 3N, 4N, and 12N, this is the output for those structures specifically. The other 25 will be present during actual analysis.

```
 CSHL_simple_global_registration/
└── DEMO999_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json
CSHL_classifiers/
└── setting_899
    └── classifiers
        ├── 12N_clf_setting_899.dump
        ├── 3N_clf_setting_899.dump
        └── 4N_clf_setting_899.dump
```

```
CSHL_volumes/
└── STACK
    └── STACK_detector799_10.0um_scoreVolume
        ├── score_volume_gradients
        │   ├── STACK_detector799_10.0um_scoreVolume_12N_gradients.bp
        │   ├── STACK_detector799_10.0um_scoreVolume_12N_origin_wrt_wholebrain.txt
        │   ├── STACK_detector799_10.0um_scoreVolume_3N_L_gradients.bp
        │   ├── STACK_detector799_10.0um_scoreVolume_3N_L_origin_wrt_wholebrain.txt
        │   ├── STACK_detector799_10.0um_scoreVolume_3N_R_gradients.bp
        │   ├── STACK_detector799_10.0um_scoreVolume_3N_R_origin_wrt_wholebrain.txt
        │   ├── STACK_detector799_10.0um_scoreVolume_4N_L_gradients.bp
        │   ├── STACK_detector799_10.0um_scoreVolume_4N_L_origin_wrt_wholebrain.txt
        │   ├── STACK_detector799_10.0um_scoreVolume_4N_R_gradients.bp
        │   └── STACK_detector799_10.0um_scoreVolume_4N_R_origin_wrt_wholebrain.txt
        └── score_volumes
            ├── STACK_detector799_10.0um_scoreVolume_12N.bp
            ├── STACK_detector799_10.0um_scoreVolume_12N_origin_wrt_wholebrain.txt
            ├── STACK_detector799_10.0um_scoreVolume_3N_L.bp
            ├── STACK_detector799_10.0um_scoreVolume_3N_L_origin_wrt_wholebrain.txt
            ├── STACK_detector799_10.0um_scoreVolume_3N_R.bp
            ├── STACK_detector799_10.0um_scoreVolume_3N_R_origin_wrt_wholebrain.txt
            ├── STACK_detector799_10.0um_scoreVolume_4N_L.bp
            ├── STACK_detector799_10.0um_scoreVolume_4N_L_origin_wrt_wholebrain.txt
            ├── STACK_detector799_10.0um_scoreVolume_4N_R.bp
            └── STACK_detector799_10.0um_scoreVolume_4N_R_origin_wrt_wholebrain.txt
```
```
CSHL_scoremaps/
└── 10.0um
    └── STACK
        └── DEMO999_prep2_10.0um_detector799
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_12N_scoremap.bp
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_3N_scoremap.bp
            │   └── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_4N_scoremap.bp
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_12N_scoremap.bp
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_3N_scoremap.bp
                └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_4N_scoremap.bp
```
```
CSHL_scoremap_viz/
└── 10.0um
    ├── 12N
    │   └── STACK
    │       └── detector799
    │           └── prep2
    │               └── SLICECF_prep2_10.0um_12N_detector799_scoremapViz.jpg
    ├── 3N
    │   └── STACK
    │       └── detector799
    │           └── prep2
    │               └── SLICECF_prep2_10.0um_3N_detector799_scoremapViz.jpg
    └── 4N
        └── STACK
            └── detector799
                └── prep2
                    └── SLICECF_prep2_10.0um_4N_detector799_scoremapViz.jpg
```


## Alex Running Notes

#### For running the first command `demo/download_demo_data_generate_prob_volumes.py`:
- Ran with `python demo/download_demo_data_generate_prob_volumes.py --demo_data_dir $ROOT_DIR`. Downloading the files takes at least 3-5 hours.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`


#### For running the second command `./demo/from_images_to_score_volumes_demo.py`:
- Outputs shown in summary, too many to list properly.

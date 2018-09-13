---
- `$ ./demo/download_demo_data_scoring.py`
- `$ ./demo/from_images_to_score_volumes_demo.py DEMO999 799 NtbNormalizedAdaptiveInvertedGammaJpeg --structure_list "[\"3N\", \"4N\", \"12N\"]"`
---

Note that the data needed to download for this demo is about 35G.

#### Alex Running Notes
For `demo/download_demo_data_generate_prob_volumes.py`:
- Ran with `python demo/download_demo_data_generate_prob_volumes.py --demo_data_dir $ROOT_DIR`. Downloading the files takes at least 3-5 hours.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`
 
 CSHL_simple_global_registration/
└── DEMO999_registered_atlas_structures_wrt_wholebrainXYcropped_xysecTwoCorners.json
CSHL_classifiers/
└── setting_899
    └── classifiers
        ├── 12N_clf_setting_899.dump
        ├── 3N_clf_setting_899.dump
        └── 4N_clf_setting_899.dump

For `./demo/from_images_to_score_volumes_demo.py`
- Running does not work properly with the suggested command. Does not take in a description of preprocessing files as input.
- Issues with the code running, does not download necessary files from S3 https://s3.console.aws.amazon.com/s3/buckets/mousebrainatlas-data/CSHL_volumes/atlasV6/atlasV6_10.0um_scoreVolume/score_volumes/?region=us-east-1&tab=overview

CSHL_volumes/
└── DEMO999
    └── DEMO999_detector799_10.0um_scoreVolume
        ├── score_volume_gradients
        │   ├── DEMO999_detector799_10.0um_scoreVolume_12N_gradients.bp
        │   ├── DEMO999_detector799_10.0um_scoreVolume_12N_origin_wrt_wholebrain.txt
        │   ├── DEMO999_detector799_10.0um_scoreVolume_3N_L_gradients.bp
        │   ├── DEMO999_detector799_10.0um_scoreVolume_3N_L_origin_wrt_wholebrain.txt
        │   ├── DEMO999_detector799_10.0um_scoreVolume_3N_R_gradients.bp
        │   ├── DEMO999_detector799_10.0um_scoreVolume_3N_R_origin_wrt_wholebrain.txt
        │   ├── DEMO999_detector799_10.0um_scoreVolume_4N_L_gradients.bp
        │   ├── DEMO999_detector799_10.0um_scoreVolume_4N_L_origin_wrt_wholebrain.txt
        │   ├── DEMO999_detector799_10.0um_scoreVolume_4N_R_gradients.bp
        │   └── DEMO999_detector799_10.0um_scoreVolume_4N_R_origin_wrt_wholebrain.txt
        └── score_volumes
            ├── DEMO999_detector799_10.0um_scoreVolume_12N.bp
            ├── DEMO999_detector799_10.0um_scoreVolume_12N_origin_wrt_wholebrain.txt
            ├── DEMO999_detector799_10.0um_scoreVolume_3N_L.bp
            ├── DEMO999_detector799_10.0um_scoreVolume_3N_L_origin_wrt_wholebrain.txt
            ├── DEMO999_detector799_10.0um_scoreVolume_3N_R.bp
            ├── DEMO999_detector799_10.0um_scoreVolume_3N_R_origin_wrt_wholebrain.txt
            ├── DEMO999_detector799_10.0um_scoreVolume_4N_L.bp
            ├── DEMO999_detector799_10.0um_scoreVolume_4N_L_origin_wrt_wholebrain.txt
            ├── DEMO999_detector799_10.0um_scoreVolume_4N_R.bp
            └── DEMO999_detector799_10.0um_scoreVolume_4N_R_origin_wrt_wholebrain.txt

CSHL_scoremaps/
└── 10.0um
    └── DEMO999
        └── DEMO999_prep2_10.0um_detector799
            ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_12N_scoremap.bp
            │   ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_3N_scoremap.bp
            │   └── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_detector799_4N_scoremap.bp
            └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_12N_scoremap.bp
                ├── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_3N_scoremap.bp
                └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_detector799_4N_scoremap.bp

CSHL_scoremap_viz/
└── 10.0um
    ├── 12N
    │   └── DEMO999
    │       └── detector799
    │           └── prep2
    │               ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_12N_detector799_scoremapViz.jpg
    │               └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_12N_detector799_scoremapViz.jpg
    ├── 3N
    │   └── DEMO999
    │       └── detector799
    │           └── prep2
    │               ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_3N_detector799_scoremapViz.jpg
    │               └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_3N_detector799_scoremapViz.jpg
    └── 4N
        └── DEMO999
            └── detector799
                └── prep2
                    ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_prep2_10.0um_4N_detector799_scoremapViz.jpg
                    └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_prep2_10.0um_4N_detector799_scoremapViz.jpg

This demo assumes a subject brain (DEMO999) is roughly globally aligned with the atlas (atlasV7).
It shows how one can:
- register 7N_L (facial motor nucleus) individually.
- register 3N_R and 4N_R as a group.
- visualize the aligned atlas overlaid on original images

---------------------------

## Download input data
First run `download_demo_data.py [demo_data_dir]` to download input data. `[demo_data_dir]` is a folder specified by the user to store demo input data. Make sure the following files are downloaded:
  - `CSHL_volumes/DEMO999/DEMO999_detector799_10.0um_scoreVolume/score_volumes/*`
  - `CSHL_volumes/atlasV7/score_volumes/*`
  - `CSHL_simple_global_registration/DEMO999_T_atlas_wrt_canonicalAtlasSpace_subject_wrt_wholebrain_atlasResol.bp`

## Register 12N individually
- `$ ROOT_DIR=[demo_data_dir] DATA_ROOTDIR=[demo_data_dir]  ./register_brains_demo.py demo_fixed_brain_spec_12N.json demo_moving_brain_spec_12N.json 7 -g`

## Register 3N_R and 4N_R as a group
- `$ ROOT_DIR=[demo_data_dir] DATA_ROOTDIR=[demo_data_dir]  ./register_brains_demo.py demo_fixed_brain_spec_3N_R_4N_R.json demo_moving_brain_spec_3N_R_4N_R.json 7 -g`

The program should finish in 2 minutes.

The outputs are also generated in _demo_data_ folder under the following paths. You can download the expected output from our S3 bucket using URLs formed by prepending https://s3-us-west-1.amazonaws.com/mousebrainatlas-data/ to the paths.

**Best set of transform parameters**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_parameters.json`

**Optimization trajectory of transform parameters**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_trajectory.bp`

**Score history**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreHistory.bp`

**Score evolution plot**
- `CSHL_registration_parameters/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_scoreEvolution.png`

**Simple globally aligned moving brain volumes**
- `CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp0_DEMO999_detector799_10.0um_scoreVolume_3N_4N_10.0um/score_volumes/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp0_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R.bp`

**Locally aligned moving brain volume**
- `CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_4N_10.0um/score_volumes/atlasV7_10.0um_scoreVolume_3N_R_4N_R_warp7_DEMO999_detector799_10.0um_scoreVolume_3N_R_4N_R_10.0um_3N_R.bp`

------------------------

## Visualize registration results

To visualize the multi-probability level structures of the aligned atlas overlaid on original images:
- make sure the following image files are available:
  - `CSHL_data_processed/DEMO999/DEMO999_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg/[imgName]\_prep2_raw_NtbNormalizedAdaptiveInvertedGammaJpeg.jpg`
- `$ ROOT_DIR=[demo_data_dir] DATA_ROOTDIR=[demo_data_dir] ./visualize_registration_demo.py demo_visualization_per_structure_alignment_spec.json -g demo_visualization_global_alignment_spec.json`

The outputs are the following:

**Atlas-overlaid images**
- CSHL_registration_visualization/DEMO999_atlas_aligned_multilevel_down16_all_structures/NtbNormalizedAdaptiveInvertedGammaJpeg/

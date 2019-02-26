# File Organization on S3

## List of Buckets

 Generated using AWS CLI command: `aws s3 ls` :
* __mousebrainatlas-data__ 2017-09-13 11:19:25
* __mousebrainatlas-rawdata__ 2017-08-14 12:23:57
* mousebrainatlas-data-backup 2018-08-30 18:00:12
* mousebrainatlas-data-yuncong 2018-08-30 18:02:39
  * Not being used (move to glacier?)
* mousebrainatlas-scripts 2017-05-16 15:59:36
  * Not being used
* mousebraindata-open 2018-07-10 20:10:09
* tmsn-data 2018-09-21 14:14:42
  * ?
* yoav-seed-backup 2017-05-10 17:30:28

## Bucket mousebrainatlas-data

`aws ls s3://mousebrainatlas-data/`
 
* CSHL_SPM/
* CSHL_annotation_viz/
* CSHL_cells_v2/
* CSHL_classifiers/
* __CSHL_data_processed/__
* CSHL_labelings_thalamus/
* CSHL_labelings_v3/
* CSHL_meshes/
* CSHL_patch_features/
* CSHL_patch_locations/
* CSHL_patch_scores/
* CSHL_registration_parameters/
* CSHL_registration_visualization/
* CSHL_registration_visualization_atlasV5/
* CSHL_registration_viz_juxtaposed/
* CSHL_scoremap_viz/
* CSHL_scoremap_viz_grid/
* CSHL_scoremaps/
* CSHL_simple_global_registration/
* __CSHL_volumes/__ 
   * The location of the information about the shape of the structures.
   * The directory Yoav used to create a 3D visualization of the atlas: CSHL_volumes/atlasV7/atlasV7_10.0um_scoreVolume/score_volumes/
* Dropbox/
* HRNTS2017/
* LGN3Datlas/
* blob_matching_atlas/
* image_examples/
* image_examples_raw/
* lauren_data/
* mxnet_models/
* raw_image_histograms/
* raw_image_histograms_fullImage/
* raw_image_histograms_log/
* raw_image_histograms_log_fullImage/
* stacy_data/
* training_examples/ 
    
    
## Bucket 2: mousebrainatlas-rawdata

All files stored in glacier.

Contains only raw, unprocessed files, labelled as *lossless. These files are in the folder named May be in either .jp2 or .tiff format, depends on the institution supplying the stacks.

The following is a list of the possible files stored in each brain's folder:
- *_lossless.jp2 
  - raw stack
- *_lossy.jp2    
  - downsampled 32X

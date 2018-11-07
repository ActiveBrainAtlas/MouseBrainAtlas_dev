## File Organization on S3

### Buckets

 Generated using AWS CLI command: `aws s3 ls` :
* 2017-09-13 11:19:25 __mousebrainatlas-data__
* 2017-08-14 12:23:57 __mousebrainatlas-rawdata__
* 2017-05-16 15:59:36 mousebrainatlas-scripts
* 2018-07-10 20:10:09 mousebraindata-open
* 2017-05-10 17:30:28 yoav-seed-backup

##### Bucket mousebrainatlas-data

`aws ls s3://mousebrainatlas-data/`
 
* CSHL_SPM/
* CSHL_annotation_viz/
* CSHL_cells_v2/
* CSHL_classifiers/
* CSHL_data_processed/
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
* **CSHL_volumes/** the location of the information about the shape of the structures.
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
    
*_lossless.jp2 is the only file that is NOT a thumbnail. Everything else is downsized.

##### Bucket 2: mousebrainatlas-rawdata
All files stored in glacier.

Contains only raw, unprocessed files, labelled as *lossless. These files are in the folder named May be in either .jp2 or .tiff format, depends on the institution supplying the stacks.

The following is a list of the possible files stored in each brain's folder.
    - *_lossless.jp2 
      - raw stack
    - *.lossy.jp2    
      - downsampled 32X

To run any demo,
```
cd /home/yuncong/Brain/
source demo/set_env_variables.sh
```

## Preprocess 
- Run `download_demo_data_preprocessing.py --step 1` to download an example JPEG2000 image.
- Run `preprocess_demo.py --step 1`
- Run `download_demo_data_preprocessing.py --step 2`
- `$ ./align.py DEMO999 `
- 

## Compute patch features
- Run `demo/download_demo_data_compute_features.py`
- `$ ENABLE_UPLOAD_S3=0 ENABLE_DOWNLOAD_S3=0 ./demo/compute_features_demo.py DEMO999 --section 151 --version NtbNormalizedAdaptiveInvertedGamma`

#### Alex Running Notes
For DOWNLOAD DEMO DATA:
- Ran with `python demo/download_demo_data_compute_features.py --demo_data_dir /media/alexn/BstemAtlasDataBackup/demo/` to copy all files into the external hard drive. Only takes in 1 arg which is the download dir, otherwise defaults to ./demo_data. All files go into `[demo_data_dir]/CSHL_data_processed/DEMO999/`, Downloaded 4 files:
  - `DEMO999_sorted_filenames.txt`
  - `DEMO999_anchor.txt`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_sectionLimits.json`
  - `DEMO999_alignedTo_MD662&661-F116-2017.06.07-04.39.41_MD661_1_0346_prep2_cropbox.json`
  
For COMPUTE FEATURE DEMO:
- Running it gives me the following error: `IOError: [Errno 2] No such file or directory: '/home/alexn/mxnet_models/inception-bn-blue/mean_224.npy'`. Attempting to fix
  - MXNET_MODEL_ROOTDIR set as ROOT_DIR/mxnet_models. I am changing that to be in BstemAtlasDataBackup 
    - I continue to get errors because the code will insert /data/ at the beginning on my filepath each time
    - Error fixed, root filepath set to never be automatically chosen. distributed_utilities.py around line 148
    - Getting a bunch more errors... Seems to remove/add filepaths to the one I specify seemingly at random, this also spans at the bare minimum 6 different scripts
    - Now that I actually got the download statement for mxnet models to work it says I don't have permission to access my own directory
  - Okay I'm going to undo most of my changes as the situation is getting worse and worse. This file path organization is going to take a long long time to figure out. Altering it will take even longer seeing how it's almost the backbone of the code itself...

## Generate probability volumes
- Run `demo/download_demo_data_scoring.py`
- `$ ENABLE_UPLOAD_S3=0 ENABLE_DOWNLOAD_S3=0 ./from_images_to_score_volumes_demo.py DEMO999 799 --structure_list [\"3N, 4N, 12N\"]`

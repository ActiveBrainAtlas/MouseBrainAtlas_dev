This toolkit is written in Python 2.7.2 and have been tested on a machine with Intel Xeon W5580 3.20GHz 16-core CPU, 128GB RAM and a Nvidia Titan X GPU, running Linux Ubuntu 16.04. 

## Installation

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas-virtualenv** and install necessary packages.

- Change `REPO_DIR`, `ROOT_DIR`, `DATA_ROOTDIR`, `THUMBNAIL_DATA_ROOTDIR` in `setup/config.sh`
- The default `requirements.txt` assumes CUDA version of 9.0. If your CUDA version (check using `nvcc -V` or `cat /usr/local/cuda/version.txt`) is 9.1, replace `mxnet-cu90` with `mxnet-cu91` in `requirements.txt`. If your machine does not have a GPU, replace `mxnet-cu90` with `mxnet`. Refer to [official mxnet page](https://mxnet.incubator.apache.org/install/index.html?platform=Linux&language=Python&processor=CPU) for available pips.
- `source setup/config.sh`. Make sure we are now working under the mousebrainatlas python virtual environment.
- `cd demo`.

### Install non-python packages

- Install ImageMagick 6.8.9. `sudo apt-get install imagemagick`
- To use GUIs, install PyQt4 into the virtualenv according to [this answer](https://stackoverflow.com/a/28850104).
    - Install python-qt4 globaly: `sudo apt-get install python-qt4`
    - Create symbolic link of PyQt4 to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/PyQt4/ mousebrainatlas_virtualenv/lib/python2.7/site-packages/`
    - Create symbolic link of sip.so to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/sip.x86_64-linux-gnu.so mousebrainatlas_virtualenv/lib/python2.7/site-packages/`


## Preprocess

Note that the `input_spec.ini` files for most steps are different and must be manually created according to the actual input. In the following instructions, "create `input_spec.ini` as (prep_id, version, resolution)" means using the same set of image names as `image_name_list` but set the `prep_id`, `version` and `resolution` accordingly.

- Run `download_demo_data_preprocessing.py` to download necessary data. Make sure the folder content looks like:

```bash
├── brains_info
│   └── DEMO998.ini
├── jp2_files
│   └── DEMO998
│       ├── MD662&661-F81-2017.06.06-12.44.40_MD661_2_0242_lossless.jp2
│       ├── MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250_lossless.jp2
│       └── MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257_lossless.jp2
├── mxnet_models
│   └── inception-bn-blue
│       ├── inception-bn-blue-0000.params
│       ├── inception-bn-blue-symbol.json
│       └── mean_224.npy
└── operation_configs
    ├── crop_orig.ini
    ├── from_aligned_to_none.ini
    ├── from_aligned_to_padded.ini
    ├── from_aligned_to_wholeslice.ini
    ├── from_none_to_aligned.ini
    ├── from_none_to_brainstem.ini
    ├── from_none_to_padded.ini
    ├── from_none_to_wholeslice.ini
    ├── from_padded_to_brainstem.ini
    ├── from_padded_to_none.ini
    └── from_wholeslice_to_brainstem.ini
```
- Edit `DEMO998_raw_input_spec.json`. Set `data_dirs`, `filepath_to_imageName_mapping` and `imageName_to_filepath_mapping`. Run `python jp2_to_tiff.py DEMO998 DEMO998_raw_input_spec.json`.
- 




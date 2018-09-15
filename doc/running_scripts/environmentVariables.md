## Setup

All environment variables are set in setup/config.sh. This file will set 4 environment variables as described below as well as set up a virtual environment from which you will run the code.

This file should be run with `$ source ./setup/config.sh` to set the repository directory properly.

### Evironmental variables	
```python	
REPO_DIIR = the directory holding the code repository	
ROOT_DIR = the root of the data sub-directories, all downloaded data goes here	
DATA_ROOTDIR = this is where high level data past the preprocessing stage is saved	
THUMBNAIL_DATA_ROOTDIR = this is for most preprocessing outputs, location of downsampled images	
```	

During Alex's testing on the Atlas computer these variables were set to: 
```python	
REPO_DIIR = $PWD/../src/	
ROOT_DIR = /media/alexn/BstemAtlasDataBackup/demo/	
DATA_ROOTDIR = /media/alexn/BstemAtlasDataBackup/demo/	
THUMBNAIL_DATA_ROOTDIR = /media/alexn/BstemAtlasDataBackup/demo/	
```	

S3 file locations:	
```python	
S3_ROOT = The root of all downloaded and uploaded data	
S3_ROOT = s3://mousebrainatlas-data/	
```	
S3 filepaths are NOT changeable by the user and can be ignored for the most part unless the user wishes to directly access pertinent data.


- note: The relative filepath from $S3_ROOT will exactly match the relative filepath from $ROOT_DIR. As well as the other ROOT directories.

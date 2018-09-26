## Setup

All environment variables are set in `setup/config.sh`. This file will set 4 environment variables as described below as well as set up a virtual environment, called `mousebrainatlas_virtualenv`, from which you will run the code.

`$ source ./setup/config.sh` will run the entire setup procedure. It will create `mousebrainatlas_virtualenv` in your repository folder and set all environment variables. These should be changed BEFORE running the command as described below.

### Evironmental variables	
```python	
PROJECT_DIR is 'the root directory of the repository. Contains src/ doc/ etc...'
REPO_DIIR is 'the directory holding the code, should be PROJECT_DIR/src/'
ROOT_DIR is 'all downloaded data past the preprocessing stage is stored here'
DATA_ROOTDIR is 'this is where high level data gnerated during the preprocessing stage is saved'
THUMBNAIL_DATA_ROOTDIR is 'this is for most preprocessing outputs, location of downsampled images'
```	

During Alex's testing on the Atlas computer these variables were set to: 
```python	
PROJECT_DIR = $PWD/..
REPO_DIR = $PROJECT_DIR/src/
ROOT_DIR = /media/alexn/BstemAtlasDataBackup/demo/
DATA_ROOTDIR = /media/alexn/BstemAtlasDataBackup/demo/
THUMBNAIL_DATA_ROOTDIR = /media/alexn/BstemAtlasDataBackup/demo/
```	
Note: It's recommended that `ROOT_DIR`, `DATA_ROOTDIR`, and `THUMBNAIL_DATA_ROOTDIR` all be set to the same filepath to reduce complexity and consolidate all the data.

S3 file locations:	
```python	
S3_ROOT is 'The root of all downloaded and uploaded data'
S3_ROOT = s3://mousebrainatlas-data/	
```	
S3 filepaths are NOT changeable by the user and can be ignored for the most part unless the user wishes to directly access pertinent data.


- note: The relative filepath from $S3_ROOT will exactly match the relative filepath from $ROOT_DIR. As well as the other ROOT directories. For example when downloading `/S3_ROOT/folder/file` it will be saved to `/ROOT_DIR/folder/file` on your machine.

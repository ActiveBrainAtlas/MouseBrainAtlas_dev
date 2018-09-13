
##### Evironmental variables	
```python	
REPO_DIIR = the directory holding the code repository	
ROOT_DIR = the root of the data sub-directories, all downloaded data goes here	
DATA_ROOTDIR = this is where high level data past the preprocessing stage is saved	
THUMBNAIL_DATA_ROOTDIR = this is for most preprocessing outputs, location of downsampled images	
```	
Alex set these variables to: 	
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
- note: The relative filepath from $S3_ROOT will exactly match the relative filepath from $ROOT_DIR. As well as the other ROOT directories.

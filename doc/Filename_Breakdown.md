## File Naming Structure

Every slice has an associated slice_name that does not change. This along with the slice's index can be found in the sorted_filenames.txt document associated with each stack. This document can be found in `s3://mousebrainatlas-data/CSHL_data_processed/<stack>/<stack>_sorted_filenames.txt`. Each different version of every each slice (normalization, cropping, alignment, etc..) is encoded in a set of 3 keywords appended to each slice_name. The fields are listed below.
- prep_id
- resolution
- version

Files will always be stored in folders under the following naming scheme: `s3://mousebrainatlas-data/CSHL_data_processed/<stack>_<prep_id>_<resolution>_<version>/<slice_name>_<prep_id>_<resolution>_<version>`. I will go through each of the 3 fields' properties and possible values.


### prep_id
Prep_id describes the alignment and cropping of the images.

- Possible values:
  - "": Image has not cropped or aligned
  - "prep1"
      - Images have all been aligned to each other
  - "prep5"
      - Images have all been aligned, cropped to only contain width and height spanned by the brain (cropped from prpep5)
  - "prep2"
      - Images have all been aligned, cropped to only contain width and height spanned by the brainstem region (cropped from prep5)
  
### resolution




### version




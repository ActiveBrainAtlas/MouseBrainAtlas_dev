Note: Script names may change when the code is officially released. The current names are iterative using the order the scripts are meant to be run. The prepended `a_script_preprocess` is simply to organize the scripts together while in development.

These scripts assume the stack has been given a name (example stack="MD585"), and the associated stain for each set of images has been defined (stain="NTB" or stain="Thionin" are the two current options). As a shorthand when referring to these stains, I will define T = Thionin and NTB = Neurotrace Blue.


# Preprocessing Scripts

The single setup script and seven preprocessing scripts are spaced with user intervention steps such that the first script is run, the user is required to perform some step by hand, then the second script is run, etc... For every script there is listed the command to run it, a brief description of what the script does, and the manual step for the user after completion.

### Setup Script
---
__Command__: `python a_script_preprocess_setup.py $stack`

__Description__: 


### Script 1
---
__Command__: `python a_script_preprocessing_1.py $stack $stain`

__Description__: Converts images from .jp2 format to .tiff format. Extracts the blue channel for slides stained with T or NTB. NTB slides are intensity normalized. 32x downsampled thumbnails are generated for every image.

__User step__: Check slice orientations. All slices must be cut sagittally, roughly oriented with the rostral side on the left, and slices must begin on the left hemisphere of the brain.


### Script 2
---
__Command__: `python a_script_preprocessing_2.py $stack $stain`

__Description__: 

__User step__:


### Script 3
---
__Command__: `python a_script_preprocessing_3.py $stack $stain`

__Description__:  

__User step__:


### Script 4
---
__Command__: `python a_script_preprocessing_4.py $stack $stain`

__Description__:  

__User step__:


### Script 5
---
__Command__: `python a_script_preprocessing_5.py $stack $stain`

__Description__:  

__User step__:


### Script 6
---
__Command__: `python a_script_preprocessing_6.py $stack $stain`

__Description__:  

__User step__:


### Script 7
---
__Command__: `python a_script_preprocessing_7.py $stack $stain`

__Description__:  

__User step__:


# Structure Registration Scripts

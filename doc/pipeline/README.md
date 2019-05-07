# User Guide - Aligning atlas to a new brain stack

## Setup

This guide in its current form assumes the computer being worked on has the necessary dependant software already installed and configured (CUDA, Python, ImageMagick, PyQt). 

#### Initialize the virtual environment

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas-virtualenv** and install necessary packages.

- Change `REPO_DIR`, `ROOT_DIR`, `DATA_ROOTDIR`, `THUMBNAIL_DATA_ROOTDIR` in `setup/config.sh`
    - `REPO_DIR` is simply the directory in which this Github repo is located on your computer.
    - It is strongly recommended that the remaining path variables are set to the same path to reduce complexity. This will ensure that all data is stored in the same root location for convenience. 
- `cd` into this repository's directory and run the command `source setup/config.sh`. Check we are now working under the `mousebrainatlas_virtualenv` virtual environment. The command prompt should now have `mousebrainatlas_virtualenv` in parentheses prepended on the left side.
- `cd demo`.

#### Input new brain metadata

Now we enter in the metadata for the new brain. You will need to know the name of the brain stack, the cutting plane, the planar resolution of the images, the slice thickness, the stain used, and the alternating stain number two if applicable.

Run the following commands:
- `cd demo`
    - Move into the "demo/" directory, which contains all of the necessary scripts.
- `python input_new_brain_metadata.py`
    - This will ask a series of questions about the new brain that you must answer. Once finished the script will save your answers into several files that will be automatically read throughout the rest of the pipeline.
- `source ../setup/set_<STACK>_metadata.ini`, where "<STACK>" should be replaced with the name of the brain stack. 
    - This will set the variables `stack`, `stain`, and `detector_id` in your terminal for convenice. Run `echo $stack` to verify that the variables were saved properly.


#### Set up new brain raw images

## Running the pipeline

The pipeline is organized as a set of python scripts that are called iteratively, between each set of python scripts will be a manual step the user is required to perform. These user-intervention steps are necessary checks for some automatic processes throughout the pipeline.

The python scripts are intended to be run through a terminal (on Mac or Linux) from the `demo/` folder of this project while in the virtual environment that was initialized as described in "Setup". [This document](pipeline.md) lists the command to run every script in order as well as an in depth description of the user-intervention steps and should be followed to properly run through the pipeline.

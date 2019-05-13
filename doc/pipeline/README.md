# User Guide - Aligning atlas to a new brain stack

## Setup New Brain Metainformation

---

This guide in its current form assumes the computer being worked on has the necessary dependant software already installed and configured (CUDA, Python, ImageMagick, PyQt). 

#### Initialize the virtual environment

A configuration script is provided to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) called **mousebrainatlas-virtualenv** and install necessary packages.

Firstly, you need to know the directory in which you installed this "MouseBrainAtlas_dev" repository. This is considered the "REPO_DIR", or repository directory, of the project. Whenever a filepath is given, such as "setup/config.sh", it assumes you are starting from the repository directory.

- Open the file "setup/config.sh" in your favorite text editor. Notice "PROJECT_DIR" and "ROOT_DIR" are set equal to certain filepaths at the beginning of the file. Change these filepaths as described in the following bullet points.
    - Set `PROJECT_DIR` to the directory in which this Github repo is located on your computer.
    - Set `ROOT_DIR` to a folder that will be the root of all data loaded and generated throughout the pipeline. Expect about 1TB of space to be taken up by every brain stack as it runs through the pipeline.
- `cd` into this repository's directory and run the command `source setup/config.sh`. Check we are now working under the `mousebrainatlas_virtualenv` virtual environment. The command prompt should now have `mousebrainatlas_virtualenv` in parentheses prepended on the left side.
- `cd demo`.

#### Input new brain metadata

Now we enter in the metadata for the new brain. You will need to know the name of the brain stack, the cutting plane, the planar resolution of the images, the slice thickness, the stain used, and the alternating stain number two if applicable.

Run the following commands:
- `cd demo`
    - Move into the "demo/" directory, which contains all of the necessary scripts.
- `python input_new_brain_metadata.py`
    - This will ask a series of questions about the new brain that you must answer. Once finished the script will save your answers into several files that will be automatically read throughout the rest of the pipeline.
- `source ../setup/set_<STACK>_metadata.sh`, where "`<STACK>`" should be replaced with the name of the brain stack. 
    - This will set the variables `stack`, `stain`, and `detector_id` in your terminal for convenice. Run `echo $stack` to verify that the variables were saved properly.


#### Copy files into proper input location
The mouse brain atlas pipeline relies on a strict filepath managemant system such that files must be located in the correct locations or it will not work. This script will ask the user for the locations of two sets of input data (the sorted filenames text file, and the raw jp2 images) and automatically copy them into the proper locations.

Run the following command:
- `python setup_new_brain_files.py $stack`
    - This script will prompt you to first select the location of your `<STACK>_sorted_filenames.txt` and will automatically copy it to the porper location. Next the script will prompt you for the location of one of the raw jp2 files, and those will be copied to the proper location as well. (No files will be deleted at any point automatically)
    
    
## Setup New Brain Metainformation

---

Assumes you have already inputted the metadata for the chosen stack. 

- `source ../setup/set_<STACK>_metadata.sh`, where "`<STACK>`" should be replaced with the name of the brain stack. 
    - This will set the variables `stack`, `stain`, and `detector_id` in your terminal for convenice. Run `echo $stack` to verify that the variables were saved properly.
    - Example: `source ../setup/set_MD635_metadata.sh`


## Running the pipeline

The pipeline is organized as a set of python scripts that are called iteratively, between each set of python scripts will be a manual step the user is required to perform. These user-intervention steps are necessary checks for some automatic processes throughout the pipeline.

The python scripts are intended to be run through a terminal (on Mac or Linux) from the `demo/` folder of this project while in the virtual environment that was initialized as described in "Setup". [This document](pipeline.md) lists the command to run every script in order as well as an in depth description of the user-intervention steps and should be followed to properly run through the pipeline.

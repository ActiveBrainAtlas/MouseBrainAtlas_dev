# Docker Instructions

The Docker image for this project is still being actively developped and is not intended for unsupervised use.

The Docker image has been tested on the ubuntu v16.04 operating system. To run any of the GUIs in the pipeline, there are some additional steps before running the image.

This document assumes Docker is already installed on your machine, you are using a linux machine, and that you understand some basic functionality of the terminal.

## Your data root directory

Before getting started, ensure that you have a directory to use as the root of the pipeline. This shall be known as the ROOT_DIRECTORY. Ensure that there is at least 1TB of free space in your ROOT_DIRECTORY. It is recommended that this directory be empty and reserved only for the outputs of the pipeline.

Here is an example of a good ROOT_DIRECTORY: `/media/john/external_drive_1/atlas_root`

## Download the initial script

Enter in the multiline command below into your linux terminal while you are logged into your user account (you can copy and paste the entire chunk). It will create a directory called "atlas_docker_demo" in your home folder and copy the shell script "run_docker.sh" into it.

__Command 1:__
```
cd ~ && \
mkdir -p ./atlas_docker_demo/ && \
cd ./atlas_docker_demo/
curl -O "https://raw.githubusercontent.com/ActiveBrainAtlas/MouseBrainAtlas_dev/master/doc/docker/run_docker.sh" \
"./run_docker.sh"
```

Next we will want to run the script we just downloaded, named "run_docker.sh". Before attempting to run the Docker container, it will first verify that you have Docker installed as well as the latest Docker Image for this project. If either are not installed, they will be automatically installed. Please replace the `$ROOT_DIRECTORY` with the root directory you have chosen as described above.

__Command 2:__

```source run_docker.sh $ROOT_DIRECTORY```

This will need several minutes to run as it downloads and runs the Docker Image. You will know it has finished successfully when a GUI is displayed prompting to either "continue a brain" or "start a new brain" through the pipeline.

__Using the GUI:__

[The guide for using the main GUI (either continuing a brain or starting a new one) can be found here.](../pipeline/pipeline.md)

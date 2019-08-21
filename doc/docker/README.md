# Docker Instructions

The Docker image for this project is still being actively developped and is not intended for unsupervised use.

The Docker image has been tested on the ubuntu v16.04 operating system. To run any of the GUIs in the pipeline, there are some additional steps before running the image.

This document assumes Docker is already installed on your machine, you are using a linux machine, and that you understand some basic functionality of the terminal.

## Your data root directory

Before getting started, ensure that you have a directory to use as the root of the pipeline. This shall be known as the ROOT_DIRECTORY. Ensure that there is at least 1TB of free space in your ROOT_DIRECTORY. It is recommended that this directory be empty and reserved only for the outputs of the pipeline.

Here is an example of a good ROOT_DIRECTORY: `/media/john/external_drive_1/atlas_root`

## Download the Docker image

The current docker image is denoted: `anewberry/atlas_demo:atlas_v0.0.3`. 

To download it, enter into the command line: `docker pull anewberry/atlas_demo:atlas_v0.0.3`

## Run the Docker image

### No GUI

"ROOT_DIRECTORY" must be replaced with the actual data root directory that you have chosen. A symbolic link will automatically connect it to directories inside of the docker container. 
  - `docker run -it -v ROOT_DIRECTORY:/mnt/data anewberry/atlas_demo:atlas_v0.0.3`


### With GUI (Required to properly run the pipeline)

```
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    osrf/ros:indigo-desktop-full \
    rqt
export containerId=$(docker ps -l -q)
```

`xhost +local:root`

```
docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v ROOT_DIRECTORY:/mnt/data anewberry/atlas_demo:atlas_v0.0.3
```

`xhost -local:root`

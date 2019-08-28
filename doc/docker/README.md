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

`source run_docker.sh $ROOT_DIRECTORY`. 

This will need several minutes to run as it downloads and runs the Docker Image. You will know it has finished successfully when a GUI is displayed prompting to either "continue a brain" or "start a new brain" through the pipeline.




## Download the Docker image manually

The current docker image is denoted: `anewberry/atlas_demo:atlas_v0.0.5`. 

To download it, enter into the command line: `docker pull anewberry/atlas_demo:atlas_v0.0.5`

## Run the Docker image manually

### No GUI

"ROOT_DIRECTORY" must be replaced with the actual data root directory that you have chosen. A symbolic link will automatically connect it to directories inside of the docker container. 
  - `docker run -it -v ROOT_DIRECTORY:/mnt/data anewberry/atlas_demo:atlas_v0.0.3`


### With GUI (Required to properly run the pipeline)

Commands 1 and 2 allow you to use GUI applications when running the Docker image. Command 3 runs the docker image, remember to add your ROOT_DIRECTORY into the command. Command 4 undoes the effects of command 2, which most users will prefer as command 2 can be considered unsafe to leave on.

This workaround was copied from http://wiki.ros.org/docker/Tutorials/GUI

##### Command 1
```
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    osrf/ros:indigo-desktop-full \
    rqt
export containerId=$(docker ps -l -q)
```
##### Command 2
`xhost +local:root`
##### Command 3
```
docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v ROOT_DIRECTORY:/mnt/data anewberry/atlas_demo:atlas_v0.0.3
```
##### Command 4

`xhost -local:root`

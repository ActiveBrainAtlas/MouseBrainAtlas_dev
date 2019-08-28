

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

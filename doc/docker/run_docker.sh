#!/bin/bash

if [ "$1" == "" ]; then
	echo "Argument ROOT_FP not passed in."
	echo "source run_docker.sh \$ROOT_FP"
	return 0
fi


xhost +local:root

echo "*********************************"
echo "  Entering the Docker Container"
echo "*********************************"


docker run -it \
--env="DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
-v "$1":"/mnt/data" \
-v "/":"/mnt/computer_root" \
anewberry/atlas_demo:atlas_v0.0.3


echo "*********************************"
echo "  Leaving the Docker Container"
echo "*********************************"

xhost -local:root


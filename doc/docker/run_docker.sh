```#!/bin/bash

# Insist that the root filepath be passed in
if [ "$1" == "" ]; then
	echo "Argument ROOT_FP not passed in."
	echo "source thisScript.sh \$ROOT_FP"
	return 0
fi

xhost +local:root

docker run -it --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v "$1":"/mnt/data" -v "/":"/mnt/computer_root" anewberry/atlas_demo:atlas_v0.0.3

xhost -local:root```

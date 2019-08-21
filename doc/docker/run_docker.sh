#!/bin/bash

if [ "$1" == "" ]; then
	echo ""
	echo "Argument ROOT_FP not passed in."
	echo "source run_docker.sh \"\$ROOT_FP\""
	echo ""
	return 0
elif [ "$2" != "" ]; then
	echo ""
	echo "Either you tried to pass multiple arguments, or your first argument has a space in it. If the filepath you are passing has spaces in it, ensure you have quotation marks around it."
	echo "Replace this: source run_docker.sh \"\$ROOT_FP\""
	echo ""
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
-v "${1}":"/mnt/data" \
-v "/":"/mnt/computer_root" \
anewberry/atlas_demo:atlas_v0.0.3

echo "*********************************"
echo "  Leaving the Docker Container"
echo "*********************************"

xhost -local:root

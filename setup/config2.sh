#!/bin/bash

# User should change the PROJECT_DIR and ROOT_DIR as specified on the Github page
export PROJECT_DIR=/app/MouseBrainAtlas_dev/
export ROOT_DIR=/mnt/data/

##################################################
###  DO NOT MODIFY ANYTHING BELOW THIS POINT  ###
##################################################
virtualenv="mousebrainatlas_virtualenv"

red='\e[1;31m'
purple='\e[1;35m'
green='\e[1;32m'
cyan='\e[1;36m'
NC='\033[0m' # No Color

export REPO_DIR=$PROJECT_DIR/src/
export DATA_ROOTDIR=$ROOT_DIR
export THUMBNAIL_DATA_ROOTDIR=$ROOT_DIR

if [ ! -d $virtualenv ]; then
        echo ""
        echo -e "${green}Creating a virtualenv environment${NC}"
        #virtualenv --system-site-packages $virtualenv
        virtualenv -p python $PROJECT_DIR/$virtualenv --system-site-packages
fi

echo ""
echo -e "${green}Activating the virtualenv environment${NC}"
source $PROJECT_DIR/$virtualenv/bin/activate

echo ""
echo -e "${green}[virtualenv] Installing Python packages${NC}"
pip install -r $PROJECT_DIR/setup/requirements.txt


# PyQT stuff
#ln -s /usr/lib/python2.7/dist-packages/PyQt4/ $PROJECT_DIR/$virtualenv/lib/python2.7/site-packages/

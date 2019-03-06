#!/bin/bash

# User can modify this part
PROJECT_DIR=/home/alexn/brainDev
virtualenv="mousebrainatlas_virtualenv"
##################################################

red='\e[1;31m'
purple='\e[1;35m'
green='\e[1;32m'
cyan='\e[1;36m'
NC='\033[0m' # No Color

export REPO_DIR=$PROJECT_DIR/src/

# export ROOT_DIR=/media/alexn/BstemAtlasDataBackup/demo_preprocess/
# export DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/demo_preprocess/
# export THUMBNAIL_DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/demo_preprocess/

# FOR UCSD BRAIN
export ROOT_DIR=/media/alexn/BstemAtlasDataBackup/ucsd_brain/
export DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/ucsd_brain/
export THUMBNAIL_DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/ucsd_brain/

# FOR Script testing
#export ROOT_DIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/
#export DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/
#export THUMBNAIL_DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/


if [ ! -d $virtualenv ]; then
        echo ""
        echo -e "${green}Creating a virtualenv environment${NC}"
        #virtualenv --system-site-packages $virtualenv
        virtualenv -p python $PROJECT_DIR/$virtualenv
fi

echo ""
echo -e "${green}Activating the virtualenv environment${NC}"
source $PROJECT_DIR/$virtualenv/bin/activate

echo ""
echo -e "${green}[virtualenv] Installing Python packages${NC}"
pip install -r $PROJECT_DIR/setup/requirements.txt

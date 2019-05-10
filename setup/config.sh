#!/bin/bash

# User can modify this part
PROJECT_DIR=/data/Github/MouseBrainAtlas_dev
virtualenv="mousebrainatlas_virtualenv"
##################################################

red='\e[1;31m'
purple='\e[1;35m'
green='\e[1;32m'
cyan='\e[1;36m'
NC='\033[0m' # No Color

export REPO_DIR=$PROJECT_DIR/src/

# FOR UCSD BRAIN
export ROOT_DIR=/data/BstemAtlasDataBackup/ucsd_brain/
export DATA_ROOTDIR=/data/BstemAtlasDataBackup/ucsd_brain/
export THUMBNAIL_DATA_ROOTDIR=/data/BstemAtlasDataBackup/ucsd_brain/

# FOR Script testing
# export ROOT_DIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/
# export DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/
# export THUMBNAIL_DATA_ROOTDIR=/media/alexn/BstemAtlasDataBackup/pipeline_test/

venv_dir=/data/venv/$virtualenv

if [ ! -d $venv_dir ]; then
        echo ""
        echo -e "${green}Creating a virtualenv environment${NC}"
        #virtualenv --system-site-packages $virtualenv
        virtualenv -p python2 $venv_dir
	
	echo ""
	echo -e "${green}Activating the virtualenv environment${NC}"
	source $venv_dir/bin/activate
        
	echo ""
        echo -e "${green}[virtualenv] Installing Python packages${NC}"
        pip install -r $PROJECT_DIR/setup/requirements.txt
fi

echo ""
echo -e "${green}Activating the virtualenv environment${NC}"
source $venv_dir/bin/activate

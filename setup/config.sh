#!/bin/bash

red='\e[1;31m'
purple='\e[1;35m'
green='\e[1;32m'
cyan='\e[1;36m'
NC='\033[0m' # No Color
virtualenv="mousebrainatlas"

if [ ! -d $virtualenv ]; then
        echo ""
        echo -e "${green}Creating a virtualenv environment${NC}"
        #virtualenv --system-site-packages $virtualenv
        virtualenv -p python $virtualenv
fi

echo ""
echo -e "${green}Activating the virtualenv environment${NC}"
source $virtualenv/bin/activate

#echo ""
#echo -e "${green}[virtualenv] Installing pip${NC}"
#python oss/get-pip.py

echo ""
echo -e "${green}[virtualenv] Installing Python packages${NC}"
#pip install --use-wheel --no-index --find-link=oss/packages -r oss/requirements_gpu.txt
pip install -r requirements.txt


# Installation Guide

This toolkit is written in Python 2.7.2 and has been tested on a machine with Intel Xeon W5580 3.20GHz 16-core CPU, 128GB RAM and a Nvidia Titan X GPU, running Linux Ubuntu 16.04. 

#### Install CUDA (refer to [this page](https://mxnet.apache.org/versions/master/install/ubuntu_setup.html#cuda-dependencies))

```bash
wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run`
sudo chmod +x cuda_9.0.176_384.81_linux-run
sudo ./cuda_9.0.176_384.81_linux-run
```
- Select "no" to “Install NVIDIA Accelerated Graphics Driver for Linux-x86_64 384.81?”.
- Then download cuDNN (latest version for CUDA 9.0)

```bash
tar xvzf cudnn-9.0-linux-x64-v7.4.2.24.tgz
sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include
sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
sudo ldconfig
```

#### Install other non-python packages

- Install ImageMagick 6.8.9. `sudo apt-get install imagemagick`
- To use GUIs, install PyQt4 into the virtualenv according to [this answer](https://stackoverflow.com/a/28850104).
    - Install python-qt4 globaly: `sudo apt-get install python-qt4`
    - Create symbolic link of PyQt4 to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/PyQt4/ mousebrainatlas_virtualenv/lib/python2.7/site-packages/`
    - Create symbolic link of sip.so to your virtual env: `ln -s /usr/lib/python2.7/dist-packages/sip.x86_64-linux-gnu.so mousebrainatlas_virtualenv/lib/python2.7/site-packages/`

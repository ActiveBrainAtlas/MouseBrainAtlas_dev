# Installation

This part needs to be done only once. It has already been done on the atlas room workstation. No need to do it for regular uses.

```
＃ Install vtk 7.1.1 (Cannot use newest version 8 because the window crashes immediately after it launches)
cd /home/yuncong/MouseBrainAtlas/setup/
wget https://www.vtk.org/files/release/7.1/vtkpython-7.1.1-Linux-64bit.tar.gz
tar xfz vtkpython-7.1.1-Linux-64bit.tar.gz

# Install required python packages
sudo apt-get install libgeos-dev
pip install cython==0.28.5 # see this issue https://github.com/h5py/h5py/issues/535
pip install git+https://github.com/pmneila/PyMCubes.git@9fd6059
```

# Regular use

```
cd /home/yuncong/MouseBrainAtlas
source setup/config.sh

cd setup
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/vtkpython-7.1.1-Linux-64bit/lib/
export PYTHONPATH=$PYTHONPATH:`pwd`/vtkpython-7.1.1-Linux-64bit/lib/python2.7/site-packages/

cd ../demo/
python download_demo_data_render3d.py (Not necessary since all data are already downloaded)
python demo_render3d.py --render_config_atlas render_config_atlas.csv --experiments_config lauren_experiments.csv 
```

- The file `lauren_experiments.csv` specifies which experiments to display markers for and the color of each.
- The file `render_config_atlas.csv` specifies the color/opacity of each atlas structure.
- Levels can be any of [0, 0.1, 0.2, ... 0.9, 1.0].
- If want to show SNR_L with the largest possible probability level, in `demo_render3d.py` set `use_big_snr_l` to True.
- You can also choose to show all markers or a subset of them in `demo_render3d.py` (line 110).
- In the 3D viewer, use mouse wheel to zoom and SHIFT+drag to move. Press Q to quit.

If encounter the error "X Error of failed request", follow [this fix](https://askubuntu.com/a/882047).

## Changing initial viewing angle

The angle is controlled by three parameters:
- view_up: vector representing the up direction
- position: position of the camera
- focal: position of focal point

I have defined a few presets of these parameters in the function launch_vtk() in src/utilities/vis3d_utilities.py.
The presets are: 15 (meaning 15 degrees from above), 30, 45, sagittal, coronal_posteriorToAnterior, horizontal_bottomUp, horizontal_topDown

You can choose which preset to use by modifying Line 144 of demo/demo_render3d.py, just change the argument init_angle='sagittal' to any of above.

Alternatively, you can choose to directly set the three arguments (view_up, position and focal).

To obtain the values of these parameters, just rotate/move/zoom the atlas in the viewer until you are satisfied with the angle. Then press "g". These parameters will be printed in the terminal.
Then you can feed them as arguments to launch_vtk(). The next time you run the code, the viewer will initialize to this angle.

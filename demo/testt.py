import os, cv2
print cv2.__version__

import numpy as np

tiff_target_folder = '/media/alexn/Data_2/czi_convert_test/tiffs/f-test/'
for tiff_fn in os.listdir(tiff_target_folder):
        # Do nothing if expected patterns don't show up in the file
        if not '.czi' in tiff_fn or not '.tiff' in tiff_fn:
            continue
        
        # Remove unwanted symbols and whatnot
        new_fn = tiff_target_folder + tiff_fn.replace('.czi #','')
        # Read the image we just extracted
        img = cv2.imread( tiff_target_folder + tiff_fn )
        print np.shape(img)
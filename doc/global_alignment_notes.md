Temporary file with instructions on the pipeline in place

## Yuncong's Instructions

You will need to manually provide the x,y coordinates of the midpoint of 12 and of 3N. Then create a new case (DEMO998 had 558/207 and 366/171) anchor1 = 12N, anchor2 = 3N_L.

in resolution "dataResol", what is dataResol? That is given by `intensity_volume_spec`

where is the origin? you may ask: with respect to (wrt) wholebrainWithMargin. That is the volume you would have loaded using DataManager.load_original_volume_v2(intensity_volume_spec, return_origin_instead_of_bbox=True). the coordinate should be relative to this volume. 

This volume is what I call the "intensity volume", This is the exact volume that the GUI loaded. So you need to get these four coordinates by running the labeling GUI

### Labelling GUI

you can browse using 3/4, 5/6, 7/8 automatically.

You need to specify the right "version" in the commandline, probably "NtbNormalizedGammaInvertedJpeg"

Currently has an error loading high-resolution image on left side of GUI window

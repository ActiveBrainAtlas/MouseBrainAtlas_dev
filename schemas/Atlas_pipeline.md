## Atlas project

The Atlas takes in histology sections as input and constructs a 3D atlas with gnerated probability volumes for certain structures of interest. No actual experimentation, fairly linear pipeline.

## Collection of tables

- __Mouse__
  - (Mouse table)[mouse_info.md]
  
- __Raw Stack__
  - Orientation: saggital, coronal, or horozontal: `saggital`
  - Number of sections: total number of histology sections made: `500`
  - List of unusable sections: Should be a part of "Sorted Filenames"
  - Sorted filenames: a list of the filenames numbered in order: 
  - Extensions: filename extensions: `jp2`
  - Microscope resolution: microns per pixel: `0.46um`
  - Section thickness: The thickness in microns of each slice: `20um`
  - Stain type: Injected compound for neuron visualization: `Ntb`
  - Stack: The stack itself, nearly 1 terrabyte. A series of images about 2GB each.
  
- __Preprocessing Stages__
  - Downsampling factor: All thumbnail images will be downsampled by this amount: `32X`
  - Everything below this point is a stack of images with a certain transformation/normalization/cut applied to them.
  - Thumbnail: 
  - Aligned thumbnails: 
  - Global intensity normalization: 
  - Thumbnail masks: 
  - Lossless Local Adaptive Intensity Normalized Brainstem Crops: 
  
- __Patch Features__
  - 

- __Probability Volumes__
  - 

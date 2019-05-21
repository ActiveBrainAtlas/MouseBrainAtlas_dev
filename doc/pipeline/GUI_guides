# Alignment GUI:
Command: `python $REPO_DIR/gui/preprocess_tool_v3.py $stack --tb_version $img_version_1`

The automatic intra-stack alignment has an error rate of about 5-10%, it will be expected that the user corrects any erroneous alignments.
  - Click the button, `load_sorted_filenames`
  - Click the dropdown menu and select `Original_Aligned`
  - Identify the number of broken pairs. Slices are aligned to their neighbors, one slice being misaligned will require two corrections.
  - Click the button `edit transform`
    - A new screen should pop up with three images. The left and middle images are two slices that have been aligned, the right image is the overlay of both images. For every broken pair, follow the remaining instructions.
  - Click the button `add anchor pair`
    - Every time you click this button you add a corresponding pair of points to the left and middle images. Click on the leftmost image to add its point, then click on the middle image to add the corresponding point. These points should be located in the exact same region on both images such that when overlayed, the points will overlap. Do this for 4-6 points for every pair of misaligned images.
    - Click the button `compute transform` and move on to the next pair of images



# Masking GUI:
Command: `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`




# Annotation GUI:

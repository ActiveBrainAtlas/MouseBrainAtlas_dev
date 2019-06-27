# Alignment GUI:
Command: `python $REPO_DIR/gui/preprocess_tool_v3.py $stack --tb_version $img_version_1`

The automatic intra-stack alignment has an error rate of about 5-10%, it will be expected that the user corrects any erroneous alignments.
  - Click the button, `load_sorted_filenames`
  - Click the dropdown menu and select `Original_Aligned`
  - Identify the number of broken pairs. Slices are aligned to their neighbors, one slice being misaligned will require two corrections. Use "`[`" and "`]`" to the previous and next images.
  - Click the button `edit transform`
    - A new screen should pop up with three images. The left and middle images are two slices that have been aligned, the right image is the overlay of both images. For every broken pair, follow the remaining instructions.
  - Click the button `add anchor pair`
    - Every time you click this button you add a corresponding pair of points to the left and middle images. Click on the leftmost image to add its point, then click on the middle image to add the corresponding point. These points should be located in the exact same region on both images such that when overlayed, the points will overlap. Do this for 4-6 points for every pair of misaligned images.
    - Click the button `compute transform` and move on to the next pair of images
  - Close the GUI

# Masking GUI:
Command: `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`\

This GUI is used twice. Once so the user can create rough outlines of the brain tissue on each image, this assists the automatic mask-generation by giving it a starting point. After the automatic mask-generation, this GUI is run again to correct the masks that have been created.

## Masking GUI: Initial Manual Mask Contours
GUI controls:
- Wheel to zoom
- Click and drag to translate
- `[` and `]` to cycle through images

Working on the top-left image field:
  - Right click, select `create initial snake contour`.
    - Click around the tissue, creating a set of vertices joined together by lines. Ensure that the tissue is within the polygon you are creating. Once the encapsulating polygon is about finished, click your first point to close and complete it.
    - Right click, select `set this contour as anchor contour`
  - Run the last bullet in its entirety for about 5-8 sections in a stack of 300-400 images. Try to keep the anchor contours spaced out.
  - Right click, select `automatically estimate all contours`. This generates contours on every image that is NOT an anchor contour via linear interpolation.
  Looking at the bottom push buttons: 
    - Press `save anchor contours`
    - Press `save initial contours`
  - Close the GUI
    - Note: this GUI will bring up a tiny, blank window that also needs to be closed

## Masking GUI: Correct Auto-generated Masks

Working in the bottom-left image field:
  - Initially, if there is no image in the bottom left, click the image on the TOP left and press either `[` or `]` to load the next slice. Read the GUI controls above under "Masking GUI: Initial Manual Mask Contours"  as a reminder, this is the same GUI window, just being used for a different purpose.
  - Using the right click menu, add and remove vertices as is necessary. Left click and drag existing vertices to move them. For every incorrect mask, create / remove / drag the contours until they are correct.
    - Once finished, push `update merged mask`, then click `save final mask for current section`.
  - After every incorrect mask has been corrected following the above bullet point:
    - Push `save final masks for all sections`
    - Push `export masks as PNG for all sections`
  - Close the GUI

# Annotation GUI
Command: `python $REPO_DIR/gui/brain_labeling_gui_v28.py $stack --prep 2 --img_version $img_version_2`

- This GUI consists of one large window on the left, and three smaller windows on the right. For each window, you can scroll through slices using number keys, one to advance a slice and one to go back a slice, as follows:
  - For the left window: `1` and `2`
  - For the upper right window: `3` and `4`
  - For the middle right window: `5` and `6`
  - For the bottom right window: `7` and `8`
- Hold space, then click on brain tissue in any of the four windows. This will select the point you clicked. If you hold space, red crosshairs should now be visible in each of the three planes. At the header bar of the GUI it will display the x, y, and z coordinates of your selection (z coordinate is just section number). Use this to find the centerpoint coordinates (X and Y) of `3N_R` and `12N`.
  - This can also be done to find the midline of the stack, though you can use any method that you find intuitive. Record the section that lies at the approximate midpoint.

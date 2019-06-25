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
  - Close the GUI

# Masking GUI:
Command: `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`\

This GUI is used twice. Once so the user can create rough outlines of the brain tissue on each image, this assists the automatic mask-generation by giving it a starting point. After the automatic mask-generation, this GUI is run again to correct the masks that have been created.

## Masking GUI 1: Initial Manual Mask Contours
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

## Masking GUI 2: Correct Auto-generated Masks

Working in the bottom-left image field:
  - Using the right click menu, add and remove vertices as is necessary. Click and drag existing vertices to move them. For every incorrect mask, create / remove / drag the contours until they are correct.
    - Once finished, push `update merged mask`, then click `save final mask for current section`.
  - After every incorrect mask has been corrected following the above bullet point:
    - Push `save final masks for all sections`
    - Push `export masks as PNG for all sections`
  - Close the GUI

# Annotation GUI:
Command: `python $REPO_DIR/gui/brain_labeling_gui_v28.py $stack --prep 2 --img_version $img_version_2`




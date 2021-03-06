### GUI Steps (Local)
1) Convert raw slides into tiff for each secion and placeholders.
1) [Setup: Step 3, Create Sorted Filenames](#create-sorted-filenames-gui)
2) [Setup: Step 4, Orient Images](#orient-images-gui)
3) [Alignment: Step 1, Correct Automatic ALignments](#alignment-gui)
4) [Masking: Step 1, Create Initial Masks](#initial-mask-contours)
5) [Masking: Step 3, Correct Automatic Masks](#correct-auto-generated-masks)
6) [Cropping: Step 1, Brainstem Crop](#choose-brainstem-cropping-box)
7) [Rough Global Fit: Step 1, Select Centers of 12N and 3N_R](#select-structure-centers)
8) [Annotation GUI](#annotation-gui)

# Setup GUIs:

## Create Sorted Filenames GUI:
GUI controls:
- Wheel to zoom
- Click and drag to translate
- `[` and `]` to cycle through images

The order of the images is assumed to be alphabetical initially. The user's job is to cycle through all of the images, and reorder images that are not in the correct order. The current filename appears in the top-left, the current slice number appears in the top right. We define "slice number" as the slice's position in the stack, i.e. slice 0 is the first slice, then slice 1, then slice 2, with the last slice being the highest number.
  - Use the Left-arrow and Right-arrow buttons on the bottom of the GUI to decrease or increase the slice number respectively.
  - For every single slice: Mark it as "blurry" if the slice is mostly intact but out of focus. Mark it as "unuseable" if the slice is distorted or missing a large chunk of tissue. Mark it as "good" if the slice is not significantly distorted or out of focus. "good" slices will be run through the classifiers.
  - Once you have ensured that ALL of the slices have been properly ordered, AND all blurry/unuseable slices have been marked, click the "Finished" button.

## Orient Images GUI:
GUI controls:
- Wheel to zoom
- Click and drag to translate
- `[` and `]` to cycle through images

Cycle through all existing images and ensure that the rostral side is pointing to the left, caudal to the right, dorsal to the top, ventral to the bottom. If any image needs to be rotated, click the dropdown menu and select the rotation amount, then click the "Rotate image(s)" button. Note that there is a checkbox to toggle whether transformations are applied to ALL the images, be very careful whether it is checked or not. Finally there is a "Flip" and a "Flop" button, which mirror the image(s) across a central vertical or horozontal line respectively.
  - Once you have ensured that ALL of the slices have been properly oriented, click the "Done orienting" button.

# Alignment GUI:
GUI controls:
- Wheel to zoom
- `[` and `]` to cycle through images
- `m`: Toggle between VIEW mode (grayscale) and ALIGN mode (red & blue)
- Use the buttons on the bottom when in ALIGN mode to align slices.

    This GUI should start in VIEW mode, you can tell it is in VIEW mode because it will display only grayscale images. While it is in VIEW mode, press and hold either `[` or `]` to quickly cycle through images. The images should be aligned to one another such that quickly scrolling through is seamless, every subsequent section should be oriented the same way. In a case where going from one image to another clearly shows that they are not aligned, i.e. overlaying the images would show that they are not on top of one another, this is considered to be a "broken chain". 
  
    Alignment is such that slice A is aligned to slice B, B to C, C to D, D to E, E to F, and so on. If slice C is misaligned to slice D, then A->B->C will be aligned together, and D->E->F will be aligned together. C->D is the broken link, and must be corrected. Correcting broken links is done in ALIGN mode. Hit `m` on your keyboard to toggle modes. You know you are in ALIGN mode when you see two slices overlain, one in red, one in blue. Find the broken pair and go into ALIGN mode, you'll know it's a broken pair when the red and blue slices are not overlain properly.
  
    While still in ALIGN mode, use the buttons in the GUI's footer to align the red slice to the blue slice. The options include translating the red slice up/down/left/right, or rotating it clockwise/counterclockwise. Use these six buttons to align the red to the blue by eye. Once finished fixing the broken pair, click the `Save Transformation` button in the bottom right. REPEAT THESE INSTRUCTIONS FOR EVERY SINGLE BROKEN PAIR.
  
    Double and triple check that all broken pairs have been corrected. Best way to do this: go into VIEW mode and hold either `[` or `]`, verify by eye that every slice is aligned properly. Once you are certain there are no more broken pairs, click the button labeled `DONE`.


# Masking GUI:
Command: `python $REPO_DIR/gui/mask_editing_tool_v4.py $stack $img_version_1`\

This GUI is used twice. Once so the user can create rough outlines of the brain tissue on each image, this assists the automatic mask-generation by giving it a starting point. After the automatic mask-generation, this GUI is run again to correct the masks that have been created.

## Initial Mask Contours
GUI controls:
- Wheel to zoom
- Click and drag to translate
- `[` and `]` to cycle through images

Working on the top-left image field:
  - Right click, select `create initial snake contour`.
    - Click around the tissue, creating a set of vertices joined together by lines. Ensure that the tissue is within the polygon you are creating. Once the encapsulating polygon is about finished, click your first point to close and complete it.
    - Right click, select `set this contour as anchor contour`
  - Run the last step in its entirety for about 5-8 sections in a stack of 300-400 images. Try to keep the anchor contours spaced out.
  - Right click, select `automatically estimate all contours`. This generates contours on every image that is NOT an anchor contour via linear interpolation.
  Looking at the bottom push buttons: 
    - Press `save anchor contours`
    - Press `save initial contours`
  - Close the GUI
    - Note: this GUI will bring up a tiny, blank window that also needs to be closed

## Correct Auto-generated Masks
GUI controls:
- Wheel to zoom
- Click and drag to translate
- `[` and `]` to cycle through images
- Right click -> add vertices
  - Left clicking should now add new vertices. To disable, right click and select "remove vertices" and click anywhere
- Right click -> remove vertices
  - Then left click and drag a box, all vertices within this box will be deleted

Working in the bottom-left image field:
  - Initially, if there is no image in the bottom left, click the image on the TOP left and press either `[` or `]` to load the next slice.
  - Using the right click menu, add and remove vertices as is necessary. Left click and drag existing vertices to move them. For every incorrect mask, create / remove / drag the contours until they are correct.
    - Once finished, push `update merged mask`, then click `save final mask for current section`.
  - After every incorrect mask has been corrected following the above bullet point:
    - Push `save final masks for all sections`
    - Push `export masks as PNG for all sections`
  - Close the GUI
    - Note: this GUI will bring up a tiny, blank window that also needs to be closed

## Choose Brainstem Cropping Box
GUI controls:
- `[` and `]` to cycle through images

Using this GUI, you need to set 6 parameters in the 6 text boxes on the footer of the GUI screen. We want to define a 3 dimensional cropping box over the __brainstem__ region. 

For the Rostral/Caudal/Dorsal/Ventral limits, simply click on the button labeled as one of these limits, and then click on the image where the limit is. For example, for the dorsal limi, I would click the button labeled "Dorsal Limit:" and then I would click any pixel just above the highest part of the brain, ensuring to not cut any tissue off of any of the sections. A line will appear showing where each limit has been placed. You can always tweak the limits by typing a new limit into the associated text box and pushing "enter" on your keyboard.

For the z limits, the first/last slices with brainstem, simply navigate to the first/slice slice that contains the brainstem and click the associated button.

## Select Structure Centers
Two dots should be displayed, a red dot and a blue dot, corresponding to the structures labeled "12N" and "3N" respectively. The GUI will automatically display an image close to the midline, you should keep close to the midline throughout using this GUI.

Pick a structure to work on first, let's say 12N. Locate the two text boxes on the bottom pane of the GUI, they should be the same color and labeled "X" and "Y" where X is the horozontal coordinate and y is the vertical coordinate (y=0 is the top of the image). Type in the X and Y values for the centerpoint of 12N, push enter after each time, and the dot should move accordingly.

Once the centerpoint of both 12N and 3N appear to be correct (does not have to be perfect, but should be close) push Enter and wait for the automatic scripts to finish.

# Annotation GUI
Command: `python $REPO_DIR/gui/brain_labeling_gui_v28.py $stack --prep 2 --img_version $img_version_2`

- This GUI consists of one large window on the left, and three smaller windows on the right. For each window, you can scroll through slices using number keys, one to advance a slice and one to go back a slice, as follows:
  - For the left window: `1` and `2`
  - For the upper right window: `3` and `4`
  - For the middle right window: `5` and `6`
  - For the bottom right window: `7` and `8`
- Hold space, then click on brain tissue in any of the four windows. This will select the point you clicked. If you hold space, red crosshairs should now be visible in each of the three planes. At the header bar of the GUI it will display the x, y, and z coordinates of your selection (z coordinate is just section number). Use this to find the centerpoint coordinates (X and Y) of `3N_R` and `12N`.
  - This can also be done to find the midline of the stack, though you can use any method that you find intuitive. Record the section that lies at the approximate midpoint.

## Preprocess

For each step below that requires `input_spec.ini`, the ini file is a different one and must be manually created.

- Run `download_demo_data_preprocessing.py` to download 4 JPEG2000 images of the demo brain.
- **(HUMAN)** Create meta data information for this brain
- Create `DEMO998_input_spec.json`. `python jp2_to_tiff.py DEMO998 DEMO998_input_spec.json`.
- `python extract_channel.py input_spec.ini 2 Ntb`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- `python normalize_intensity.py input_spec.ini NtbNormalized`
- **(HUMAN)** browse thumbnails to verify orientations are all correct
- **(HUMAN)** Obtain a roughly correct sorted list of image names from the data provider.
- `python align.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_elastix_output ../src/preprocess/parameters/Parameters_Rigid_MutualInfo_noNumberOfSpatialSamples_4000Iters.txt`
- **(HUMAN)** select anchor image, using preprocessGUI `preprocess_gui.py`
- `python compose.py --elastix_output_dir "demo_data/CSHL_data_processed/DEMO998/DEMO998_elastix_output" \
--custom_output_dir "demo_data/CSHL_data_processed/DEMO998/DEMO998_custom_output" \
--input_spec input_spec.ini  \
--anchor "MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250" \
--out "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv"`
- **(HUMAN)** create `DEMO998.ini` and put it in `demo_data/brains_info/`
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --out_prep_id alignedPadded`
- **(HUMAN)** Inspect aligned images using preprocessGUI `preprocess_gui.py`, correct pairwise transforms and check each image's order in stack. Create `DEMO998_sorted_filenames.txt` based on the given roughly correct list.
- **(HUMAN)** draw initial snake contours for masking using maskingGUI. 
`python mask_editing_tool_v4.py DEMO998`
- `python masking.py input_spec.ini demo_data/CSHL_data_processed/DEMO998/DEMO998_prep1_thumbnail_initSnakeContours.pkl`
- **(HUMAN)** Return to masking GUI to inspect and correct the automatically generated masks. 
`python mask_editing_tool_v4.py DEMO998`
- **(HUMAN)** Create `DEMO998_original_image_crop.csv`
- `python warp_crop.py --input_spec input_spec.ini \
 --inverse_warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_original_image_crop.csv" \
 --out_prep_id None`
- `python normalize_intensity_adaptive.py input_spec.ini NtbNormalizedAdaptiveInvertedGamma`
- **(HUMAN)** Manually specify the alignedWithMargin cropbox based on alignedPadded images, or automatically infer based on alignedPadded masks.
- `python warp_crop.py --input_spec input_spec.ini \
 --warp "demo_data/CSHL_data_processed/DEMO998/DEMO998_transformsTo_MD662&661-F84-2017.06.06-14.03.51_MD661_1_0250.csv" \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_cropbox.ini" \
 --out_prep_id alignedWithMargin`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- **(HUMAN)** Specify prep2 (alignedBrainstemCrop) cropping box, based on alignedWithMargin thumbnails or alignedPadded thumbnails
- `python warp_crop.py --input_spec input_spec.ini \
 --crop "demo_data/CSHL_data_processed/DEMO998/DEMO998_cropbox.ini" \
 --out_prep_id alignedBrainstemCrop`
- `python rescale.py input_spec.ini thumbnail -f 0.03125`
- `python compress_jpeg.py input_spec.ini`

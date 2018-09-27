- Raw data folder might contain images with different filenames but are of the same slice. One can be the re-scanned version of the other. So the number of retrieved files by searching data folder might be more than that provided in the sorted filename list.
- 444 images found. convert jp2 to raw tiff: Sep 26 07:25 - Sep 26 10:19. Using more than one process tends to blow up memory and cause IO thrashing. Also, remember to run these commands in a `screen` session, so that a disconnected ssh connection will not stop the program.
- Put `MD585_sorted_filenames.txt` under data folder.
- In `MD585_input_spec.ini`, set image list to "all". This will expand to all image names according to the sorted filename list. To get a RGB-average gray channel rather than the blue channel, `python extract_channel.py MD585_input_spec.ini -1 gray` Sep 26 18:30 - Sep 27 01:01. Can only use one process.
- thumbnail: Sep 27 07:29 - Sep 27 08:11
- I should make `from_none_to_aligned.ini` not dependent on DATA_ROOTDIR (TODO).
- `align_v3.py` and `compose_v3.py` still use "sorted_image_name_list", changed to using "image_name_list".
- 


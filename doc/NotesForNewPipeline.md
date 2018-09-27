- There are images with different names but are of the same slice. One can be the re-scanned version of the other. So retrieved files by searching data folder might be more than that provided in the sorted filename list.
- Put `MD585_sorted_filenames.txt` under data folder.
- In `MD585_input_spec.ini`, set image list to "all". This will expand to all image names according to the sorted filename list. To get a RGB-average gray channel rather than the blue channel, `python extract_channel.py MD585_input_spec.ini -1 gray`


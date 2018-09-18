
Commands:
```
./demo/download_demo_data_registration.py
./demo/register_brains_demo_12N.py
./demo/register_brains_demo_3N_R_4N_R.py
./demo/visualize_registration_demo_3_structures.py
```
The download takes less than 1 minute. Next command registers 12N individually. Last command registers 3N_R and 4N_R as a group.

`./visualize_registration_demo_3_structures.py`

To visualize the registration results.

---

## Summary
For the sake of generalization the following substitutions will be used.
- `STACK` = the name of the current brain stack, ex: 'MD662', 
- `SLICE` = the name of the current slice, this is typically long, ex: 'MD662&661-F86-2017.06.06-14.56.48_MD661_2_0257'
- `ANCHOR` = a particular SLICE, all other slices are aligned to this ANCHOR
- `SLICECF` = the slice you have computed features for. Must have run these slices through the last demo script fully (2 slices for the demo).

Folders already present:
`CSHL_classifiers,  CSHL_data_processed,  CSHL_patch_features,  CSHL_scoremaps,  CSHL_scoremap_viz,  CSHL_simple_global_registration,  CSHL_volumes,  mxnet_models`


#### INPUTS:

```

```

#### OUTPUTS:

```

```


## Alex Running Notes

#### For running the first command `demo/download_demo_data_registration.py`:
***
- Ran with `python demo/download_demo_data_generate_prob_volumes.py --demo_data_dir $ROOT_DIR`. Downloading the files takes at least 3-5 hours.
- Downloads an entire stack's feature data (272 sections for MD661 specifically). For each slice there are two *.bp files as listed below:
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_features.bp`
 - `[SLICENAME]_prep2_none_win7_inception-bn-blue_locations.bp`
***

#### For running the second command `demo/register_brains_demo_12N.py`:
- Outputs shown in summary, too many to list properly.

#### For running the second command `demo/register_brains_demo_3N_R_4N_R.py`:
- Outputs shown in summary, too many to list properly.

### For running the third command `demo/visualize_registration_demo_3_structures.py`:
- Outputs shown in summary, too many to list properly.

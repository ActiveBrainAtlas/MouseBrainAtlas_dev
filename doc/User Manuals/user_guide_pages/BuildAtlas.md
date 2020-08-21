# Building atlas

Reference: `3d/build_atlas_from_aligned_annotated_brains_v6.ipynb`

Most important function
[average_location()](https://github.com/ActiveBrainAtlas/MouseBrainAtlas_dev/blob/a46bfc4341d403cbef17da977ee93da22664e357/src/utilities/registration_utilities.py#L2147)

## Compute average positions

- Mean positions (wrt _canonicalAtlasSpace_). `/CSHL_meshes/<atlas_name>/<atlas_name>_1um_meanPositions.pkl`

## Compute average shapes

- Mean shapes
    - `/CSHL_meshes/<atlas_name>/mean_shapes/<atlas_name>_10.0um_<sided_or_surround_structure>_meanShape_volume.bp`
    - `/CSHL_meshes/<atlas_name>/mean_shapes/<atlas_name>_10.0um_<sided_or_surround_structure>_meanShape_origin_wrt_meanShapeCentroid.txt`.
    
- Individual instances
  - Instance number to brain/side map. `/CSHL_meshes/<atlas_name>/instance_sources/<atlas_name>_<unsided_structure>_sources.pkl`
  - Instance-to-instance registration parameters
    - `/CSHL_meshes/<atlas_name>/mean_shapes/instance_registration/<unsided_structure>_instance<instance_num>/<registration_spec>/`.
      - `<registration_spec>_parameters.json`
      - `<registration_spec>_scoreEvolution.png`
      - `<registration_spec>_scoreHistory.bp`
      - `<registration_spec>_trajectory.bp`
    
##  Put average shape at average position

- Atlas structures (located in _canonicalAtlasSpace_). 
    - `/CSHL_volumes/<atlas_name>/<atlas_name>_10.0um_scoreVolume/score_volumes/<atlas_name>_10.0um_scoreVolume_<sided_or_surround_structure>.bp`.
    - `/CSHL_volumes/<atlas_name>/<atlas_name>_10.0um_scoreVolume/score_volumes/<atlas_name>_10.0um_scoreVolume_<sided_or_surround_structure>_origin_wrt_canonicalAtlasSpace.txt`.

nominal_centroids_wrt_canonicalAtlasSpace_um -> 
CSHL_meshes/atlasV6/atlasV6_1um_meanPositions.pkl
nominal centroid position for each structure

canonical_center_wrt_fixed_um -> 
atlasV6/atlasV6_canonicalCentroid_wrt_fixedWholebrain.txt

`midplane_normal`: normal vector of the mid-sagittal plane estimated from centroids in original coordinates. Note that this is NOT the mid-plane normal using canonical coordinates, which by design should be (0,0,1).

midplane_anchor_wrt_fixedBrain: a point on the mid-sagittal plane that is used as the origin of canonical atlas space.

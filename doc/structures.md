## Structure names

- `3N_L/R`
  - oculomotor nucleus
- `4N_L/R`
  - trochlear nucleus
- `5N_L/R`
  - motor trigeminal nucleus
- `6N_L/R`
  - abducens nucleus
- `7N_L/R`
  - facial nucleus
- `7n_L/R`
  - facial nerve
- `10N_L/R`
  - dorsal motor nucleus of vagus
- `12N`
  - hypoglossal nucleus
- `Amb_L/R`
  - ambiguus nucleus
- `PBG_L/R`
  - parabigeminal nucleus
- `AP`
  - area postrema
- `LC_L/R`
  - locus coeruleus
- `SNC_L/R`
  - substantia nigra, compact part 
- `SNR_L/R`
  - substantia nigra, reticular part
- `Tz_L/R`
  - nucleus of the trapezoid body
- `RMC_L/R`
  - red nucleus, magnocellular part
- `LRt_L/R`
  - lateral reticular nucleus
- `DC_L/R`
  - dorsal cochlear nucleus
- `VCP_L/R`
  - ventral cochlear nucleus, posterior part
- `VCA_L/R`
  - ventral cochlear nucleus, anterior part
- `VLL_L/R`
  - ventral nucleus of the lateral lemniscus
- `Sp5O_L/R`
  - spinal trigeminal nucleus, oral part
- `Sp5I_L/R`
  - spinal trigeminal nucleus, interpolar part
- `Pn_L/R`
  - pontine nuclei
- `RtTg`
  - reticulotegmental nucleus of the pons
- `Sp5C_L/R`
  - spinal trigeminal nucleus caudalis
- `IC`
  - inferior colliculus
- `SC`
  - superior colliculus

notes: 
- `L/R` = This structures appears in both the right and left hemispheres
- `N` = Motor Nucleas

Structures mentioned in paper butnot part of pipeline: 
- lateral parabrachial nucleus (LBP)
- spinal trigeminal nucleus, caudal part (SP5C)

## Motor Nuclei Information

motor_nuclei = `['3N', '4N', '5N','6N', '7N', 'Amb', '12N', '10N']`

motor_nuclei_sided_sorted_by_rostral_caudal_position = `['3N_R', '3N_L', '4N_R', '4N_L', '5N_R', '5N_L', '6N_R', '6N_L', '7N_R', '7N_L', 'Amb_R', 'Amb_L', '12N', '10N_R', '10N_L']`


## Structures sorted by various parameters

structures_sided_sorted_by_size = `['4N_L', '4N_R', '6N_L', '6N_R', 'Amb_L', 'Amb_R', 'PBG_L', 'PBG_R', '10N_L', '10N_R', 'AP', '3N_L', '3N_R', 'LC_L', 'LC_R', 'SNC_L', 'SNC_R', 'Tz_L', 'Tz_R', '7n_L', '7n_R', 'RMC_L', 'RMC_R', '5N_L', '5N_R', 'VCP_L', 'VCP_R', '12N', 'LRt_L', 'LRt_R', '7N_L', '7N_R', 'VCA_L', 'VCA_R', 'VLL_L', 'VLL_R', 'DC_L', 'DC_R', 'Sp5O_L', 'Sp5O_R', 'Sp5I_L', 'Sp5I_R', 'Pn_L', 'Pn_R', 'RtTg', 'SNR_L', 'SNR_R', 'Sp5C_L', 'Sp5C_R', 'IC', 'SC']`

structures_sided_sorted_by_rostral_caudal_position = `['SNC_R', 'SNC_L', 'SC', 'SNR_R', 'SNR_L', 'RMC_R', 'RMC_L', '3N_R', '3N_L', 'PBG_R', 'PBG_L', '4N_R', '4N_L', 'Pn_R', 'Pn_L', 'VLL_R', 'VLL_L', 'RtTg', '5N_R', '5N_L', 'LC_R', 'LC_L', 'Tz_R', 'Tz_L', 'VCA_R', 'VCA_L', '7n_R', '7n_L', '6N_R', '6N_L', 'DC_R', 'DC_L','VCP_R', 'VCP_L', '7N_R', '7N_L', 'Sp5O_R', 'Sp5O_L', 'Amb_R', 'Amb_L', 'Sp5I_R', 'Sp5I_L', 'AP', '12N', '10N_R', '10N_L', 'LRt_R', 'LRt_L', 'Sp5C_R', 'Sp5C_L']`

structures_unsided_sorted_by_rostral_caudal_position = `['SNC', 'SC', 'IC', 'SNR', 'RMC', '3N', 'PBG','4N', 'Pn','VLL','RtTg', '5N', 'LC', 'Tz', 'VCA', '7n', '6N', 'DC', 'VCP', '7N', 'Sp5O', 'Amb', 'Sp5I', 'AP', '12N', '10N', 'LRt', 'Sp5C']`

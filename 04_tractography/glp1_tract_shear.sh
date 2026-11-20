#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test
for S in "$@"; do
  SRC=$E/glp1_check/$S; L=${LABEL:-$E/glp1_tract/$S/label_global_v3.mif}; O=$E/glp1_tract_shear/$S
  for f in $E/eddy_sc/$S/corr.nii.gz $SRC/mask.mif $L $E/gc_shear/$S.flip.b $E/gc_shear/$S.full.b; do [ -f $f ] || { echo "$S MISSING $f"; continue 2; }; done
  mkdir -p $O/flip $O/full; echo "## $S start $(date +%H:%M:%S)"
  for V in flip full; do (
    mrconvert $E/eddy_sc/$S/corr.nii.gz $O/dwi_$V.mif -grad $E/gc_shear/$S.$V.b -force -quiet
    dwi2response tournier $O/dwi_$V.mif $O/$V/response.txt -mask $SRC/mask.mif -nthreads 8 -force -quiet
    dwi2fod csd $O/dwi_$V.mif $O/$V/response.txt $O/$V/fod.mif -mask $SRC/mask.mif -nthreads 8 -force -quiet
    tckgen $O/$V/fod.mif $O/$V/tracks_100k.tck -algorithm iFOD2 -seed_image $SRC/mask.mif -mask $SRC/mask.mif -select 100000 -cutoff 0.1 -minlength 0.5 -maxlength 80 -nthreads 8 -force -quiet
    tck2connectome $O/$V/tracks_100k.tck $L $O/$V/count_v4.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet
    rm -f $O/$V/fod.mif
  ) & done
  wait
  for V in flip full; do [ -s $O/$V/count_v4.csv ] && echo "$S $V ok" || echo "$S $V FAILED"; done
  echo "## $S done $(date +%H:%M:%S)"
done

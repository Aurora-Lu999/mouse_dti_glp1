#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1; O=$E/ctrl_tract_sc/$S; mkdir -p $O/rep/orig $O/rep/yflip
for V in orig yflip; do
  tckgen $O/$V/fod.mif $O/rep/$V/tracks_100k.tck -algorithm iFOD2 -seed_image $O/mask.mif -mask $O/mask.mif -select 100000 -cutoff 0.1 -minlength 0.5 -maxlength 80 -nthreads 8 -force -quiet
  tck2connectome $O/rep/$V/tracks_100k.tck $O/label_global.mif $O/rep/$V/count_shift.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet
done
[ -s $O/rep/orig/count_shift.csv ] && [ -s $O/rep/yflip/count_shift.csv ] && echo "## $S rep done" || echo "## $S rep FAILED"

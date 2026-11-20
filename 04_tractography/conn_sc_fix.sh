#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; N=$E/glp1_tract_sc
cc() { for V in orig yflip; do tck2connectome $N/$1/$V/tracks_100k.tck $2 $N/$1/$V/$3 -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done; }
for S in B26010600 B26010602 B26010604 B26010605 B26010606 B26010607 B26010608 B26010800; do
  cc $S $E/glp1_tract_shift/$S/label_global_v3.mif count_v4.csv; echo "new $S done"
done
cc B25123002 $E/glp1_tract/B25123002/label_global_v4.mif count_v4_relabel.csv; echo "relabel B25123002 done"
C=$E/glp1_tract/B25123005/cand4/C_label.nii.gz; L5=$N/B25123005/label_global_v4C.mif
mrcalc $C 1000 -gt $C 834 -sub $C -if $L5 -datatype uint16 -force -quiet
cc B25123005 $L5 count_v4_relabel.csv; echo "relabel B25123005 done"

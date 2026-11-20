#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
L=$E/glp1_tract/$S/label_global_v3.mif; O=$E/glp1_tract_sc/$S
[ -f $L ] && [ -f $O/yflip/tracks_100k.tck ] || { echo "skip $S"; exit 0; }
for V in orig yflip; do tck2connectome $O/$V/tracks_100k.tck $L $O/$V/count_v4.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done

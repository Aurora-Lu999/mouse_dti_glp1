#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1; C=$E/glp1_check/$S; T=$E/glp1_tract_shift/$S
T2=/mnt/newStor/paros/paros_WORK/skull_stripping/GLP1_T2s/${S}_T2.nii.gz
L=$E/glp1_labeling/$S/${S}_labels_native.nii.gz
[ -f $L ] && [ -f $T/orig/tracks_100k.tck ] && [ -f $T/yflip/tracks_100k.tck ] || { echo "skip $S"; exit 0; }
{
mrconvert $C/b0.mif $T/b0_v3.nii.gz -force -quiet
flirt -in $T2 -ref $T/b0_v3.nii.gz -out $T/T2_in_b0_v3.nii.gz -omat $T/T2_to_b0_v3.mat -dof 6 -cost mutualinfo
flirt -in $L -ref $T/b0_v3.nii.gz -out $T/label_flirt_v3.nii.gz -applyxfm -init $T/T2_to_b0_v3.mat -interp nearestneighbour
mrcalc $T/label_flirt_v3.nii.gz 1000 -gt $T/label_flirt_v3.nii.gz 834 -sub $T/label_flirt_v3.nii.gz -if $T/label_global_v3.mif -datatype uint16 -force -quiet
echo "max label: $(mrstats $T/label_global_v3.mif -output max)  nonzero voxels: $(mrstats $T/label_global_v3.mif -ignorezero -output count)"
for V in orig yflip; do tck2connectome $T/$V/tracks_100k.tck $T/label_global_v3.mif $T/$V/count_v4.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done
echo "v4 done"
} > $T/conn_v4new.log 2>&1

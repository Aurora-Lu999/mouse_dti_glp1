#!/bin/bash
ROOT=/mnt/newStor/paros/paros_WORK/aurora; E=$ROOT/eddy_ysign_test; S=$1
O=$E/glp1_tract_sc/$S; M=$E/glp1_check/$S/mask.mif; F=$O/fix
T2=/mnt/newStor/paros/paros_WORK/skull_stripping/GLP1_T2s/${S}_T2.nii.gz; LAB=$E/glp1_labeling/$S/${S}_labels_native.nii.gz
mkdir -p $F/orig $F/yflip
{
[ -f $O/b0_corr.nii.gz ] && [ -f $M ] && [ -f $O/orig/tracks_100k.tck ] && [ -f $O/yflip/tracks_100k.tck ] && [ -f $T2 ] && [ -f $LAB ] || { echo "## $S MISSING INPUT"; exit 1; }
mrconvert $O/b0_corr.nii.gz $F/b0_corr_s.nii.gz -strides $T2 -force -quiet
echo "strides T2: $(mrinfo -strides $T2)  b0: $(mrinfo -strides $F/b0_corr_s.nii.gz)"
flirt -in $T2 -ref $F/b0_corr_s.nii.gz -omat $F/T2_to_b0.mat -dof 6 -cost mutualinfo -out $F/T2_in_b0.nii.gz
flirt -in $LAB -ref $F/b0_corr_s.nii.gz -out $F/label_flirt.nii.gz -applyxfm -init $F/T2_to_b0.mat -interp nearestneighbour
mrcalc $F/label_flirt.nii.gz 1000 -gt $F/label_flirt.nii.gz 834 -sub $F/label_flirt.nii.gz -if $F/label_global.mif -datatype uint16 -force -quiet
for V in orig yflip; do tck2connectome $O/$V/tracks_100k.tck $F/label_global.mif $F/$V/count_shift.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done
[ -s $F/orig/count_shift.csv ] && [ -s $F/yflip/count_shift.csv ] || { echo "## $S NO CONNECTOME"; exit 1; }
NL=$(mrcalc -quiet $F/label_flirt.nii.gz 0 -gt $M -mult - | mrstats -quiet - -ignorezero -output count); NM=$(mrstats -quiet $M -ignorezero -output count)
echo "## $S done labelled_in_mask=$NL of $NM ratio=$(awk -v a=$NL -v b=$NM 'BEGIN{printf "%.3f", a/b}') diag=$(awk 'NR==1{a=$1} NR==2{b=$2} NR==3{c=$3} END{printf "%.3f %.3f %.3f", a,b,c}' $F/T2_to_b0.mat)"
} > $F/label.log 2>&1

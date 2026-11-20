#!/bin/bash
ROOT=/mnt/newStor/paros/paros_WORK/aurora; E=$ROOT/eddy_ysign_test; S=$1
O=$E/ctrl_tract_sc/$S; D=$ROOT/diffusion_control_batch_corrected/$S
T2=$ROOT/data/GLP_1/control_niis/T2/${S}_T2_bfc.nii.gz; LAB=$D/${S}_labels_BFCspace.nii.gz; OLD=$D/${S}_labels_in_lowb_corrected.nii.gz
{
[ -f $O/b0_corr.nii.gz ] && [ -f $O/mask.mif ] && [ -f $O/orig/tracks_100k.tck ] && [ -f $O/yflip/tracks_100k.tck ] && [ -f $T2 ] && [ -f $LAB ] && [ -f $OLD ] || { echo "## $S MISSING INPUT"; exit 1; }
mrconvert $O/b0_corr.nii.gz $O/b0_corr_s.nii.gz -strides $T2 -force -quiet
echo "strides T2: $(mrinfo -strides $T2)  b0: $(mrinfo -strides $O/b0_corr_s.nii.gz)"
flirt -in $T2 -ref $O/b0_corr_s.nii.gz -omat $O/T2_to_b0.mat -dof 6 -cost mutualinfo -out $O/T2_in_b0.nii.gz
flirt -in $LAB -ref $O/b0_corr_s.nii.gz -out $O/label_flirt.nii.gz -applyxfm -init $O/T2_to_b0.mat -interp nearestneighbour
mrcalc $O/label_flirt.nii.gz 1000 -gt $O/label_flirt.nii.gz 834 -sub $O/label_flirt.nii.gz -if $O/label_global.mif -datatype uint16 -force -quiet
for V in orig yflip; do tck2connectome $O/$V/tracks_100k.tck $O/label_global.mif $O/$V/count_shift.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done
[ -s $O/orig/count_shift.csv ] && [ -s $O/yflip/count_shift.csv ] || { echo "## $S NO CONNECTOME"; exit 1; }
NL=$(mrcalc -quiet $O/label_flirt.nii.gz 0 -gt $O/mask.mif -mult - | mrstats -quiet - -ignorezero -output count)
NS=$(mrcalc -quiet $O/label_flirt.nii.gz $OLD -eq $O/label_flirt.nii.gz 0 -gt -mult $O/mask.mif -mult - | mrstats -quiet - -ignorezero -output count)
echo "## $S done labelled_in_mask=$NL same_as_old=$NS ratio=$(awk -v a=$NS -v b=$NL 'BEGIN{printf "%.3f", a/b}') diag=$(awk 'NR==1{a=$1} NR==2{b=$2} NR==3{c=$3} END{printf "%.3f %.3f %.3f", a,b,c}' $O/T2_to_b0.mat)"
} > $O/label.log 2>&1

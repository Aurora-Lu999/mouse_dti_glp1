#!/bin/bash
ROOT=/mnt/newStor/paros/paros_WORK/aurora; E=$ROOT/eddy_ysign_test
S=$1; SRC=$E/glp1_check/$S; O=$E/glp1_tract_sc/$S
T2=/mnt/newStor/paros/paros_WORK/skull_stripping/GLP1_T2s/${S}_T2.nii.gz
LAB=$E/glp1_labeling/$S/${S}_labels_native.nii.gz
mkdir -p $O/orig $O/yflip
{
echo "## $S start $(date +%H:%M:%S)"
[ -f $E/eddy_sc/$S/corr.nii.gz ] && [ -f $E/eddy_sc/$S/grad_orig.b ] && [ -f $SRC/mask.mif ] && [ -f $LAB ] || { echo "MISSING INPUT"; exit 0; }
mrconvert $E/eddy_sc/$S/corr.nii.gz $O/corr.mif -grad $E/eddy_sc/$S/grad_orig.b -force -quiet
awk '/^#/{print;next} NF==4{printf "%.8f %.8f %.8f %.8f\n",$1,-$2,$3,$4;next} {print}' $E/eddy_sc/$S/grad_orig.b > $O/grad_yflip.b
mrconvert $O/corr.mif $O/dwi_yflip.mif -grad $O/grad_yflip.b -force -quiet
for V in orig yflip; do (
  DWI=$O/corr.mif; [ $V = yflip ] && DWI=$O/dwi_yflip.mif
  dwi2response tournier $DWI $O/$V/response.txt -mask $SRC/mask.mif -nthreads 8 -force -quiet
  dwi2fod csd $DWI $O/$V/response.txt $O/$V/fod.mif -mask $SRC/mask.mif -nthreads 8 -force -quiet
  tckgen $O/$V/fod.mif $O/$V/tracks_100k.tck -algorithm iFOD2 -seed_image $SRC/mask.mif -mask $SRC/mask.mif -select 100000 -cutoff 0.1 -minlength 0.5 -maxlength 80 -nthreads 8 -force -quiet
) & done
wait
dwiextract $O/corr.mif $O/b0vols.mif -bzero -config BZeroThreshold 50 -force -quiet
mrmath $O/b0vols.mif mean $O/b0_corr.nii.gz -axis 3 -force -quiet
flirt -in $T2 -ref $O/b0_corr.nii.gz -omat $O/T2_to_b0.mat -dof 6 -cost mutualinfo -out $O/T2_in_b0.nii.gz
flirt -in $LAB -ref $O/b0_corr.nii.gz -out $O/label_flirt.nii.gz -applyxfm -init $O/T2_to_b0.mat -interp nearestneighbour
mrcalc $O/label_flirt.nii.gz 1000 -gt $O/label_flirt.nii.gz 834 -sub $O/label_flirt.nii.gz -if $O/label_global.mif -datatype uint16 -force -quiet
for V in orig yflip; do tck2connectome $O/$V/tracks_100k.tck $O/label_global.mif $O/$V/count_shift.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done
echo "## $S done $(date +%H:%M:%S)"
} > $O/run.log 2>&1

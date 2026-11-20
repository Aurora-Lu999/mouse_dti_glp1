#!/bin/bash
ROOT=/mnt/newStor/paros/paros_WORK/aurora; E=$ROOT/eddy_ysign_test; S=$1
for d in $ROOT/eddy_cohort/$S $HOME/eddy_test/$S; do [ -f $d/mask.nii.gz ] && { SRC=$d; break; }; done
O=$E/ctrl_tract_sc/$S
T2=$ROOT/data/GLP_1/control_niis/T2/${S}_T2_bfc.nii.gz
LAB=$ROOT/diffusion_control_batch_corrected/$S/${S}_labels_BFCspace.nii.gz
mkdir -p $O/orig $O/yflip
{
echo "## $S start $(date +%H:%M:%S)"
[ -n "$SRC" ] && [ -f $E/ctrl_sc/$S/corr.nii.gz ] && [ -f $E/ctrl_sc/$S/grad_orig.b ] && [ -f $T2 ] && [ -f $LAB ] || { echo "MISSING INPUT"; exit 1; }
echo "T2: $(mrinfo -size -spacing $T2 | tr '\n' ' ')"
echo "LAB: $(mrinfo -size -spacing $LAB | tr '\n' ' ')"
mrcalc $SRC/mask.nii.gz 0.5 -gt $O/mask.mif -datatype uint8 -force -quiet
mrconvert $E/ctrl_sc/$S/corr.nii.gz $O/corr.mif -grad $E/ctrl_sc/$S/grad_orig.b -force -quiet
awk '/^#/{print;next} NF==4{printf "%.8f %.8f %.8f %.8f\n",$1,-$2,$3,$4;next} {print}' $E/ctrl_sc/$S/grad_orig.b > $O/grad_yflip.b
mrconvert $O/corr.mif $O/dwi_yflip.mif -grad $O/grad_yflip.b -force -quiet
for V in orig yflip; do (
  DWI=$O/corr.mif; [ $V = yflip ] && DWI=$O/dwi_yflip.mif
  dwi2response tournier $DWI $O/$V/response.txt -mask $O/mask.mif -nthreads 8 -force -quiet
  dwi2fod csd $DWI $O/$V/response.txt $O/$V/fod.mif -mask $O/mask.mif -nthreads 8 -force -quiet
  tckgen $O/$V/fod.mif $O/$V/tracks_100k.tck -algorithm iFOD2 -seed_image $O/mask.mif -mask $O/mask.mif -select 100000 -cutoff 0.1 -minlength 0.5 -maxlength 80 -nthreads 8 -force -quiet
) & done
wait
dwiextract $O/corr.mif $O/b0vols.mif -bzero -config BZeroThreshold 50 -force -quiet
mrmath $O/b0vols.mif mean $O/b0_corr.nii.gz -axis 3 -force -quiet
flirt -in $T2 -ref $O/b0_corr.nii.gz -omat $O/T2_to_b0.mat -dof 6 -cost mutualinfo -out $O/T2_in_b0.nii.gz
flirt -in $LAB -ref $O/b0_corr.nii.gz -out $O/label_flirt.nii.gz -applyxfm -init $O/T2_to_b0.mat -interp nearestneighbour
mrcalc $O/label_flirt.nii.gz 1000 -gt $O/label_flirt.nii.gz 834 -sub $O/label_flirt.nii.gz -if $O/label_global.mif -datatype uint16 -force -quiet
for V in orig yflip; do tck2connectome $O/$V/tracks_100k.tck $O/label_global.mif $O/$V/count_shift.csv -symmetric -zero_diagonal -assignment_radial_search 1 -force -quiet; done
[ -s $O/orig/count_shift.csv ] && [ -s $O/yflip/count_shift.csv ] || { echo "NO CONNECTOME"; exit 1; }
echo "## $S done $(date +%H:%M:%S)"
} > $O/run.log 2>&1

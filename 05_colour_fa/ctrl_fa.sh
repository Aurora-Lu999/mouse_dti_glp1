#!/bin/bash
R=/mnt/newStor/paros/paros_WORK/aurora; E=$R/eddy_ysign_test; S=$1; O=$E/fa_ctrl/$S
for d in $R/eddy_cohort/$S $HOME/eddy_test/$S; do [ -f $d/mask.nii.gz ] && { MK=$d/mask.nii.gz; break; }; done
[ -n "$MK" ] && [ -f $E/ctrl_sc/$S/corr.nii.gz ] || { echo "$S MISSING"; exit 1; }
mkdir -p $O; rm -f $O/V1b_sc.nii.gz
awk '!/^#/ && NF>=4 {printf "%.6f %.6f %.6f %.6f\n",$1,-$2,$3,$4}' $E/ctrl_sc/$S/grad_orig.b > $O/grad_ycorr_sc.b
mrconvert $E/ctrl_sc/$S/corr.nii.gz $O/dwi_sc.mif -grad $O/grad_ycorr_sc.b -force -quiet
dwi2tensor $O/dwi_sc.mif $O/dt_sc.mif -mask $MK -force -quiet
tensor2metric $O/dt_sc.mif -fa $O/FA_sc.nii.gz -vector $O/V1_sc.nii.gz -mask $MK -force -quiet
mrcalc $O/V1_sc.nii.gz $O/FA_sc.nii.gz -mult 2.5 -mult 1 -min $O/V1b_sc.nii.gz -force -quiet
echo $MK > $O/mask_path.txt
[ -s $O/V1b_sc.nii.gz ] && echo "$S ok" || echo "$S FAILED"

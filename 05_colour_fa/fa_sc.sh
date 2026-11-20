#!/bin/bash
cd /mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test
for S in $(ls eddy_sc | grep -E '^B[0-9]{8}$'); do
  IN=glp1_check/$S/eddy; O=fa_check/$S; mkdir -p $O
  rm -f $O/V1b_sc.nii.gz
  awk '!/^#/ && NF>=4 {printf "%.6f %.6f %.6f %.6f\n",$1,-$2,$3,$4}' eddy_sc/$S/grad_orig.b > $O/grad_ycorr_sc.b
  mrconvert eddy_sc/$S/corr.nii.gz $O/dwi_sc.mif -grad $O/grad_ycorr_sc.b -force -quiet
  dwi2tensor $O/dwi_sc.mif $O/dt_sc.mif -mask $IN/mask.nii.gz -force -quiet
  tensor2metric $O/dt_sc.mif -fa $O/FA_sc.nii.gz -vector $O/V1_sc.nii.gz -mask $IN/mask.nii.gz -force -quiet
  mrcalc $O/V1_sc.nii.gz $O/FA_sc.nii.gz -mult 2.5 -mult 1 -min $O/V1b_sc.nii.gz -force -quiet
  if [ -s $O/V1b_sc.nii.gz ]; then echo "$S ok"; else echo "$S FAILED"; fi
done

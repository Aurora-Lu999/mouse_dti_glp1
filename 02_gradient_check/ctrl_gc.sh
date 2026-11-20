#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
for d in /mnt/newStor/paros/paros_WORK/aurora/eddy_cohort/$S $HOME/eddy_test/$S; do
  [ -f $d/mask.nii.gz ] && { IN=$d; break; }
done
[ -n "$IN" ] && [ -f $E/ctrl_sc/$S/corr.nii.gz ] || { echo "## $S MISSING INPUT"; exit 1; }
mrconvert $E/ctrl_sc/$S/corr.nii.gz $E/gc_ctrl/$S.mif -grad $E/ctrl_sc/$S/grad_orig.b -force -quiet || { echo "## $S MRCONVERT FAILED"; exit 1; }
dwigradcheck $E/gc_ctrl/$S.mif -mask $IN/mask.nii.gz -number 10000 -nthreads 4 -force > $E/gc_ctrl/$S.txt 2>&1
[ -s $E/gc_ctrl/$S.txt ] && grep -q "scanner" $E/gc_ctrl/$S.txt || { echo "## $S NO RESULT"; exit 1; }
echo "## $S done"

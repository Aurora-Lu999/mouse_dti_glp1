#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
mrconvert $E/eddy_sc/$S/corr.nii.gz $E/gc/$S.mif -grad $E/eddy_sc/$S/grad_orig.b -force -quiet
dwigradcheck $E/gc/$S.mif -mask $E/glp1_check/$S/mask.mif -number 10000 -nthreads 4 -force > $E/gc/$S.txt 2>&1
echo "## $S done"

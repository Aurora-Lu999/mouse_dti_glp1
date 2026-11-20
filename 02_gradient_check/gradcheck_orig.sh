#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
mrconvert $E/glp1_check/$S/eddy/deg.nii.gz $E/gc_orig/$S.mif -grad $E/glp1_check/$S/eddy/grad_orig.b -force -quiet
dwigradcheck $E/gc_orig/$S.mif -mask $E/glp1_check/$S/mask.mif -number 10000 -nthreads 4 -force > $E/gc_orig/$S.txt 2>&1
echo "## $S done"

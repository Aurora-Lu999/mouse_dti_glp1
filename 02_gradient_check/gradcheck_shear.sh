cd /mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test
for S in B25123000 B26010902 B26010600; do
  for V in flip full rot; do
    mrconvert -force -quiet eddy_sc/$S/corr.nii.gz gc_shear/$S.$V.mif -grad gc_shear/$S.$V.b
    dwigradcheck gc_shear/$S.$V.mif -mask glp1_check/$S/mask.mif -number 10000 -nthreads 4 -force > gc_shear/$S.$V.txt 2>&1
    if [ $(wc -l < gc_shear/$S.$V.txt) -gt 10 ]; then echo "$S $V ok"; else echo "$S $V FAILED"; fi
  done
done

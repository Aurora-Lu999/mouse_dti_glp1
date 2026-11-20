#!/bin/bash
# usage: adc_tab.sh <mouse> <tag> <table>   -> adc_tab/<mouse>/<tag>.txt
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test
M=$1; T=$2; TAB=$3; O=$E/adc_tab/$M; mkdir -p $O
MK=$(cat $E/fa_ctrl/$M/mask_path.txt)
[ -f "$TAB" ] && [ -f "$MK" ] || { echo "$M $T MISSING"; exit 1; }
mrconvert $E/ctrl_sc/$M/corr.nii.gz $O/$T.mif -grad $TAB -force -quiet
dwi2tensor $O/$T.mif $O/${T}_dt.nii.gz -mask $MK -force -quiet
tensor2metric $O/${T}_dt.nii.gz -fa $O/${T}_fa.nii.gz -mask $MK -force -quiet
/home/aurora/.conda/envs/aurora_ants/bin/python - "$O/${T}_dt.nii.gz" "$O/${T}_fa.nii.gz" "$MK" "$M" "$T" <<'PY' | tee $O/$T.txt
import sys,numpy as np,nibabel as nib
dt,fa,mk,m,t=sys.argv[1:6]
D=nib.load(dt).get_fdata(); F=nib.load(fa).get_fdata(); K=nib.load(mk).get_fdata()>0
s=K&(F>0.2); a=[D[...,i][s].mean()*1e3 for i in range(3)]; b=[D[...,i][K].mean()*1e3 for i in range(3)]
print(m,t,'n',s.sum(),'FA>0.2 Dx Dy Dz %.3f %.3f %.3f ratio %.3f | mask %.3f %.3f %.3f'%(*a,a[1]/np.mean([a[0],a[2]]),*b))
PY

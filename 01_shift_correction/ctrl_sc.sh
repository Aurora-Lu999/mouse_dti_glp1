#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
for d in /mnt/newStor/paros/paros_WORK/aurora/eddy_cohort/$S $HOME/eddy_test/$S; do
  [ -f $d/deg.nii.gz ] && [ -f $d/mask.nii.gz ] && [ -f $d/grad_orig.b ] && { IN=$d; break; }
done
[ -n "$IN" ] || { echo "## $S MISSING INPUT"; exit 1; }
mkdir -p $E/ctrl_sc/$S
python3 $E/eddy2_sc.py $IN $E/ctrl_sc/$S sc || { echo "## $S FAILED"; exit 1; }
[ -f $E/ctrl_sc/$S/corr.nii.gz ] && [ -f $E/ctrl_sc/$S/shifts.csv ] || { echo "## $S NO OUTPUT"; exit 1; }
cp $IN/grad_orig.b $E/ctrl_sc/$S/
echo "## $S done from $IN $(date +%H:%M:%S)"

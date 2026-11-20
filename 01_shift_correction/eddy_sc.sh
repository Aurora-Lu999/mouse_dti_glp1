#!/bin/bash
E=/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test; S=$1
mkdir -p $E/eddy_sc/$S
python3 $E/eddy2_sc.py $E/glp1_check/$S/eddy $E/eddy_sc/$S sc
cp $E/glp1_check/$S/eddy/grad_orig.b $E/eddy_sc/$S/
echo "## $S done $(date +%H:%M:%S)"

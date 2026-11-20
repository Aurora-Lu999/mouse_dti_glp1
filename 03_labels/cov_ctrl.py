import os, subprocess, tempfile, numpy as np, nibabel as nib
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'; tmp=tempfile.mkdtemp()
def load(p,t):
    o=f'{tmp}/{t}.nii.gz'; subprocess.run(['mrconvert',p,'-strides','1,2,3',o,'-force','-quiet'],check=True); return nib.load(o).get_fdata()
r=[]
for m in [l.strip() for l in open(E+'/ctrl_list.txt') if l.strip()]:
    K=load(f'{E}/ctrl_tract_sc/{m}/mask.mif','k')>0; c=(load(f'{E}/ctrl_tract_sc/{m}/label_global.mif','l')>0)[K].mean(); r.append((c,m))
r.sort(); print('lowest 5:',[(m,round(c,3)) for c,m in r[:5]]); print('min %.3f median %.3f max %.3f'%(r[0][0],np.median([c for c,_ in r]),r[-1][0]))

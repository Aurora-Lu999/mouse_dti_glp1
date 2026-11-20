import os, subprocess, tempfile, numpy as np, nibabel as nib
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'; tmp=tempfile.mkdtemp()
def load(p,t):
    o=f'{tmp}/{t}.nii.gz'; subprocess.run(['mrconvert',p,'-strides','1,2,3',o,'-force','-quiet'],check=True); return nib.load(o).get_fdata()
def used(m):
    sp={'B25123002':f'{E}/glp1_tract/B25123002/label_global_v4.mif','B25123005':f'{E}/glp1_tract_sc/B25123005/label_global_v4C.mif'}
    if m in sp: return sp[m]
    for d in ('glp1_tract','glp1_tract_shift'):
        p=f'{E}/{d}/{m}/label_global_v3.mif'
        if os.path.exists(p): return p
print('mouse  coverage(used)  coverage(fixed)   [labelled voxels in mask / mask voxels]')
for m in sorted(x for x in os.listdir(E+'/fa_check') if len(x)==9 and x[0]=='B'):
    K=load(f'{E}/glp1_check/{m}/mask.mif','k')>0
    cu=(load(used(m),'u')>0)[K].mean(); cf=(load(f'{E}/glp1_tract_sc/{m}/fix/label_global.mif','f')>0)[K].mean()
    print(m,'%.3f'%cu,'%.3f'%cf)

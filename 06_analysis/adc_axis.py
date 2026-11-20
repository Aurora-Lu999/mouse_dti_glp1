import sys, subprocess, os, numpy as np, nibabel as nib
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'
print("mouse  n_FA>0.2  Dx Dy(j) Dz (FA>0.2, 1e-3 mm2/s)  Dy/mean(Dx,Dz)  | all-mask Dx Dy Dz")
for m in [l.strip() for l in open(E+'/ctrl_list.txt') if l.strip()]:
    d=f'{E}/fa_ctrl/{m}'
    if not os.path.exists(d+'/dt_sc.mif'): print(m,'MISSING'); continue
    subprocess.run(['mrconvert',d+'/dt_sc.mif',d+'/dt_sc.nii.gz','-force','-quiet'],check=True)
    T=nib.load(d+'/dt_sc.nii.gz').get_fdata()
    fa=nib.load(d+'/FA_sc.nii.gz').get_fdata()
    mk=nib.load(open(d+'/mask_path.txt').read().strip()).get_fdata()>0
    s=mk&(fa>0.2)
    a=[T[...,i][s].mean()*1e3 for i in range(3)]
    b=[T[...,i][mk].mean()*1e3 for i in range(3)]
    print(m,s.sum(),*[f'{x:.3f}' for x in a],f'{a[1]/np.mean([a[0],a[2]]):.3f}','|',*[f'{x:.3f}' for x in b])

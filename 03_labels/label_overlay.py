import os, subprocess, tempfile, numpy as np, nibabel as nib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'
G=f'{E}/glp1_tract_sc/B26010803'; tmp=tempfile.mkdtemp()
cases=[('B26010803 old label (wrong FLIRT)',f'{G}/b0_corr.nii.gz',f'{G}/label_global.mif'),
       ('B26010803 fixed FLIRT',f'{G}/b0_corr.nii.gz',f'{G}/fix/label_global.mif'),
       ('B26010803 v3 (used for GLP-1 results)',f'{G}/b0_corr.nii.gz',f'{E}/glp1_tract/B26010803/label_global_v3.mif')]
for m in ('B26062501','B26062401','B26062910'):
    d=f'{E}/ctrl_tract_sc/{m}'; cases.append((f'{m} control, fixed',f'{d}/b0_corr.nii.gz',f'{d}/label_global.mif'))
def load(p,tag):
    o=f'{tmp}/{tag}.nii.gz'
    subprocess.run(['mrconvert',p,'-strides','1,2,3',o,'-force','-quiet'],check=True)
    return nib.load(o).get_fdata()
def edges(L):
    e=np.zeros(L.shape,bool)
    e[1:,:]|=L[1:,:]!=L[:-1,:]; e[:,1:]|=L[:,1:]!=L[:,:-1]; return e
fig,ax=plt.subplots(len(cases),3,figsize=(9,2.6*len(cases)))
for r,(t,bg,lab) in enumerate(cases):
    if not (os.path.exists(bg) and os.path.exists(lab)): print('MISSING',t); [a.axis('off') for a in ax[r]]; continue
    B=load(bg,f'b{r}'); L=np.round(load(lab,f'l{r}')).astype(int)
    if B.ndim==4: B=B.mean(-1)
    ks=np.where((L>0).any((0,1)))[0]; sl=[int(np.percentile(ks,p)) for p in (30,50,70)]
    cov=(L>0).sum()/max((B>0.2*np.percentile(B[B>0],99)).sum(),1)
    print(f'{t}: slices {sl}, labelled voxels {(L>0).sum()}')
    for c,k in enumerate(sl):
        a=ax[r,c]; img=B[:,:,k]; Ls=L[:,:,k]
        a.imshow(img.T,cmap='gray',vmin=0,vmax=np.percentile(B[B>0],99),origin='lower')
        inner=edges(Ls)&(Ls>0); outer=edges((Ls>0).astype(int))
        ov=np.zeros(img.T.shape+(4,)); ov[inner.T]=[1,0.9,0,0.9]; ov[outer.T]=[1,0,0,1]
        a.imshow(ov,origin='lower'); a.set_title(f'{t}\nk={k}' if c==0 else f'k={k}',fontsize=7); a.axis('off')
plt.tight_layout(); plt.savefig(f'{E}/label_overlay.png',dpi=150); print('saved label_overlay.png')

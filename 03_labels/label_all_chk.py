import os, subprocess, tempfile, numpy as np, nibabel as nib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'; tmp=tempfile.mkdtemp()
def load(p,tag):
    o=f'{tmp}/{tag}.nii.gz'
    subprocess.run(['mrconvert',p,'-strides','1,2,3',o,'-force','-quiet'],check=True)
    return nib.load(o).get_fdata()
def used(m):
    sp={'B25123002':f'{E}/glp1_tract/B25123002/label_global_v4.mif','B25123005':f'{E}/glp1_tract_sc/B25123005/label_global_v4C.mif'}
    if m in sp: return sp[m]
    for d in ('glp1_tract','glp1_tract_shift'):
        p=f'{E}/{d}/{m}/label_global_v3.mif'
        if os.path.exists(p): return p
    return None
glp=sorted(x for x in os.listdir(E+'/fa_check') if len(x)==9 and x[0]=='B')
ctl=[l.strip() for l in open(E+'/ctrl_list.txt') if l.strip()]
print('mouse  used_vs_fixed: nlab_used nlab_fixed  Dice(label>0)  same_label_in_both')
for m in glp:
    u=used(m); f=f'{E}/glp1_tract_sc/{m}/fix/label_global.mif'
    if not (u and os.path.exists(u) and os.path.exists(f)): print(m,'MISSING',u); continue
    A=np.round(load(u,'a')).astype(int); B=np.round(load(f,'b')).astype(int)
    if A.shape!=B.shape: print(m,'SHAPE',A.shape,B.shape); continue
    a=A>0; b=B>0; both=a&b
    print(m,a.sum(),b.sum(),'%.3f'%(2*both.sum()/(a.sum()+b.sum())),'%.3f'%((A[both]==B[both]).mean()),os.path.basename(u))
cases=[(m,f'{E}/glp1_tract_sc/{m}/b0_corr.nii.gz',used(m)) for m in glp]+[(m,f'{E}/ctrl_tract_sc/{m}/b0_corr.nii.gz',f'{E}/ctrl_tract_sc/{m}/label_global.mif') for m in ctl]
nc=8; nr=(len(cases)+nc-1)//nc; fig,ax=plt.subplots(nr,nc,figsize=(nc*2.2,nr*1.9))
for a in ax.ravel(): a.axis('off')
for i,(m,bg,lab) in enumerate(cases):
    a=ax.ravel()[i]
    if not(lab and os.path.exists(bg) and os.path.exists(lab)): a.set_title(m+' MISSING',fontsize=6); continue
    B=load(bg,'bg'); L=np.round(load(lab,'lb')).astype(int)
    if B.ndim==4: B=B.mean(-1)
    k=int(np.median(np.where((L>0).any((0,1)))[0])); Ls=L[:,:,k]
    e=np.zeros(Ls.shape,bool); o=np.zeros(Ls.shape,bool)
    e[1:,:]|=Ls[1:,:]!=Ls[:-1,:]; e[:,1:]|=Ls[:,1:]!=Ls[:,:-1]; M=(Ls>0).astype(int)
    o[1:,:]|=M[1:,:]!=M[:-1,:]; o[:,1:]|=M[:,1:]!=M[:,:-1]
    a.imshow(B[:,:,k].T,cmap='gray',vmin=0,vmax=np.percentile(B[B>0],99),origin='lower')
    ov=np.zeros(Ls.T.shape+(4,)); ov[(e&(Ls>0)).T]=[1,.9,0,.6]; ov[o.T]=[1,0,0,1]; a.imshow(ov,origin='lower')
    a.set_title(f'{m} k={k}'+(' (ctrl)' if i>=len(glp) else ''),fontsize=6)
plt.tight_layout(); plt.savefig(f'{E}/label_montage.png',dpi=130); print('saved label_montage.png')

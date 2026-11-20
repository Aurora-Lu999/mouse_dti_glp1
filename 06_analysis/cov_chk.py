import numpy as np, nibabel as nib, glob, os
from scipy import stats
R='/mnt/newStor/paros/paros_WORK/aurora'; E=R+'/eddy_ysign_test'
def load(p):
    with open(p) as f: first=f.readline()
    return np.loadtxt(p, delimiter=',' if ',' in first else None)
def hom(p):
    m=load(p); return 100*sum(m[k,k+166] for k in range(166))/np.triu(m,1).sum()
def tab(p): return np.array([l.split() for l in open(p) if l.strip() and not l.startswith('#')],float)
def cov(corr,grad,mask,shifts):
    data=np.asarray(nib.load(corr).dataobj,dtype=np.float32); mk=np.asarray(nib.load(mask).dataobj)>0
    b=tab(grad)[:,3]; low=b<100; b0=data[...,low]; mean=b0.mean(-1); sd=b0.std(-1,ddof=1)
    sel=mk&(mean>np.median(mean[mk])); snr=np.median(mean[sel]/np.maximum(sd[sel],1e-6))
    ratio=np.median(data[...,~low].mean(-1)[mk]/np.maximum(mean[mk],1e-6))
    a=np.genfromtxt(shifts,delimiter=',',names=True); m=a['b']>=100
    return [snr,ratio,np.median(a['ncc'][m]),np.max(np.abs(a['C_k'])),mk.sum()]
names=['b0_snr','dw/b0','ncc','max|C|','mask_vox']
for grp in ('GLP1','CTRL'):
    rows=[];dh=[]
    for d in sorted(glob.glob(E+('/glp1_tract_sc/B2*/fix' if grp=='GLP1' else '/ctrl_tract_sc/B26*'))):
        S=d.split('/')[-2] if grp=='GLP1' else d.split('/')[-1]
        if grp=='GLP1': c=cov(f'{E}/eddy_sc/{S}/corr.nii.gz',f'{E}/eddy_sc/{S}/grad_orig.b',f'{E}/glp1_check/{S}/eddy/mask.nii.gz',f'{E}/eddy_sc/{S}/shifts.csv')
        else:
            mk=[x for x in (f'{R}/eddy_cohort/{S}/mask.nii.gz',os.path.expanduser(f'~/eddy_test/{S}/mask.nii.gz')) if os.path.exists(x)][0]
            c=cov(f'{E}/ctrl_sc/{S}/corr.nii.gz',f'{E}/ctrl_sc/{S}/grad_orig.b',mk,f'{E}/ctrl_sc/{S}/shifts.csv')
        rows.append(c); dh.append(hom(d+'/yflip/count_shift.csv')-hom(d+'/orig/count_shift.csv'))
    X=np.array(rows); dh=np.array(dh)
    print(f"\n== {grp}: n={len(dh)}")
    for i,n in enumerate(names):
        r,p=stats.spearmanr(X[:,i],dh); print(f"  {n:9s} mean {X[:,i].mean():10.3f}  range {X[:,i].min():.3f}-{X[:,i].max():.3f}   rho(delta_homo)={r:+.2f} p={p:.3f}")

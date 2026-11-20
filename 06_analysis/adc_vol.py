import numpy as np, nibabel as nib
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'
J=[('ctrl','B26062910'),('ctrl','B26062501'),('glp1','B25123000'),('glp1','B26010902')]
def fit(g,y):
    X=np.c_[g[:,0]**2,g[:,1]**2,g[:,2]**2,2*g[:,0]*g[:,1],2*g[:,0]*g[:,2],2*g[:,1]*g[:,2]]
    c=np.linalg.lstsq(X,y,rcond=None)[0]; return c
for grp,m in J:
    if grp=='ctrl':
        dwi=f'{E}/ctrl_sc/{m}/corr.nii.gz'; tab=f'{E}/fa_ctrl/{m}/grad_ycorr_sc.b'
        mk=open(f'{E}/fa_ctrl/{m}/mask_path.txt').read().strip(); fa=f'{E}/fa_ctrl/{m}/FA_sc.nii.gz'
    else:
        dwi=f'{E}/eddy_sc/{m}/corr.nii.gz'; tab=f'{E}/fa_check/{m}/grad_ycorr_sc.b'
        mk=f'{E}/glp1_check/{m}/eddy/mask.nii.gz'; fa=f'{E}/fa_check/{m}/FA_sc.nii.gz'
    D=nib.load(dwi).get_fdata(); T=np.loadtxt(tab,comments='#')
    K=nib.load(mk).get_fdata()>0; F=nib.load(fa).get_fdata()
    sel=K&(F>0.2); b=T[:,3]; b0=b<100; dw=~b0
    S0=D[...,b0].mean(-1); ok=sel&(S0>0)
    adc=[]; 
    for v in np.where(dw)[0]:
        r=D[...,v][ok]/S0[ok]; r=np.clip(r,1e-3,None)
        adc.append(np.median(-np.log(r)/(b[v]-b[b0].mean()))*1e3*1.0 if False else np.median(-np.log(r))/(b[v]-b[b0].mean())*1e3)
    adc=np.array(adc); g=T[dw,:3]; g=g/np.linalg.norm(g,axis=1,keepdims=True)
    c=fit(g,adc); r6=c[1]/np.mean([c[0],c[2]])
    order=np.argsort(-g[:,1]**2); keep=np.ones(len(adc),bool); keep[order[:5]]=False
    c2=fit(g[keep],adc[keep]); r2=c2[1]/np.mean([c2[0],c2[2]])
    top=[adc[np.argsort(-g[:,i]**2)[:5]].mean() for i in range(3)]
    res=adc-np.c_[g[:,0]**2,g[:,1]**2,g[:,2]**2,2*g[:,0]*g[:,1],2*g[:,0]*g[:,2],2*g[:,1]*g[:,2]]@c
    print(f'{m} {grp} nDW {dw.sum()} nvox {ok.sum()}')
    print('  fit Dxx Dyy Dzz %.3f %.3f %.3f ratio %.3f | without 5 largest gy^2: ratio %.3f'%(c[0],c[1],c[2],r6,r2))
    print('  mean ADC of 5 volumes closest to x/y/z axis: %.3f %.3f %.3f'%tuple(top))
    print('  gy^2 of those top-5 y volumes: %s ; max |residual| %.3f (sd of ADC %.3f)'%(np.round(np.sort(g[:,1]**2)[::-1][:5],2),np.abs(res).max(),adc.std()))

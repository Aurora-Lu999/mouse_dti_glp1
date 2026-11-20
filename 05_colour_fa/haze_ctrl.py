import os, numpy as np, nibabel as nib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
os.chdir('/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test')
mice=sorted(d for d in os.listdir('fa_ctrl') if os.path.exists(f'fa_ctrl/{d}/V1_sc.nii.gz'))
ks=[20,26,32,38,44]; meanfa={}
def fig(ms,name):
    f,ax=plt.subplots(len(ms),len(ks),figsize=(10,1.5*len(ms)))
    for r,S in enumerate(ms):
        fa=nib.load(f'fa_ctrl/{S}/FA_sc.nii.gz').get_fdata(); v1=np.abs(nib.load(f'fa_ctrl/{S}/V1_sc.nii.gz').get_fdata())
        m=nib.load(open(f'fa_ctrl/{S}/mask_path.txt').read().strip()).get_fdata()>0
        meanfa[S]=fa[fa>0].mean()
        c=np.clip(v1[...,[0,2,1]]*fa[...,None]*2.5,0,1)*m[...,None]
        for col,k in enumerate(ks):
            a=ax[r,col]; a.imshow(np.transpose(c[::-1,::-1,k,:],(1,0,2)),origin='lower'); a.axis('off'); a.set_xlim(15,115); a.set_ylim(5,80)
            if col==0: a.set_title(S,fontsize=7,loc='left')
    plt.tight_layout(); plt.savefig(name,dpi=90); plt.close(f); print('saved',name,len(ms))
fig(mice[:17],'haze_ctrl_1.png'); fig(mice[17:],'haze_ctrl_2.png')
v=np.array(list(meanfa.values())); print('control mean FA in mask: mean %.3f sd %.3f range %.3f-%.3f (n=%d)'%(v.mean(),v.std(ddof=1),v.min(),v.max(),len(v)))
g=[]
for S in sorted(d for d in os.listdir('fa_check') if d.startswith('B') and os.path.exists(f'fa_check/{d}/FA_sc.nii.gz')):
    f=nib.load(f'fa_check/{S}/FA_sc.nii.gz').get_fdata(); g.append(f[f>0].mean())
g=np.array(g); print('GLP-1 mean FA in mask: mean %.3f sd %.3f range %.3f-%.3f (n=%d)'%(g.mean(),g.std(ddof=1),g.min(),g.max(),len(g)))

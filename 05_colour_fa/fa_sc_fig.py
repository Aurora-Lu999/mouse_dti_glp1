import os, nibabel as nib, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
os.chdir('/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test')
ks=[20,26,32,38,44]
def load(S,tag): return np.abs(nib.load(f'fa_check/{S}/V1b_{tag}.nii.gz').get_fdata())[::-1,::-1][...,[0,2,1]]
def show(a,v,k):
    a.imshow(np.clip(v[:,:,k,:],0,1).transpose(1,0,2),origin='lower'); a.axis('off'); a.set_xlim(15,115); a.set_ylim(5,80)
mice=['B25123000','B26010902','B26010801']
fig,ax=plt.subplots(2*len(mice),len(ks),figsize=(12,2.2*2*len(mice)))
r=0
for S in mice:
    for tag,name in (('noscale','noscale (s0, A, C)'),('sc','s0, C')):
        v=load(S,tag)
        for c,k in enumerate(ks):
            show(ax[r,c],v,k)
            if c==0: ax[r,c].set_title(f'{S}  {name}',fontsize=7,loc='left')
        r+=1
plt.tight_layout(); plt.savefig('fa_check/colourFA_B25123000_sc_vs_noscale.png',dpi=100)
rows=[]
for S in sorted(d for d in os.listdir('fa_check') if d.startswith('B') and os.path.exists(f'fa_check/{d}/FA_sc.nii.gz')):
    f=nib.load(f'fa_check/{S}/FA_sc.nii.gz').get_fdata(); m=f[f>0]
    fn=f'fa_check/{S}/FA_noscale.nii.gz'; mn=float('nan')
    if os.path.exists(fn):
        x=nib.load(fn).get_fdata(); mn=x[x>0].mean()
    rows.append((m.mean(),mn,S))
for a,b,S in sorted(rows): print('%s  mean FA in mask: s0,C %.3f   noscale %.3f'%(S,a,b))
print('n=%d'%len(rows))

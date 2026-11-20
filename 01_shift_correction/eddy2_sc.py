import sys, os
import numpy as np, nibabel as nib
from scipy import ndimage as ndi
from scipy.optimize import minimize
ind, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
free = {'trans':[0], 'noscale':[0,1,3], 'sc':[0,3], 'full':[0,1,2,3]}[model]
os.makedirs(out, exist_ok=True)
img = nib.load(ind+'/deg.nii.gz'); data = np.asarray(img.dataobj, dtype=np.float32)
mask = np.asarray(nib.load(ind+'/mask.nii.gz').dataobj) > 0
G = np.loadtxt(ind+'/grad_orig.b'); b = G[:,3]; N = data.shape[3]
assert G.shape[0]==N
low = b < 100; ref = data[..., low].mean(-1)
nz = np.argwhere(mask); lo = np.maximum(nz.min(0)-6,0); hi = np.minimum(nz.max(0)+7, mask.shape)
sl = tuple(slice(int(lo[a]),int(hi[a])) for a in range(3))
cen = (nz.min(0)+nz.max(0))/2.0; half = np.maximum((nz.max(0)-nz.min(0))/2.0,1.0)
w = ndi.binary_dilation(mask, iterations=2)[sl]
ii,jj,kk = np.meshgrid(*[np.arange(s,dtype=np.float64) for s in ref[sl].shape], indexing='ij')
I=ii+lo[0]; J=jj+lo[1]; K=kk+lo[2]
sig=(1.0,1.0,0.5); ref_s = ndi.gaussian_filter(ref[sl].astype(np.float64), sig)
def field(p,I_,J_,K_): return p[0]+p[1]*(I_-cen[0])/half[0]+p[2]*(J_-cen[1])/half[1]+p[3]*(K_-cen[2])/half[2]
def ncc(a,c):
    a=a[w]; c=c[w]; a=a-a.mean(); c=c-c.mean(); return (a*c).sum()/np.sqrt((a*a).sum()*(c*c).sum()+1e-12)
def full(q):
    p=np.zeros(4); p[free]=q; return p
def cost(q,vs):
    s=field(full(q),I,J,K); return -ncc(ref_s, ndi.map_coordinates(vs,[ii,jj+s,kk],order=1,mode='nearest'))
params=np.zeros((N,4)); nccs=np.zeros(N); scan=np.arange(-9.0,9.01,0.5)
for n in range(N):
    vs=ndi.gaussian_filter(data[...,n][sl].astype(np.float64),sig)
    c0=[cost(np.r_[s0,np.zeros(len(free)-1)],vs) for s0 in scan]
    q0=np.r_[scan[int(np.argmin(c0))],np.zeros(len(free)-1)]
    r=minimize(cost,q0,args=(vs,),method='Powell',options={'xtol':1e-2,'ftol':1e-6,'maxiter':15})
    params[n]=full(r.x); nccs[n]=-r.fun
If,Jf,Kf=np.meshgrid(*[np.arange(s,dtype=np.float64) for s in data.shape[:3]],indexing='ij')
corr=np.zeros(data.shape,dtype=np.float32)
for n in range(N):
    s=field(params[n],If,Jf,Kf)
    corr[...,n]=np.maximum(ndi.map_coordinates(data[...,n].astype(np.float64),[If,Jf+s,Kf],order=3,mode='nearest'),0)
h=img.header.copy(); h.set_data_dtype(np.float32); nib.save(nib.Nifti1Image(corr,img.affine,h),out+'/corr.nii.gz')
with open(out+'/shifts.csv','w') as fh:
    fh.write('vol,b,gx,gy,gz,s0,A_i,B_j,C_k,ncc\n')
    for n in range(N): fh.write('%d,%.1f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n'%(n,b[n],G[n,0],G[n,1],G[n,2],*params[n],nccs[n]))
d=b>=50
print("%s %-8s mean ncc (DW) %.4f  min %.3f  max|B| %.1f max|A| %.1f max|C| %.1f"%(os.path.basename(out),model,nccs[d].mean(),nccs[d].min(),np.abs(params[d,2]).max(),np.abs(params[d,1]).max(),np.abs(params[d,3]).max()))

import numpy as np, glob, hashlib, collections
def tab(p):
    return np.array([l.split() for l in open(p) if l.strip() and not l.startswith('#')],float)
first={}
for name,gp,sp in [('GLP1','eddy_sc/B2*/grad_orig.b','eddy_sc/{}/shifts.csv'),('CTRL','ctrl_sc/B26*/grad_orig.b','ctrl_sc/{}/shifts.csv')]:
    ps=sorted(glob.glob(gp)); tabs=[tab(p) for p in ps]; ids=[p.split('/')[1] for p in ps]
    print(f"== {name}: {len(ps)} mice; table shapes {set(t.shape for t in tabs)}")
    hs=collections.defaultdict(list)
    for i,t in zip(ids,tabs): hs[hashlib.md5(np.round(t[:,:3],3).tobytes()).hexdigest()[:6]].append(i)
    print("  distinct direction tables:", {h:len(v) for h,v in hs.items()})
    t0=tabs[0]; first[name]=t0
    print("  volumes", len(t0), "b<100:", int((t0[:,3]<100).sum()), "b values (rounded to 10):", dict(collections.Counter(np.round(t0[:,3],-1))))
    bmin=[t[t[:,3]>=100,3].min() for t in tabs]; bmax=[t[:,3].max() for t in tabs]
    print(f"  DW b over mice: min {min(bmin):.0f} max {max(bmax):.0f}")
    s0=[];C=[];nc=[]
    for i in ids:
        a=np.genfromtxt(sp.format(i),delimiter=',',names=True); m=a['b']>=100
        s0.append(np.median(a['s0'][m])); C.append(np.max(np.abs(a['C_k']))); nc.append(np.median(a['ncc'][m]))
    for k,v in [('median s0 (voxels)',s0),('max|C| (voxels)',C),('median NCC (b>=100)',nc)]:
        print(f"  {k}: mean {np.mean(v):.3f}  range {np.min(v):.3f}-{np.max(v):.3f}")
a,b=first['GLP1'],first['CTRL']
if a.shape==b.shape:
    d=np.abs(a[:,:3]-b[:,:3]).max(); print(f"\nGLP1 vs CTRL first tables: same shape, max abs difference in direction columns {d:.4f}; b differs max {np.abs(a[:,3]-b[:,3]).max():.1f}")
else: print("\nfirst tables differ in shape", a.shape, b.shape)

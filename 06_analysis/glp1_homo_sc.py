import numpy as np, re, glob, os
R="/mnt/newStor/paros/paros_WORK/aurora"; E=R+"/eddy_ysign_test"
def load(p):
    rows=[[float(x) for x in re.split(r'[,\s]+',l.strip()) if x] for l in open(p) if l.strip()]
    m=np.array(rows); n=332; out=np.zeros((n,n)); k=min(n,m.shape[0]); out[:k,:k]=m[:k,:k]; return out
def P(S,V):
    r=f"{E}/glp1_tract_sc/{S}/{V}/count_v4_relabel.csv"
    return r if os.path.exists(r) else f"{E}/glp1_tract_sc/{S}/{V}/count_v4.csv"
def shares(m):
    tot=np.triu(m,1).sum()
    homo=sum(m[k,k+166] for k in range(166))
    inter=m[:166,166:].sum()
    return 100*homo/tot, 100*inter/tot, tot
print("--- formula check on controls (B26062201); earlier values: old 1.69, repeat 1.65, y flip 2.73, shift+y flip 4.46")
for d in ("diffusion_control_batch_corrected","diffusion_control_batch_origrerun","diffusion_control_batch_ycorr","diffusion_control_batch_shiftycorr"):
    for p in glob.glob(f"{R}/{d}/**/B26062201_count_v4.csv",recursive=True)[:1]:
        h,i,t=shares(load(p)); print(f"{d:40s} homotopic {h:.2f}%  interhemispheric {i:.1f}%  streamlines {t:.0f}")
print("--- GLP_1: homotopic share (%)  orig -> y flip")
rows=[]
for S in sorted(os.listdir(E+"/glp1_tract_sc")):
    try:
        a=shares(load(P(S,"orig"))); b=shares(load(P(S,"yflip")))
    except Exception as e: print(S,"ERROR",e); continue
    rows.append((S,a,b)); print(f"{S}  {a[0]:.2f} -> {b[0]:.2f}  ({'up' if b[0]>a[0] else 'down'})   interhemispheric {a[1]:.1f} -> {b[1]:.1f}")
up=sum(1 for _,a,b in rows if b[0]>a[0]); print(f"y flip higher in {up} of {len(rows)} mice; mean {np.mean([a[0] for _,a,b in rows]):.2f} -> {np.mean([b[0] for _,a,b in rows]):.2f}")
ex=[r for r in rows if r[0] not in ("B25122902","B25122903")]
print("34-volume mice only (n=%d): y flip higher in %d; mean %.2f -> %.2f" % (len(ex), sum(1 for _,a,b in ex if b[0]>a[0]), np.mean([a[0] for _,a,b in ex]), np.mean([b[0] for _,a,b in ex])))

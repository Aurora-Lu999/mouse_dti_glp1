import numpy as np, glob, os, sys
from scipy import stats
def load(p):
    with open(p) as f: first=f.readline()
    return np.loadtxt(p, delimiter=',' if ',' in first else None)
def shares(m):
    assert m.shape==(332,332), m.shape
    tot=np.triu(m,1).sum(); return 100*sum(m[k,k+166] for k in range(166))/tot, 100*m[:166,166:].sum()/tot
rows=[]
for d in sorted(glob.glob(sys.argv[1])):
    r=[d]
    for V in ('orig','yflip'): r+=list(shares(load(f'{d}/{V}/count_shift.csv')))
    rows.append(r)
n=len(rows); a=np.array([r[1] for r in rows]); b=np.array([r[3] for r in rows]); up=int((b>a).sum())
print(f"{sys.argv[1]}: n={n}; homotopic y flip higher {up}/{n}; mean {a.mean():.2f} -> {b.mean():.2f}; sign p={stats.binomtest(up,n,0.5).pvalue:.4f}")
a=np.array([r[2] for r in rows]); b=np.array([r[4] for r in rows]); print(f"   interhemispheric higher {int((b>a).sum())}/{n}; mean {a.mean():.1f} -> {b.mean():.1f}")

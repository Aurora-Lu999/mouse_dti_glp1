import numpy as np, glob, os
from scipy import stats
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test/ctrl_tract_sc'
def load(p):
    with open(p) as f: first=f.readline()
    return np.loadtxt(p, delimiter=',' if ',' in first else None)
def shares(m):
    assert m.shape==(332,332), m.shape
    tot=np.triu(m,1).sum()
    homo=sum(m[k,k+166] for k in range(166))
    inter=m[:166,166:].sum()
    return 100*homo/tot, 100*inter/tot, tot
rows=[]
for d in sorted(glob.glob(E+'/B26*')):
    S=os.path.basename(d); r=[S]
    for V in ('orig','yflip'):
        h,i,t=shares(load(f'{d}/{V}/count_shift.csv')); r+=[h,i,t]
    rows.append(r)
print("mouse  homo_orig homo_yflip | inter_orig inter_yflip | total_orig total_yflip")
for r in rows: print(f"{r[0]} {r[1]:.2f} {r[4]:.2f} | {r[2]:.1f} {r[5]:.1f} | {r[3]:.0f} {r[6]:.0f}")
a=np.array([r[1] for r in rows]); b=np.array([r[4] for r in rows]); n=len(rows)
up=int((b>a).sum()); print(f"\nhomotopic: y flip higher in {up}/{n}; mean {a.mean():.2f} -> {b.mean():.2f}; sign p={stats.binomtest(up,n,0.5).pvalue:.4f}; Wilcoxon p={stats.wilcoxon(a,b).pvalue:.4f}")
a=np.array([r[2] for r in rows]); b=np.array([r[5] for r in rows]); up=int((b>a).sum())
print(f"interhemispheric: y flip higher in {up}/{n}; mean {a.mean():.1f} -> {b.mean():.1f}")

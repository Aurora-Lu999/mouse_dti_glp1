import numpy as np, glob, sys
def load(p):
    with open(p) as f: first=f.readline()
    return np.loadtxt(p, delimiter=',' if ',' in first else None)
def hom(d,V,sub=''):
    m=load(f'{d}/{sub}{V}/count_shift.csv'); return 100*sum(m[k,k+166] for k in range(166))/np.triu(m,1).sum()
for name,g in [('GLP1 fix','glp1_tract_sc/B2*/fix'),('CTRL','ctrl_tract_sc/B26*')]:
    dh=np.array([hom(d,'yflip')-hom(d,'orig') for d in sorted(glob.glob(g))])
    print(f"{name}: n={len(dh)} delta homotopic mean {dh.mean():.3f} sd {dh.std(ddof=1):.3f} min {dh.min():.2f} max {dh.max():.2f}")
print("\nmouse  orig  orig_rep | yflip yflip_rep | delta delta_rep")
D=[]
for S in sys.argv[1:]:
    d=f'ctrl_tract_sc/{S}'; o,orp,y,yrp=hom(d,'orig'),hom(d,'orig','rep/'),hom(d,'yflip'),hom(d,'yflip','rep/')
    print(f"{S} {o:.2f} {orp:.2f} | {y:.2f} {yrp:.2f} | {y-o:+.2f} {yrp-orp:+.2f}"); D+= [o-orp,y-yrp]
print(f"\nrun-to-run difference (same table, new streamlines): sd {np.std(D,ddof=1):.3f}, mean abs {np.mean(np.abs(D)):.3f}")

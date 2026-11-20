import numpy as np, re, os
E = "/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test"
def load(p):
    rows = [[float(x) for x in re.split(r'[,\s]+', l.strip()) if x] for l in open(p) if l.strip()]
    m = np.array(rows); n = 332; out = np.zeros((n, n)); k = min(n, m.shape[0]); out[:k, :k] = m[:k, :k]; return out
def shares(m):
    tot = np.triu(m, 1).sum(); homo = sum(m[k, k + 166] for k in range(166)); inter = m[:166, 166:].sum()
    return 100 * homo / tot, 100 * inter / tot, tot
def old(S):
    r = f"{E}/glp1_tract_sc/{S}/yflip/count_v4_relabel.csv"
    return r if os.path.exists(r) else f"{E}/glp1_tract_sc/{S}/yflip/count_v4.csv"
print('mouse      version         homotopic%  interhemispheric%  streamlines-in-matrix')
for S in ['B25123000', 'B26010902', 'B26010600']:
    for name, p in (('yflip (11/16)', old(S)), ('flip (rerun)', f"{E}/glp1_tract_shear/{S}/flip/count_v4.csv"), ('full J', f"{E}/glp1_tract_shear/{S}/full/count_v4.csv")):
        if not os.path.exists(p): print(S, name, 'MISSING'); continue
        h, i, t = shares(load(p)); print(f"{S}  {name:14s}  {h:6.2f}      {i:6.1f}            {t:.0f}")

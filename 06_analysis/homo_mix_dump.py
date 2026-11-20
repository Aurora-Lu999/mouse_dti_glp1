import os, numpy as np
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'
def sh(p):
    try: m=np.loadtxt(p,delimiter=',')
    except Exception: m=np.loadtxt(p)
    up=np.triu(m,1).sum(); return 100*sum(m[i,i+166] for i in range(166))/up, 100*m[:166,166:].sum()/up
def path(m,v):
    if m in ('B25123002','B25123005'):
        for n in ('count_v4_relabel.csv','count_v4.csv'):
            p=f'{E}/glp1_tract_sc/{m}/{v}/{n}'
            if os.path.exists(p): return p
    return f'{E}/glp1_tract_sc/{m}/fix/{v}/count_shift.csv'
print('mouse,homo_orig,homo_yflip,inter_orig,inter_yflip')
for m in sorted(x for x in os.listdir(E+'/fa_check') if len(x)==9 and x[0]=='B'):
    o=sh(path(m,'orig')); y=sh(path(m,'yflip')); print(f'{m},{o[0]:.3f},{y[0]:.3f},{o[1]:.2f},{y[1]:.2f}')

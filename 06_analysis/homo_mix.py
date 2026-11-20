import os, numpy as np
from scipy.stats import binomtest
E='/mnt/newStor/paros/paros_WORK/aurora/eddy_ysign_test'
def sh(p):
    try: m=np.loadtxt(p,delimiter=',')
    except Exception: m=np.loadtxt(p)
    up=np.triu(m,1).sum(); return 100*sum(m[i,i+166] for i in range(166))/up, 100*m[:166,166:].sum()/up
def fixed(m,v): return f'{E}/glp1_tract_sc/{m}/fix/{v}/count_shift.csv'
def usedp(m,v):
    for n in ('count_v4_relabel.csv','count_v4.csv'):
        p=f'{E}/glp1_tract_sc/{m}/{v}/{n}'
        if os.path.exists(p): return p
glp=sorted(x for x in os.listdir(E+'/fa_check') if len(x)==9 and x[0]=='B'); bad=['B25123002','B25123005']
def rep(name,get):
    H=[];I=[];ms=[]
    for m in glp:
        o,y=get(m,'orig'),get(m,'yflip')
        if not(o and y and os.path.exists(o) and os.path.exists(y)): print(name,m,'MISSING'); continue
        H.append((sh(o)[0],sh(y)[0])); I.append((sh(o)[1],sh(y)[1])); ms.append(m)
    H=np.array(H);I=np.array(I);n=len(ms);up=(H[:,1]>H[:,0]).sum();ui=(I[:,1]>I[:,0]).sum()
    print(f'{name}: n={n} homotopic up {up}/{n} mean {H[:,0].mean():.2f} -> {H[:,1].mean():.2f} (sign p {binomtest(up,n,.5).pvalue:.4f}) | interhemi up {ui}/{n} mean {I[:,0].mean():.1f} -> {I[:,1].mean():.1f}')
    return dict(zip(ms,H))
a=rep('A all 23 fixed',fixed)
b=rep('B 21 fixed + 2 used',lambda m,v:(usedp(m,v) if m in bad else fixed(m,v)))
c=rep('C 21 fixed only',lambda m,v:None if m in bad else fixed(m,v))
print('per mouse homotopic orig -> yflip:')
for m in bad:
    ud=[sh(usedp(m,v))[0] for v in('orig','yflip')]
    print(m,'fixed %.2f -> %.2f | used %.2f -> %.2f'%(*a[m],*ud),os.path.basename(usedp(m,'yflip')))

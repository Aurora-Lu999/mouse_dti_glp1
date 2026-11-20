import os, sys, subprocess, csv, math
import numpy as np, nibabel as nib
res = []
for S in sorted(x for x in os.listdir('eddy_sc') if os.path.exists('eddy_sc/%s/corr.nii.gz' % x)):
    d = nib.load('eddy_sc/%s/corr.nii.gz' % S).get_fdata()
    mp = '/tmp/mask_%s.nii.gz' % S
    subprocess.run(['mrconvert', '-force', '-quiet', 'glp1_check/%s/mask.mif' % S, mp], check=True)
    m = nib.load(mp).get_fdata() > 0
    if m.shape != d.shape[:3]:
        print(S, 'MASK SHAPE MISMATCH', m.shape, d.shape); continue
    rows = list(csv.DictReader(open('eddy_sc/%s/shifts.csv' % S)))
    b = np.array([float(r['b']) for r in rows]); C = np.array([float(r['C_k']) for r in rows])
    ks = np.where(m.any(axis=(0, 1)))[0]; hk = (ks.max() - ks.min()) / 2.0
    Cdw = np.abs(C[b >= 100])
    ang = lambda c: math.degrees(math.atan(c * 0.125 / (hk * 0.3)))
    b0 = d[..., b < 100].mean(axis=3)
    bg = d[:16, :16, :, :][..., b < 100].std() + 0  # corner background, all b0 volumes
    bg2 = d[-16:, -16:, :, :][..., b < 100].std()
    noise = min(bg, bg2)
    snr = b0[m].mean() / noise
    res.append((S, hk, Cdw.mean(), Cdw.max(), ang(Cdw.mean()), ang(Cdw.max()), snr))
w = csv.writer(open('shear_snr.csv', 'w')); w.writerow(['mouse','hk','C_mean','C_max','ang_mean_deg','ang_max_deg','SNR_b0'])
for r in res: w.writerow([r[0]] + ['%.3f' % x for x in r[1:]])
print('mouse hk Cmean Cmax angmean angmax SNR')
for r in sorted(res, key=lambda r: r[6]): print(r[0], *['%.2f' % x for x in r[1:]])

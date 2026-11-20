import os, csv, subprocess, numpy as np, nibabel as nib
res = []
for S in sorted(d for d in os.listdir('eddy_sc') if os.path.exists('eddy_sc/%s/corr.nii.gz' % d)):
    d = nib.load('eddy_sc/%s/corr.nii.gz' % S).get_fdata()
    subprocess.run(['mrconvert', '-force', '-quiet', 'glp1_check/%s/mask.mif' % S, '/tmp/m_%s.nii.gz' % S], check=True)
    m = nib.load('/tmp/m_%s.nii.gz' % S).get_fdata() > 0
    b = np.array([float(r['b']) for r in csv.DictReader(open('eddy_sc/%s/shifts.csv' % S))])
    v = d[..., b < 100]; mean = v.mean(axis=3); sd = v.std(axis=3, ddof=1)
    sel = m & (mean > np.median(mean[m]))
    res.append((S, np.median(mean[sel] / np.maximum(sd[sel], 1e-6)), mean[sel].mean(), int(b[b < 100].size)))
print('mouse  SNR_b0 (median over bright mask voxels of mean/sd across b0 volumes)  mean_b0  n_b0')
for r in sorted(res, key=lambda r: r[1]): print(r[0], '%.1f' % r[1], '%.0f' % r[2], r[3])

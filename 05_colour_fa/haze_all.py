import os, subprocess, numpy as np, nibabel as nib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
mice = sorted(d for d in os.listdir('eddy_sc') if os.path.exists('fa_check/%s/V1_sc.nii.gz' % d))
mice = ['B25123000'] + [m for m in mice if m != 'B25123000']
ks = [20, 26, 32, 38, 44]
fig, ax = plt.subplots(len(mice), len(ks), figsize=(10, 1.5 * len(mice)))
for r, S in enumerate(mice):
    fa = nib.load('fa_check/%s/FA_sc.nii.gz' % S).get_fdata(); v1 = np.abs(nib.load('fa_check/%s/V1_sc.nii.gz' % S).get_fdata())
    subprocess.run(['mrconvert', '-force', '-quiet', 'glp1_check/%s/mask.mif' % S, '/tmp/m_%s.nii.gz' % S], check=True)
    m = nib.load('/tmp/m_%s.nii.gz' % S).get_fdata() > 0
    c = np.clip(v1[..., [0, 2, 1]] * fa[..., None] * 2.5, 0, 1) * m[..., None]
    for col, k in enumerate(ks):
        a = ax[r, col]; a.imshow(np.transpose(c[::-1, ::-1, k, :], (1, 0, 2)), origin='lower'); a.axis('off'); a.set_xlim(15, 115); a.set_ylim(5, 80)
        if col == 0: a.set_title(S, fontsize=7, loc='left')
plt.tight_layout(); plt.savefig('haze_all23.png', dpi=90); print('saved haze_all23.png', len(mice))

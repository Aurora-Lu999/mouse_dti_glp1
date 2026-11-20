import numpy as np, nibabel as nib, os
from scipy.ndimage import binary_erosion
print('mouse  all  k_third1 k_third2 k_third3  shell(outer3) core')
for S in sorted(d for d in os.listdir('fa_ctrl') if os.path.exists('fa_ctrl/%s/V1_sc.nii.gz' % d)):
    fa = nib.load('fa_ctrl/%s/FA_sc.nii.gz' % S).get_fdata()
    v1 = nib.load('fa_ctrl/%s/V1_sc.nii.gz' % S).get_fdata()
    m = nib.load(open('fa_ctrl/%s/mask_path.txt' % S).read().strip()).get_fdata() > 0
    assert fa.shape == m.shape and v1.shape[:3] == m.shape, (fa.shape, v1.shape, m.shape)
    sel = m & (fa > 0.2)
    alongj = np.argmax(np.abs(v1), axis=3) == 1
    ks = np.where(m.any(axis=(0, 1)))[0]; edges = np.linspace(ks.min(), ks.max() + 1, 4)
    th = []
    for a, b in zip(edges[:-1], edges[1:]):
        kk = np.zeros(m.shape, bool); kk[:, :, int(a):int(b)] = True
        q = sel & kk; th.append(alongj[q].mean() if q.any() else float('nan'))
    core = binary_erosion(m, iterations=3); shell = m & ~core
    ssh = sel & shell; sco = sel & core
    print(S, '%.2f' % alongj[sel].mean(), *['%.2f' % t for t in th], '%.2f' % alongj[ssh].mean(), '%.2f' % alongj[sco].mean(), '  n_sel', int(sel.sum()))

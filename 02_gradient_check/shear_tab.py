import sys, csv, subprocess, numpy as np, nibabel as nib
S = sys.argv[1]
rows = list(csv.DictReader(open('eddy_sc/%s/shifts.csv' % S)))
C = np.array([float(r['C_k']) for r in rows]); G = np.array([[float(r['gx']), float(r['gy']), float(r['gz'])] for r in rows])
T = [l.split() for l in open('eddy_sc/%s/grad_orig.b' % S) if l.strip() and not l.startswith('#') and len(l.split()) >= 4]
T = np.array(T, dtype=float); assert len(T) == len(rows) == 34, (len(T), len(rows))
print(S, 'table vs shifts.csv max diff (raw / y-flipped):', np.abs(T[:, :3] - G).max().round(4), np.abs(T[:, :3] * [1, -1, 1] - G).max().round(4))
subprocess.run(['mrconvert', '-force', '-quiet', 'glp1_check/%s/mask.mif' % S, '/tmp/m_%s.nii.gz' % S], check=True)
m = nib.load('/tmp/m_%s.nii.gz' % S).get_fdata() > 0
ks = np.where(m.any(axis=(0, 1)))[0]; hk = (ks.max() - ks.min()) / 2.0
F = T[:, :3] * [1, -1, 1]
full = F.copy(); rot = F.copy(); ang = []
for n in range(len(F)):
    if np.linalg.norm(F[n]) < 1e-6: continue
    t = (C[n] / hk) * 0.125 / 0.3
    J = np.eye(3); J[1, 2] = -t
    g = J @ F[n]; full[n] = g / np.linalg.norm(g)
    U, s, Vt = np.linalg.svd(J); R = U @ Vt; r = R @ F[n]; rot[n] = r / np.linalg.norm(r)
    ang.append(np.degrees(np.arccos(np.clip(full[n] @ F[n] / np.linalg.norm(F[n]), -1, 1))))
print(S, 'hk', hk, 'angle change full J: mean %.2f max %.2f deg' % (np.mean(ang), np.max(ang)))
for name, A in (('flip', F), ('full', full), ('rot', rot)):
    with open('gc_shear/%s.%s.b' % (S, name), 'w') as f:
        for g, b in zip(A, T[:, 3]): f.write('%.6f %.6f %.6f %.6f\n' % (g[0], g[1], g[2], b))

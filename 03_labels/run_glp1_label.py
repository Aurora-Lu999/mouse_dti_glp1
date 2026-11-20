import os, sys, glob, importlib.util
os.environ["WORK"] = "/mnt/newStor/paros/paros_WORK"
import numpy as np, nibabel as nib
S, MASK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
M = "/mnt/newStor/paros/paros_WORK/skull_stripping/GLP1_T2s"
cands = [p for p in glob.glob(f"{M}/{S}_T2*.nii*") if "mask" not in os.path.basename(p)]
assert cands, f"no T2 for {S}"
T2 = sorted(cands)[0]
os.makedirs(OUT, exist_ok=True)
t = nib.load(T2); m = nib.load(MASK)
print("T2:", T2, t.shape, "\nmask:", MASK, m.shape)
assert t.shape == m.shape, "T2 and mask shapes differ"
# same APflip as the control cohort: flip data along axis 1, header unchanged
t2f = f"{OUT}/{S}_T2_APflip.nii.gz"; mf = f"{OUT}/{S}_mask_APflip.nii.gz"
nib.save(nib.Nifti1Image(np.flip(np.asarray(t.dataobj, dtype=np.float32), 1).copy(), t.affine), t2f)
nib.save(nib.Nifti1Image(np.flip((np.asarray(m.dataobj) > 0).astype(np.uint8), 1).copy(), t.affine), mf)
spec = importlib.util.spec_from_file_location("ap", "/mnt/newStor/paros/paros_WORK/aurora/control_labeling/scripts/02_atlas_to_subject_debug.py")
ap = importlib.util.module_from_spec(spec); spec.loader.exec_module(ap)
ap.atlas_to_subject(study_id=S, t2_path=t2f, t2_mask_path=mf, output_dir=OUT)
lab = nib.load(f"{OUT}/{S}_T2_labels.nii.gz")
d = np.rint(np.asarray(lab.dataobj)).astype(np.int32)
def com(ids, dd, aff):
    c = np.argwhere(np.isin(dd, ids)); return nib.affines.apply_affine(aff, c.mean(0)) if len(c) else np.full(3, np.nan)
fr, ce = com([15, 1015], d, lab.affine), com([91, 1091], d, lab.affine)
print("QC (APflip space) frontal y - cerebellar y = %.2f  -> %s" % (fr[1]-ce[1], "PASS" if fr[1] > ce[1] else "CHECK"))
nat = np.flip(d, 1).copy()
nib.save(nib.Nifti1Image(nat.astype(np.int16), t.affine), f"{OUT}/{S}_labels_native.nii.gz")
L = com(list(range(1, 167)), nat, t.affine); R = com(list(range(1001, 1167)), nat, t.affine)
print("QC (native) left-right centroid diff x,y,z (mm):", np.round(R - L, 2), " labels present:", len(np.unique(nat[nat > 0])), "/332")

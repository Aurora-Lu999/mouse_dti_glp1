# Mouse DTI: shift correction, gradient-table check and connectome pipeline

Scripts used for in-vivo mouse DTI (Bruker DtiEpi, 128 x 96 x 64, 34 volumes, b = 1005-1038). Code only: no data, no atlas.
These are lab working scripts with absolute paths of our server; adapt the paths before running.

## Steps
1. `01_shift_correction`: after denoising and Gibbs removal, every DW volume is shifted along the phase-encoding axis j: s = s0 + C (k - ck) / hk, with s0 and C fitted per volume by maximising normalised cross-correlation with the mean b0 (`eddy2_sc.py`). The gradient directions are not used in the fit.
2. `02_gradient_check`: the gradient table (y flip = negate column 2) is chosen with MRtrix `dwigradcheck` (48 axis permutation and flip options, 10000 streamlines); mean streamline length is the criterion.
3. `03_labels`: atlas labels (332 regions) in T2 space are moved to b0 space with FLIRT (6 dof, mutual information). Make sure b0 and T2 have the same NIfTI strides (`mrconvert -strides`), otherwise FLIRT can fail by a 180 degree offset. Check the label coverage of the mask for every mouse (`label_all_chk.py`, `cov2.py`).
4. `04_tractography`: CSD, iFOD2, 100k streamlines, cutoff 0.1, length 0.5-80 mm, `tck2connectome -symmetric -zero_diagonal -assignment_radial_search 1`.
5. `05_colour_fa`: tensor fit with the chosen table, colour FA, principal-direction shares.
6. `06_analysis`: homotopic and interhemispheric connectome shares, group comparisons, covariate checks.

Homotopic share = sum of m[i, i+166] over the 166 region pairs / sum of the upper triangle of the 332 x 332 matrix.

## Known issues
- `04_tractography/glp1_tract_sc.sh` registers T2 to a b0 written with different NIfTI strides than the T2 (T2 -1 -2 3, b0 1 2 3). Its label step is wrong in most mice: do not use its labels or count files. `glp1_tract_shift.sh` (not included here) has the same T2-to-b0 step.
- `03_labels/glp1_label_fix.sh` adds the strides fix, but still fails on 2 of 23 mice (label coverage of the mask 0.62 and 0.69). Two mice needed their own registration (scripts not included). Always check label coverage for every mouse (`cov2.py`, `label_all_chk.py`).
- The labels used for the homotopic / interhemispheric analysis come from `glp1_conn3.sh` / `conn_v4new.sh` (FLIRT to a b0 with the same strides as the T2); their coverage of the mask was checked for all mice.
- Test / exploratory scripts (3-mouse shear-reorientation test): `gradcheck_shear.sh`, `shear_tab.py`, `glp1_tract_shear.sh`, `homo_shear.py`.
- Atlas-to-T2 registration scripts (ANTs) are not included.

## Requirements
MRtrix3, FSL, ANTs (Python), Python 3 with numpy, scipy, nibabel, matplotlib.

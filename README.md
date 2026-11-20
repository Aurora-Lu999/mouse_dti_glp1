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

## Known issue
`04_tractography/glp1_tract_sc.sh` registers T2 to a b0 written with different strides than the T2; its label step is wrong in most mice (superseded by `03_labels/glp1_label_fix.sh`, which still fails on 2 of 23 mice and needs a coverage check).

## Requirements
MRtrix3, FSL, ANTs (Python), Python 3 with numpy, scipy, nibabel, matplotlib.

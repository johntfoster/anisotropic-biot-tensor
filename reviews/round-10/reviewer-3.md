# Reviewer 3 — exposition, physical interpretation, and scientific readiness

## Reviewed object and independence

- Snapshot: `.agent-runtime/review-snapshots/round-10`.
- Snapshot ID: `69e5e45a1ca3bf0596906abf4aa91ca8aab27016da90d93594efae34d5194030`.
- PDF SHA-256: `1e352f568db8a03b034cff798df4db644857916d35fff58f5960a01a9ddb0696` (17 pages).
- I checked all 100 entries in `source-manifest.json`; every file hash agrees. The manifest hash agrees with the supplied snapshot ID.
- This is an independent simulated review of that frozen object. I read its governing instructions, author profile, vision, manuscript root, included sections, numerical evidence, and PDF. I did not read earlier reviews or other reviewers’ reports. Computation and PDF extraction used only a separate `/tmp` directory; no manuscript or snapshot files were changed.

## Required corrections

None identified within this review’s scope. The paper is scientifically ready as a theoretical constitutive study of the expressly restricted conformal, volume-only distention mechanism, supported by homogeneous numerical verification rather than experimental validation.

## Assessment

**R3-A1 — Physical argument and normalization are self-contained.** Sections 2–4, especially equations (6)–(23), distinguish intrinsic mineral stress from mixture stress, current volume from reference volume, and mineral reference volume from mixture reference volume. The factor of reference solid fraction is carried through work and energy consistently. The full stress balance, rather than its trace alone, is used to cancel pressure work. The independently differentiated energy then returns both the spherical and deviatoric stresses. This is enough to follow the construction without the companion manuscript.

**R3-A2 — Rotation and anisotropy are not conflated.** Equations (2), (6), (11), and (20), with `main.tex:262–285`, clearly state why the internal rotation disappears from an objective energy while stresses still require transformation into the mixture frame. Section 7.3 and Figure 4 distinguish a change of internal representation from a physical superposed rotation. Appendix A retains the logarithmic derivative for noncoaxial stress and strain and supplies the repeated-eigenvalue limit. The abstract’s rotation claims are supported by the body.

**R3-A3 — Constitutive restrictions are central, not hidden.** Section 4 derives the rank-one compliance restriction in equation (43) after fixing the volume-only distention energy. The paper explicitly denies arbitrary independent selection of mineral and drained stiffnesses, distinguishes spherical-strain coefficients from hydrostatic-stress moduli, and identifies pore-shape anisotropy as outside the mechanism. The cubic-mineral observation following equation (52) usefully distinguishes mineral anisotropy from directional pressure coupling. Equations (55)–(56) also prevent confusion between the pressure tangent and a finite pressure increment multiplied by the instantaneous tensor.

**R3-A4 — Numerical conclusions and limitations are appropriately stated.** Section 7 identifies synthetic parameters, homogeneous constitutive calculations, and the comparison conditions. Positivity of phase volumes, local scalar branch stability, and general deformation stability are distinguished. Section 8 does not claim measured-material calibration, universal anisotropic poroelasticity, or finite-element validation. The abstract is consistent with these limits.

## Optional improvements

**R3-O1 — Explain the mineral expansion in the isotropic constrained layer.** Location: `sections/experiments.tex:146–166`, Figure 5(c), PDF page 13. The isotropic mineral volume first falls and then exceeds one at the largest positive pressure, while the anisotropic mineral continues to contract. A short interpretation would help: the imposed pressure also drives axial skeleton extension, and the resulting deformation contribution to the mineral-volume equation can outweigh direct pressure compression. This would make the most counterintuitive plotted result more informative. The existing result is consistent with the equations and is not an error.

**R3-O2 — Make the normal directional contrast easier to see.** Location: Figure 3(a), PDF page 12; `sections/experiments.tex`, `fig:conformal-directional`. The polar curves are readable but their small departures from the isotropic circle are visually compressed by the radial scale. An inset or a companion Cartesian normal-sensitivity curve could expose the directional differences more clearly. Preserve the full polar geometry if an inset is added. This is a presentation preference, not a condition of acceptance.

## Actual verification performed

1. Extracted the embedded `conformal-2026-09-20-v1.zip` with `pdfdetach`. It is byte-identical to the snapshot ZIP. All 33 payload hashes in the supplement manifest verify. Thus availability is actual PDF-delivered access, not merely a repository-relative filename.
2. Ran all five numerical commands in the extracted README: `weighted_stress.py`, `verify_reconstruction.py`, `verify_tensor.py`, `verify_conformal.py`, and `conformal_experiments.py`. All exited successfully. No companion repository was required. The existing environment used Python 3.10.12, NumPy 1.26.4, and SciPy 1.15.3; the snapshot’s conformal report used NumPy 2.2.6.
3. Reproduced 186 conformal checks, including 67 retained conformal identities, with maximum constitutive-identity error `2.4549890331732928e-09`. Observed finite-difference orders agree with the reported second-order behavior. The tensor suite passed 273 states across 13 minerals; the reconstruction suite passed its energy, compliance, storage, work, and unjacketed checks.
4. All numeric values in the six regenerated CSV files agree exactly with the archived files, with identical categorical labels. The experiment report reproduces 1,051 state evaluations, maximum mineral residual `3.452793606584237e-14`, solid-fraction range approximately `[0.43435, 0.6]`, and minimum scalar stability value 28.
5. Read the entire extracted PDF text and visually inspected rendered pages 4, 6, 8, 11–14, and 17, including all five main figures and the long explicit Biot-tensor equation. No clipping, missing symbols, or illegible equation layout was found on these pages. The supplied build log contains no warning, overfull-box, or underfull-box entries.
6. Spot-checked the cited Gajo full text at equations (3.27), (3.32), and (3.34). Eliminating its constituent volume factors gives the stated isotropic mineral-volume equation. The manuscript correctly limits this correspondence to the volumetric law rather than asserting equivalence of the complete shear model.

## Limits of this review

I did not rebuild the LaTeX manuscript, independently reproduce every literature claim, test publisher handling of PDF attachments, or verify the companion’s public URL. The executable checks establish implementation consistency and reproducibility, not experimental correctness, global stability, strong ellipticity, or compatibility of arbitrary spatial distention fields. Those limits do not contradict the manuscript’s stated scope.

ACCEPT

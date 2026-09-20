# Independent simulated peer review — reviewer 2

## Manuscript and review scope

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work*.

**Snapshot:** `.agent-runtime/review-snapshots/round-10`, identifier
`69e5e45a1ca3bf0596906abf4aa91ca8aab27016da90d93594efae34d5194030`.

I reviewed this immutable snapshot only, without consulting earlier reviews or mutable manuscript sources. I read its local instructions, author profile, manuscript and included sections, numerical implementation, verification scripts, reports, supplement packaging code, and PDF text. I inspected rendered PDF pages 11 and 13 containing Figures 1, 2, 4, and 5. The emphasis is numerical verification, reproducibility, and readiness of the claims actually made, rather than experimental validation.

All 100 files in `source-manifest.json` matched their SHA-256 hashes. The manifest hash equals the snapshot identifier. The manuscript PDF hash is `1e352f568db8a03b034cff798df4db644857916d35fff58f5960a01a9ddb0696`.

## Overall assessment

The manuscript presents a coherent, restricted constitutive construction. It distinguishes the objective anisotropic mineral law from a volume-only distention law, derives the restriction on drained compliance, and retains the matrix-logarithm derivative needed for noncoaxial states. The numerical examples support its stated conclusions and are explicitly identified as synthetic homogeneous constitutive calculations. I found no numerical or reproducibility defect requiring correction before acceptance.

## Findings

### R2-01 — Full stress and energy verification

**Locations:** main manuscript sections 3 and 5; `sections/logarithmic_derivative.tex`; `examples/verify_conformal.py`; `examples/verify_tensor.py`.

**Classification:** Verified; no required change.

The work calculation retains the full phase-stress tensor rather than only its trace. Mineral stress is differentiated in its true frame and rotated before phase averaging. The mixture pressure potential is differentiated independently to obtain total stress. These are meaningful complementary calculations: energy differences do not merely restate the implemented stress formula. The tests include noncoaxial states, repeated stretches, arbitrary internal rotations, superposed physical rotations, and a deliberately incorrect unrotated phase-stress control.

The extracted supplement reproduced all 186 conformal checks, with maximum constitutive-identity error `2.4549890331732928e-9`. The 273-state, 13-material tensor suite also passed; its maximum componentwise energy/stress error was `9.894327579473838e-10`, and pressure-tangent error was `1.77870529416424e-9`. The observed second-order refinement rates support the derivative implementation rather than relying solely on a single finite-difference step.

I additionally evaluated 25 independently generated positive-definite mineral laws and finite deformation states, including negative pressure. This separate scratch calculation used SciPy `logm` for strain, the principal Lambert-W solution for mineral volume, and centered differences of a separately assembled energy. Maximum discrepancies were `6.66e-16` in mineral volume, `2.89e-15` in energy, and `2.35e-9` in the full Cauchy stress. A pressure finite difference gave maximum tensor error `1.20e-9`.

### R2-02 — Compliance normalization and reference response

**Locations:** `sections/stress_reconstruction.tex:167–202`, especially `eq:drained-compliance-restriction`; `sections/limits.tex`.

**Classification:** Verified; no required change.

The compliance difference uses `(phi_s0 C_s)^{-1}`, equivalently `C_s^{-1}/phi_s0`, consistent with mineral energy per reference mineral volume and skeleton energy per reference mixture volume. Its coefficient is `(1-K/(phi_s0 K_s))/(9K)`. The added strain is spherical and the rank-one restriction is not presented as a property of arbitrary independent drained/mineral stiffness pairs. The independent 25-material check reproduced this identity to a maximum Frobenius discrepancy of `8.77e-17`. The supplied reconstruction suite also passed its reference stress/storage, drained-energy, work-equivalence, isotropic, and finite unjacketed checks.

### R2-03 — Mineral root and admissible domain

**Locations:** `sections/stress_reconstruction.tex:139–150`; `examples/conformal_model.py:105–140`; `sections/experiments.tex:198–205`.

**Classification:** Verified; no required change.

The numerical root is selected on the increasing branch continuous from zero pressure. In shifted logarithmic volume, the negative-pressure turning point is handled explicitly rather than using an unconstrained fixed bracket. The checks at pressures -14 and -13 agree with the principal Lambert-W solution; the large positive-pressure check at 800 passes. Separate errors distinguish loss of scalar stability from loss of positive fluid volume. The model correctly rejects the provided -18 and -16 controls for these different reasons.

The manuscript appropriately separates this scalar local stability from stability against all deformation modes. The phase-volume restriction is explicit. No global stability, finite-element convergence, or material calibration is inferred from the numerical residuals.

### R2-04 — Reproduction from the actual PDF attachment

**Locations:** section 7.5, code/data availability paragraph; PDF attachment `conformal-2026-09-20-v1.zip`.

**Classification:** Verified; no required change.

I used `pdfdetach -saveall` on the frozen article PDF. Its single attachment is byte-identical to the snapshot ZIP, SHA-256 `cec4b5ff171ecec27c2c0d8d797afef8f0b65f79ac899b1d4b60ce4313535d4d`. All 33 payload hashes in the attachment manifest match. The archive is self-contained for the documented numerical reproduction.

From the extracted archive in a writable temporary directory I executed, in README order:

```text
python3 examples/weighted_stress.py
python3 examples/verify_reconstruction.py
python3 examples/verify_tensor.py
python3 examples/verify_conformal.py
python3 examples/conformal_experiments.py
```

All exited successfully. Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3, and Matplotlib 3.10.8 were used through the supplied dependency overlay; no source files were changed. All six conformal CSV files reproduced byte-for-byte, as did the conformal verification and experiment JSON reports. The tensor-suite numerical results also reproduce exactly; its environment metadata changes from the archived NumPy 1.26.4 to the rerun NumPy 2.2.6. The supplement explicitly records actual versions and disclaims byte-identical reproduction across environments, so this is not a scientific discrepancy.

The regenerated experiments include 1,051 recorded state evaluations, maximum mineral residual `3.45e-14`, solid fractions between approximately 0.43435 and 0.60000, and minimum scalar stability denominator 28. The constrained-layer solve enforces the specified zero axial stress. The figures distinguish the finite pressure integral from instantaneous `p B(p)` and separate internal-frame changes from physical rotation.

### R2-05 — Optional future verification extension

**Locations:** `examples/verify_conformal.py`, branch checks; section 7.5.

**Classification:** Optional; not an acceptance condition.

For future use as a general constitutive library, an automated sequence approaching the negative-pressure turning point would document conditioning of the volume and pressure derivatives as the scalar stability denominator tends to zero. The present tests establish correct branch selection at the stated states and the manuscript does not claim uniform conditioning near the boundary, so this extension is not required for the current paper.

## Limitations of this review

I did not rebuild the article with LuaLaTeX or independently audit every cited primary reference. I inspected the delivered PDF, its extraction behavior, and the frozen build log; the log search found no overfull/underfull, undefined-reference, or warning matches. Numerical reproduction used an existing supported dependency environment rather than a fresh package installation. The independent numerical checks cover a finite sample, not all admissible deformations, and do not establish experimental validity or strong ellipticity. The absent shared workflow files in the review snapshot were not replaced by reading mutable repository material.

## Required changes

None within the numerical, reproducibility, and constitutive-readiness scope of this review.

ACCEPT

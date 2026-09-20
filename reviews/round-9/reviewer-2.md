# Round 9 — Reviewer 2: numerical verification and scientific readiness

## Reviewed object and scope

Independent simulated scientific peer review of immutable snapshot `.agent-runtime/review-snapshots/round-9`, snapshot ID **1fa4b3bc4508cc6e9b9a305643bcb33ab50b748ad9ee173e2b90117c1287ec8a**. I read its AGENTS.md, author profile, VISION.md, main manuscript, included sections, numerical implementations, numerical evidence, and reproduction instructions. I extracted the text of its 17-page PDF and visually inspected the actual PDF's figure pages 11–13. No other reviewer reports or earlier review rounds were consulted. Scientific files were not edited; calculations and extraction used `/tmp/round9-reviewer2`.

All **100** entries in `source-manifest.json` passed SHA-256 verification. The manifest's own SHA-256 equals the supplied snapshot ID. Reviewed PDF SHA-256: `d524bdd6f83940484612d90f18aca3221024504c53fd4d2498567f90ab4190dd`.

## Overall assessment

The manuscript is scientifically ready within its stated scope: an elastic, homogeneous constitutive construction with anisotropy inherited from the mineral, conformal distention, and volume-only distention energy. Its central derivation preserves the complete spatial phase-stress balance, rather than identifying a tensor extension from the scalar trace alone. The rotation of intrinsic mineral stress into the mixture frame is retained correctly. The restriction on drained versus mineral compliance follows from the allowed deformation mechanism and is stated as a restriction, not as a general characterization of porous anisotropy.

The pressure-coupling tensor is consistently both the fixed-pressure pore-volume derivative and the negative fixed-deformation total-stress pressure derivative. The manuscript correctly distinguishes the finite pressure integral from multiplication by the instantaneous tensor. Reference stress/storage, the isotropic reduction, and finite unjacketed compression support the construction. Positive logarithmic elastic energy and the scalar mineral-volume condition are not overclaimed as general finite-deformation stability.

The figures demonstrate the intended effects, including shear pressure sensitivity and the difference between internal-frame changes and physical rotations. They are readable, reproducible, and explicitly synthetic. The relatively large constrained extensions are therefore constitutive illustrations, not validated predictions for an actual mineral. No experimental or finite-element validation is necessary to substantiate the narrower claims actually made here.

## Findings with stable IDs

### R9-R2-01 — Mineral root and domain: satisfactory; no required correction

**Locations:** `sections/stress_reconstruction.tex`, mineral EOS and `eq:trace-mineral-stability-domain`, especially lines 133–150; `examples/conformal_model.py:105–140`; `sections/experiments.tex:198–205`.

The positive-pressure equation is monotone. At negative pressure the implementation brackets the increasing branch continuous from zero pressure before its turning point, rejects branch loss, and separately rejects nonpositive phase volumes. These operations agree with the manuscript's local-minimum interpretation. Independent Lambert-W calculations confirmed the selected root, including near the fold with a smaller reference solid fraction that keeps the fluid volume positive. The other Lambert branch had negative scalar stability. Neither the paper nor these tests establishes stability against arbitrary deformation; the paper states this limitation clearly.

**Optional enhancement:** add a near-fold case with a low reference solid fraction to the permanent regression suite. My additional test already passes; this is additional coverage, not a defect or publication condition.

### R9-R2-02 — Stress/energy derivatives and verification independence: satisfactory; no required correction

**Locations:** `main.tex`, `eq:distention-mineral-energy-work`, `eq:anisotropic-biot-explicit`, and `eq:cauchy-pressure-tangent`; `sections/logarithmic_derivative.tex`; `examples/verify_conformal.py`; `examples/verify_tensor.py`.

The logarithmic Fréchet derivative, repeated-stretch limit, noncoaxial stresses, rotation covariance, and full tensor pressure derivative are treated consistently. The supplied finite differences evaluate energy versus phase stress separately, although some numerical helpers and the mineral solver are shared. I therefore also evaluated the energy with SciPy's matrix logarithm and an independent Lambert-W mineral root. That additional route agreed with the implementation at general finite tensor states. This is substantive implementation verification, not merely a comparison of a formula with its own rearrangement.

### R9-R2-03 — Embedded reproducibility deliverable: satisfactory; no required correction

**Locations:** `sections/experiments.tex:207–218`; PDF attachment; `tools/package_numerical_supplement.py`; embedded README and `manifest.json`.

`pdfdetach` extracted the advertised ZIP directly from the reviewed PDF. Its SHA-256 is `cec4b5ff171ecec27c2c0d8d797afef8f0b65f79ac899b1d4b60ce4313535d4d`, matching the snapshot archive. All **33 payload hashes** in its manifest passed. The extracted archive is sufficient to run the numerical commands without the companion repository. All six regenerated CSV files, including refinement data, were byte-identical to their archived counterparts in the tested environment. The stated distinction between supported dependency ranges and recorded actual versions is appropriate.

**Optional enhancement:** a separately downloadable archival supplement would improve access for readers whose PDF viewers hide attachments. Extraction with the published command already works, so this is not a required correction.

## Actual execution and numerical results

I ran the embedded archive's `weighted_stress.py`, `verify_reconstruction.py`, `verify_tensor.py`, `verify_conformal.py`, and `conformal_experiments.py`, using Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3, and Matplotlib 3.10.8. NumPy was supplied through the authorized dependency overlay; bytecode writing was disabled. All completed successfully.

- Conformal suite: **186 checks**, including 67 retained identities; maximum constitutive-identity error **2.454989e-9**. Difference-refinement orders were approximately 2; the pressure sequence ranged from 1.98915 to 2.00029.
- Tensor suite: **273 states across 13 stiffnesses**; maximum componentwise energy/phase stress discrepancy **9.89433e-10**, pressure derivative discrepancy **1.77871e-9**.
- Reconstruction suite: **20 materials**; all 20 deliberately incompatible stiffness pairs rejected. Maximum minimization discrepancy **2.72835e-9**; finite unjacketed discrepancy **5.09037e-14**.
- Figure generation: **1,051 state evaluations**, maximum mineral residual **3.45279e-14**, solid fractions between **0.4343494 and 0.6000000**, and internal/physical rotation errors below **1.71e-14**. Regeneration includes the constrained normal-stress solve.
- Additional independent calculation: **45 finite states**, random positive-definite mineral stiffnesses, pressures chosen from −1.5, 0, 4, and 200. Independent Lambert-W volumes differed by at most **8.88e-16**; independently evaluated energies by **1.78e-14**; central-difference spatial stresses by **2.15e-8**; pressure derivatives by **1.03e-8**.
- Additional fold approach: four negative-pressure states at relative distances from **1e-2 to 1e-8** from scalar branch termination, with reference solid fraction 0.1. All selected the stable branch; maximum volume discrepancy from Lambert-W was **5.15e-12**.

## Limits of this review and required corrections

No required corrections identified. I did not independently retrieve cited literature, rebuild the full TeX document, test every supported dependency version, prove global/rank-one stability, or perform an experimental or spatial boundary-value validation. The assessment of literature priority therefore remains bounded by the supplied manuscript; the numerical evidence does not substitute for citation verification. These limits do not invalidate the explicitly local theoretical and synthetic numerical claims reviewed here.

ACCEPT

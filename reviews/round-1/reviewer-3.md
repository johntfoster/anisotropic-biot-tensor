# Simulated peer review — reviewer 3, round 1

**Verdict: ACCEPT.** No substantive change is required for the claims made in this manuscript. The suggestions below are optional clarifications and verification improvements. This is a simulated JMPS-style review, not a journal editorial decision.

## Scope and evidence

I reviewed `AGENTS.md`, `VISION.md`, the full `main.tex` and `sections/experiments.tex`, both numerical scripts, the generated numerical diagnostics, and the rendered manuscript. I inspected the rendered pressure and layer figures on PDF pages 12 and 14. All five source hashes in `reviews/round-1/source-sha256.txt` verified. I applied the derivation-auditor and narrative-review guidance to this read-only scientific assessment. I did not modify manuscript or numerical source. I reran both numerical scripts using the available numerical environment; regenerating their ignored output does not alter the reviewed source snapshot.

My primary expertise assignment here is numerical correctness, reproducibility, comparison design, admissibility, and engineering interpretation. I assessed the constitutive argument directly from its definitions; I did not independently repeat a full-text historical-priority audit of every cited source.

## Assessment of the contribution

The paper's useful contribution is the connection between a mineral-volume coordinate, an operational pressure tangent, the constrained mixed elastic tangent, and the additional unjacketed volume constraint. The tensorial differentiation alone would be a relatively modest contribution. The compatibility calculation makes the paper more valuable: reproducing the classical stress coefficient while predicting an incorrect constituent volume and storage is a concrete modeling failure that the paper both exhibits and remedies. The distinction between an isolated mineral modulus and the fixed-skeleton mineral-volume tangent is physically meaningful and sufficiently explained.

The daughter-energy calculation correctly uses the constrained mineral shape. The paper does not pretend that positivity of separate daughter blocks establishes stability, or that fitting a measured Biot tensor identifies the complete coupling tensor. The finite Hencky realization is consistent with the small-strain reduction without confusing its constant logarithmic-coordinate stiffness with the spatial tangent. These distinctions prevent several otherwise serious interpretive errors.

## Numerical findings

1. **The reported verification results reproduce.** Running `examples/verify_tensor.py` gives maximum absolute errors of 7.0060710e-8 for the pressure tangent, 2.6910627e-9 for the mineral-volume derivative, 2.6076608e-10 for the total-potential gradient, and 3.9745984e-14 for the rotation check. The minimum sampled acoustic eigenvalue is 2.1065395603 in the stated stress unit, over 28 states and 103 directions per state. The manuscript's numerical statements at `sections/experiments.tex:293` accurately describe these checks.

2. **The plotted and tabulated model follows the specified energy.** The scalar residual is the derivative of the pressure potential with respect to the mineral coordinate. Its tangent is strictly positive for the pressure range used. The coaxial stress includes the correct finite-pressure contribution; the extra factor in the incremental Biot tangent is not incorrectly inserted into the finite-pressure stress increment. The independent tensor implementation includes the spectral derivative of the logarithmic strain and correctly recovers the coaxial formulas.

3. **The engineering percentages reproduce.** At p/Ks = 0.1 the full, frozen-tensor, and scalar extensions are respectively 0.3060010272, 0.2774139349, and 0.2485204193 times the original layer thickness. The lateral stresses are respectively -0.8918539059, -0.7916666667, and -0.8888888889 in the common stress unit. These values support the quoted 9.3%, 11.2%, and 18.8% differences. At p/Ks = 0.01 the extension error of the tensor approximation is approximately 0.61%.

4. **The loading problem is solved consistently for each comparator.** `finite_pressure.py:layer` solves each stress law's own zero-vertical-traction equation. This avoids estimating an approximate displacement by merely evaluating approximate stresses at the full model's deformation. An additional small-pressure check at p = 1e-5 gives ds/dp = 0.095833453 and the lateral-reaction slope -0.395833556, agreeing with the analytical limits 0.095833333 and -0.395833333. A supplementary grid over the stated scalar bracket and pressures found a positive layer residual derivative throughout; its minimum was approximately 1.26454. These supplementary samples are not a general uniqueness proof.

5. **Reproduction is practical.** The figure/table generator uses the standard library, the build hook invokes it, the tensor check has explicit dependencies and deterministic sampling, and output is kept under `build/examples/`. There is no hidden finite-element solver or inaccessible material dataset needed to reproduce the reported example.

## Comparator fairness and engineering significance

The frozen reference tensor retains the complete zero-pressure response and all reference pressure-tangent components. It is therefore a useful controlled approximation for asking how much finite-state pressure coupling matters in this particular energy. The scalar mean is a deliberately less informative comparison, and its exact calibration is stated. Neither is advertised as a complete alternative hyperelastic theory. The favorable scalar endpoint reaction is correctly identified as error cancellation rather than superior general predictive accuracy.

The example does not establish that a 9–11% correction should be expected in real rock engineering. It uses a synthetic material, large reversible strains, and p/Ks reaching 0.1. The paper explicitly says all of this, includes a smaller-pressure comparison, and avoids experimental-validation language. A homogeneous confined layer is adequate to demonstrate the boundary-condition consequence of this theoretical construction. Requiring a consolidation computation or experimental calibration would expand the paper's advertised scope rather than correct an unsupported present claim.

Physical admissibility is treated at the appropriate levels: positive mineral-branch tangent, positive phase fractions, and a separate local check of the condensed total potential. The sampled acoustic calculation is useful evidence, and the manuscript does not promote it into a global stability theorem. The paper also distinguishes the unconstrained daughter-family demonstration of mineral anisotropy from the reference-compatible model used for the engineering calculation.

## Optional improvements

- At `sections/experiments.tex:285`, qualify “independent script” as an independently implemented tensor/derivative check. The script shares material constants and the scalar root routine with `finite_pressure.py`; it is not a completely independent codebase. This does not invalidate its comparisons against energy and pressure finite differences.
- In `examples/verify_tensor.py`, future diagnostics could record the state and propagation direction attaining the smallest acoustic eigenvalue, plus Python/NumPy/SciPy versions. Those additions would make the stability sample easier to inspect across environments. The current deterministic seed and code suffice to reproduce the reported result.
- The analytical layer initial slopes are valuable and were confirmed during this review. Adding them as explicit automatic assertions would preserve this independent boundary-value check against future changes. The current manuscript values and solver are correct.
- The layer figure would be slightly easier to read if the reaction axis directly used decimal values rather than the separate 10^-2 multiplier. The current figure remains legible and unambiguous.

There are no mandatory revision requests from this review.

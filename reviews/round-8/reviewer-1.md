# Independent simulated peer review — Reviewer 1

## Reviewed version and scope

Snapshot: `round-8`  
Snapshot ID: `5ca2dd88c8341509f3b74bdc7a68c481b04362184bd816364277c435f3183925`

I verified all 95 entries in `source-manifest.json`: every file SHA-256 matches. The SHA-256 of the manifest itself equals the snapshot ID above. This review concerns only this frozen scientific version. I did not inspect earlier reviews or other reviewers' reports, and did not alter the snapshot or manuscript.

I read `main.tex`, all four included scientific sections, the author style profile, the README, the rendered 17-page `build/main.pdf`, and the relevant numerical implementation and verification evidence. I inspected rendered images of PDF pages 8 and 12 in addition to extracting the full PDF text, and checked the supplied build log for unresolved references and layout warnings. I checked the relevant local primary-source passages in Drumheller (2000), Gajo (2010), and Foster and Xu (2025). I did not independently verify every bibliographic claim or certify exhaustive novelty relative to the entire literature. The locally available Foster plasticity PDF has a different title from reference [7], so I do not count that document as verification of the cited companion version; the present derivation is self-contained and its scalar correspondence can independently be checked against Gajo.

## Overall assessment

The manuscript presents a coherent, limited constitutive construction, not a general solution for arbitrary anisotropic pore structures. Its main contribution is the connection between the complete phase-stress work, an objective anisotropic mineral energy, and the compatibility condition imposed by conformal, volume-only distention. The limitations are explicit in the introduction, derivation, numerical discussion, and conclusions. Within that scope I found no mathematical error requiring revision and no missing physical mechanism that the paper implicitly claims to supply.

The theory and its implementation evidence are sufficiently developed for publication as a theoretical constitutive paper. The numerical examples are illustrative material-point calculations rather than experimental validation, and the manuscript accurately says so. The comments below are optional improvements, not conditions of this recommendation.

## Theory checks

1. **Kinematics, frames, and weighting — equations (1)–(12), `main.tex`, section 2.** For `A = a^(1/3) R_A`, direct substitution gives `Cbar = a^(-2/3) C`. Conservation of solid mass gives `J phi_s = phi_s0 Jbar`. Consequently the current-volume-weighted Cauchy balance transforms to `tau' = phi_s0 (taubar_s + p Jbar I)` with exactly the stated reference-volume factor. The true mineral stress must be conjugated by `R_A`; simply adding its unrotated components to the mixture stress is incorrect. The paper makes this distinction consistently. Drumheller's equations (17)–(23) support the underlying multiplicative split, and his equations (118)–(119) explicitly contain the dilation-times-rotation form.

2. **Work and objectivity — equations (13)–(23), `main.tex`, section 3.** The skew rotation variation contributes no work against symmetric Kirchhoff stress. Substituting the full phase balance cancels the pressure work and leaves the mineral work with factor `phi_s0`. The integrated energy has the correct normalization. Left-rotation invariance is valid for material anisotropy because the right metric is unchanged. Thus the cancellation of `R_A` does not inadvertently assume isotropy or coaxial stress and strain. Differentiation at fixed mineral volume and at fixed skeleton deformation produces equations (21) and (22), whose combination recovers all components of equation (12). The volume-only remainder is identified as a constitutive specialization, rather than attributed to objectivity alone.

3. **Logarithmic law and drained restriction — equations (24)–(43), `sections/stress_reconstruction.tex`.** The logarithmic strain split is exact for conformal distention. The mineral volume–shape cross term in equation (35) has the correct factor. I independently differentiated this energy to obtain equation (37). Eliminating mineral volume at zero pressure gives the rank-one subtraction in equation (40); inverting it gives equation (43). The compliance difference is with the inverse of the *volume-fraction-weighted* mineral stiffness, as required. The relation is necessary and sufficient within this prescribed energy family. The definitions of `K` and `K_s` correctly distinguish spherical-strain coefficients from hydrostatic-stress moduli in anisotropy. Positive definiteness of the drained logarithmic stiffness follows from the stated parameter restriction.

4. **Finite Biot tensor and observable pressure derivative — equations (44)–(56), `main.tex`, section 5, and equations (68)–(73), appendix A.** Implicit differentiation of equation (37) gives equation (51). Applying the self-adjoint matrix-logarithm derivative yields the spatial, symmetric equation (52), including its factor of one rather than an erroneous extra factor of one-half. The repeated-eigenvalue formula is correct. The pressure Legendre transform uses the correct sign, and mixed differentiation gives `partial sigma/partial p|F = -B`. The distinction between this instantaneous tangent and multiplication by a finite pressure increment is essential and handled correctly. The pressure transformation is consistent with Foster and Xu's equations (32)–(39).

5. **Limits and scope — equations (57)–(64), `sections/limits.tex`.** The reference Biot relation and solid-storage identities follow from the same rank-one stiffness relation. Isotropic reduction removes the volume–shape term and gives the stated scalar coefficient. Eliminating Gajo's constituent factors using his equations (3.27), (3.32), and (3.34) reproduces equation (61); the manuscript appropriately limits this equivalence to the volumetric law. The finite unjacketed construction gives intrinsic and mixture Cauchy stress `-p I` and constant solid fraction even when the homogeneous mineral stretch is anisotropic. The manuscript correctly separates scalar branch stability from stability against general deformation, and does not claim global convexity of a quadratic logarithmic energy.

## Numerical and presentation checks actually performed

I copied the frozen snapshot to `/tmp/round8-reviewer1`, made only the scratch copy writable, and reran the three verification scripts with Python 3.10.12, NumPy 1.26.4, and SciPy 1.15.3. The initial scratch runs reached their output writes but inherited read-only snapshot output files; rerunning after correcting the scratch permissions completed successfully. This was a scratch-file permission issue, not a scientific test failure.

- `examples/verify_conformal.py`: all 175 checks passed; maximum constitutive-identity error `2.4535896960865923e-9`. Energy-stress and pore-volume refinement orders are essentially two; pressure refinement orders range from approximately 2.000 to 2.017. The noncoaxial commutator is nonzero (`0.18156549`), so these tests are not confined to simultaneously diagonalizable strain and stress.
- `examples/verify_tensor.py`: all 273 finite states across 13 materials passed. Maximum reported pressure-derivative error is `1.77870529416424e-9`; phase-energy stress error is `9.894327579473838e-10`.
- `examples/verify_reconstruction.py`: checks across 20 materials passed, including drained energy, compliance, reference storage, and unjacketed compression. The maximum reported minimization discrepancy is `2.728350281810954e-9`; unjacketed error is `5.090372567906343e-14`.
- I inspected the model's stress, energy, root equation, and matrix-logarithm implementation and independently evaluated selected scalar roots with the principal Lambert-W branch, identifying the optional solver limitation below.
- The frozen PDF is readable, the tensor typography distinguishes scalar and tensor quantities, and the central equation (52) is legible. The figure inspected on page 12 supports the directional-traction discussion. I found no unresolved references or relevant warnings in the supplied build log. I did not rebuild LaTeX or regenerate all figures during this review.

## Required changes

None identified for the scientific claims and demonstrated loading paths in this snapshot.

## Optional suggestions

### R1-01 — Clarify or broaden the numerical root solver's supported domain

**Severity:** Optional implementation robustness improvement; not a defect in the derivation or reproduced figures.  
**Locations:** `examples/conformal_model.py:105–114`; equation (38) and its preceding negative-pressure discussion; section 7.5.

The fixed bracket `target - 2, target + 2` can reject a positive, locally stable, physically admissible mineral-volume root. With the supplied default material, `F = I`, and `p = -13`, independent evaluation gives `ln Jbar = 0.4067876299222667`, `Jbar = 1.5019850950976001`, `phi_s = 0.9011910570585601`, and the equation (38) denominator `16.60994636217653`. The equation residual is about `-1.8e-15`, yet `Model.state` raises the Brent sign-bracket error because both chosen endpoints lie on the same side of the residual. This does not affect the nonnegative pressure paths plotted in the manuscript. For reuse outside those paths, either document the example solver's narrower supported domain or bracket the stable branch explicitly (and use an expanding bracket for nonnegative pressure). A regression check at an admissible negative-pressure state would then be useful.

### R1-02 — Specify the variable in the positive-curvature statement

**Severity:** Optional wording precision.  
**Location:** `sections/stress_reconstruction.tex`, immediately after equation (33), PDF page 5.

The distention energy has positive curvature with respect to `ln a`. Its second derivative with respect to `a` is proportional to `(1 - ln a)/a^2`, and is not everywhere positive. Writing “positive curvature in logarithmic distention” would make the existing statement exact without implying a stronger convexity property. The manuscript's later stability qualifications already prevent this from becoming a substantive scientific overclaim.

## Recommendation

The full tensor work, frame handling, compatible energy, pressure derivative, and limiting responses are consistent. The numerical verification is reproducible and appropriately characterized. Neither optional suggestion changes the main results or requires a new scientific derivation.

ACCEPT

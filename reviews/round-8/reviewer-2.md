# Reviewer 2 — independent numerical and reproducibility review

## Snapshot and scope

Reviewed snapshot **5ca2dd88c8341509f3b74bdc7a68c481b04362184bd816364277c435f3183925**. The SHA-256 of `source-manifest.json` equals that ID, and all 95 listed file hashes verified. I read the manuscript source and included sections, the 17-page PDF, numerical implementation and verification scripts, README, and conformal JSON/CSV evidence; I visually inspected the five manuscript figures on PDF pages 11–13. I did not consult other reviewers or earlier reviews. All computations and rebuilding used a writable `/tmp/biot-round8-reviewer2-mjbunzj0/snapshot` copy; the frozen snapshot and author build were not modified.

## Overall scientific assessment

The paper is scientifically coherent as a deliberately restricted, local elastic constitutive construction. Its meaningful results are the work-consistent full spatial phase balance, the rank-one compliance restriction, and the finite anisotropic pressure derivative. Internal rotation is correctly treated as a frame freedom rather than additional elastic physics. The compliance restriction and inability to represent pore-shape anisotropy with an isotropic mineral are stated clearly. The numerical experiments support the claims actually made, including noncoaxial stress/strain, shear pressure sensitivity, isotropic recovery, and the distinction between instantaneous coupling and an integrated pressure response. They do not establish experimental validity or general finite-strain stability; the manuscript explicitly acknowledges both limitations. I found no central equation, sign, normalization, or frame-factor error requiring theoretical reconstruction.

One bounded implementation-domain defect should be corrected or explicitly scoped before publication. It does not alter the reported plots or undermine the derivation.

## Checks actually performed

- Ran `verify_conformal.py`: **175 checks passed**, including 67 retained conformal identities. Maximum constitutive-identity error was **2.4535896961e-9**. Centered-difference observed orders were 2.000006–2.000393 for energy/stress, 2.000003–2.000212 for pore volume, and 1.999990–2.016717 for pressure. These substantiate Section 7.5's convergence and error statements.
- Ran `verify_reconstruction.py`: 20 random materials, all 20 deliberately incompatible stiffness pairs rejected; minimum drained stiffness eigenvalue 1.8415. Largest reported reconstruction error was 2.73e-9. Work, storage, isotropic and finite unjacketed checks passed.
- Ran `verify_tensor.py`: **273 states over 13 mineral stiffnesses** passed. Maximum phase/energy error was 9.89e-10; pressure error 1.78e-9; objectivity error 1.08e-12. This suite supplies meaningful full-tensor checks beyond a trace comparison.
- Independently implemented the mineral root with the principal Lambert-W branch and evaluated logarithmic strain using SciPy `logm`, rather than the supplied eigendecomposition/root solver. For ten seeded noncoaxial states with pressures sampled between -3 and 6, root and potential discrepancies were at most 3.34e-16 and 4.89e-15. Centered differences of that separate pressure potential gave stress within 3.21e-9; mineral-volume differences gave B within 1.60e-11. This checks Eqs. (34), (37), (49), (52), and (53) through a distinct implementation route.
- Regenerated all conformal experiments: **1,051 state evaluations**, maximum mineral residual 3.73e-14, solid fractions 0.434349–0.600000, minimum scalar-stability denominator 28. Every numeric and categorical field in the six regenerated CSV files matched the snapshot (maximum numeric difference zero). This includes the constrained-layer zero-normal-stress solve and the rotation and traction plots.
- Confirmed the Mandel normalization, K=7, Ks=28, reference solid fraction 0.6, reference B=(0.7, 0.7583333, 0.7916667), and isotropic comparison shear modulus 16.8. The isotropic comparison preserves the stated spherical and average deviatoric stiffnesses, not an independently chosen drained stiffness. Equations (43), (55), and (71) are implemented consistently.
- Regenerated `weighted_stress.py` outputs and ran the README's LuaLaTeX/latexmk command successfully: 17 pages, with no final undefined references/citations or overfull/underfull warnings. The copied snapshot lacks repository tooling files, so the README's dependency-profile helper was not run; this is a limitation of this review package, not evidence that the repository helper fails.
- Actual environments: Python 3.10.12, SciPy 1.15.3. Initial verification also passed under installed NumPy 1.26.4. The final conformal verification and figure regeneration used the supplied dependency overlay, NumPy 2.2.6 and Matplotlib 3.10.8, satisfying `examples/requirements.txt`. Build used LuaHBTeX 1.14.0 and latexmk 4.76.

## Comments

### R2-01 — fixed root bracket rejects admissible stable branches

**Severity: minor. Status: required.**

**Locations:** `examples/conformal_model.py:105–114`; `sections/stress_reconstruction.tex:139–150`, Eqs. (37)–(38); `sections/experiments.tex:193–201`.

`brentq(residual, target-2, target+2)` is not a branch-aware solution of the stated constitutive domain. With the default material, `Model().state(np.eye(3), -14.0)` raises `ValueError: f(a) and f(b) must have different signs`. Yet Eq. (37) has the zero-pressure-continuous root Jbar=1.5900473937477393, giving solid fraction 0.9540284362486435 and positive Eq. (38) denominator 15.014612951060128. Its residual is approximately 1.8e-15. Both phase volumes are positive. The bracket spans both crossings of the negative-pressure residual, so its endpoints have the same sign despite a valid stable root inside. This is an algorithmic failure, not the model's admissibility cutoff. At positive p=800, the same fixed bracket misses the unique valid root Jbar=0.12484225697035065, solid fraction 0.07490535418221038, denominator 86.25971991949697.

**Required action:** use a pressure-dependent bracket that isolates the positive-derivative branch, or an equivalent robust branch-explicit solution, with regression checks for a valid negative-pressure state, branch termination/inadmissibility, and large positive pressure. An acceptable narrower alternative is to explicitly document and enforce a restricted supported numerical domain, distinct from the wider theoretical domain. Do not present a generic bracketing exception as physical inadmissibility. All published paths lie in a successfully reproduced range, so this is a minor implementation correction, not a reason to redo the science.

### R2-02 — order the supplemental refinement-generation commands

**Severity: low. Status: optional.**

**Locations:** `README.md:24–28,45–49`; `examples/conformal_experiments.py:173–182`.

The experiment script writes `step_refinement.csv/pdf/png` only if `verification.json` already exists. A clean checkout following the README in order runs experiments before verification and therefore does not generate these supplemental refinement artifacts. The manuscript figures still build and the convergence data are subsequently available in JSON, so this does not obstruct reproducing the paper. For a complete clean-run recipe, run `verify_conformal.py` before `conformal_experiments.py`, or document a final experiment regeneration after verification.

## Recommendation

The manuscript's main theory and published numerical evidence are ready. Resolve R2-01 through a focused numerical correction or explicit implementation-domain statement; no broader theoretical revision, finite-element study, calibration exercise, or unsupported global-stability claim is needed for this paper's stated scope.

MINOR REVISION

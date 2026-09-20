# Round-16 review 3 — prose, notation, significance, and claim-versus-artifact consistency

## (1) Reviewed version, snapshot identity, integrity

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Frozen snapshot reviewed (read-only): `.agent-runtime/review-snapshots/round-16`
- Declared `SNAPSHOT_ID`: `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`
- `sha256(source-manifest.json)` computed from the snapshot **equals SNAPSHOT_ID exactly**.
- Re-hash of every path listed in `source-manifest.json`: **listed 438 ok 438 mismatch 0 missing 0**.
- Additional artifact-level integrity inside the snapshot (not part of the declared count):
  - Embedded numerical supplement `build/conformal-2026-09-20-v1.zip`: its internal `manifest.json` lists 33 payload files; **listed 33 ok 33 mismatch 0 missing 0** (the only unlisted file on disk is `manifest.json` itself, which is correct).
  - `site/evidence.json`: 23 allowlisted artifacts, **0 missing, 0 hash mismatch**.
  - `site/scientific-snapshot.json`: 33 source files, **0 missing, 0 mismatch**.
  - `fe-evidence/manifest.json`: 202 run files, **0 missing, 0 mismatch**.
- All work was done on a writable copy at `/tmp/r16rev3`; the frozen snapshot was never modified.
- Per policy, only `reviews/README.md` was read from the review area. No earlier-round report, directory listing, or verdict was consulted; prior verdicts were treated as carrying no weight.
- Manuscript shipped as `main.tex` (22 pages, `build/main.pdf` present) with sections, appendix, provenance, and bibliography.

## (2) Independent recomputation evidence

I re-ran the shipped numerical sources in the scratch copy and compared against the shipped JSON/CSV. The shipped reports reproduced exactly on every field compared.

| Re-run | Result | Matches shipped artifact |
| --- | --- | --- |
| `examples/verify_conformal.py` | `checks_passed=186`, `legacy_identities_rechecked=67`, `max_constitutive_identity_error=2.4549890331732928e-09`, `observed_orders` energy 2.0004/2.0001/2.0000/2.0000, pore-volume 2.0002/…, pressure 2.0000/2.0003/2.0003/1.9891 | `build/conformal/verification.json` — identical |
| `examples/verify_reconstruction.py` | compliance 1.388e-16, drained_energy 1.110e-15, minimization 2.728e-09, work_equivalence 5.041e-10, reference_storage 4.002e-12, 20 materials, 20 incompatible pairs rejected | `build/weighted-stress/reconstruction-verification.json` — identical |
| `examples/verify_tensor.py` | 273 states, 13 materials, 21 states/material, phase_energy 9.894e-10, pressure 1.779e-09, noncoaxial commutator 2.614 | `build/weighted-stress/tensor-verification.json` — identical |
| `examples/conformal_experiments.py` | reference_B `[0.7, 0.758333, 0.791667]`; pressure6_B `[0.7587, 0.8056, 0.8324]`; shear065 B12 `0.0144776181`; layer anisotropic `σ11=-5.18116`, `σ22=-5.35543`, isotropic `σ33` reactions equal | `build/conformal/experiments.json` — identical |

Independent arithmetic on the shipped moduli:

- `K_s = (1/9) I:ℂ_s:I = (180+2(12+10+14))/9 = 28 K_*` (stated `K_s=28K_*`). ✔
- Deviatoric eigenvalues of the shipped `ℂ_s`: `[20, 24, 28, 42.9668, 53.0332]`, mean `33.6`, half `16.8`. The stated isotropic-comparison mineral shear modulus `16.8K_*` is therefore the mean of the five deviatoric modes divided by two. ✔
- Drained Mandel shear entries = `0.6 × (20, 24, 28) = (12, 14.4, 16.8)`; the rank-one compliance term is purely spherical, as claimed. ✔
- Reference Biot components shipped as `0.7000/0.7583/0.7917`; recomputed from the shipped drained/mineral tensors. ✔
- FE reference block: `G = φ_s0 μ_s = 0.9 × 5/6 = 0.75`; `B_0 = 1 − K/K_s = 1 − 1/2.5 = 0.6`; total storage `(1−φ_s0)/K_f + (φ_s0/K_s)(1−K/(φ_s0K_s)) = 0.1/8 + 0.2 = 0.2125 = 17/80`. ✔
- `mandel-reference.json`: `M = 1/0.2125 = 4.70588…`; 38 self-checks present; central overshoot ratio `1.0546586 → 5.4659%` at `t=0.01516535`, matching the site text. ✔
- `figures/fe_load_limit.csv`: `pressure_max_normalized = 0.0032209…` for `nonlinear_load_0.0001` at `nx=20, dt=0.001`, confirming the "about `3.2×10^{-3}`" floor. ✔
- Suite contents: `verification.json` holds exactly 186 named checks, of which 5 legacy states × 13 identical identity names = 65, plus the two reference relations = 67 rechecked; categories 139 implementation / 44 analytical / 3 convergence. Matches the manuscript's description. ✔
- Figure data row counts: `pressure_response` 242, `shear_response` 322, `rotation_response` 242, `directional_response` 1083, `constrained_layer` 242 → 2×121, 2×161, 2×121, 3×361, 2×121, matching the stated 121/161/one-degree/121/121 sampling. ✔
- Site engineering: `tools/build_verification_site.py --validate-only` → `manifest valid, artifacts 23`; `python3 -m unittest discover -s site` → 12 tests OK; `tools/check_dependency_profile.py manuscript` → exit 0.
- Site claim cross-checks: 38 Mandel self-checks; 110 fluid checks with max scaled error 8.087e-9; C++/Python constitutive agreement 6.395e-14 over 41 finite states; finite-deformation family ranges (anisotropic peak 0.20618–0.21577, force 1.276e-10, mass 2.470e-10; isotropic 0.22383 / 3.214e-12; partial 0.20052–0.20163, force 2.052e-10, mass 4.636e-10) — every number quoted in the manuscript/site is present in the listed artifacts.

## (3) Findings

**Notation.** Every symbol obeys the conventions declared on page 1. Bars resolve to four declared families: kinematic/energetic mineral quantities (`\bar F, \bar C, \bar U, \bar ε, \bar W_s`, `\bar J`), intrinsic per-phase densities (`\bar ρ_s, \bar ρ_f, \bar ρ_{s0}, \bar ρ_{f0}`), the referential boundary flux (`\bar Q_f`, with the vector written `Q_f` and `Q_f·N=\bar Q_f`), and mixture-frame stress (`\bar σ_s, \bar τ_s`), with hats only for the true frame (`\hat σ_s, \hat τ_s`). Second-order tensors and vectors are upright bold; the only blackboard-bold symbols are the fourth-order stiffness/compliance tensors `ℂ_s`, `ℂ^d`. No undeclared exceptions were found. The one deliberate convention switch (current-configuration densities in §§2–5 versus reference-volume measures in the FE section) is flagged explicitly in `finite_elements.tex`.

**Prose and cross-references.** All `\eqref/\ref/\cref` targets resolve (no undefined references). All 22 citation keys resolve to `references.bib`, and all 22 bib entries are cited. Abstract, roadmap (Introduction), section scope paragraphs, and Conclusions agree on scope: the constitutive results are verified, the FE implementation is an implementation verification of the weak balances and the constant reference tangent, the finite-load rotated-anisotropy and partial-drainage runs are demonstrations, and no experimental validation is claimed. The site's category labels (`analytical`/`convergence` passed on self-checks, `finite_deformation` pending, `physical_validation` not_performed) are consistent with that scope.

- **F1 (optional).** `site/README.md` gives `python3 .agent/shared/tools/research_project.py links .agent-runtime/site`, but `.agent/shared/tools/` is absent from the snapshot (only `.agent/shared/AGENTS.shared.md` and `.agent/shared/skills/` ship). The root `README.md` explicitly qualifies the analogous absent `tools/agentctl`, but `site/README.md` does not qualify this command. It is an infrastructure instruction, not a reproduction command for any reported result, and no shipped evidence depends on it.
- **F2 (observational).** `build/weighted-stress/derivation-scan.json` and `build/weighted-stress/display-scan.json` carry a `.json` extension but are plain-text scanner output and are not parseable JSON. Nothing in the manuscript, README, or site represents them as machine-readable JSON, and the packaging script does not require them.
- **F3 (observational).** Root `README.md` says the energy is derived from the "current-volume-weighted" mineral and fluid stresses; the manuscript says "volume-fraction-weighted phase stresses". The weights are current volume fractions, so this is loose wording rather than a contradiction.
- **F4 (observational).** The manuscript states the FE discretization "reproduces the constant-coefficient consolidation reference in the constant-tangent limit", while the shipped linear spatial refinement is non-monotone at the finest level (`nx=10,20,40` → 2.083e-3, 4.577e-4, 6.364e-4 for normalised pressure error). The site records this non-monotonicity and attributes it to the initial drainage-boundary discontinuity; the manuscript explains the discontinuity mechanism but does not state the non-monotonicity itself.
- **F5 (observational).** The abstract says the implementation is "verified against a manufactured solution of the constant reference tangent and, in the same limit, the constant-coefficient consolidation reference". The site's `analytical` summary restricts its `passed` status to the reference self-checks and labels the finite-load FE comparison a demonstration. The abstract's "in the same limit" qualifier keeps this consistent with the section's own "implementation verification … of the constant reference tangent", but the wording is close enough to the site's stricter label that a reader may wish for the identical qualifier in both places.
- **F6 (observational).** `experiments.tex` describes the "two reference Biot and rank-one compliance relations used to establish the specialization"; these entries are verification checks, not steps that establish the specialization. Minor wording.

**Significance and engineering relevance.** Assessed on its own terms: the contribution is a finite-deformation anisotropic Biot tensor derived from phase-stress work under a conformal (dilation-times-rotation) distention and volume-only distention energy, together with the drained compliance restriction and the mineral-volume equation. The engineering framing (anisotropic poroelasticity in shales/cracked rock, directional pressure sensitivity, laterally constrained layers) is appropriate, and the stated restrictions — anisotropy inherited from the mineral; shape-changing distention and pore-shape anisotropy require additional constitutive mechanics; synthetic parameters; no experimental validation — are consistently repeated rather than buried. I did not infer a desired outcome.

## (4) Required corrections

None.

## (5) Optional suggestions

1. Qualify the `research_project.py` command in `site/README.md` the same way the root `README.md` qualifies `tools/agentctl` (shared-checkout tool, not shipped).
2. Either rename the two plain-text `build/weighted-stress/*-scan.json` files to a non-JSON extension or emit valid JSON, to avoid a misleading extension.
3. Make the abstract's description of the consolidation-reference comparison exactly parallel to the site's category wording (`analytical` = reference self-checks; FE comparison = implementation verification/demonstration), so the two labels cannot be read as divergent.
4. Consider stating the non-monotone linear spatial refinement (and its drainage-boundary explanation) in the FE scope paragraph, since the site already reports it.
5. Harmonise "current-volume-weighted" (README) with the manuscript's "volume-fraction-weighted".

## (6) Review limitations

- I verified the frozen snapshot only; I did not consult any other round's reports, and prior-round verdicts were deliberately excluded.
- The MOOSE finite-element runs were not re-executed (no MOOSE build/solver in this review environment); FE claims were checked against the shipped per-run `analysis.json`, `reference_comparison.csv`, `fe-evidence/manifest.json` digests, figures, and the site evidence manifest, not against a fresh solve.
- The manuscript PDF was not rebuilt from source in this pass; `build/main.pdf` and `build/main.log` were inspected as shipped (single Underfull hbox, no overfull/undefined-reference warnings, 22 pages).
- Physical/numerical fidelity of the derivations and of the FE discretization is outside this reviewer's charge and was not adjudicated here; this report is limited to prose, notation, significance framing, and claim-versus-artifact consistency.

VERDICT: ACCEPT

# Round-15 independent review 1 — mathematics and correctness

## (1) Reviewed version, snapshot identity, integrity

Snapshot root (read-only):
`/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-15`

Writable copy used for all work: `cp -r <snapshot> /tmp/r15rev1 && chmod -R u+w /tmp/r15rev1`

```
$ cat SNAPSHOT_ID
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617
$ sha256sum source-manifest.json
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617  source-manifest.json
```

Manifest matches SNAPSHOT_ID. Every path in `source-manifest.json` re-hashed (sha256 over file bytes):

```
listed 438 ok 438 mismatch 0 missing 0
```

**Integrity: PASS** (438/438 listed files present and hash-exact). No other reviewer's report or prior round was read; the only file consulted under `reviews/` was skipped entirely (policy file only).

Scope of this charge: derivations, constitutive law and its `moose_app/` implementation, manufactured-solution forcing and observed orders, assembled-Jacobian step study, discrete conservation/force identities, and every numeric claim in the manuscript and evidence files.

## (2) Independent recomputation evidence

All commands below were run inside `/tmp/r15rev1` with `conda activate moose`. Nothing was written outside the copy except this report.

### 2.1 Derivations re-derived by hand (symbolic, no tooling)

Performed in full, not sampled:

* **Conformal kinematics.** `F = A F̄`, `A = a^{1/3} R_A`, `F̄ = a^{-1/3} R_A^T F`; `C̄ = F̄^T F̄ = a^{-2/3} C`. Verified by substitution.
* **Mineral-volume EOS (eq. `anisotropic-mineral-eos`).** Differentiating the prescribed energy `W_s = W_A(a) + φ_{s0} W̄_s(F̄)` at fixed `F` and using `∂W_A/∂ln a = tr τ'/3` reproduces exactly
  `0 = K_s ln J̄ + (1−K/(φ_{s0}K_s)) p J̄ − (K/φ_{s0}) ln J + (1/3)(1−K/(φ_{s0}K_s)) I:C_s:dev ε`.
  I checked the two cancellations that make it work: `K/φ + αK_s = K_s` and `K_s − K/φ = αK_s` with `α = 1−K/(φ_{s0}K_s)`. The algebra closes term by term.
* **Distention energy.** `∂W_A/∂ln a = K ln J` on the spherical drained path, and `ln a = (1−K/(φ_{s0}K_s)) ln J`, integrates to `W_A = K (ln a)^2 / [2(1−K/(φ_{s0}K_s))]` — eq. `distention-energy`.
* **Drained stiffness / compliance.** The stated `C^d = φ_{s0}C_s − φ_{s0}α/(9K_s)(C_s:I)⊗(C_s:I)` inverts in closed form to
  `(C^d)^{-1} = (φ_{s0}C_s)^{-1} + α/(9K) I⊗I`, using `(C_s:I):C_s^{-1}:I = 9K_s` and `α/(1−α)·1/(φ_{s0}K_s) = 1/K`. This is exactly eq. `drained-compliance-restriction`; the stated "rank-one spherical" form is correct, and `(1/9)I:C^d:I = K` holds identically.
* **Reference Biot relation.** `B_0 = I − C^d:C_s^{-1}:I`. I verified this equals the exact `p→0` linearisation of the EOS: `B_0 = (1−K/K_s)I + (φ_{s0}α/(3K_s)) dev(C_s:I)` and, using `dev(C_s:I) = C_s:I − 3K_s I` with `I:C_s:I = 9K_s`, reduces to `(1−φ_{s0})I + (φ_{s0}α/(3K_s))C_s:I`. Both routes agree; the manuscript's `(1−K/K_s)I` isotropic form follows.
* **Biot tensor by implicit differentiation.** From `(K_s+αp J̄) dq = (K/φ_{s0})dlnJ − (α/3)d(shape)` with `∂_F(I:C_s:dev ε) = F[∂logC/∂C : dev(C_s:I)]`, I obtain
  `B = I − (J̄/(J[K_s+αp J̄])){ K I − (φ_{s0}/3) α F[∂logC/∂C:dev(C_s:I)]F^T }`,
  identical to eq. `anisotropic-biot-explicit`. The `F[·]F^T` push-forward and the `1/3` are correct.
* **Reference solid storage.** `S_s = φ_{s0}I:C_s^{-1}:I − I:C_s^{-1}:C^d:C_s^{-1}:I` evaluates to `φα/K_s = (φ_{s0}/K_s)(1−K/(φ_{s0}K_s))` — eqs. `reference-solid-storage` and `reference-storage-compatibility` are mutually consistent.
* **Finite unjacketed path.** For `a=1`, `J=J̄`, `C_s:ε = −pJ I`: the EOS holds (trace identity), and `L[I] = C̄^{-1}` gives `τ̂_s = −pJ̄ I ⇒ σ = −pI`, `φ_s = φ_{s0}`. Confirmed.
* **Weak forms vs. kernels.** `ReferenceMomentum::computeQpResidual = Σ_j grad_test[j]·P(component,j)` matches `∫Grad v:P`; `ReferenceFluidMass` gives `test·(m−m_old)/dt − grad_test·Q_f`, matching eq. `fe-fluid-residual`. `ReferenceDarcyLaw`, fluid EOS, and `m_f = ρ̄_f(J − φ_{s0}J̄)` match `finite_elements.tex` verbatim.
* **`ConformalLaw.h` / `ConformalMaterial.C` fidelity.** Every formula in the C++ matches the manuscript: `Ks = Σ_{i,j≤3}Cs_{ij}/9`; `alpha = 1−K/(φKs)`; `cd = φ cs − φα/(9Ks)(cs·ONE)⊗(cs·ONE)`; `devCsI = cs:I − 3Ks I`; `LB = ∫_0^1(I+tD)^{-1} devCsI (I+tD)^{-1}dt` (the Gauss–Legendre resolvent form of `∂logC/∂C`); `B = I − y/(J·stability)(K·I − (φα/3)F·LB·F^T)`; `σ = φ/J τ_space − (1−solid)p I`; `P = JσF^{-T}`; `mass = ρ(J − φy)`; `flux = −mobility J ρ F^{-1}F^{-T}Grad p`. The AD root lift `q = q0 − (residual − raw(residual))/den` gives `dq =(Ks·d target − α y0 dp)/(Ks+αpy0)`, which is the exact implicit derivative.

### 2.2 Python suites re-executed

```
$ python3 validation/mandel_reference.py --self-check
... "verification": {"category": "analytical-reference-only", "passed": true, ...}
    central_overshoot ratio 1.0546586069998425 at t = 0.015165352045764979   -> 5.4659% (matches evidence)
$ python3 examples/verify_conformal.py
{"checks_passed": 186, "legacy_identities_rechecked": 67,
 "max_constitutive_identity_error": 2.4549890331732928e-09,
 "observed_orders": {"energy_stress":[2.0004,2.0001,2.0000,2.0000],
                     "pore_volume":[2.0002,2.0001,2.0000,2.0000],
                     "pressure":[2.0000,2.0003,2.0003,1.9891]},
 "noncoaxial_commutator": 0.1815654919475954,
 "instantaneous_times_pressure_error": 0.23887239106565072}
$ python3 examples/verify_tensor.py
{"errors": {...}, "materials": 13, "states_per_material": 21, "total_states": 273,
 "maximum_stress_strain_commutator": 2.613958036329473}
$ python3 examples/verify_fluid_coupling.py
{"count": 110, "passed": true, "maximum_scaled_error": 8.086725789002713e-09}
$ python3 examples/verify_reconstruction.py
{"errors": {"compliance": 1.39e-16, "drained_energy": 1.11e-15, "drained_hooke": 6.44e-15,
 "minimization": 2.73e-09, "work_equivalence": 5.04e-10, "unjacketed": 5.09e-14,
 "reference_biot": 2.22e-16, "reference_storage": 4.00e-12, "isotropic_eos": 2.22e-15,
 "isotropic_biot": 1.11e-16}, "materials": 20, "incompatible_pairs_rejected": 20,
 "minimum_drained_eigenvalue": 1.8415045063808817}
```

The `compliance` and `legacy_reference_rank_one_compliance_identity` checks re-verify eq. `drained-compliance-restriction` to machine precision, and `incompatible_pairs_rejected = 20/20` confirms that independently chosen stiffness pairs are rejected (the manuscript's claim that two independent anisotropic stiffnesses generally fail the restriction).

### 2.3 MMS forcing recomputed from scratch

I re-derived the body force and fluid source independently (SymPy): rotate the example `C_s` by the code's angle convention, build `C^d` and `B_0` from the constitutive restrictions, form `σ = C^d:ε − B_0 p`, take `b = −div σ`, and form `mass_source = ∂m/∂t − ρ_0·(k/μ_f)∇²p` with `m = (1−φ)+B_0:ε+S p`, `S = (1−φ)/K_f + φα/K_s`.

```
best match: phi=0.6, K=7, angle* = −30° (== code's angle=+30 under its R^T convention)
body_x coefficients (sin x sin y, sin x cos y, cos x sin y, cos x cos y):
  mine    [ 3.151557  1.324546 -0.124330 -0.253689]
  shipped [ 3.151557  1.324546 -0.124330 -0.253689]
body_y coefficients:
  mine    [-0.125123 -0.503143  3.272671 -1.346995]
  shipped [-0.125123 -0.503143  3.272671 -1.346995]
momentum max|recomputed−shipped| = 2.39e-15  (machine precision, grid of 4 points)
mass_source sin(t) coefficient: mine 0.29608813 == shipped 0.29608813203268076
mass_source cos(t) coefficients:
  mine    [ 0.00079354 -0.00079354  0.02244930  0.02399060]
  shipped [ 0.00079354 -0.00079354  0.02244930  0.02399060]
```

So the manufactured forcing is exactly the analytic divergence/source of the prescribed fields under the deck's own linear reference tangent (`φ=0.6`, `K=7`, `angle=30`, `linear_reference=true` — confirmed in `mms_space_4/input.i`). **The MMS is a genuine independent verification of the linear reference tangent, not a self-consistent artefact.**

### 2.4 MMS convergence orders recomputed from raw artifacts

```
$ python3 fe-evidence/compute_mms_order.py --runs fe-evidence/runs
space naive orders: ux [2.9916668663, 2.9584792405]  uy [2.9982612864, 2.9599857747]  p [1.9966292363, 2.0008072999]
time difference orders: nx16 ux 1.0931948217 uy 0.9783037977 p 1.0151767156
                        nx32 ux 1.3968779373 uy 1.0183455409 p 1.1251994970
                        nx64 ux 1.3963663098 uy 1.0762038449 p 1.2519312797
```
Reproduces `fe-evidence/mms-convergence.json` and the `site/evidence.json` convergence prose ("ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00"; "nx=16 (1.093, 0.978, 1.015)"; "nx=32 (1.397, 1.018, 1.125)"; "nx=64 (1.396, 1.076, 1.252)").

### 2.5 Jacobian step study

`jacobian_0.{0001,1e-05,1e-06}/analysis.json`: `max_relative_difference` = 2.38892e-07, 2.38797e-07, 2.39529e-07; contract target 1e-6; `passed: true`. Recomputed the same 3 values and the pairwise span (2.3880e-7 … 2.3953e-7), consistent with the recorded note ("inside 2.39e-7 ± 4e-9"). All below the 1e-6 target and step-independent, so the discrepancy is not FD-step limited.

### 2.6 Discrete conservation / force identities and one-element anchors

```
one_element_drained:  expected (edge_ux, platen, p) = (0.0013271584736625449, -0.0005291067041957089, 0)
                      actual                                   (0.0013271584736627,   -0.00052910670419578,   0.0)
                      absolute_error 1.55e-16 ; mass_change -2.38e-04 ; pass
one_element_undrained: expected (0.002476998516454143, -0.0004156360113397226, 0.004783296459228801)
                       actual     (0.0024769985164543,   -0.00041563601133972,   0.0047832964592326)
                       absolute_error 3.80e-15 ; mass_change -1.01e-16 ; pass
```
I reproduced both `expected` triples independently (homogeneous plane-strain solve with the isotropic mineral `K_s=2.5, μ_s=5/6`, `φ=0.9`, `K=1`):
```
drained    edge_ux=0.0013271584736625  platen=-0.0005291067041957  (shipped 0.0013271584736625449 / -0.0005291067041957089)
undrained  edge_ux=0.0024769985164541  platen=-0.0004156360113397  p=0.0047832964592288
```
Reference-parameter consistency, all recomputed from the stated inputs: `φ=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, ρ̄_{f0}=1, k/μ_f=1.5` give `G = φμ_s = 0.75`, `B_0 = 1−K/K_s = 0.6`, `S_s = (φ/K_s)(1−K/(φK_s)) = 0.2`, total storage `(1−φ)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80`, `M = 80/17 = 4.705882352941177`, `K_u = K+α²M = 229/85 = 2.694117647058824`, `c = 3.821656050955414` — all match `site/reports/mandel-reference.json` and `finite_elements.tex`.

### 2.7 Manuscript numeric claims

```
reference Biot at p=0 (pressure_response.csv): anisotropic 0.7000000 / 0.7583333 / 0.7916667 ; isotropic 0.75
  -> matches "0.7000, 0.7583, 0.7917"
isotropic-comparison mineral shear: mean of five deviatoric modes = (20+24+28+λa+λb)/5 = (72+96)/5 = 33.6 ; μ_s = 16.8  -> matches
K_s for example C_s: (50+12+10+12+60+14+10+14+70)/9 = 252/9 = 28  -> matches "K_s = 28K_*"
step_refinement.csv ratios: 0.00996505/0.00249058/0.00062260/0.00015565/3.89119e-05 -> successive ratios 4.00 -> second order
  pore_volume and pressure columns also ratio 4.00 (second order)
figure row counts: pressure_response 242 rows (2 materials x 121) ; shear_response 322 (2x161) ;
  rotation_response 242 (2x121) ; constrained_layer 242 (2x121) ; directional_response 1083 (3 states x 361, one-degree spacing)
admissibility scan: all plotted states have solid_fraction in (0,1), scalar stability > 0, |mineral_residual| <= 3.5e-14
shear experiment: max|B12| anisotropic 0.01672 (nonzero, zero at gamma=0), isotropic 0.0 ; J==1 exactly on the path
rotation experiment: internal-frame mode has constant B over 121 angles ; physical-rotation mode varies
fe_load_limit.csv: nonlinear_load_0.0001 at nx=20, dt=1e-3 -> pressure_max_normalized = 0.00322092 ; linear reference at same nx/dt = 0.00319572
  -> "floors at about 3.2e-3 at nx=20, dt=1e-3" is correct
fe_mandel_refinement.csv: pressure_max_normalized 10->20 decreases, 20->40 increases -> "non-monotone at the finest level" is correct
conformal report check composition: 5 states x 13 per-state identities = 65 ; legacy_reference_biot and
  legacy_reference_rank_one_compliance_identity are present in the conformal suite -> "186 ... including the 65 ... plus the two" is accurate
mandel-reference.json: 38 checks -> matches "38 self-checks"
```

## (3) Findings

No correctness defects were found. The derivations are internally consistent and reproduce; the implementation is faithful to the stated equations; the manufactured forcing is an independent verification; and every numeric claim I could recompute matches its artifact.

Severity legend: **S1** blocking/mathematical error, **S2** significant, **S3** minor.

* **F1 (S3, observational).** `ConformalLaw.h` applies the mineral rotation as `C_s ↔ R(C_s:(R^T e R))R^T`, i.e. `R^T` relative to a standard `+angle` about z. I confirmed this by matching the shipped MMS forcing exactly at the code's `angle = 30` (`R^T`) and only at `−30°` in the standard convention. This changes only the *sense* of the prescribed orientation; it does not affect any magnitude, any verification claim, or any conclusion, and the manuscript does not state a rotation-matrix convention. Observational only.
* **F2 (S3, observational).** The `directional_response` figure caption opens by naming two anisotropic states while `build/conformal/directional_response.csv` contains three curves (`Anisotropic, F=I`, `Anisotropic, finite shear`, `Isotropic, finite shear`); the caption's later sentence does describe the isotropic comparison, so the figure is not misleading, just terse.
* **F3 (S3, observational).** `fe-evidence/manifest.json` lists 28 `reference_comparison.csv` entries under `"missing"`. These are intentionally absent (the rotated-anisotropy, partial-drainage, Jacobian, MMS, and one-element decks do not solve the reference-modulus Mandel problem), and the accompanying note in `site/reports/finite-deformation-summary.json` says so. The label "missing" is slightly loaded for a deliberate omission.

## (4) Required corrections

None. (Empty list — every item verified is correct as shipped.)

## (5) Optional suggestions

1. State the rotation-matrix convention for the `angle` deck parameter (e.g. "a positive `angle` rotates the mineral axes by the transpose of the stated `R_z(angle)`, i.e. clockwise"), or flip the sign inside `ConformalLaw.h` and regenerate the `angle`-carrying decks, so a reader reproducing the 30°/45°/90° cases gets the intended orientation without trial and error. Evidence: F1.
2. If the directional-response figure is meant to show the isotropic contrast, name all three curves in the caption's first sentence. Evidence: F2.
3. Consider renaming the manifest key from `"missing"` to `"not_applicable"` (or documenting the omission inline) for the non-comparable cases. Evidence: F3.
4. The Jacobian note reports a wider 1e-2…1e-10 sweep that is not machine-readable in the snapshot. Recording those extra rows in the same `analysis.json` schema would let a reviewer re-verify the "not step-limited" claim without re-running the solver.

## (6) Review limitations

* No compiled MOOSE application ships with the snapshot, so `moose_app/` was audited by source fidelity (re-derivation of every formula) and by re-deriving the coupled results from the recorded artifacts, not by re-running the solver. `examples/conformal_model.py` (Python) was re-executed; the C++ law itself was checked by inspection against the Python law and the manuscript, and by the shipped `cpp-python-constitutive.json` (41 states, 6.4e-14), which I could not regenerate.
* `examples/verify_constitutive.py` and the `run_*.py` drivers write to `.agent-runtime/...` paths that are not in the snapshot and invoke the compiled binary; I did not (and could not) re-execute them.
* Reported Python-error digits differ in the last 1–2 ulp between the shipped reports (numpy 1.26.4) and my re-runs (numpy 2.4.2); all conclusions are unchanged.
* Literature claims I did not verify against the cited sources: the correspondence with Gajo (2010) eqs. (3.27), (3.32), (3.34); the Walker et al. appendix-D series; the Drumheller (2000) §8.9 similarity-transformation argument; and the citation-accuracy of `references.bib`. These are outside a mathematics/correctness recomputation.
* The finite-load rotated-anisotropy and partial-drainage cases are explicitly demonstrations; I verified their recorded diagnostics (force_relative ≤ 1.28e-10, normalized mass balance ≤ 2.47e-10, peak pressures 0.2062–0.2158) are internally consistent, but they carry no verification claim and I did not attempt to establish one.

VERDICT: ACCEPT

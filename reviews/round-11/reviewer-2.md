# Independent peer review — Reviewer 2 (physics and source fidelity)

**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Reviewed artifact:** immutable snapshot `round-11`
**Snapshot ID (sha256 of `source-manifest.json`):** `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a`
**Reviewer role:** independent reviewer 2 — physical soundness, mixture-theory / Foster–Xu source fidelity, FE traceability, honesty of coupling physics and numerical evidence.
**Independence:** I did not read any other round-11 report or anything in `reviews/`. All judgments below are formed from the snapshot plus read-only `/tmp` copies. I did not modify the snapshot.

---

## 1. Integrity verification (mandatory first step)

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` | `b9fadd66e96794417a4bed1f674064928716ffb3f2cc30d09edc0a663586fe6a` |
| Matches SNAPSHOT ID and `SNAPSHOT_ID` file | **YES** |
| Listed files hash-verified | **286 / 286 OK** |
| Hash mismatches | **0** |
| Missing listed files | **0** |
| Files on disk not in manifest | **0** |
| Suspicious manifest paths (`..`, absolute) | none |

**Integrity: PASS.** No blocking integrity finding.

Snapshot scope actually inspected: `main.tex`; `sections/*.tex` (incl. new `sections/finite_elements.tex`); `build/main.pdf`, `build/main.log`; `build/conformal/**`; `build/weighted-stress/**`; `figures/**`; `fe-evidence/**` (`site-evidence.json`, `mms-convergence.json`, `compute_mms_order.py`, `runs/*/{analysis.json,input.i,provenance.json,reference_comparison.csv}`); `moose_app/**` (kernels, materials, postprocessors, inputs, scripts); `examples/**`; `provenance/**`; `references.bib`.

---

## 2. Independent recomputation (commands and numbers)

All execution was done on `/tmp` copies; the snapshot was never written to.

**(a) Discrete fluid-mass balance and force diagnostic — reproduced exactly.**
`sha256(live …/runs/partial_30_fine/solution.csv) = 09897c5278c1ca1b5ef0b32ad2e3cbbeaefa19591d400085631166d6313c0a0e`, identical to the hash pinned in the snapshot at `fe-evidence/runs/partial_30_fine/provenance.json["outputs"]["solution.csv"]`. Re-ran the exact budget formula from `moose_app/scripts/analyze_mandel.py` (lines 12–16, 29):

| Quantity | Mine | Recorded `analysis.json` |
|---|---|---|
| `discrete_mass_absolute` | `1.810418134851055e-13` | `1.810418134851055e-13` |
| `discrete_mass_mobilized_relative` | `1.2755987657065335e-10` | `1.2755987657065335e-10` |
| `force_relative` | `1.0000000000025715` | `1.0000000000025715` |
| `platen_equality_absolute` | `4.000272335602517e-14` | `4.000272335602517e-14` |

**(b) Rebuilt the reference Biot components from scratch** (φs0=0.6, K=7, Cs from `experiments.tex` eq. for `example-mineral-stiffness`): Ks=28, α=1−K/(φs0Ks)=0.583333; `B0 = I − Cd:Cs⁻¹:I` gave exactly **(0.700000, 0.758333, 0.791667)**, matching `sections/experiments.tex:25`. Isotropic comparison B0 = 0.75. Drained 11,22,33 block = (22.8, 25.7278, 29.7278) — matches `build/conformal/experiments.json`.

**(c) Rebuilt the FE reference coefficients** (`sections/finite_elements.tex:159–161`): G = φs0·μs = 0.9·(5/6) = **0.75**; B0 = 1−K/Ks = 1−1/2.5 = **0.6**; total storage = (1−φs0)/Kf + φs0·α/Ks = 0.1/8 + 0.9·0.55556/2.5 = **17/80 = 0.2125**. All match.

**(d) Ran the four verification suites in `/tmp`** (independent execution, not assertion):

| Suite | Reproduced |
|---|---|
| `examples/verify_conformal.py` | `checks_passed = 186` (implementation 139, analytical 44, convergence 3); `legacy_identities_rechecked = 67`; `max_constitutive_identity_error = 2.4549890331732928e-9` |
| `examples/verify_tensor.py` | 13 materials × 21 = **273** states |
| `examples/verify_reconstruction.py` | 20 materials, **20/20** incompatible pairs rejected, min drained eigenvalue 1.8415 |
| `examples/verify_fluid_coupling.py` | `count = 110`, `maximum_scaled_error = 8.086725789002713e-09`, passed |

**(e) Mandel analytical self-check** (copied live `validation/mandel_reference.py` to `/tmp`, ran `self_check`): **38 checks, passed**, `central_overshoot.ratio = 1.0546586` → **5.4659 %** at **t = 0.015165352**, matching `fe-evidence/site-evidence.json:14`.

**(f) Recomputed run diagnostics** from `reference_comparison.csv`: `pressure_max_normalized` = `0.8595353844750974` for `partial_30_fine` (recorded identical) and `0.7575671811855765` for `anisotropic_30` (recorded `…768`).

**(g) MMS orders** recomputed from `figures/fe_mms_convergence.csv`: p 1.9966/2.0008, ux 2.9917/2.9585, uy 2.9983/2.9599 — matching `site-evidence.json:31` and `fe-evidence/mms-convergence.json`.

**(h) Kernel/material → equation traceability** (≥2 kernels; here 4 items):
- `moose_app/src/kernels/ReferenceBalance.C`, `ReferenceMomentum::computeQpResidual` = Σ_j ∂(test)/∂x_j·P_ij ⟶ **eq. `fe-momentum-residual`** (`sections/finite_elements.tex:102`).
- `ReferenceFluidMass::computeQpResidual` = test·(m_f − m_f^old)/dt − ∇test·Q_f ⟶ **eq. `fe-fluid-residual`** (`:107`), with m_f and Q_f as defined.
- `ConformalLaw::evaluate`: `sigma = φ/J·tau − (1−solid)·p·I` ⟶ **eq. `total-stress-phase-energy`** (`main.tex:417`); `P = J·sigma·F⁻ᵀ` ⟶ **eq. `fe-total-first-piola`**.
- `ConformalLaw::evaluate`: `B = I − J̄/(J·(Ks+α p J̄))·(K·I − (φ/3)·F·(∫(I+xD)⁻¹ dev(Cs:I)(I+xD)⁻¹dx)·Fᵀ)` ⟶ **eq. `anisotropic-biot-explicit`** (`main.tex:393`) with ∂logC/∂C evaluated by the resolvent integral of `logarithmic_derivative.tex` eq. `log-frechet-spectral-form`; `mass = ρ_f·(J−φs0 J̄)` ⟶ eq. `fe-reference-fluid-mass`; `flux = −(k/μ) J ρ_f F⁻¹F⁻ᵀ∇p` ⟶ eq. `fe-reference-darcy-law`.

---

## 3. Findings

### BLOCKING
None. `physical_validation` remains `not_performed` (`site-evidence.json:47–50`) and `finite_deformation` remains `pending` (`:36–42`). No false scientific pass and no verification claim is made about the coupled finite-deformation runs. The synthetic-parameter caveat is stated in `main.tex:497–499` and `sections/experiments.tex:190–192`.

### MAJOR
None that change a scientific conclusion. The single substantive defect (M-1 below) is an incorrect *explanation* of a diagnostic in the evidence document, not a wrong result; the manuscript's own statement is correct. I record it prominently but do not treat it as blocking.

### MINOR

**m-1 (lead item) — the force diagnostic is misdescribed in the FE evidence file.**
`fe-evidence/site-evidence.json:38` states: *"A force_relative value of approximately 1.0 reflects the kinematic platen constraint, not a force-balance failure."* The conclusion (not a force-balance failure) is correct, but the stated mechanism is not. My recomputation shows the plate reaction equals the applied **resultant** `−2a·q_L = −1.4` to ≈1e-12 once the 0.002-time load ramp completes (`max|top_reaction + 2a·q_L|/(2a·q_L) ≈ 1e-12`; `top_reaction = −1.4000000000018` at t=0.0535). The value `force_relative ≈ 1.0` arises **only** because `moose_app/scripts/analyze_mandel.py:16` sets `expected_force = −q` (the traction, −0.7) instead of the resultant `−2a·q_L` (−1.4), so `|−1.4 − (−0.7)|/0.7 = 1.0`. This contradicts the manuscript's own definition at `sections/finite_elements.tex:135–137` ("the integrated plate reaction equals the prescribed resultant force", with resultant `2a q_L` at `:151`). The evidence document's explanation should be corrected (or `expected_force` fixed to `−2a·q_L`).

**m-2 — "displacement-controlled" is an inaccurate label for the demonstration runs.**
`site-evidence.json:38` and `:284` call the rotated-anisotropy and partial-drainage runs *"displacement-controlled demonstrations."* Per `moose_app/scripts/decks.py:44–47` and `fe-evidence/runs/partial_30_fine/input.i`, the load is applied as a traction (`FunctionNeumannBC` on `top`) and the platen is a kinematic common-displacement constraint (`EqualValueBoundaryConstraint`, formulation kinematic). That is **force-controlled with a rigid plate**, which is exactly the configuration described at `sections/finite_elements.tex:135–137`. Terminology should be harmonized.

**m-3 — the partial-drainage demonstration is compared against a reference of a different geometry, undisclosed.**
`sections/finite_elements.tex:146–149` defines the Mandel reference on `[-a,a]×[-b,b]` with `a=1`, `b=0.1` (ratio 10:1). But `fe-evidence/runs/partial_30_fine/input.i` and `partial_30/`, `partial_30_coarse/` use `ymin=-1, ymax=1`, i.e. a square `[-1,1]²` (`decks.py:29`, `h=1` for the partial case), while `anisotropic_30/input.i` correctly uses `ymin=-0.1, ymax=0.1`. The `reference_comparison.csv` therefore compares a square-domain run to the 10:1 analytical reference. Since no quantitative claim is attached and the isotropic (correct-geometry) run shows comparable differences (finite-load effect dominates), this is an honesty/disclosure issue, not a wrong number — but the geometric mismatch should be stated.

**m-4 — the quoted difference range "60-100 percent" does not cover the recorded metrics.**
`site-evidence.json:38`: *"Differences of 60-100 percent in pressure and displacement…"*. Recorded normalized differences span: `pressure_max_normalized` 0.513–0.860, `platen_max_normalized` 0.634–0.756, `edge_ux_max_normalized` **1.687–1.797** (≈170–180 %), `profile_max_normalized` 0.608–0.875. The edge-displacement metric is understated by ~80 percentage points and the low end of pressure is below 60 %. The descriptor should be corrected to the recorded ranges or replaced with a pointer to `analysis.json`.

**m-5 — the snapshot omits sources/artifacts needed to reproduce and support some quoted FE evidence numbers.**
`source-manifest.json` contains no `validation/**` and no `site/**`. Consequently:
- `fe-evidence/site-evidence.json:14,201` ("38 self-checks, peak overshoot 5.4659 % at t=0.01516535") is backed by no artifact inside the snapshot (the referenced `site/reports/mandel-reference.json` is absent). I verified this claim is **true** from the live `validation/mandel_reference.py` (38 checks passed; ratio 1.0546586), so this is a completeness gap, not a false claim.
- The reproduction commands at `site-evidence.json:216–220` (`run_verification.py`, `run_demonstrations.py`) import `validation.mandel_reference` and `examples.conformal_model`; they cannot run from the snapshot alone.
Recommend including `validation/**` (at least `mandel_reference.py`, `mms_reference.py`, `equation_to_moose_map.yml`, `theory_traceability.yml`) and the generated `site/reports/*.json` in the reviewed snapshot.

**m-6 — the embedded numerical supplement is not hash-pinned by the snapshot.**
`main.tex:26–27` embeds `build/conformal-2026-09-20-v1.zip`, and `build/main.pdf` does contain a real attachment (281 547 bytes, 34 files, own `manifest.json` with payload hashes — I extracted and checked it). But no `build/*.zip` is listed in `source-manifest.json`, so the PDF's payload is not covered by the snapshot's own hash manifest.

### OPTIONAL

**o-1.** The discrete mass-balance diagnostic (`analyze_mandel.py:12–15`) closes the budget with the pressure-residual boundary reaction (`DofReactionSum`, `ReferenceOutflow`-derived `mass_reaction`) — the same algebraic residual the solver drives to `nl_abs_tol = 1e-12`. Its ~1e-10 relative closure is therefore near a solver-tolerance measurement. The manuscript is transparent about this (`sections/finite_elements.tex:196–201`, and it keeps the gradient-reconstructed outflow separate), but reporting the independent `outflow_gradient` comparison alongside `discrete_mass_*` would make the conservation claim more convincing.

**o-2.** `figures/fe_load_limit.csv` shows the finite-load error flooring at ≈3.2e-3 (pressure) as q→1e-4; the site summary (`:31`, `:44`) could state this floor explicitly rather than "tolerance statement … still being finalized."

**o-3.** `ReferenceFluidMass`/`ReferenceMomentum` are compact single-expression kernels with no inline equation comments; adding the `\label` of the implemented equation (in the style of `validation/equation_to_moose_map.yml`) would strengthen traceability for readers.

---

## 4. Assessment against the specifically requested judgments

- **Kernel/material fidelity:** Confirmed for four items (m(h) above); residuals and the constitutive `B`, `sigma`, `mass`, `flux` match their referenced equations exactly.
- **Fluid mass conservation:** The quoted numbers (`1.81e-13` absolute, `1.28e-10` mobilized relative) reproduce exactly and are small; the conservation claim is fairly stated, with the caveat in o-1.
- **Rotated-anisotropy / partial-drainage framing:** The runs are demonstrations, not verification; that framing is honest in substance. However the stated *cause* of `force_relative ≈ 1.0` (m-1) and the "displacement-controlled" label (m-2) are inaccurate, and the partial-domain geometry mismatch (m-3) is undisclosed. No statement in the manuscript overclaims verification; `sections/finite_elements.tex:194` explicitly limits the MMS test, and `:190–192` disclaims experimental validation.
- **`physical_validation`:** Remains `not_performed` (synthetic parameters). Correct, and no unsupported pass is asserted.
- **Quoted run results:** Every FE number I could trace is supported by a recorded artifact and reproduces; the only unsupported-in-snapshot number (38 checks / 5.4659 %) is verified true from the live repository source.
- **Source fidelity:** The treatment of Drumheller–Bedford (`main.tex:99–103`, and the careful `:487–496` discussion that the dilation-times-rotation restriction is a *constitutive specialization*, not a consequence of stress symmetry) and the Foster–Xu pressure conjugacy / Legendre construction (`main.tex:340–360`) are accurate and appropriately qualified; no overreach into experimental validation.

**Verdict:** MINOR REVISION

---

### Final verdict line
MINOR REVISION

# Round 19 — Reviewer 1 (mathematics and correctness)

Reviewed artifact: frozen snapshot
`/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-19`
(read-only). I reviewed only this snapshot; no other round output or reviewer report was read.
Scratch work was done under `/tmp`.

## 1. Snapshot identity and manifest

- `source-manifest.json` sha256 = `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682`.
- `SNAPSHOT_ID` = `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682`.
- **Declared SNAPSHOT_ID matches the manifest hash.**
- Manifest entries re-hashed file-by-file: **534/534 match**, **0 missing**, **0 hash mismatches**.
- Files present but unlisted: **1** — `SNAPSHOT_ID` itself (expected snapshot marker, not a payload).
- `fe-evidence/manifest.json` (case/file SHA list) is itself one of the 534 verified entries.

Snapshot integrity: **PASS**.

## 2. Re-derivations

I re-derived the results independently rather than reading them off. All agree with the manuscript.

**Kinematics (main.tex §kinematics, eqs. 1–12).**
`F = A F̄`, `J = a J̄`, `a = det A` are exact for `A = a^{1/3} R_A`, `det R_A = 1`:
`J̄ = a^{-1} J`, `C̄ = a^{-2/3} C`, `Ū = a^{-1/3} U`. Phase sum
`σ = φ_s σ̄_s − (1−φ_s) p I` and `τ' = φ_{s0}(τ̄_s + p J̄ I)` (eq. 12) both reproduce from
`Jφ_s = φ_{s0}J̄`.

**Virtual work (eqs. 14–16).** With `F = a^{1/3}R_A F̄` I obtain
`δF F^{-1} = ⅓ I δ ln a + δR_A R_Aᵀ + R_A(δF̄ F̄^{-1})R_Aᵀ`; the skew term vanishes against the
symmetric `τ'`; the `δJ̄` term and the pressure term cancel exactly, giving eq. (16). The `⅓` and
the cancellation do not require coaxial stress/strain — confirmed.

**Equivalent energy and returned stress (eqs. 17–22).** Objectivity `W̄_s(a^{-1/3}R_AᵀF)=W̄_s(a^{-1/3}F)`
is correct (left rotation). Independently re-differentiating
`W_s = W_A(a)+φ_{s0}W̄_s(F̄)` gives `τ' = (∂W_A/∂ln a) I + φ_{s0} dev τ̄_s` and, via pressure
conjugacy, `∂W_A/∂ln a = (φ_{s0}/3) tr τ̄_s + φ_{s0} p J̄` (eqs. 19–20). The volumetric reduction
(eq. 22) also reproduces.

**Finite Biot tensor (main.tex §finite-biot, eqs. 23–36).** Re-derived `P' = P'' + φ_{s0}p ∂J̄/∂F`,
`σ = σ'' − pB`, `B = I − (φ_{s0}/J)(∂J̄/∂F)Fᵀ`, and `δ(J−φ_{s0}J̄)/J = B:(δF F^{-1})`. I checked
the sign-sensitive tangent `∂σ/∂p|_F = −B` (eq. 35) carefully, because `σ''` is pressure dependent:
using `σ = σ' − pI` with `σ' = J^{-1}(∂W'/∂F)Fᵀ` gives `∂σ/∂p = (φ_{s0}/J)(∂J̄/∂F)Fᵀ − I = −B`.
Equation (35) is correct. The fixed-pressure mineral derivative (eq. 28) and the explicit Biot tensor
(eq. 29) both reproduce; in particular the `F[∂logC/∂C : dev(C_s:I)]Fᵀ` term carries **no** spurious
factor 2 (I checked the index-level chain rule), and `B` is symmetric.

**Logarithmic-stress appendix (eqs. 64–67).** Verified `M:C = I`, `push(F,I) = I`, `tr τ = tr T`, and the
spectral/continuous-limit form of the Fréchet derivative.

**Drained restrictions (stress_reconstruction.tex, eqs. 37–48).** Verified
`ln a = (1−K/(φ_{s0}K_s))/(3K_s) I:C_s:ε`, `C^d = φ_{s0}C_s − (φ_{s0}/(9K_s))(1−K/(φ_{s0}K_s))(C_s:I)⊗(C_s:I)`
(eq. 45), and, by Sherman–Morrison, `(C^d)^{-1} = (φ_{s0}C_s)^{-1} + (1−K/(φ_{s0}K_s))/(9K) I⊗I` (eq. 48).
I also verified `I − C^d:C_s^{-1}:I = (1−φ_{s0})I + (φ_{s0}/(3K_s))(1−K/(φ_{s0}K_s))(C_s:I)`, which is the
`F=I, p=0` limit of eq. (29) — the two independent routes to the reference Biot tensor agree.

**Reference storage and limits (limits.tex, eqs. 49–56).** `S_s = (φ_{s0}/K_s)(1−K/(φ_{s0}K_s))` follows by
differentiating the EOS at `ε=0`; the storage compatibility (eq. 52) also reproduces symbolically.
For the unjacketed path I re-derived the key step: `T = C_s:ε̄ = −pJ I ⇒ M:T = −pJ I ⇒ τ̂_s = −pJ I ⇒ σ̂_s = −pI`
when `a=1`, `J=J̄` — correct, and the appendix identity `push(F,I)=I` is what makes it work.
The cubic statement (`dev(C_s:I)=0 ⇒ B` spherical) is correct.

**Pore fabric (sections/pore_fabric.tex, eqs. 57–71).** Polar `A=R_A G^{1/2}`, `det H=1`, `G=a^{2/3}H`, the
transverse-isotropic `H` and `E_d = (ln a/3)I + ln h(½I − 3/2 m⊗m)` all check out. The reference
compliance `(C^d)^{-1}=(φ_{s0}C_s)^{-1}+D^{-1}` and its conformal reduction are consistent: volume-only
`W_A` corresponds to `D=(K/γ)I⊗I` (with `γ=1−K/(φ_{s0}K_s)`), and the rank-one inverse on the volume
direction is `D^{-1}=(γ/(9K))I⊗I`, reproducing eq. (48). I independently confirmed `B_0=I−C^d:C_s^{-1}:I` is the
reference limit of the general `B` in the fabric case, and — via Sherman–Morrison — that an isotropic
mineral with only the in-plane fabric modulus differing keeps `B` spherical, while the volume–axial
coupling makes `B` transversely isotropic (`B_∥≠B_⊥`).

## 3. Numbers recomputed from raw data

All recomputed with python3 from the snapshot's own JSON/CSV.

| Quantity | Manuscript | Recomputed | Source |
|---|---|---|---|
| Reference Biot components (`φ_{s0}=0.6`, `K=7`, `K_s=28`, eq. 71 matrix) | 0.7000, 0.7583, 0.7917 | 0.700000, 0.758333, 0.791667 | eq. (29) limit, annotated inputs |
| Isotropic comparison shear modulus | `16.8 K_*` = mean of five deviatoric modes ÷ 2 | deviatoric eigenvalues (20,24,28,42.967,53.033); mean 33.6; /2 = 16.8 | eq. (71) |
| FE reference: `G=0.75`, `B=0.6`, storage `17/80` | ✓ | 0.75, 0.6, 0.2125 = 17/80 | decks.py, eq. (48)/(52) |
| Fabric probe worst abs diff | 4.9×10⁻¹⁵ | 4.885×10⁻¹⁵ (max over all fields/cases) | build/fabric/fabric-verification.json |
| Fabric `B` (iso / coupled a0) | 0.88387 / 0.85065, 0.91027 | 0.883871 = 1−K_d/K_s with K_d=0.290323; reproduced analytically | fabric-verification.json, figures/fe_fabric_probe.csv |
| Fabric coupled peak centre pressures | 6.28e-5, 5.10e-5, 3.95e-5, 5.13e-5 | 6.280289e-5, 5.102155e-5, 3.946133e-5, 5.132551e-5 | figures/fe_fabric_mandel_peak.csv |
| Conformal suite: 186 checks; max constitutive identity error | 186; 2.5×10⁻⁹ | checks_passed=186; max implementation-category error 2.454989e-9 | build/conformal/verification.json |
| Spherical-gauge suite | 273 states, 13 stiffnesses | total_states=273, materials=13 | site/reports/tensor-verification.json |
| per-state identities | 5 states × 13 | legacy_states=5, legacy_identities_rechecked=67 (=65+2) | verification.json |
| Step refinement | second order | observed orders ≈2.0000 (energy/pore volume), ≈2.0000 (pressure) | build/conformal/step_refinement.csv |
| FE nonlinear "floor" at nx=20, dt=1e-3 | ~3.2×10⁻³ | 3.2209197e-3 (load 1e-4); 3.4479e-3 (1e-3); 5.7060e-3 (1e-2) | figures/fe_load_limit.csv |
| MMS spatial orders | (not stated numerically) | ux 2.992/2.958, uy 2.998/2.960, p 1.997/2.001 | fe-evidence/mms-convergence.json |

**MMS order estimation (`compute_mms_order.py`).** I re-implemented the arithmetic and confirmed every stored
`naive_orders`, `norm_deficits` and `difference_orders` value exactly. The spatial rates (~3 for Q2 displacement,
~2 for Q1 pressure, QUAD9 mesh) are the optimal rates for the element pair and are clean. The script's
"successive-difference" estimator (documented in the header) is a reasonable way to remove the mesh floor from
the temporal series: the naive temporal ratios are ≈3×10⁻³ (floor-dominated) while the difference estimator gives
≈1, consistent with backward Euler. The estimator is a heuristic, with one independent order estimate per series
(see F6).

## 4. Findings

All locations are in the snapshot. Labels: **required** = must be fixed/addressed before publication;
**optional** = improvement.

**R19-R1-01 — required — supplement filename mismatch.**
Location: `sections/experiments.tex` line ~212 ("The numerical supplement is embedded in the PDF as
`conformal-2026-09-20-v1.zip`") vs `main.tex` line 26 (`\embedfile[...filespec=anisotropic-biot-2026-09-20-v2.zip]`
of `build/anisotropic-biot-2026-09-20-v2.zip`). Evidence: the embedded archive's own `manifest.json` gives
`"version": "anisotropic-biot-2026-09-20-v2"`, and its `README.md` is titled with that same v2 name. The text's
v1 name does not exist in the snapshot. A reader following the extraction instruction is given the wrong
attachment name.

**R19-R1-02 — required — symbol collision: `W_d` denotes two different energies.**
Location: `sections/stress_reconstruction.tex` eq. (41) defines the *drained skeleton energy*
`W_d = ½ ε:ℂ^d:ε` (with conjugate law eq. 40, label `eq:prescribed-skeleton-log-hooke`), whereas
`sections/pore_fabric.tex` (label `eq:fabric-equivalent-energy`) and the Discussion write
`W_s = W_d(𝐆) + φ_{s0}W̄_s(F̄)` for the *distention* energy, "replacing the volume-only energy `W_A(a)`".
The same symbol therefore means the drained energy in one section and the distention energy in another.
This is a genuine notational defect in the key constitutive equations; rename one of them (e.g. keep `W_A`
for the distention family and use a distinct symbol for the drained energy).

**R19-R1-03 — required — the "3.2×10⁻³ floor" is not established as a model floor.**
Location: Discussion/conclusions (`main.tex`, "their normalized pressure discrepancy floors at about
3.2×10⁻³ at nx=20, dt=10⁻³ rather than decaying to it"); evidence: `figures/fe_load_limit.csv`,
`figures/fe_mandel_refinement.csv`. The smallest-load run (1e-4) gives 3.2209e-3, but the *constant-tangent*
problem at the same dt=1e-3 gives 3.6579e-3 (`linear_time_0.001`), and halving dt halves that error
(3.6579e-3 → 7.1039e-3 when dt doubles to 2e-3). The residual at nx=20, dt=1e-3 is therefore dominated by the
backward-Euler temporal error, not by an irreducible finite-deformation discrepancy. The claim should be
reworded (the value is a fixed-dt discretization residual) or supported by a dt refinement at fixed load.

**R19-R1-04 — optional — Mandel spatial refinement is non-monotone, so "reproduces the reference under
spatial refinement" is not demonstrated.**
Location: `sections/finite_elements.tex` §fe-reference-problems
("compare profiles ... under separate spatial and temporal refinement"); evidence:
`figures/fe_mandel_refinement.csv`. `pressure_max_normalized` = 2.0832e-3 (h=0.1), 4.5764e-4 (h=0.05),
6.3641e-4 (h=0.025): the finest grid is worse than the middle grid, and the same holds for
`profile_rms_normalized` (3.6460e-3, 8.8474e-4, 1.3520e-3). The linear consolidation comparison therefore
does not exhibit a clean convergence order; state this explicitly, since the MMS (not the Mandel comparison)
is what actually demonstrates the order.

**R19-R1-05 — optional — "186 named checks" conflates categories and one category is not an error metric.**
Location: `sections/experiments.tex` §Independent verification.
`build/conformal/verification.json`: `checks_passed=186` decomposes into 139 `implementation`, 44 `analytical`,
and 3 `convergence` entries. The 65 per-state identities plus the 2 reference relations = 67
(`legacy_identities_rechecked`), not 186. The three `convergence` entries carry `error` values up to
1.0850e-2 (`second_order_pressure`, tolerance 0.06) that are order deficits, not errors; the quoted
"largest absolute error ... 2.5×10⁻⁹" applies only to the implementation category. The wording should
distinguish the identity checks from the convergence checks.

**R19-R1-06 — optional — temporal MMS order estimate is single-sample and inconsistent across meshes.**
Location: `fe-evidence/compute_mms_order.py`, `fe-evidence/mms-convergence.json`. The difference estimator
returns one estimate per series from three dt levels; `ux_l2` gives 1.093 (nx=16), 1.397 (nx=32), 1.396 (nx=64),
and `p_l2` gives 1.015/1.125/1.252 — plausible for backward Euler but noisier than first order alone would be,
indicating incomplete removal of the mesh floor. Report the methodology and the spread rather than a single
implied order.

**R19-R1-07 — optional — the implemented/verified fabric distention stiffness omits one strain mode.**
Location: `sections/pore_fabric.tex` §fabric-biot (eq. 57 and the claim of a "general fabric-symmetric
fourth-order tensor") vs `examples/verify_fabric.py` (`basis()` builds 5 directions: `I/√3`,
`m⊗m−I/3`, `p1⊗p1−p2⊗p2`, `sym(p1,m)`, `sym(p2,m)`). The in-plane shear mode `sym(p1,p2)` is absent, so the
fabric compliance is realized on a 5-dimensional subspace and retains the pure mineral compliance in the
`p1p2` shear direction. The general restriction (eq. 57) is a mathematical statement, but the demonstration
energy is narrower than "general". State the omission or add the mode.

**R19-R1-08 — optional — "manifest.json identifies ... SHA-256 hashes of all payload files" is inaccurate.**
Location: `sections/experiments.tex` §Code and data availability. The embedded
`build/anisotropic-biot-2026-09-20-v2.zip` `manifest.json` contains only `{"version", "sha256"}`
(a single digest), not a per-file hash list. `fe-evidence/manifest.json` does carry per-file hashes for the FE
runs; clarify which manifest is meant.

## 5. Overall assessment

**Correctness.** I independently re-derived every central result — the multiplicative decomposition and its
conformal specialization, the virtual-work separation, the equivalent energy and returned stress, the finite
Biot tensor and its pressure tangent, the explicit `B` from the mineral EOS, the drained stiffness/compliance
restrictions, the reference Biot/storage, the unjacketed reduction, and the tensorial (fabric) extension — and
found no algebraic, index, symmetry, contraction, or dimensional error. Sign-sensitive and factor-sensitive
steps (the `−B` pressure tangent, the absence of a factor 2 in the log-derivative push, the rank-one inverse in
the conformal reduction, the unjacketed `push(F,I)=I` step) all check out. Every published number I could
recompute from raw snapshot data matches, including the reference Biot components (0.7000/0.7583/0.7917), the
`16.8` isotropic shear modulus, the fabric probe values and peak pressures, the FE reference coefficients
(`G=0.75`, `B=0.6`, `17/80`), the conformal/`273`-state suite counts, and the MMS observed orders.

**Novelty and significance.** The construction is a genuine contribution: it derives the anisotropic Biot tensor
from volume-fraction-weighted phase stresses plus reversible work, identifies that the internal distention
rotation cancels from the constitutive response while the mineral stress must still be rotated into the mixture
frame, and shows that volume-only (conformal) distention forces the additional drained compliance to be
spherical rank-one. Replacing the scalar dilation with a symmetric positive-definite distention whose unimodular
part is a pore-fabric tensor is a defensible and useful extension that relaxes the rank-one restriction and
produces distinct axial/transverse Biot coefficients behind an isotropic mineral. The demonstration that
cubic-symmetry minerals give a spherical `B` is a nice, checkable prediction.

**Engineering relevance.** The finite-deformation coupling and the pore-fabric mechanism are directly relevant
to anisotropic shales/cracked rock and to reaction-induced pore fabrics; the FE verification against a
manufactured solution and against the constant-coefficient consolidation reference is appropriate, and the
manuscript is commendably explicit that the finite-load rotated-anisotropy, partial-drainage and rotated-fabric
runs are demonstrations rather than quantitative verification or experimental validation.

**Reservations.** The three required items are minor but real: a wrong supplement filename in the text, a `W_d`
symbol collision between the drained and distention energies, and an over-stated interpretation of the
`3.2×10⁻³` residual as a floor rather than a fixed-dt discretization error. The optional items (non-monotone
Mandel spatial refinement, the check-count wording, the single-sample temporal order estimate, the truncated
fabric mode set, and the manifest description) are clarity/robustness improvements. None of these affect the
correctness of the core derivation or the trustworthiness of the reported verification, and all are
addressable without new physics.

VERDICT: MINOR REVISION

# Reviewer 1 — mathematics and correctness

Snapshot under review (read-only): `.agent-runtime/review-snapshots/round-20`
Declared `SNAPSHOT_ID = 542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b`
This reviewer read only that snapshot. Scratch work was done under `/tmp/rev1` and `/tmp/snap20`
(a writable copy). No snapshot file was modified.

---

## 1. Snapshot identity and manifest

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` | `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b` |
| Declared `SNAPSHOT_ID` (file `SNAPSHOT_ID`) | `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b` |
| Match | **yes** |
| Files listed in manifest | 534 |
| Re-hashed OK | 534 |
| Missing | 0 |
| Hash mismatch | 0 |
| Additional files present on disk but not listed | 2 (`SNAPSHOT_ID`, `source-manifest.json` — expected) |

All 534 listed files re-hash to their manifest digests. Snapshot integrity is confirmed and the
frozen artifact is internally consistent.

Two recorded verification outputs were regenerated from the snapshot and reproduced bit-identical
hashes:

| Artifact | Manifest sha256 | Regenerated sha256 |
|---|---|---|
| `build/fabric/fabric-verification.json` | `30fc975bd611950cfc532eb82bc9070bf6c9834fde87f18fe3254ff3ec513784` | identical |
| `build/conformal/verification.json` | reproduced numerically (186 checks, same error values) | identical content |

---

## 2. Independent re-derivations

I re-derived the chain from the stated postulates rather than reading it off. Unless noted, every
step below agrees with the manuscript.

### 2.1 Kinematics and distention (eqs. `true-mineral-jacobian` … `conformal-mineral-metric`)

`F = A F̄`, `J = a J̄`, `a = det A` is correct. With `A = a^{1/3} R_A`, `R_A` proper orthogonal,
`F̄ = a^{-1/3} R_A^T F` and `C̄ = F̄^T F̄ = a^{-2/3} F^T R_A R_A^T F = a^{-2/3} C`. ✓
Mass relations `J̄ = ρ̄_{s0}/ρ̄_s`, `φ_s = φ_{s0}J̄/J`, `φ_s a = φ_{s0}` all follow from
`Jφ_sρ̄_s = φ_{s0}ρ̄_{s0}`. ✓

### 2.2 Virtual work (`spherical-distention-virtual-deformation` … `distention-mineral-energy-work`)

`δF F^{-1} = ⅓ I δ ln a + δR_A R_A^T + R_A(δF̄ F̄^{-1})R_A^T` is correct; the middle term is skew
(`δ( R_A R_A^T ) = 0`) so it annihilates a symmetric `τ'`. Substituting into
`δW_s = τ':(δFF^{-1}) − φ_{s0}p δJ̄` and using the phase balance
`τ' = φ_{s0}(τ̄_s + pJ̄I)` with `τ̄_s = R_A τ̂_s R_A^T` gives
`R_A^Tτ'R_A − φ_{s0}pJ̄I = φ_{s0}τ̂_s`, hence exactly eq. `distention-mineral-energy-work`. ✓

### 2.3 Energy return (`energy-returned-effective-stress`, `energy-returned-pressure-balance`)

Independently (setting `R_A = I`, which objectivity permits): differentiating
`W_s = W_A(J/J̄) + φ_{s0}W̄_s(a^{-1/3}F)` at fixed `J̄` gives

```
P' = W_A' F^{-T} + φ_{s0} a^{-1/3}[ M − ⅓(M:F)F^{-T} ],   M = ∂W̄_s/∂F̄
τ' = W_A' I + φ_{s0}[ τ̂_s − ⅓ tr(τ̂_s) I ] = W_A' I + φ_{s0} dev τ̄_s
```

using `M:F = a^{1/3} tr τ̂_s` and `M F^T = a^{1/3} τ̂_s`. This is exactly
eq. `energy-returned-effective-stress`, and with `W_A' = ⅓ tr τ'` it recovers the full phase
balance including shear. The paper's claim that the distention energy alone is fixed by the
spherical drained path, while the mineral contribution carries the shear, is correct.

### 2.4 Mineral equation and drained restrictions (`anisotropic-mineral-eos`, `drained-stiffness-restriction`, `drained-compliance-restriction`)

* `∂W_s/∂ln J̄|_F = −φ_{s0}pJ̄` reproduces eq. `anisotropic-energy-pressure-derivative`; multiplying
  by `(1−k)` with `k = K/(φ_{s0}K_s)` and using `φ_{s0}K_s(1−k) = φ_{s0}K_s − K` gives exactly
  eq. `anisotropic-mineral-eos`. ✓
* Monotonicity/unique positive root: derivative of the RHS w.r.t. `J̄` is `K_s/J̄ + (1−k)p > 0`
  for `p ≥ 0`, `k < 1`; limits are `−∞` and `+∞`. ✓ The negative-pressure branch and the stability
  domain `K_s + (1−k)pJ̄ > 0` match the manuscript's caveats. ✓
* Drained stiffness: I substituted the equilibrium `ln a = (1−k)/(3K_s) I:C_s:ε` into the energy and
  expanded. The `(I:C_s:ε)^2` coefficient reduces to `−φ_{s0}(1−k)/(18K_s)`, reproducing
  `W_s = ½ε:C^d:ε` with eq. `drained-stiffness-restriction` exactly. ✓
* Compliance: `ε = ε̄ + ⅓ln a I` with `ε̄ = (φ_{s0}C_s)^{-1}:C^d:ε` and
  `ln a = (1−k)/(3K) I:C^d:ε` gives `(C^d)^{-1} = (φ_{s0}C_s)^{-1} + (1−k)/(9K) I⊗I`, i.e.
  eq. `drained-compliance-restriction`. ✓ I also confirmed the identity
  `(C^d)^{-1} − (φ_{s0}C_s)^{-1} − D^{-1} = 0` numerically (`2.2e-16`).

### 2.5 Finite Biot tensor (`finite-biot-tensor` … `anisotropic-biot-explicit`)

Writing `α = 1 − K/(φ_{s0}K_s)`, the implicit derivative
`[K_s + αpJ̄]∂lnJ̄/∂F = (K/φ_{s0})F^{-T} − (α/3)∂_F[I:C_s:dev ε]` and
`B = I − (φ_{s0}/J)∂J̄/∂F F^T` combine to

```
B = I − J̄/(J[K_s+αpJ̄]) { K I − (φ_{s0}α/3) F[∂logC/∂C : dev(C_s:I)] F^T }
```

which is eq. `anisotropic-biot-explicit` exactly (the appendix supplies the Fréchet derivative,
and its spectral form and repeated-eigenvalue limit are the standard ones). Symmetry of `B` follows
because the matrix-logarithm derivative maps symmetric tensors to symmetric tensors, and the
superposed-rotation equivariance `B(QF,p) = Q B(F,p) Q^T` is correct. ✓

### 2.6 Tensorial distention and the fabric law (`sec:pore-fabric`)

* `A = R_A G^{1/2}`, `G = A^T A`, `a = (det G)^{1/2}`, `C̄ = F^T R_A G^{-1} R_A^T F`. ✓ The
  conformal reduction (`G = a^{2/3}I`) recovers §2.1 exactly. ✓
* `H = (det G)^{-1/3}G`, `det H = 1`, `G = a^{2/3}H`. ✓
* Virtual work: `δF F^{-1} = δR_A R_A^T + R_A[δ(G^{1/2})G^{-1/2}]R_A^T + R_A G^{1/2}(δF̄F̄^{-1})G^{-1/2}R_A^T`.
  Contracting with `τ'`, dropping the skew term, and using `G^{1/2}τ̃G^{-1/2} = φ_{s0}(G^{1/2}τ̂_sG^{-1/2} + pJ̄I)`
  gives eq. `fabric-phase-work` with the pressure canceling. ✓
* Transverse isotropy: with `H = h^{-2}m⊗m + h(I−mm)`, `ln H = ln h (I−3mm)`, so
  `E_d = ½ln G = (ln a/3)I + ln h(½I − 3/2 mm)` — eq. `fabric-transverse-strain` is arithmetically
  consistent with eq. `fabric-transverse-h`. ✓ However see finding **R1** for the sign the
  implementation attaches to `ln h`.
* Reference-state compliance: minimizing `½E_d:D:E_d + (φ_{s0}/2)(ε−E_d):C_s:(ε−E_d) + φ_{s0}p tr(ε−E_d)`
  gives `(D+φ_{s0}C_s)ε_d = φ_{s0}C_s:ε + φ_{s0}pI`, `C^d = φ_{s0}C_s(D+φ_{s0}C_s)^{-1}D`, hence
  `(C^d)^{-1} = (φ_{s0}C_s)^{-1} + D^{-1}` — eq. `fabric-compliance-restriction` is correct, and the
  conformal limit `D = (K/(1−k))I⊗I` reduces it to eq. `drained-compliance-restriction`
  (`D^{-1} = (1−k)/(9K) I⊗I`). ✓
* `B_0 = I − C^d:C_s^{-1}:I` is the correct reference-state limit of eq. `finite-biot-tensor`
  (I re-derived it from `δ(J−φ_{s0}J̄)/J = B:(δFF^{-1})` at `F = I`). ✓
* The claim that a vanishing volume–axial coupling keeps `B` spherical while `C^d` is transversely
  isotropic is correct: the frozen in-plane-shear direction is orthogonal to `I`, so `C^d:I ∝ I`.
  I verified this numerically and against the recorded runs (§3). ✓
* The shape balance has no pressure term because `J̄ = J/a` with `a = (det G)^{1/2}` independent of
  `h`. ✓

### 2.7 Isotropic / reference limits (`sec:compatibility`)

`B_0 = (1 − K/K_s)I` for an isotropic mineral, `S_s = (φ_{s0}/K_s)(1 − K/(φ_{s0}K_s))`, and the
unjacketed path `a = 1`, `J = J̄`, `C_s:ε = −pJ I` ⟹ `σ = −pI`, `φ_s = φ_{s0}` are all correct.
✓ The unjacketed statement "the logarithmic stress transformation maps `I` to `I`" is exactly
eq. `logarithmic-stress-trace`. ✓

**Conclusion of §2: I found no error in any derivation presented in `main.tex`,
`sections/stress_reconstruction.tex`, `sections/limits.tex`, `sections/logarithmic_derivative.tex`,
`sections/finite_elements.tex`, or `sections/pore_fabric.tex`, apart from the reporting-sign issue of
finding R1.**

---

## 3. Code and verification cross-checks

### 3.1 Independent re-implementation (my own, from the equations)

I wrote a from-scratch NumPy implementation of the reference-state fabric model (basis, equilibrium,
`C^d`, `B`, stress) directly from the manuscript equations — not from `examples/verify_fabric.py`.
Results versus `build/fabric/fabric-verification.json` (recorded MOOSE output):

| case | quantity | mine | recorded MOOSE |
|---|---|---|---|
| `fabric_probe_iso` | `B_par`, `B_per` | 0.883870967742, 0.883870967742 | 0.88387096774194, 0.88387096774194 |
| `fabric_probe_coup_a0` | `B_par`, `B_per` | 0.850654419793, 0.910269979799 | 0.85065441979279, 0.91026997979915 |
| `fabric_probe_coup_a45` | `ln_a`, `Jbar`, `σ11`, `σ22` | 0.011361662234, 0.9936383378, −0.010992383690, −0.019992383690 | identical to 12 sf |
| `fabric_probe_coup_a90` | `ln_a`, `σ11`, `sol` | 0.011858458567, −0.013102347494, 0.8893804849 | identical to 12 sf |
| `fabric_probe_conformal` | `B_par`, `B_per`, `ln_a` | 0.6, 0.6, 0.007222222222 | 0.6, 0.6, 0.007222222222 |

All agree to ~1e-12. The recorded FE material-point values are exactly what the manuscript equations
give. The `fabric_mandel_*` reference Biot data also match (`coupling=0.4`, `vol=5.4`:
`B_par = 0.577372982834`, `B_per = 0.615285045899`, matching `0.57737298283364`, `0.61528504589908`).

### 3.2 Recorded suites re-run from the snapshot

| Script | Exit | Result |
|---|---|---|
| `examples/verify_fabric.py` | 0 | worst probe-field abs. difference `4.885e-15`; JSON hash identical to manifest |
| `examples/verify_conformal.py` | 0 | 186 checks pass; `max_constitutive_identity_error = 2.4549890331732928e-09`; refinement orders ≈ 2.000 for energy/stress, pore volume, pressure |
| `examples/verify_tensor.py` | 0 | 273 states / 13 materials; `maximum_stress_strain_commutator = 2.613958036329473`; `seed 20260919` |
| `examples/verify_reconstruction.py` | 0 | 20 materials; `incompatible_pairs_rejected = 20`; `minimum_drained_eigenvalue = 1.8415045063808817` |

### 3.3 Manuscript numeric claims vs recorded data

| Claim in manuscript | Recorded value | Verdict |
|---|---|---|
| 186 named checks; 65 per-state identities (5×13) | 186 total; 65 `legacy_state*`; 67 rechecked | ✓ |
| largest constitutive identity error `2.5e-9` | `2.4549890331732928e-09` | ✓ |
| 273 finite states across 13 mineral stiffnesses | `273`, `13` | ✓ |
| reference Biot components 0.7000 / 0.7583 / 0.7917 | `0.7 / 0.75833 / 0.79167` (my recompute + `experiments.json`) | ✓ |
| probe worst abs. difference `4.9e-15` | `4.884981308350689e-15` | ✓ |
| conformal cross-check `1.9e-14` | `1.87436871579294e-14` (σ11) | ✓ |
| peak centre pressure `6.28e-5 / 5.10e-5 / 3.95e-5`; `5.13e-5` coupling-off | `6.2802893621e-05 / 5.1021552208e-05 / 3.9461330e-05 / 5.1325507554e-05` | ✓ |
| "each peak coincides with the final recorded state" | `peak == final` in `figures/fe_fabric_mandel_peak.csv` | ✓ |
| `nx=20, dt=1e-3` pressure discrepancy `≈3.2e-3` | `0.003220919735602341` (`nonlinear_load_0.0001`) | ✓ |
| deck integrity for the fabric runs (`fabric_coupling=0` for the "coupling off" run, `fabric_angle=0/45/90`) | confirmed in each `provenance.json` `command_overrides` | ✓ |

The manuscript's scoping is honest and matches the evidence: the finite-load, rotated-anisotropy,
partial-drainage and fabric-coupled runs are labelled demonstrations, and `site/evidence.json`
records `finite_deformation: pending`, `physical_validation: not_performed`. I found no overclaim in
the constitutive or verification sections.

---

## 4. Findings

### Required

**R1 (minor, correctness of a reported quantity). The recorded/plotted `ln_h` is the negative of the
manuscript's `ln h`.**
`moose_app/include/utils/FabricLaw.h:599` reports `s.ln_h = xi / std::sqrt(1.5)`, where `xi` is the
coefficient of the basis vector `e[1] = √(3/2)(m⊗m − I/3)` in `E_d`. The manuscript
(`sections/pore_fabric.tex`, eqs. `fabric-transverse-h`, `fabric-transverse-strain`) defines
`E_d = (ln a/3)I + ln h (½I − 3/2 m⊗m)`, and
`½I − 3/2 m⊗m = −√(3/2) e[1]` (verified numerically: Mandel vector `[-1, 0.5, 0.5, 0, 0, 0]`,
coefficient `−1.2247448713915892`). Hence `xi = −√(3/2) ln h`, so

```
reported ln_h = +xi/√(3/2) = − ln h      (paper convention)
```

This is not a matter of E_d's decomposition being ambiguous — the manuscript's two equations fix
`ln h` uniquely, and `FabricLaw.h`'s own header comment restates the same equation the code then
violates. Decisive numerical confirmation: for a pure transversely isotropic state
(`m ∥ X1`, `F = diag(1.01, 0.995, 0.995)`, `p = 0.02`, coupling 0.4) the unimodular fabric
`H = (det G)^{-1/3}G` has eigenvalues `(0.99449516, 0.99449516, 1.01110126)`; the transverse
eigenvalue is `h = 0.99449516`, i.e. `ln h = −0.00552004`, while the material reports
`ln_h = +0.00552004`.

Propagation: `moose_app/src/materials/FabricMaterial.C:67,105` (property `ln_h`),
`build/fabric/fabric-verification.json` (`ln_h` fields), `figures/fe_fabric_probe.csv` (`ln_h`
column), and panel (c) of `fig:fe-fabric-probe` (`sections/finite_elements.tex`), whose caption
calls the plotted quantity the deviatoric distention. `examples/verify_fabric.py` computes the same
`x[1]/√1.5`, so the "independent re-implementation" reproduces the flipped convention and cannot
detect it.

Required correction: either flip the sign in `FabricLaw.h:599`, or define the reported scalar
explicitly (e.g. as `m·dev(E_d)·m = −ln h`) in the material documentation, the figure caption and
the data dictionary. Nothing physical (B, stresses, energies, storage) depends on this sign; the
model's responses are unaffected.

**R2 (minor, reproducibility of a published panel).** Panel (c) of `fig:fe-fabric-probe` is built
from `fabric_probe_a0/a45/a90`, which are read by `examples/plot_fabric_results.py`
(`DEFAULT_RUNS = .agent-runtime/anisotropic-fabric-goal-2026-09-20/runs`, a path absent from the
snapshot and from the supplement archive). Running the documented command
`python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots` from
the frozen artifact succeeds but records
`{"family": "fabric_probe_a0", "reason": "Recorded scalar history is absent"}` (likewise `a45`,
`a90`) and draws "Shape-response probes absent", so the regenerated figure differs from the
manuscript's. Only the derived rows in `figures/fe_fabric_probe.csv` survive. The
code-and-data-availability sentence in `sections/experiments.tex` ("together with the recorded run
histories those scripts read") is therefore broader than what ships — `tools/package_numerical_supplement.py`
(`FABRIC_RUN_CASES`) ships the probe/mandel families but not the shape family. Required correction:
ship the three shape-probe run histories, or narrow the sentence to name the families that ship.

### Optional

**O1 (clarity).** The embedded distention stiffness is not a general transversely isotropic
`D`. `FabricLaw.h` lists five moduli, but its five-direction basis omits the in-plane shear
direction `sym(p1,p2)`, so `D^+` has rank 5 in the six-dimensional symmetric-tensor space and that
mode is frozen to the mineral compliance. `sections/pore_fabric.tex` contrasts "a full-rank `D`" with
the conformal rank-one case; stating explicitly which modes the implemented `D` leaves frozen would
make the two statements agree on their face. The manuscript already limits itself to "the
two-parameter energy used in `sec:fe-fabric`", and the recorded `coupling=0` results (spherical `B`,
transversely isotropic `C^d`) are exactly what this restricted `D` implies, so this is presentational.

**O2 (verification depth).** `examples/verify_fabric.py` is a faithful transcription of the
`FabricLaw.h` formulas (same basis construction, same equilibrium `(Dd+φG)x = φ(g + p√3 ê1)`, same
`ln_h` convention). It verifies the implementation but shares the modeling conventions, which is why
R1 passes both. A short equation-level check of the extraction conventions (or a note in the
`sec:fe-fabric` wording that the agreement is an implementation check, which it already calls a
"re-implementation") would close that gap.

**O3 (evidence wording).** `main.tex:556–557` states the `nx=20, dt=1e-3` residual is "dominated by
the fixed-step backward-Euler temporal error rather than by an irreducible model discrepancy",
whereas `site/evidence.json` calls the same number "a discretization floor". The refinement runs that
support it (`linear_time_0.001`/`0.002`: `3.658e-3` vs `7.104e-3`, ratio 1.94, first order in `dt`)
are linear rather than finite-load nonlinear, so the attribution carries an inference. The
manufactured-solution temporal orders (`difference_orders` 0.98–1.40 at `nx=16/32/64`) do justify
first-order backward-Euler error, so the claim is defensible; aligning the two sentences would be
cleaner.

---

## 5. Verdict

The frozen snapshot is intact (534/534 hashes). The mathematics is correct: I re-derived the
kinematics, the virtual work and equivalent energy, the mineral-volume equation, the drained
compliance restriction, the explicit finite Biot tensor, and the tensorial-distention extension
(work conjugate, equilibrium, compliance relaxation, transverse isotropy) and found no error in any
of them. The MOOSE implementation matches those equations: my independent from-scratch
re-implementation reproduces every recorded fabric field, the shipped suites re-run clean
(186/273/20 checks, fabric worst difference `4.885e-15`), and every quantitative claim in the
manuscript matches the recorded data, with the finite-load and fabric-coupled runs honestly labelled
as demonstrations rather than verification or validation. Two small but real corrections remain: the
`ln_h` diagnostic and the panel-(c) data it feeds are the *negative* of the manuscript's `ln h`
(R1), and the shape-probe run histories behind panel (c) are not shipped, so that panel cannot be
regenerated and the availability sentence overstates what the artifact contains (R2). Neither
affects any constitutive result.

VERDICT: MINOR REVISION

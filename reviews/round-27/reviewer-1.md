# Round-27 Independent Review — Reviewer 1 (mathematics / correctness)

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work* (J. T. Foster)
**Frozen snapshot:** `.agent-runtime/review-snapshots/round-27`
**Snapshot ID (declared):** `c5050c77dd04628f149ddc417cce99eb6b53c4315884974efc6331c3267eda5e`
**Declared file count:** 591

Working method: the snapshot was copied to `/tmp/r27-rev1` and all work was performed
there (read-only against the snapshot and the repository tree). Every shipped verification
script was executed from the copy; every quoted manuscript number was either regenerated
from the shipped scripts/artifacts or re-derived independently in a scratch script written
for this review. No other reviewer's report and no prior-round verdict was read.

---

## 1. Snapshot integrity

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` vs declared `SNAPSHOT_ID` | **match** (`c5050c77…a5e`) |
| Manifest entries re-hashed by me | **591 / 591 OK** |
| Missing files | 0 |
| Hash mismatches | 0 |
| Extra files not in manifest | 1 — `SNAPSHOT_ID` (expected: it is the digest declaration, not a payload) |
| `site/scientific-snapshot.json` pinned hashes | **47 / 47 OK**, 0 missing, 0 mismatched |
| `site/evidence.json` pinned `path`/`sha256` pairs | **41 / 41 OK** |
| `build/anisotropic-biot-2026-09-20-v2.zip` `manifest.json` payload hashes | **68 / 68 OK**, 0 missing, 0 mismatched, no unlisted payload files |
| `build/main.pdf` | present, 33 pp., LuaTeX, 2.80 MB; `pdftotext` extraction consistent with `sections/*.tex` |

The snapshot re-hashes clean. (`cp -r` preserved the read-only bits; I relaxed permissions
only inside `/tmp/r27-rev1` so the shipped scripts could write their reports into the copy.
Nothing was written inside the snapshot or the repository tree except this one report.)

---

## 2. Independent mathematical re-derivation

I re-derived the new results from scratch rather than reading them off the manuscript.

### 2.1 Distention kinematics and the fabric tensor `H`

* `A = R_A G^{1/2}`, `G = A^T A`, `a = det A = (det G)^{1/2}`, `J = a J̄` — consistent.
* `H = (det G)^{-1/3} G = a^{-2/3} G`, so `det H = 1` and `G = a^{2/3} H`. Correct: the
  unimodular split is exact and `H` is SPD whenever `G` is.
* `C̄ = F̄^T F̄ = F^T R_A G^{-1} R_A^T F` — verified by direct substitution of
  `F̄ = G^{-1/2} R_A^T F`.
* Volume-only specialization `G = a^{2/3} I` gives `A = a^{1/3} R_A`,
  `F̄ = a^{-1/3} R_A^T F`, `C̄ = a^{-2/3} C`, recovering `eq:spherical-distention` /
  `eq:conformal-mineral-metric` exactly.
* Claim "its eigenvalues are the squared principal shape ratios of the distention":
  **correct**. Eigenvalues of `H` are `(det A)^{-2/3} ×` (squared singular values of `A`),
  i.e. the squared principal stretches normalized to unit determinant.

### 2.2 Transverse isotropy of the fabric (`eq:fabric-transverse-h`, `eq:fabric-transverse-strain`)

For `H = h^{-2} m⊗m + h(I − m⊗m)` I verified independently (scratch NumPy, three values of
`ln h` at four fabric angles):

* `det H − 1 = 0` to ≤ 2.2e-16,
* eigenvalues of `H` are exactly `{h^{-2}, h, h}`,
* `E_dis = (ln a)/3 · I + ln h (½ I − 3/2 m⊗m)` satisfies `exp(2 E_dis) = a^{2/3} H`
  to ≤ 2.2e-16 and `det G = a²` to ≤ 2.2e-16.

The stated transformation of the reported scalars is also correct: with the fabric basis
`e₁ = I/√3`, `e₂ = √(3/2)(m⊗m − I/3)`, one has `½ I − 3/2 m⊗m = −√(3/2) e₂`, hence
`x₁ = ln a/√3` and `ln h = −x₂/√1.5` — the same convention as `moose_app/include/utils/FabricLaw.h`.

**On the flagged point — `ln h` versus an "eigenvalue ratio".** `ln h` is the logarithm of
the unimodular *transverse* fabric eigenvalue `h = e^{ln h}`, exactly as the manuscript
states (`sections/pore_fabric.tex`: "the reported shape scalar is the logarithm of the
unimodular transverse fabric eigenvalue `h = e^{ln h}`, not a projection of it"). It is **not**
an eigenvalue ratio: the eigenvalue ratio (largest/smallest) of `H` is `h^{-3}`, whose
logarithm is `−3 ln h`. For the recorded `h` of `fabric_probe_coup_a45`, `ln h = 3.5695e-4`
while `ln(h^{-3}) = −1.0708e-3` and `h^{-3} = 0.9989297`. The manuscript text, `site/evidence.json`,
and `tools/register_fabric_evidence.py` all use the correct wording; one shipped source file
does not (see Finding R1).

### 2.3 Virtual work, phase balance, and pressure conjugacy

* `δF F^{-1} = (1/3) I δ ln a + δR_A R_A^T + R_A(δF̄ F̄^{-1})R_A^T`; `δR_A R_A^T` is skew and
  contracts to zero against symmetric `τ'`; the fluid-pressure work cancels, leaving
  mineral work weighted by `φ_s0`. All correct.
* `τ' = φ_s0(τ̄_s + p J̄ I)` follows from `J φ_s = φ_s0 J̄`; sign convention (positive `p`
  = compression, `σ = φ_s σ̄_s − (1−φ_s) p I`, `σ = −p I` unjacketed) is Coleman–Noll
  consistent and reproduces the finite unjacketed identities in `sections/limits.tex`.
* `τ' = (∂W_A/∂ln a) I + φ_s0 dev τ̄_s` with `∂W_A/∂ln a = (φ_s0/3) tr τ̄_s + φ_s0 p J̄`:
  substituting the second into the first reproduces `eq:constitutive-kirchhoff-phase-stress`
  including shear. Verified symbolically.

### 2.4 Drained compliance restriction (`eq:drained-stiffness-restriction`, `eq:drained-compliance-restriction`)

Re-derived analytically. With `β = 1 − K/(φ_s0 K_s)` and `W_A = K/(2β)(ln a)²`:

* equilibrium ⇒ `ln a = (1/(3K_s)) β I:C_s:ε`, matching `eq:drained-anisotropic-distention`;
* `dσ/dε = φ_s0 C_s − (φ_s0/(9K_s)) β (C_s:I)⊗(C_s:I)`, matching `eq:drained-stiffness-restriction`;
* Sherman–Morrison with `A = φ_s0 C_s`, `g = β/(9 φ_s0 K_s)`, `v = A:I` gives
  `(C^d)^{-1} = (φ_s0 C_s)^{-1} + (β/(9K)) I⊗I`, matching `eq:drained-compliance-restriction`
  (the Sherman–Morrison denominator is `K/(φ_s0 K_s) ≠ 0`).

I also confirmed this numerically **by direct energy condensation**, minimizing
`½φ_s0(ε−E):C_s:(ε−E) + ½E:D:E` over `E ∈ range(D)` and central-differencing the condensed
stress. Agreement with the closed form was ≤ 4.0e-12 for a coupled case (`Dd = [[1,0.4],[0.4,1]]`,
30°), an uncoupled case (`[[2,0],[0,0.7]]`), and a negative-coupling case (45°, `−0.35`).

### 2.5 Anisotropic Biot tensor (`eq:anisotropic-biot-explicit`)

Re-derived. The key identity is `I:C_s:dev ε = dev(C_s:I):ε`, hence
`(∂/∂F[I:C_s:dev ε])F^T = F[∂log C/∂C : dev(C_s:I)]F^T` by the symmetry of the Fréchet
derivative of `log C`. Substituting into the differentiated mineral equation reproduces
`eq:anisotropic-biot-explicit` with the stated prefactors, including the
`φ_s0`-weighted `(1−K/(φ_s0 K_s))` factor and the `J̄/(J[K_s + (1−K/(φ_s0K_s)) p J̄])` denominator.
The claim that `dev(C_s:I) = 0` for cubic symmetry is correct (`C_s:I = (C_11+2C_12) I`),
so `B` stays spherical while the shear response is anisotropic.
`B` symmetry follows from the self-adjointness of the log-derivative, as claimed.

### 2.6 Reference Biot, storage, and the reduced-distention basis

* `B_0 = I − C^d:C_s^{-1}:I`; isotropic limit `(1 − K/K_s) I`. Correct.
* `S_s = −φ_s0 ∂J̄/∂p|_{F=I,p=0} = (φ_s0/K_s)(1 − K/(φ_s0K_s))`; the compatibility form
  `φ_s0 I:C_s^{-1}:I − I:C_s^{-1}:C^d:C_s^{-1}:I` reduces to the same expression
  (`= φ_s0/K_s − K/K_s²`). Verified symbolically.
* Fabric basis: independently built `D` on `span(e₁,e₂)`; found `rank D = 2`,
  eigenvalues `{0.6, 1.4}` for `Dd = [[1,0.4],[0.4,1]]` (the complementary four modes are 0),
  `D:e₃ = 0` (4.4e-17), `D:e₆ = 0` (exact), and invariance under a 47° rotation about `m`
  to 1.1e-16. This confirms the manuscript's transversely isotropic, rank-two characterization.
* Consequence the manuscript states (and which is easy to get wrong): with an **isotropic**
  mineral and **zero volume–axial coupling**, `B` is spherical for *any* axial modulus. I
  confirmed this independently — in the `{e_i}` eigenbasis, `C^d:I = c₁ I` with
  `c₁ = [1/(3φ_s0K_s) + 1/k_v]^{-1}`, which is independent of `k_a`; so
  `B = [1 − c₁/(3K_s)] I`. The recorded probes (`fabric_probe_softaxial`,
  `fabric_probe_stiffaxial`, `fabric_probe_a*`) all show zero anisotropy, consistent.

---

## 3. Reproduction of every quoted number

All scripts were run from the temp copy; all manuscript values were regenerated.

### 3.1 Pore-fabric material-point numbers (`sections/finite_elements.tex` §fe-fabric)

`examples/verify_fabric.py`, worst probe-field absolute difference **4.885e-15**:

| Manuscript | My value | OK |
|---|---|---|
| H reconstruction differs by `2.2e-16` | 2.220446e-16 | ✔ |
| `det H − 1 = −3.3e-16` | −3.330669e-16 | ✔ |
| eigenvalues `h^{-2}, h, h` | `[0.99928635, 1.00035701, 1.00035701]` for `h = e^{3.5695e-4}` | ✔ |
| `‖D:e₃‖ = 1.6e-16` | 1.582311e-16 | ✔ |
| `D:e₆ = 0` | 0.0 | ✔ |
| rotation invariance `2.5e-16` | 2.496536e-16 | ✔ |
| NumPy re-implementation `4.9e-15` | 4.885e-15 | ✔ |
| volume-only limit vs `ConformalMaterial` `1.9e-14` | 1.874e-14 | ✔ |

### 3.2 Conformal suite (`sections/experiments.tex`)

| Manuscript | My value | OK |
|---|---|---|
| 186 named checks | 186 | ✔ |
| 65 per-state identities = 5 states × 13 | 5×13 = 65 verified by reading the check list; `legacy_identities_rechecked = 67 = 65 + 2` reference relations | ✔ |
| largest constitutive identity error `2.5e-9` | 2.454989e-9 | ✔ |
| second-order step refinement | energy/pore-volume/pressure orders ≈ 2.000 | ✔ |
| spherical-gauge: 273 states, 13 stiffnesses | 273, 13 | ✔ |

### 3.3 Manufactured solution and consolidation

| Manuscript | My value | OK |
|---|---|---|
| spatial order p `2.00` and `2.00` | 1.9966, 2.0008 | ✔ |
| spatial order ux `2.99` and `2.96` | 2.9917, 2.9585 | ✔ |
| spatial order uy `3.00` and `2.96` | 2.9983, 2.9600 | ✔ |
| temporal successive-difference orders 0.98–1.40 at nx=16/32/64 | 0.9783 … 1.3969 (nx16: 1.093/0.978/1.015; nx32: 1.397/1.018/1.125; nx64: 1.396/1.076/1.252) | ✔ |
| linear step refinement `3.7e-3`, `7.1e-3`, ratio `1.94` | 3.6580e-3, 7.1039e-3, ratio 1.9420 | ✔ |
| finite-load pressure floor `3.2e-3` at nx=20, dt=1e-3 | 3.220920e-3 | ✔ |

### 3.4 Coupled pore-fabric demonstration

`figures/fe_fabric_mandel_peak.csv` (peak = final recorded state in every case):

| Manuscript | My value | OK |
|---|---|---|
| uncoupled `3.62e-5` | 3.616393e-5 | ✔ |
| 0° `4.36e-5` | 4.362759e-5 | ✔ |
| 45° `4.99e-5` | 4.990085e-5 | ✔ |
| 90° `5.52e-5` | 5.521105e-5 | ✔ |

`figures/fe_fabric_contours.csv` (peak at final time, max on `X₁=0`):

| Manuscript | My value | OK |
|---|---|---|
| iso `3.61e-5` | 3.606194e-5, `p_max_x = 0` | ✔ |
| 0° `4.35e-5` | 4.349137e-5, `p_max_x = 0` | ✔ |
| 45° `4.97e-5` | 4.973659e-5, `p_max_x = 0` | ✔ |
| 90° `5.50e-5` | 5.503135e-5, `p_max_x = 0` | ✔ |
| displacement `5.18e-5` iso | 5.182640e-5 | ✔ |
| displacement `5.14e-5` 0° | 5.137155e-5 | ✔ |
| displacement `2.38e-5` 45° | 2.381836e-5 | ✔ |
| displacement `5.26e-5` 90° | 5.258692e-5 | ✔ |

### 3.5 Constitutive examples and reference limits (`sections/experiments.tex`, `sections/limits.tex`, `sections/finite_elements.tex` §fe-reference-problems)

| Manuscript | My value (independent computation) | OK |
|---|---|---|
| `K_s = 28 K_*` | 28.0 | ✔ |
| reference Biot `0.7000`, `0.7583`, `0.7917` | 0.700000, 0.758333, 0.791667 | ✔ |
| isotropic comparison `μ_s = 16.8 K_*` (mean of five deviatoric Mandel modes, halved) | deviatoric trace 168 / 5 / 2 = 16.8 | ✔ |
| reference Biot coefficient `0.6` | 0.6 | ✔ |
| drained shear modulus `G = 0.75` | `φ_s0 μ_s = 0.75` | ✔ |
| total storage `17/80` | 0.2125 | ✔ |
| compliance restriction satisfied for both experimental materials | max residual 8.7e-18 | ✔ |
| drained volumetric stiffness = `K = 7` | 7.0 | ✔ |

### 3.6 Supporting evidence artifacts

| Item | Value | OK |
|---|---|---|
| fluid EOS/reference-mass checks | 110 checks, max scaled error 8.0867e-9 (manuscript/evidence `8.09e-09`) | ✔ |
| Mandel reference self-checks | 38, all passed, central overshoot ratio 1.0546586 (= 5.4659 %) at `t = 0.01516535` | ✔ |
| C++ vs independent Python constitutive | 41 finite states, value error 6.3949e-14 | ✔ |
| reconstruction suite | compliance 1.4e-16, reference Biot 2.2e-16, unjacketed 5.1e-14, 20 materials, 20 incompatible pairs rejected | ✔ |
| supplement archive manifest | 68/68 payload hashes OK | ✔ |

No quoted numerical claim in the manuscript was found unsupported or unreproducible.

---

## 4. Findings

### REQUIRED corrections

**R1 — `moose_app/include/utils/FabricLaw.h`, lines 19–20 (wrong description of `ln h`).**
The comment reads

```
// reconstructed fabric H = exp(2 E_d) equals h^{-2} m (x) m + h (I - m (x) m)
// with h = exp(ln h), so the reported ln_h IS the unimodular fabric eigenvalue
// ratio.
```

`ln h` is the logarithm of the unimodular *transverse* fabric eigenvalue `h = e^{ln h}`; it
is not an eigenvalue ratio. The eigenvalue ratio of `H` is `h^{-3}` (e.g. `h^{-3} = 0.9989297`,
`ln(h^{-3}) = −1.0708e-3`, against `ln h = 3.5695e-4` for the shipped `fabric_probe_coup_a45`
state). This sentence contradicts the manuscript's own statement
(`sections/pore_fabric.tex`: "the reported shape scalar is the logarithm of the unimodular
transverse fabric eigenvalue `h = e^{ln h}`"), contradicts the equally correct wording in
`site/evidence.json` and `tools/register_fabric_evidence.py`, and is shipped twice over —
in the repository and inside the PDF-embedded supplement archive
(`build/anisotropic-biot-2026-09-20-v2.zip → moose_app/include/utils/FabricLaw.h`).
*One-line fix:* replace "the unimodular fabric eigenvalue ratio" with "the logarithm of the
unimodular transverse fabric eigenvalue". No computed quantity changes; this is a
documentation correctness defect only, but it concerns the sign/shape convention that
`verify_fabric.py` explicitly declares itself to share, so a supplement reader would be
misled about the meaning of the one scalar the new section introduces.

### OPTIONAL corrections

**O1 — Misleading artifact key name.** `examples/verify_fabric.py` line 272 emits the report
key `H_eigenvalue_ratio_expected`, whose value is the eigenvalue *triple* `[h^{-2}, h, h]`,
not a ratio; it propagates into `build/fabric/fabric-verification.json` and
`site/reports/fabric-verification.json` (line 441). Renaming it to
`H_eigenvalues_expected` removes the same "ratio" misnomer from machine-readable output.

**O2 — Notation overload (already disambiguated, but worth one more word).** The manuscript
uses `e₁,…,e₆` for the fabric-adapted basis while `eq:example-mineral-stiffness` uses Mandel
component indices; the text does explicitly say the labels are not the Mandel indices, so
this is a readability nit only.

---

## 5. Overall assessment

The snapshot is cryptographically clean (591/591 manifest entries, 47/47 and 41/41 pinned
site hashes, 68/68 archive payload hashes). The mathematics is sound: I independently
re-derived the unimodular fabric split, the transverse-isotropy relations, the drained
stiffness/compliance restriction (analytically and by direct energy condensation), the
explicit anisotropic Biot tensor, the reference Biot and storage relations, and the
rank-two transversely isotropic structure of the retained distention stiffness, and found no
tensor-algebra error, wrong index, wrong sign, dimension mismatch, or claim unsupported by
an equation. Every quoted numerical value I could locate — fabric residuals, MMS spatial and
temporal orders, the step-refinement ratio and errors, the finite-load floor, the coupled
peak pressures and contour extrema, the reference Biot components, storage, drained moduli,
the 186/273/38/110/41-count verification suites, and the Mandel overshoot — reproduces from
the shipped scripts and recorded artifacts. The single defect is the `ln h` description in
`FabricLaw.h`, which is exactly the "eigenvalue ratio" misstatement the manuscript itself
avoids; it is a located, one-line, documentation-only fix.

VERDICT: MINOR REVISION

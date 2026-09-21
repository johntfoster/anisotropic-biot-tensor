# Round 24 — Reviewer 1 (mathematics / correctness)

Independent manuscript-acceptance review of the anisotropic pore-fabric extension.
Scope: the mathematics of `sections/pore_fabric.tex`, `sections/finite_elements.tex`,
`sections/limits.tex`, `sections/stress_reconstruction.tex`,
`sections/logarithmic_derivative.tex`, and the shipped `moose_app/include/utils/FabricLaw.h`
(+ `ConformalLaw.h`, `examples/verify_*.py`, `fe-evidence/`, `validation/`).

I did not read `reviews/round-24/reviewer-2.md`, `reviewer-3.md`, or any prior-round
report. I did not modify the snapshot or the live tree; all scripts were run from a
`mktemp -d` copy.

---

## 1. Snapshot and integrity

| Check | Result |
|---|---|
| Declared `SNAPSHOT_ID` | `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423` |
| `sha256(source-manifest.json)` recomputed | `1dea9e…b423` — **matches declared ID** |
| `SNAPSHOT_ID` file contents | identical to declared ID |
| Manifest entries | 591 |
| Files re-hashed against manifest | **OK 591, MISSING 0, MISMATCH 0** |

Integrity is clean. The frozen tree is self-consistent and no manifest entry has drifted.

Environment: `moose` conda env (`python 3.14.0`, `numpy 2.4.2`, `scipy 1.17.1`),
`MOOSE_DIR=~/.local/moose`.

---

## 2. What I re-derived independently

I re-derived each item from the manuscript equations, then checked the shipped code and
the recorded evidence against that derivation. In addition to the shipped scripts I wrote
my own from-scratch NumPy implementation (`/tmp/r1own/indep.py`, `final_checks.py`,
`storage_check.py`, `cdcheck.py`, `exp_checks.py`).

### 2.1 Distention kinematics — **consistent**

`A = R_A G^{1/2}`, `G = A^T A`, `a = det A = (det G)^{1/2}`, `F = A F̄`, `J = a J̄`,
`C̄ = F^T R_A G^{-1} R_A^T F`. I verified the conformal specialization
`G = a^{2/3} I`:

- `G^{1/2} = a^{1/3} I`; `A = a^{1/3} R_A`; `F̄ = a^{-1/3} R_A^T F`; `C̄ = a^{-2/3} C`.
- Numerically (three positive `a`, random `R_A`, non-symmetric `F`): `|det A − a| ≤ 4.4e-16`,
  `|J − a J̄| = 0`, `|C̄ − a^{-2/3} C| ≤ 5.6e-16`, `|A^T A − G| ≤ 5.8e-16`. Exact reduction. OK.

### 2.2 Retained basis, `E_dis` decomposition, `H` eigenvalues — **consistent**

- `e1 = I/√3` (Frobenius norm 1) and `e2 = √(3/2)(m⊗m − I/3)`: I confirmed the prefactor
  `√(3/2)` equals `(m⊗m − I/3)/‖m⊗m − I/3‖`, the two directions are orthonormal in the
  Mandel/Frobenius metric (`e1:e1 = 1`, `e2:e2 = 1`, `e1:e2 = 2.8e-17`), and
  `1/2 I − 3/2 m⊗m = −√(3/2) e2`.
- `H = a^{-2/3} G`, `det H = 1`. With `G = a^{2/3}[h^{-2} m⊗m + h(I − m⊗m)]`:
  `exp(2 E_dis) − G` ≤ 4.4e-16 for `h ∈ {0.8, 1.3}`; `det H − 1 ≤ 5.6e-16`;
  eigenvalues of `H` = `{h^{-2}, h, h}` exactly. The eigenvalue/squared-shape-ratio
  statement holds.
- The implemented scalar convention is the manuscript's: `ln a = √3 x₁`,
  `ln h = −x₂/√(3/2)`; I independently reproduced the recorded `ln_a`, `ln_h` values.

### 2.3 Equilibrium and the `√3` pressure source — **implemented operator is correct**

Minimizing `W_dis(E_d) + (φ_s0/2)(ε − E_d):C_s:(ε − E_d) + φ_s0 p tr(ε − E_d)` over
`E_d = x₁e₁ + x₂e₂` gives

```
(Dd + φ_s0 G) x = φ_s0 g + φ_s0 √3 p ê₁ ,   G_ij = e_i:C_s:e_j ,  g_i = e_i:C_s:ε .
```

The pressure source is `φ_s0 √3 p` on `e₁` only (from `tr e₁ = √3`) and **vanishes on the
traceless `e₂`** (from `tr e₂ = 0`). `FabricLaw.h` builds exactly this operator and RHS:
`solve = inv(Dd + phi*G)`, `x_i = phi*√3*p*solve[i][0] + Σ_j phi*solve[i][j]*g_j`.
The adiabatic (pressure) term `φ_s0 p J̄` contributes `−φ_s0 p √3 δ_{i1}` at the reference
state, consistent with the code's potential. OK.

### 2.4 Compliance restriction and Moore–Penrose inverse — **correct**

`(C^d)^{-1} = (φ_s0 C_s)^{-1} + D^+` follows from the minimization
(`σ = φ_s0 C_s:(ε − E_d)` ⟹ `ε = (φ_s0 C_s)^{-1}σ + D^+σ`). `FabricLaw.h` computes
`cd = inv(inv(φ Cs) + Dp)` with `Dp = Σ_{i,j≤2} (Dd^{-1})_{ij} e_i⊗e_j`, i.e. `D^+` is the
ordinary inverse on `range(D4)` and zero on the complement. I verified the four
Moore–Penrose conditions numerically (`D D⁺ D − D`, `D⁺ D D⁺ − D⁺`, both products
symmetric) hold to ≤ 6.4e-16, with `rank(D4) = rank(D⁺) = 2` on the 6-dimensional space.
OK.

### 2.5 Transverse isotropy / rotation invariance — **exact**

The reduced `D4` is supported on `span(e₁,e₂)⊗span(e₁,e₂)`. I confirmed
`D4:e₃ = 4.4e-17`, `D4:e₆ = 0` for `e₃ = (p₁⊗p₁ − p₂⊗p₂)/√2`,
`e₆ = √2 sym(p₁⊗p₂)`, and `‖R(φ) D4 R(φ)^T − D4‖ ≤ 3.8e-16` for a 37° rotation about `m`
(checked at fabric angles 0°, 30°, 45°, 90°). The Mandel representation of the rotation is
orthogonal to 2.6e-16. OK.

### 2.6 Storage coefficient (the round-23 R1 item) — **all three now agree**

| Site | Expression | Verdict |
|---|---|---|
| `FabricLaw.h` | `storage = (1−φ)/Kf + (φ/Ks)(1 − Kd/(φ Ks))`, `Kd = (1/9)I:C^d:I` | equals manuscript |
| `ConformalLaw.h` | `storage = (1−φ)/Kf + φ·α/Ks`, `α = 1 − K/(φ Ks)` | equivalent |
| `examples/verify_fabric.py` | `storage = (1−PHI)/KF + (PHI/KS)*(1 − Kd/(PHI*KS))`, `Kd = Cd[:3,:3].sum()/9` | mirrors both |

All three reproduce `(1−φ_s0)/K_f + S_s` with `S_s = (φ_s0/K_s)(1 − K/(φ_s0 K_s))`
(`sections/limits.tex`, eq. `reference-solid-storage`), where `K` is the drained bulk
modulus. `Kd` computed from `C^d` equals the deck's `K` in the conformal limit
(`Kd = 1.0` for `conformal_probe_ref`), so `ConformalLaw.h` and `FabricLaw.h` agree.

I additionally checked the manuscript's *definition*, `S_s = −φ_s0 ∂J̄/∂p|_{F=I,p=0}`,
against the closed form, using the exact deck parameters (`kv, ka, kc`, fabric angle):

| `(kv, ka, kc)` | angle | `−φ∂J̄/∂p` (direct) | closed form | rel. diff |
|---|---|---|---|---|
| 1, 1, 0 | 0/45/90° | 0.3135483871 | 0.3135483871 | 1.8e-16 |
| 1, 1, 0.2 | 0/45/90° | 0.3141970520 | 0.3141970520 | 1.8e-16 |
| 1, 1, 0.4 | 0/45/90° | 0.3161592506 | 0.3161592506 | 1.8e-16 |
| 5.4, 1, 0.4 | 45° | 0.2010590766 | 0.2010590766 | 2.8e-16 |

So the closed form is not merely a literal formula match: it is the actual reference
pressure derivative of the mineral volume, including with volume–axial coupling. `mass` **is**
in the compared fields (`FIELDS` in `verify_fabric.py` includes `"mass"`), the probe CSVs
carry a `mass` column, and the recorded masses agree with my independent values to 1e-17.
The code's `B` and `C^d` also reproduce the recorded Mandel components
(`cd[0][0] = 0.6903225806` iso, `1.2858720611` at 45°/coupled — exact match). **No disagreement remains.**

### 2.7 Script runs (from a writable copy) — **pass, numbers match text**

`examples/verify_fabric.py` (worst probe-field absolute difference **4.885e-15**) and
`examples/verify_conformal.py` (**186 checks passed**, `legacy_identities_rechecked = 67`,
`max_constitutive_identity_error = 2.455e-09`, second-order refinement on all three
tangents) both ran clean against the snapshot's recorded `fe-evidence/runs`. My fresh
`build/fabric/fabric-verification.json` is value-for-value identical to the shipped
`site/reports/fabric-verification.json`.

### 2.8 Every in-scope numeric quote reproduces

| Quote (manuscript) | Source | Reproduced |
|---|---|---|
| `D=0.75`, Biot `0.6`, storage `17/80` | reference problem `φ=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8` | `G=0.75`, `B₀=1−K/K_s=0.6`, `(1−φ)/K_f+S_s = 0.2125 = 17/80` |
| Biot components `0.7000, 0.7583, 0.7917` | `experiments.tex`, anisotropic `C_s`, `φ=0.6`, `K=7`, `K_s=28` | `0.7, 0.758333, 0.791667` |
| isotropic shear `16.8 K_*` | mean of the five deviatoric modes / 2 | `trace(P C_s P)/10 = 16.8` |
| MMS orders `p 2.00/2.00`, `u_x 2.99/2.96`, `u_y 3.00/2.96` | `fe_mms_convergence.csv`, `mms-convergence.json` | exact |
| temporal orders `0.98–1.40` | `mms-convergence.json` `difference_orders` | min 0.978, max 1.397 |
| step ratio `1.94`; `3.7e-3`, `7.1e-3` | `fe_mandel_refinement.csv` | 1.9421, 3.658e-3, 7.104e-3 |
| floor `3.2×10^{-3}` | `fe_load_limit.csv` | 3.2209e-3 |
| reconstruction `2.2e-16`; `det H−1 = −3.3e-16` | `verify_fabric` tensor_checks | 2.220e-16; −3.331e-16 |
| `‖D:e₃‖=1.6e-16`, `D:e₆=0`, rotation `2.5e-16` | same | 1.582e-16, 0.0, 2.497e-16 |
| worst diff `4.9e-15` | same | 4.885e-15 (attained on `solid_fraction`) |
| conformal reduction `1.9e-14` | conformal cross-check | 1.874e-14 |
| peaks `4.36/4.99/5.52e-5`, uncoupled `3.62e-5` | `fe_fabric_mandel_peak.csv` | 4.3628/4.9901/5.5211e-5, 3.6164e-5 |
| refined peaks `3.61/4.35/4.97/5.50e-5` | `fe_fabric_contours.csv` | 3.6062/4.3491/4.9737/5.5031e-5 |
| `u_mag` peaks `5.18/5.14/2.38/5.26e-5` | same | 5.1826/5.1372/2.3818/5.2587e-5 |
| `40×8` mesh, `1×0.1`, eleven snapshots | `fabric_contour_a45` deck (`nx=40, ny=8, dt=1.8e-4…3e-4, end 0.003`) | 11 timesteps; 6 times × 2 rows in `fe_fabric_diffusion.csv` |
| `186` checks / `2.5e-9` | `verify_conformal.py` | 186 / 2.455e-9 |
| `273` states across `13` stiffnesses | `tensor-verification.json` | 13 × 21 = 273 |
| Mandel `38` self-checks, overshoot `5.4659%` at `t = 0.01516535` | `mantel_reference.py` (`--self-check`) | 38 checks; `1.054658607`, `t = 0.015165352` |

---

## 3. REQUIRED items

**None.** I found no wrong equation, unreproducible number, or unsupported claim in scope.
Specifically: the kinematics, the retained basis and `exp(2E_dis) = G` identity, the
equilibrium operator with its `√3`/zero source split, the compliance restriction with the
Moore–Penrose inverse, the transverse isotropy, the storage coefficient, and every numeric
quote I could trace reproduce exactly.

---

## 4. Optional notes

1. **Storage identity is stronger than claimed.** The manuscript states `S_s` as a closed
   form; I verified it also equals the definition `−φ_s0 ∂J̄/∂p` at machine precision,
   including the volume–axial coupling. The text could say this explicitly, since it is the
   identity that closes the fluid-mass residual.
2. **`mass` is compared too.** `verify_fabric.py` includes `mass` among its compared fields,
   although `sections/finite_elements.tex` lists only `B_∥, B_⊥`, the distention strains,
   volume ratios, stresses, and solid fraction. Mentioning `mass` would make the
   storage-related comparison visible in the text.
3. **Wording: "rotates the fabric in the plane."** The coupled demonstrations prescribe a
   fixed fabric axis per deck (`fabric_angle` override) with the reference-state law
   (`linear_reference = true`); they are not within-run fabric evolution. The material is
   correctly described as evaluating the "reference-state" response, so this is clarity
   rather than a defect.

---

VERDICT: ACCEPT

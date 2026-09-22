# Round 36 — Reviewer 1 (derivation and correctness)

Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Frozen snapshot (read-only): `.agent-runtime/review-snapshots/round-36`
Declared `SNAPSHOT_ID`: `c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d`
Emphasis: derivation and correctness. All manuscript, evidence and code reads below are from the snapshot. Scratch work in `/tmp` only.

---

## 1. MANDATORY FIRST CHECKS

### Check 1 — declared SNAPSHOT_ID vs. manifest hash

Command (cwd = snapshot root):

```
$ cat SNAPSHOT_ID
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d
$ sha256sum source-manifest.json
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d  source-manifest.json
```

Both equal the declared value. **PASS.**

### Check 2 — re-hash every manifest path and walk the tree

Command (Python, cwd = snapshot root): load `source-manifest.json` (a flat `path -> sha256` object), recompute `sha256` of each listed path, then `os.walk('.')` the whole snapshot and diff the on-disk file set against the listed set.

```
entries listed in manifest: 608
re-hashed OK: 608
hash mismatches: 0
listed-but-missing: 0
files on disk (excl manifest/SNAPSHOT_ID): 608
present-but-unlisted: 0
```

608 entries listed, 608 re-hashed OK, 0 mismatches, 0 listed-but-missing, 0 present-but-unlisted. **PASS.**

### Check 3 — independence

I did not open, read, list, glob or find anything under the **working-tree** `reviews/` directory, and I did not open any other `.agent-runtime/review-snapshots/round-*` directory. I did not seek any other reviewer's report, verdict or acceptance count.

Self-report (transparent, no content exposure): the mandated tree walk of Check 2 necessarily enumerated the *snapshot's* file set, which contains one file under the snapshot's own `reviews/` (`reviews/README.md`, itself a manifest-listed entry). Only its path was materialised by the walk; its contents were not opened or read. No other reviewer artifact, verdict or acceptance count was seen. **No accidental exposure.**

---

## 2. Build/equation-number resolution

`build/main.log` resolves cleanly: `Output written on main.pdf (34 pages, 2808622 bytes)`; no undefined references, no multiply-defined labels, no missing citations (one benign `Underfull \hbox` in the bibliography). Equation numbers below are resolved from `build/main.pdf` (`pdftotext -layout`); all 106 numbered display equations are present and sequential (1–106, no gaps).

---

## 3. Re-derivation and numerical verification (seat scope)

I re-derived each item in the seat and verified it symbolically and, where possible, numerically (NumPy/SciPy in `/tmp`, independent of the authors' drivers).

### 3.1 Multiplicative decomposition and conformal specialization — CORRECT
- `F = A F̄`, `J = a J̄` (1) and `A = a^{1/3}R_A` (2) imply `C̄ = a^{-2/3}C` (3): substituting `F̄ = a^{-1/3}R_A^T F` gives `C̄ = a^{-2/3}F^T R_A R_A^T F = a^{-2/3}C`. ✓
- Virtual deformation (15) `δF F^{-1} = (1/3)I δln a + δR_A R_A^T + R_A(δF̄ F̄^{-1})R_A^T` reproduces exactly under `F = a^{1/3}R_A F̄`, `F^{-1} = F̄^{-1}R_A^T a^{-1/3}`. `δJ̄ = J̄ tr(δF̄ F̄^{-1})` (16) standard. ✓
- Skewness argument: `δR_A R_A^T` is skew, so its contraction with symmetric `τ'` vanishes. ✓

### 3.2 Volume-fraction-weighted stress and Coleman–Noll-type conjugacy — CORRECT
- Phase balance (7) `σ = φ_s σ̄_s − (1−φ_s)pI`; single-prime (8)–(9); Kirchhoff (10) `τ' = Jσ'`, `τ̄_s = J̄σ̄_s`; mixture-frame mineral Kirchhoff (11); weighted Kirchhoff balance (12) `τ' = φ_{s0}(τ̄_s + pJ̄I)`. All consistent with `Jφ_s = φ_{s0}J̄`.
- Energy conjugacy (13) `∂W_s/∂J̄|_F = −φ_{s0}p`, `P' = ∂W_s/∂F|_J̄`, `τ' = P'F^T`.
- Substitution (17) and its reduction to (18) verified: with the phase balance, `R_A^Tτ'R_A − φ_{s0}pJ̄I = φ_{s0}τ̂_s`, so `δW_s = (1/3)trτ' δln a + φ_{s0}τ̂_s:(δF̄ F̄^{-1})`. Fluid-pressure work cancels. ✓
- Energy re-differentiation check (21)–(22): `τ' = (∂W_A/∂ln a)I + φ_{s0}dev τ̄_s` and `∂W_A/∂ln a = (φ_{s0}/3)trτ̄_s + φ_{s0}pJ̄` recombine into (12) including shear. Verified independently by re-expressing (12). ✓
- Volumetric work form (23) `δW_s = (1/3)trτ' δln a + (φ_{s0}/3)trσ̄_s δJ̄` verified (uses `trτ̂_s/J̄ = trσ̄_s`). ✓
- Objectivity of `W̄_s` gives `W̄_s(a^{-1/3}R_A^T F) = W̄_s(a^{-1/3}F)` (20); `R_A` cancels from the energy — correct given left-rotation invariance of an objective mineral energy. ✓

### 3.3 Reduced energies and the finite-deformation Biot tensor — CORRECT
- (44)–(48): `W'' = W_s`, `W' = W'' + φ_{s0}pJ̄`; envelope/chain rule give `P' = ∂W'/∂F|_p = ∂W_s/∂F|_J̄ = P'' + φ_{s0}p ∂J̄/∂F|_p`. Sign verified. ✓
- (49) `σ = σ'' − pB`, `B = I − (φ_{s0}/J)(∂J̄/∂F|_p)F^T`: derived from `σ' = J^{-1}P'F^T`, `σ = σ' − pI`. ✓
- (50) `δ(J−φ_{s0}J̄)/J = B:(δF F^{-1})` verified via `δJ̄ = ((∂J̄/∂F)F^T):(δF F^{-1})`. ✓
- (51) implicit-derivative equation: differentiating the EOS (37) at fixed `p` gives `[K_s+(1−K/(φ_{s0}K_s))pJ̄] ∂ln J̄/∂F = (K/φ_{s0})F^{-T} − (1/3)(1−K/(φ_{s0}K_s)) ∂_F[I:C_s:dev ε]`. Coefficient algebra verified exactly. ✓
- (52) explicit `B`: substituting (51) into (49), and using `(∂_F[I:C_s:dev ε])F^T = F[∂log C/∂C : dev(C_s:I)]F^T`, reproduces (52) term-for-term. `dev(C_s:I)` is trace-free, so `I:C_s:dev ε = dev(C_s:I):ε`. ✓
- **Independent numerical test of (52):** I solved the EOS (37) for `J̄` by Brent root-finding at random finite `F` and `p`, formed `B` from full finite-difference `∂J̄/∂F`, and compared with the explicit (52). Using the example mineral stiffness of (83), `φ_{s0}=0.6`, `K=7`:

  ```
  trial 0: max|B_expl-B_num| = 4.388e-11   sym err=2.39e-18
  trial 1: max|B_expl-B_num| = 3.586e-11   sym err=3.47e-18
  trial 2: max|B_expl-B_num| = 5.660e-11   sym err=1.73e-18
  ```

  Agreement to the finite-difference floor, and `B` symmetric. ✓
- Symmetry/objectivity of `B` (Sec. 4, "The energy depends on material strain..."): verified analytically that `B(QF) = QB(F)Q^T` for all variations `δF` (the identity `B:(δFF^{-1}) = δ(J−φ_{s0}J̄)/J` holds for arbitrary `δF`, hence `Q^TB(QF)Q = B(F)`). ✓
- "`dev(C_s:I) = 0` gives spherical `B`": `C_s:I = 72,86,94` for the example; for cubic symmetry `C_s:I = (C_11+2C_12)I`, so the second term vanishes and `B` is spherical. ✓
- (53)–(56): `σ = (φ_{s0}/J)τ̄_s − (1−φ_s)pI`, `∂W'/∂p|_F = φ_{s0}J̄`, `∂σ/∂p|_F = −B`, integrated response. I checked `∂σ''/∂p − p∂B/∂p = 0` explicitly, which is what makes `∂σ/∂p = −B` exact at fixed `F`. ✓

### 3.4 Drained stiffness, compliance restriction, Moore–Penrose limit — CORRECT
- (40) `C^d = φ_{s0}C_s − (φ_{s0}/(9K_s))(1−K/(φ_{s0}K_s))(C_s:I)⊗(C_s:I)`: re-derived by minimising the reference quadratic energy over `ln a` at fixed `ε` and applying the envelope theorem to `σ^d = φ_{s0}C_s:ε̄`. Exact match. ✓
- (43) `(C^d)^{-1} − (φ_{s0}C_s)^{-1} = [(1−K/(φ_{s0}K_s))/(9K)]I⊗I`: verified **two ways** — (i) as a Sherman–Morrison inversion of (40) with the correct rank-one denominator `1 − β (9K_s/φ_{s0}) = K/(φ_{s0}K_s)`, giving `D^+ = (1−K/(φ_{s0}K_s))/(9K)·I⊗I`; and (ii) by direct numerical inversion of (40) for isotropic `C_s` (`K_s=50, μ_s=30, φ_{s0}=0.9, K=10`), which gives extra compliance `0.0086420 = 0.7778/90` exactly. ✓
- (42) `ε = (φ_{s0}C_s)^{-1}:C^d:ε + [(1−K/(φ_{s0}K_s))/(9K)]I(I:C^d:ε)` verified, using `I:C^d:ε = (K/K_s)I:C_s:ε` and (39). ✓
- (39) `ln a = (1/(3K_s))(1−K/(φ_{s0}K_s))I:C_s:ε` and (41) `ln a = (1−K/(φ_{s0}K_s))/(3K) I:C^d:ε` verified mutually consistent. ✓
- Moore–Penrose limit in the fabric section (78): I built the retained 2-D `D` on `span(e_1,e_2)`, formed `D^+` as the ordinary inverse on `range(D)` extended by zero, and numerically confirmed `D^+:D = P` (projector, err `1.5e-17`), that `D` and `D^+` annihilate `e_3,e_4,e_5,e_6` (norm `0`), and that `(C^d)^{-1} = (φ_{s0}C_s)^{-1} + D^+` reproduces the exact energy minimisation (`max|σ − C^d:ε| = 9.7e-9`, energy mismatch `3.5e-10` — minimiser tolerance limited). With the volume–axial coupling `k_c = 0` and an isotropic mineral, `B_0` is exactly spherical; with `k_c ≠ 0` it is transversely isotropic (`0.97036, 0.98063, 0.98063`). ✓ Consistent with the manuscript's Sec. 6.5/6.6 claims.
- Conformal reduction: with `D = c I⊗I`, `c = K/(1−K/(φ_{s0}K_s))`, (78) reduces to (43) exactly (`D^+ = (1−K/(φ_{s0}K_s))/(9K) I⊗I`). ✓

### 3.5 Reference response and limits — CORRECT
- (57) `B_0 = I − C^d:C_s^{-1}:I`: numerically reproduces the quoted reference Biot components **0.7000, 0.7583, 0.7917** for the example mineral. ✓ Isotropic form `(1−K/K_s)I` ✓.
- Solid storage (58)–(60): `S_s = −φ_{s0}∂J̄/∂p|_{F=I,p=0} = (φ_{s0}/K_s)(1−K/(φ_{s0}K_s))`; differentiating the EOS at `F=I, p=0` gives this. The "compatibility" form (60) `S_s = φ_{s0}I:C_s^{-1}:I − I:C_s^{-1}:C^d:C_s^{-1}:I` verified algebraically (`9β = S_s`) and numerically. ✓
- Isotropic limits (61)–(62): (61) is (37) with `dev(C_s:I)=0`; (62) is (52) with the shape term dropped. ✓
- Unjacketed path (63)–(64): choosing `a=1, J=J̄, C_s:ε = −pJI` makes the mineral Cauchy stress `−pI`, the EOS is satisfied **identically** (I verified the residual vanishes), the distention driving term `∂W_A/∂ln a = φ_{s0}pJ̄ + (φ_{s0}/3)trτ̄_s = 0`, and the phase balance gives `σ = −pI`, `φ_s = φ_{s0}`. ✓

### 3.6 Pore-fabric kinematics, basis, retained subspace, work-conjugate pair — CORRECT
- (65)–(68): `A = R_A G^{1/2}`, `a = (det G)^{1/2}`, `F̄ = G^{-1/2}R_A^T F`, `C̄ = F^T R_A G^{-1}R_A^T F`. All verified by direct substitution; conformal limit `G = a^{2/3}I` reduces to (2)–(3) exactly. ✓
- (69) `H = a^{-2/3}G`, `det H = 1` ✓; (77) additive strain `ε̄ = ε − E_dis` verified to first order at `F=G=I`. ✓
- (72) `S̄_dis = 2∂W_dis/∂G`, `δW_dis = (1/2)S̄_dis:δG`; the pair `(S̄_dis, G)` and `(S_dis, E_dis)` are correctly conjugate in the same frame and normalisation. ✓
- (73)–(74) fabric phase work: derived independently; contracting `τ'` against (73) removes the skew rotation increment and yields `τ̃:[δ(G^{1/2})G^{-1/2}] + φ_{s0}G^{1/2}τ̂_sG^{-1/2}:(δF̄ F̄^{-1})`. The ordering `G^{1/2}τ̂_sG^{-1/2}` (not its mirror) is the correct one for non-symmetric `δF̄ F̄^{-1}`; conformal limit recovers (18). ✓
- (68)/(67) linearisation and the basis `e_1 = I/√3`, `e_2 = √(3/2)(m⊗m − I/3)`, `e_3,e_4,e_5,e_6`: I verified the basis is orthonormal (`err 2.2e-16`) and that `e_2` is trace-free (`1.1e-16`) and equals the standard axial (degree-two) direction. `e_2` coincides with `(3m⊗m − I)/√6`, i.e. the Mandel axial direction up to the stated normalisation. ✓
- (79)–(82) transverse isotropy: `H = h^{-2}m⊗m + h(I−m⊗m)`, `det H = 1`; `E_dis = (ln a/3)I + ln h(1/2 I − 3/2 m⊗m)` and `exp(2E_dis) = a^{2/3}H` verified exactly. The reported shape scalar is exactly `ln h`. ✓

### 3.7 Logarithmic-derivative / spatial-stress conversions — CORRECT
- Appendix A: `τ = F[∂log C/∂C : T]F^T` from `δW = T:δε`; the spectral form `(lnλ_i−lnλ_j)/(λ_i−λ_j)` with repeated-eigenvalue limit `1/λ_i` is the standard self-adjoint Fréchet derivative of the matrix logarithm. ✓
- `∂log C/∂C : C = I` verified (maps the metric to the identity); `tr τ = tr T` verified via self-adjointness (`C:L_f[T] = L_f[C]:T = I:T`). ✓
- Same formula applied with `F̄`, `T = C_s:ε̄` gives `τ̂_s` in the true frame; (11) maps to the mixture frame. Consistent with (52)'s use.

### 3.8 Cross-checks against the snapshot's own recorded evidence
- `site/reports/tensor-verification.json`: `materials 13`, `total_states 273`, `max stress–strain commutator 2.61` — matches "273 finite states across 13 mineral stiffnesses" and "including noncoaxial states". ✓
- `site/reports/conformal-verification.json`: `checks_passed 186`, `legacy_identities_rechecked 67`, `max_constitutive_identity_error 2.45e-9`. The `checks` object has 186 named entries, named `legacy_state{0..4}_<13 identities>` = 65 per-state identities, plus 2 reference relations = 67. Matches the manuscript's "186 named checks", "65 per-state identities (five states times thirteen identities)", "two reference Biot and rank-one compliance relations", and "largest absolute error 2.5×10^-9". ✓ Also `noncoaxial_commutator 0.1816` corroborates the noncoaxial stress/strain check.
- `build/weighted-stress/reconstruction-verification.json`: `compliance 1.4e-16`, `reference_biot 2.2e-16`, `reference_storage 4.0e-12`, `isotropic_eos 2.2e-15`, `isotropic_biot 1.1e-16`, `unjacketed 5.1e-14` — consistent with the limits/storage checks in my seat. ✓
- `build/fabric/fabric-verification.json`: `tensor_checks` gives `H_reconstruction_max_abs_diff 2.22e-16`, `H_det_minus_one −3.33e-16`, eigenvalues `h^{-2},h,h`, `D4_e3_norm 1.58e-16`, `D4_e6_norm 0.0`, `rotation_invariance_norm 2.50e-16`, `worst_probe_abs_diff 4.88e-15`; `conformal_cross_check` gives differences `≤1.9e-14`. All match the numbers quoted in `sections/finite_elements.tex` (2.2e-16, −3.3e-16, 1.6e-16, 0, 2.5e-16, 4.9e-15, 1.9e-14). ✓
- `fe-evidence/mms-convergence.json`: space orders `ux 2.99/2.96`, `uy 3.00/2.96`, `p 2.00/2.00` — matches the manuscript's panel (a) numbers. ✓
- `figures/fe_load_limit.csv`: `pressure_max_normalized = 3.22e-3` at load `10^-4` — matches the stated `3.2×10^-3` floor. ✓
- `figures/fe_mandel_refinement.csv` (`linear_time_`): `3.658e-3` (Δt=10^-3) and `7.104e-3` (Δt=2×10^-3), ratio `1.942` — matches the stated `3.7×10^-3`, `7.1×10^-3`, "ratio 1.94, first order in Δt". ✓
- Example parameters: `I:C_s:I = 252 ⇒ K_s = 28K_*` ✓; the five deviatoric modes of `C_s` have mean `33.6K_*`, half `16.8K_*` ✓; the FE reference set gives drained shear `G = 0.75`, reference Biot `0.6`, total storage `17/80` ✓.

---

## 4. REQUIRED items

None. I re-derived every element of the assigned seat — the multiplicative decomposition and conformal specialisation (1)–(3), (15)–(16); the volume-fraction-weighted phase stress and its conjugacy (7)–(14), (17)–(18), (21)–(23); the reduced energies and finite-deformation Biot tensor (44)–(52), with (52) confirmed numerically against implicit differentiation of the EOS to ~1e-11; the drained stiffness and compliance restriction (39)–(43), including the Moore–Penrose limit (78); the reference/isotropic/unjacketed limits (57)–(64); the pore-fabric kinematics, basis, retained subspace and work-conjugate pair (65)–(69), (72)–(74), (77), (79)–(82); and the logarithmic-derivative conversions of Appendix A — and found **no incorrect derivation, no inconsistent normalisation, and no index or frame error**. I could not manufacture a required item without inventing one, which I will not do.

## 5. OPTIONAL notes

- **R1-O1 (`main.tex:217`, `main.tex:221`, `main.tex:224`, `main.tex:234`, `main.tex:258`).** The overbar carries three distinct meanings (mineral state reached by removing distention; mixture-frame representation of a stress; intrinsic per-phase density), plus a fourth for prescribed boundary data, and a hat for the true frame. The manuscript documents all of them explicitly, so this is a readability load rather than an ambiguity; a compact symbol table at first use would reduce reader effort.
- **R1-O2 (`sections/pore_fabric.tex:290–299`).** The compliance restriction is written with the Moore–Penrose inverse `D^+` and correctly reduces to the conformal rank-one result; the manuscript would be marginally clearer if it stated explicitly that `D^+` is taken with respect to the trace inner product on symmetric tensors, since the reduction depends on `e_1 = I/√3` being a unit vector in that product.
- **R1-O3 (`sections/limits.tex:74`).** "Distention stress vanishes" on the unjacketed path refers to the driving term `∂W_A/∂ln a` (which is zero at `a = 1`); since that scalar is not literally a stress in the conformal model, naming the quantity would remove a possible misreading. Verified correct as intended.
- **R1-O4 (`sections/finite_elements.tex`, `Scope of these results`).** The finite-load fabric and rotated-anisotropy runs are consistently labelled demonstrations, not verification. This is honest; no change requested.
- **R1-O5 (`main.tex:533`).** The cubic-symmetry remark (`dev(C_s:I)=0`) is correct; adding the explicit `C_s:I = (C_11+2C_12)I` identity (as used implicitly) would let a reader confirm the claim in one line.

---

VERDICT: ACCEPT

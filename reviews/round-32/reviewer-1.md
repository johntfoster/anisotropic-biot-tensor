# SIMULATED AI PEER REVIEW — Reviewer 1 of 3

**This is not journal peer review and confers no acceptance.**

- **Emphasis:** derivation and correctness.
- **Snapshot reviewed (frozen, read-only):** `.agent-runtime/review-snapshots/round-32`
- **Declared SNAPSHOT_ID:** `2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44`
- **Date:** 2026-09-21

---

## 1. Mandatory first checks

### Check 1 — manifest hash equals the declared SNAPSHOT_ID

Command (run from the repository root):

```
sha256sum .agent-runtime/review-snapshots/round-32/source-manifest.json
cat      .agent-runtime/review-snapshots/round-32/SNAPSHOT_ID
```

Result:

```
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44  .agent-runtime/review-snapshots/round-32/source-manifest.json
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44
```

Both the manifest hash and the `SNAPSHOT_ID` file hold the declared string exactly. **PASS.**

### Check 2 — re-hash every listed file and walk the tree

Command (from the snapshot root): a Python pass that loads `source-manifest.json`
(a flat `path -> sha256` map), re-hashes every listed file, and walks the tree to
find files present but unlisted.

Result:

| Metric | Value |
|---|---|
| Manifest entry count | 608 |
| Entries re-hashed | 608 |
| Hash mismatches | **0** |
| Listed files missing on disk | **0** |
| Files present on disk | 610 |
| Files present but unlisted | **2** — `SNAPSHOT_ID`, `source-manifest.json` |

The only two unlisted files are exactly the two that cannot list themselves. **PASS.**

### Check 3 — independence declaration

I did not open any file under `reviews/` (including `reviews/README.md`), and I did
not read any other reviewer's report or any verdict/acceptance count. The manuscript
and evidence were read only from the frozen snapshot.

**Self-reported accidental exposure (disclosed for completeness):** one shell command
used to create my output directory also ran `ls -la reviews/`, which printed the *names*
of the `reviews/` subdirectories (e.g. `round-1 … round-31`, `foster-cycle-*`) and the
name `README.md`. I opened no file in `reviews/`, read no report text, no verdict, and
no acceptance count. No other `.agent-runtime/review-snapshots/round-*` directory was
read, listed, globbed, or found. I judge this directory-name listing not to invalidate
the vote, and disclose it so the orchestrator can decide otherwise.

---

## 2. Scope for this emphasis

Audited: the distention/true-deformation decomposition; the Coleman–Noll-type
restrictions and pressure conjugacy; the finite-deformation Biot tensor and
fixed-pressure stress; stress/energy normalizations; the logarithmic-derivative
pushforward and drained-response identities (incl. the Moore–Penrose compliance);
the pore-fabric section (fabric basis, retained subspace, uniqueness, conformal limit);
limiting cases; and equation traceability of `moose_app/` and the validation maps.

All equation numbers below are resolved from `build/main.pdf` (equation numbers are
given as `(n)`); label names are as used in the sources.

### 2.1 Kinematics, volume fractions, and intrinsic densities — **correct**

- `(1)` `F = A F̄`, `J = a J̄`, `a = det A`, `J̄ = det F̄`: with `A = a^{1/3}R_A`
  (`(2)`) this gives `C̄ = a^{-2/3} C` (`(3)`). Verified by direct algebra. **OK.**
- `(4)–(5)`: `J ρ_s = φ_{s0} ρ̄_{s0}`, `J̄ = ρ̄_{s0}/ρ̄_s`, `φ_s = φ_{s0} J̄ / J`,
  `φ_s a = φ_{s0}`. These are mutually consistent (`φ_s a = φ_{s0}` follows from the
  other three). **OK.**
- The prompt asked about a claim that intrinsic densities satisfy `ρ̄/ρ̄_0 = 1` for
  incompressible phases. **No such claim exists in the manuscript.** The model
  correctly uses `J̄ = ρ̄_{s0}/ρ̄_s` (a compressible mineral in general) and the fluid
  EOS `(87)` `ρ̄_f = ρ̄_{f0} e^{p/K_f}`. Grep for `incompressib` finds nothing outside a
  bibliography note. **OK — nothing to correct.**
- The bar/prime/double-prime/subscript-`dis` convention block (main.tex lines
  ~146–166) is consistent with every use I checked: `σ̄_s` per current mineral volume,
  `τ̄_s = J̄ σ̄_s` (`(10)`) per reference mineral volume, `S̄_dis` (`(72)`) per reference
  mixture volume in the intermediate frame, `σ''`/`P''` double-prime, `ℂ^d`/`W^d`
  drained, `dis` distention. **OK.**

### 2.2 Phase stress and reversible work — **correct**

- `(6)–(12)`: `σ = φ_s σ̄_s − (1−φ_s)p I`; `σ' = σ + p I`; `τ' = Jσ'`, `τ̄_s = J̄σ̄_s`;
  `τ' = φ_{s0}(τ̄_s + pJ̄ I)`. The last follows from `Jφ_s = φ_{s0}J̄`. **OK.**
- `(13)` pressure conjugacy `∂W_s/∂J̄|_F = −φ_{s0}p`, `P' = ∂W_s/∂F|_J̄`, `τ'=P'F^T`;
  `(14)` `δW_s = τ':(δF F^{-1}) − φ_{s0}p δJ̄`. Verified `P':δF = τ':(δF F^{-1})`. **OK.**
- `(15)` `δF F^{-1} = ⅓I δln a + δR_A R_A^T + R_A(δF̄F̄^{-1})R_A^T` and `(16)`:
  verified by direct differentiation of `F = a^{1/3}R_A F̄`. **OK.**
- `(17)–(18)`: the skew term `τ':(δR_A R_A^T) = 0`, and using `(12)`/`(11)` the bracket
  collapses to `φ_{s0}τ̂_s`; pressure work cancels against `−φ_{s0}p δJ̄`. **OK.**
- `(19)` `W_s = W_A(a) + φ_{s0}W̄_s(F̄)`, `(20)` objectivity, `(21)–(22)` energy-return:
  substituting `(22)` into `(21)` recovers `(12)` including all shear components; trace
  bookkeeping is consistent. **OK.**
- `(23)` volumetric reduction: verified that `φ_{s0}τ̂_s:I δJ̄/(3J̄) = (φ_{s0}/3) tr σ̄_s δJ̄`
  using `τ̄_s = J̄σ̄_s`. **OK.**

### 2.3 Logarithmic Hooke laws, mineral EOS, and the drained restriction — **correct**

- `(24)–(26)` `ε̄ = ε − ⅓ ln a I` from `Ū = a^{-1/3}U` (`(3)`). **OK.**
- `(31)–(32)`: trace of `(12)` at `p=0` plus trace preservation `(106)` gives
  `K ln J = φ_{s0}K_s ln J̄` and `ln a = (1 − K/(φ_{s0}K_s)) ln J`. Verified. **OK.**
- `(33)` `W_A(a) = K/[2(1−K/(φ_{s0}K_s))](ln a)²`: integrating `dW_A/dln a = K ln J` on
  the spherical path gives exactly this. **OK.**
- `(37)` mineral EOS: I differentiated `(34)`/`(35)` with respect to `J̄` at fixed `F`,
  set `∂W_s/∂J̄ = −φ_{s0}p`, multiplied by `J̄`, and recovered `(37)` term for term
  (including the `+(1/3)(1−K/(φ_{s0}K_s)) I:ℂ_s:dev ε` coupling). **OK.**
- `(38)` stability domain and the “one positive root for `p ≥ 0`” argument: the RHS of
  `(37)` is strictly increasing in `J̄` with derivative `K_s/J̄ + (1−K/(φ_{s0}K_s))p > 0`
  when `0 < K < φ_{s0}K_s`, `p ≥ 0`; limits `−∞`/`+∞`. **OK.**
- `(40)` drained stiffness `ℂ^d = φ_{s0}ℂ_s − (φ_{s0}/9K_s)(1−K/(φ_{s0}K_s))(ℂ_s:I)⊗(ℂ_s:I)`
  and `(43)` compliance form: verified by substituting `(39)`/`(41)` into `ε = ε̄ + ⅓ ln a I`
  and by an independent Sherman–Morrison inversion
  `(A−c u⊗u)^{-1} = A^{-1} + ((1−K/(φ_{s0}K_s))/(9K)) I⊗I`. **OK.**

### 2.4 Finite-deformation Biot tensor and the explicit closed form — **correct**

- `(44)–(48)`: `W'' = W_s(F,J̄(F,p))`, `W' = W'' + φ_{s0}pJ̄`, and
  `P' = P'' + φ_{s0}p ∂J̄/∂F|_p`; verified that the `W_s`-derivative terms cancel by `(13)`. **OK.**
- `(49)` `σ = σ'' − pB`, `B = I − (φ_{s0}/J)(∂J̄/∂F)|_p F^T`. I re-derived
  `σ = J^{-1}P'F^T − pI` and confirmed the `−pI` is exactly the `−p·I` inside `B`. **OK.**
- `(50)`: proved `B:(δF F^{-1}) = δ(J − φ_{s0}J̄)/J` at fixed `p` (change, not derivative). **OK.**
- `(51)`: differentiating `(37)` at fixed `p` gives exactly
  `[K_s+(1−K/(φ_{s0}K_s))pJ̄] ∂lnJ̄/∂F|_p = (K/φ_{s0})F^{-T} − (1/3)(1−K/(φ_{s0}K_s)) ∂/∂F[I:ℂ_s:dev ε]`.
  I verified `∂(I:ℂ_s:dev ε)/∂F = F[∂logC/∂C : dev(ℂ_s:I)]` and confirmed `(51)`
  numerically against finite differences of the EOS root (agreement `1.5×10^{-7}` at
  a finite anisotropic state). **OK.**
- `(52)` explicit Biot tensor: derived symbolically from `(51)`, then **verified
  independently by finite differences** of `(J−φ_{s0}J̄)/J` at fixed pressure at a
  non-coaxial anisotropic state. The nine components of `B:(δF F^{-1})` matched the FD
  pore-volume change to `≈7×10^{-15}`; `B` is symmetric to `10^{-17}`. The isotropic-
  mineral case returned a spherical `B` to `0` off-diagonal. **OK.**
- The statement “`dev(ℂ_s:I)=0` ⇒ `B` spherical (e.g. cubic)”: verified — cubic `ℂ_s:I`
  is spherical. **OK.**
- `(53)` `σ = (φ_{s0}/J)τ̄_s − (1−φ_s)pI` follows from `(7)` with `σ̄_s = τ̄_s/J̄`. **OK.**
- `(54)–(55)` `∂W'/∂p|_F = φ_{s0}J̄` and `∂σ/∂p|_F = −B`: the second is an exact identity
  `∂σ/∂p = J^{-1}∂(φ_{s0}J̄)/∂F F^T − I = −B`, valid including the pressure dependence of
  both `σ''` and `B` (see optional note R1-O4). **OK.**
- `(56)` integrated pressure response and the explicit caveat that `σ''` depends on `p`. **OK.**

### 2.5 Reference response, storage, and limiting cases — **correct**

- `(57)` `B_0 = I − ℂ^d:ℂ_s^{-1}:I`. Independently confirmed: differentiating the EOS at
  `F=I, p=0` gives `B_0 = (1−φ_{s0})I + (φ_{s0}/(3K_s))(1−K/(φ_{s0}K_s))ℂ_s:I`, and
  `I − ℂ^d:ℂ_s^{-1}:I` reduces to the same expression. Isotropic form `(1−K/K_s)I`. **OK.**
- `(58)–(60)` solid storage `S_s = (φ_{s0}/K_s)(1−K/(φ_{s0}K_s))`, and the second form
  `φ_{s0}I:ℂ_s^{-1}:I − I:ℂ_s^{-1}:ℂ^d:ℂ_s^{-1}:I`: I verified `S_s = 9c` with
  `c=(φ_{s0}/9K_s)(1−K/(φ_{s0}K_s))`, i.e. the anisotropic parts cancel, so the second
  form is correct even though `I:ℂ_s^{-1}:I ≠ 1/K_s` in general. **OK.**
- `(61)–(62)` isotropic EOS/Biot: `ℂ_s:I = 3K_s I` ⇒ `(52)` becomes `(62)`. **OK.**
- `(63)–(64)` finite unjacketed path: I verified that on `a=1, J=J̄, ℂ_s:ε = −pJ I`
  the mineral EOS residual is identically zero (the anisotropic `I:ℂ_s^{-1}:I` terms
  cancel), `σ̂_s = −pI`, and `σ = −pI`, `φ_s = φ_{s0}`. **OK.**

### 2.6 Pore fabric — **correct**

- **Basis `e_1…e_6`.** `e_1 = I/√3` (Σ-diagonal 1, `tr = √3`); `e_2 = √(3/2)(m⊗m − I/3)`
  (norm 1, `tr = 0`); `e_3 = (p_1⊗p_1 − p_2⊗p_2)/√2`; `e_6 = √2 sym(p_1⊗p_2)`;
  `e_4 = √2 sym(m⊗p_1)`; `e_5 = √2 sym(m⊗p_2)`. I verified symbolically that all six have
  unit Frobenius norm (including the `√2` normalizations of `e_4, e_5, e_6`), that
  `tr e_2 = tr e_3 = tr e_4 = tr e_5 = tr e_6 = 0`, and that every pair is orthogonal.
  The retained subspace `range 𝔻 = span(e_1,e_2)` and complement `span(e_3,e_4,e_5,e_6)`
  are correctly identified; the reduced `𝔻` is transversely isotropic about `m`. **OK.**
- `(65)–(71)` fabric kinematics, `H = a^{-2/3}G` (`det H = 1`), energy
  `W_s = W_dis(G) + φ_{s0}W̄_s(F̄)`, and `S̄_dis = 2∂W_dis/∂G`: verified the
  `W_dis ↔ S_dis` relation through the self-adjoint matrix-logarithm derivative. **OK.**
- `(73)–(74)` tensorial virtual work: verified term by term (skew rotation increment
  drops; `G^{1/2}τ̃G^{-1/2} = φ_{s0}G^{1/2}τ̂_sG^{-1/2} + φ_{s0}pJ̄ I`; pressure terms
  cancel); the conformal limit `G^{1/2}=a^{1/3}I` recovers `(18)` exactly. **OK.**
- `(75)` equilibrium, `(77)` additive strain, `(78)` compliance
  `(ℂ^d)^{-1} = (φ_{s0}ℂ_s)^{-1} + 𝔻^{+}`: I **re-derived `(78)` from scratch** by (a)
  direct minimization over `E_dis ∈ range 𝔻`, (b) the block formula, and (c) the
  Moore–Penrose construction; all three agree to `≤1.4×10^{-15}`. I also verified the
  singular-`𝔻` case is handled correctly (the formula reduces to `(43)` in the conformal
  rank-one limit, confirmed as a self-consistent fixed point). **OK.**
- **Reference Biot for the fabric model.** The claim that `B_0 = I − ℂ^d:ℂ_s^{-1}:I`
  “keeps its form” with the generalized `ℂ^d` is verified independently: I built the
  linear functional `ε ↦ tr ε − φ_{s0} tr ε̄` from `(50)` at the reference state
  (with `ε̄ = ε − E_dis`, `E_dis` from the constrained equilibrium) and found it equals
  `I − ℂ^d:ℂ_s^{-1}:I` to `2.2×10^{-16}`. **OK.**
- `(79)–(80)`: `H = h^{-2}m⊗m + h(I − m⊗m)`, `det H = 1`, and
  `E_dis = (ln a/3)I + ln h(½I − 3/2 m⊗m)`; I verified `exp(2E_dis) = a^{2/3}H` exactly
  and that the unimodular eigenvalues are `(h^{-2}, h, h)`. **OK.**
- `(82)` `B = B_∥ m⊗m + B_⊥(I − m⊗m)`, with `B_∥ − B_⊥` carried by the volume–axial
  coupling modulus (zero coupling ⇒ spherical `B` for an isotropic mineral): consistently
  reproduced by the recorded artifacts and by the code. **OK.**

### 2.7 Traceability of `moose_app/` and the validation maps — **correct**

- `moose_app/include/utils/ConformalLaw.h` implements `(37)` (root `s.y` with stability
  `Ks + α p J̄` ≡ `(38)`), the resolvent/integral form of the Fréchet derivative
  `∂log C/∂C` (`(104)`), the drained stiffness/compliance (`(40)`,`(43)`), the reference
  Biot (`(57)`), the solid storage `(59)`/`(60)`, the fluid mass `(88)`/`(93)`, and the
  total stress (`(53)`). I checked the finite branch algebra term by term against the
  cited equations. **OK.**
- `moose_app/include/utils/FabricLaw.h` implements `(65)`–`(82)`: the retained basis
  (`e_1`,`e_2` normalized in the Mandel metric — reproducing `√(3/2)(m⊗m − I/3)`), the
  constrained equilibrium `(𝔻_d + φG)x = φ(g + p√3 ê_1)` matching `(75)`/`(77)`, the
  Moore–Penrose compliance `(78)`, and the reference Biot `(57)`. Sign/normalization of
  `ln a = √3 x_1` and `ln h = −x_2/√(3/2)` match `(80)`. **OK.**
- `moose_app/src/kernels/ReferenceBalance.C`: `ReferenceMomentum` is `∫ Grad v : P`
  (`(95)`); `ReferenceFluidMass` is `(m^n − m^{n−1})/Δt − Grad w · Q_f` (`(96)`,`(97)`).
  **OK.**
- `validation/equation_to_moose_map.yml` and `validation/theory_traceability.yml` list
  only equations that exist, and their approximation/scope labels
  (`reference_state_linearized_axisymmetric…`, `general_finite_deformation_fabric_equilibrium_out_of_scope`,
  `reference_tangent_mode_not_finite_deformation_model`) match the implemented code.
  Every `moose_app` object maps to a manuscript equation. **OK.**

### 2.8 Numerical claims recomputed from frozen artifacts (no held suites run)

- Reference Biot components for `(83)`: recomputed `0.7000, 0.7583, 0.7917`. **Match.**
- `K_s = 28K_*` and the isotropic-comparison shear modulus `16.8K_*`
  (`= mean of the five deviatoric Mandel modes / 2`, since the two deviatoric normal
  eigenvalues sum to `180 − 84 = 96`): recomputed `16.8`. **Match.**
- FE reference coefficients (`φ_{s0}=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8`):
  `G = φ_{s0}μ_s = 0.75`, `B_0 = 1 − K/K_s = 0.6`, total storage `= 0.1/8 + 0.2 = 17/80`.
  **Match.**
- MMS adjacent orders from `fe-evidence/mms-convergence.json`: `p` `2.00, 2.00`;
  `u_x` `2.99, 2.96`; `u_y` `3.00, 2.96`. **Match** sections/finite_elements.tex.
- Temporal successive-difference orders at `nx=16/32/64` span `0.978–1.397` (including
  values above one); linear step-refinement ratio `0.007104/0.003658 = 1.94`; the
  load-limit pressure discrepancy floors at `3.22×10^{-3}`. **All match** the text, which
  correctly declines to assert an order above one.
- `build/conformal/verification.json`: `checks_passed = 186`,
  `max_constitutive_identity_error = 2.455×10^{-9}` (the text’s “largest absolute error
  among its constitutive identities is `2.5×10^{-9}`” refers to the `implementation`
  category; the larger `convergence`-category entries are rates, not identities — the
  wording is consistent). Fabric artifact numbers (`4.9×10^{-15}`, `2.2×10^{-16}`,
  `−3.3×10^{-16}`, `1.6×10^{-16}`, `2.5×10^{-16}`, `1.9×10^{-14}`) reproduce.
  **Match.**
- Fabric probe/contour peaks and displacement maxima recomputed from the frozen CSVs
  (`3.616, 4.363, 4.990, 5.521 ×10^{-5}`; `5.18, 5.14, 2.38, 5.26 ×10^{-5}`). **Match.**

---

## 3. REQUIRED changes

**None.** I found no incorrect derivation, no inconsistent normalization, and no
constitutive relation in `moose_app/` that disagrees with the manuscript. Every central
identity I cross-checked symbolically and, where a closed form exists, numerically
(independent finite differences and from-scratch re-derivation) holds to machine
precision. I did not identify any defect I could honestly promote to a required change,
and I decline to manufacture one in order to appear more critical.

---

## 4. OPTIONAL notes

**R1-O1 (evidence hygiene).** `build/weighted-stress/derivation-scan.txt` is stale
relative to the reviewed sources: it reports `sections/experiments.tex` lines 29/39/52/59
as carrying table labels `tab:fixed-deformation` and `tab:layer`, which do not exist in
the current `sections/experiments.tex`, and its scan omits `sections/pore_fabric.tex` and
`sections/finite_elements.tex`. It is a build artifact, not manuscript text, so it does
not affect correctness; consider regenerating or removing it so shipped evidence matches
the sources.

**R1-O2 (uniqueness wording).** `sections/pore_fabric.tex` lines 212–215 and 284–286
state that “the stationary point … is unique” for the general equilibrium `(75)`,
justified by “the retained quadratic distention potential.” The argument is valid for the
reference quadratic model actually implemented, but the mineral term
`φ_{s0}W̄_s(G^{-1/2}F)` is not quadratic in `G` in general, so uniqueness of `(75)` for a
general `W_dis(G)` is not implied by that sentence. A one-clause qualifier (“in the
reference quadratic model of section 7.5 / section 9.4”) would make the scope exact.

**R1-O3 (derivation visibility).** `(78)` is stated but its one-line minimization is not
shown (gradient `𝔻:E_dis − φ_{s0}ℂ_s:(ε−E_dis) − φ_{s0}p I = 0` on
`E_dis ∈ range 𝔻`). Since `(78)` is a headline result, showing it (or pointing to the
code’s `solve` step) would let a reader reproduce it without independent work.

**R1-O4 (pressure dependence of `B`).** `(55)` is an exact identity
`∂σ/∂p|_F = −B`. `(49)` writes `σ = σ'' − pB`, and the text correctly warns that `σ''`
depends on `p`; for symmetry of explanation it may help to state explicitly that `B`
also depends on `p`, so that `(49)` is not read as a decomposition into
pressure-independent parts.

**R1-O5 (independence of the fabric check).** `sections/finite_elements.tex` and
`examples/verify_fabric.py` already disclose that the “independent” NumPy
re-implementation shares the basis, equilibrium, and `ln h` sign convention with the
compiled law. This is honest; a genuinely convention-free check (e.g. a numerical
minimization of the potential at a random state, as I ran in `/tmp`) would additionally
test the conventions themselves. Presented only as a strengthening, not a defect.

---

VERDICT: ACCEPT

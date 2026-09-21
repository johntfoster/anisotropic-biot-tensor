# SIMULATED AI PEER REVIEW — Round 33, Reviewer 1 (derivation and correctness)

This is a simulated AI peer review. It is not journal peer review and confers no acceptance.
Emphasis: scientific and mathematical development, and whether the revised prose preserved every claim.

Snapshot under review (immutable, read-only): `.agent-runtime/review-snapshots/round-33`
Declared `SNAPSHOT_ID`: `7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53`
All reading was done from the frozen snapshot. Nothing outside my own report was written.

---

## 1. Mandatory first checks

### 1.1 Manifest hash equals the declared SNAPSHOT_ID, and SNAPSHOT_ID holds the same string

Command:

```
cd <snapshot> && sha256sum source-manifest.json && cat SNAPSHOT_ID
```

Result:

```
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53  source-manifest.json
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53
SNAPSHOT_ID file contents: 7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53
```

**PASS** — the manifest hash equals the declared SNAPSHOT_ID exactly, and the `SNAPSHOT_ID` file holds the same string.

### 1.2 Re-hash every file listed in `source-manifest.json`, and walk the tree

Command (Python, sha256 over each listed path, then `os.walk` of the snapshot):

```
cd <snapshot> && python3 - <<'EOF'
import json, hashlib, os
snap = os.getcwd(); m = json.load(open('source-manifest.json'))
... re-hash each listed rel path; collect mismatches/missing; walk tree for unlisted ...
EOF
```

Result:

- manifest entries: **608**
- entries re-hashed: **608**
- hash mismatches: **0**
- listed files missing on disk: **0**
- files present but unlisted (excluding `source-manifest.json` and `SNAPSHOT_ID`, which cannot list themselves): **0**

**PASS** — the manifest is a complete, exact, flat path→sha256 mapping of the snapshot contents.

### 1.3 Independence declaration

I declare that:

- I did **not** open any file under `reviews/` in the snapshot, including `reviews/README.md`.
- I did **not** read, list, glob, or `find` any other `.agent-runtime/review-snapshots/round-*`
  directory, nor any other reviewer's report, nor any verdict or acceptance count.
- I did **not** read the working tree for manuscript or evidence content; all manuscript, code,
  artifact, and figure reading was from the frozen snapshot.

Accidental exposure (self-reported): a single `ls -la` of the snapshot root listed the *name* of the
`reviews` directory among the snapshot's top-level entries. No file inside it was opened, listed, or
read, and no content from it influenced this report. No other round directory or report was touched.

**PASS** — independence preserved.

---

## 2. Scope audited under this emphasis

I recomputed, symbolically and/or numerically (independent of the shipped verification scripts), the
following and checked them against the manuscript. Equation numbers are as resolved from
`build/main.pdf` (constructed by `pdftotext`; `build/main.aux` is not shipped).

### 2.1 Multiplicative decomposition, conformal specialization, J, a, Jbar

- `F = A Fbar`, `J = a Jbar`, `a = det A`, `Jbar = det Fbar` (1); `A = a^{1/3} R_A` with
  `R_A^T R_A = I`, `det R_A = 1` (2). Checked: `A Fbar = a^{1/3}R_A · a^{-1/3}R_A^T F = F`, and
  `Cbar = Fbar^T Fbar = a^{-2/3} F^T R_A R_A^T F = a^{-2/3} C` (3). **Correct.**
- Mass relations `J rho_s = phi_s0 rho_s0`, `Jbar = rho_s0^bar/rho_s^bar`, `phi_s = phi_s0 Jbar / J`,
  `phi_s a = phi_s0` (4)–(5). Consistent with `J = a Jbar`.
- **On the specific item "intrinsic phase densities satisfy rho_bar/rho_bar0 = 1 for incompressible
  phases":** I could not locate any such statement anywhere in the snapshot manuscript (grep for
  `incompressib`, `intrinsic`, `per-phase` across `main.tex` and `sections/*.tex`). Equation (5),
  `Jbar = rho_s0^bar/rho_s^bar`, *implies* `Jbar = 1` for an incompressible solid phase, but the
  manuscript does not state it and never treats the incompressible limit. See **R1-O1**. This is not an
  error (the paper is explicitly a compressible-mineral formulation) but the audited claim is absent.

### 2.2 Reversible work, rotation cancellation, equivalent energy

- `delta W_s = tau':(delta F F^{-1}) - phi_s0 p delta Jbar` (14); virtual deformation
  `delta F F^{-1} = (1/3) I delta ln a + delta R_A R_A^T + R_A (delta Fbar Fbar^{-1}) R_A^T` (15),
  `delta Jbar = Jbar tr(delta Fbar Fbar^{-1})` (16). Verified by direct differentiation of `F = a^{1/3} R_A Fbar`.
- `delta R_A R_A^T` skew ⇒ vanishes against symmetric `tau'`; substitution gives (17) and then (18),
  using (12) and (11): `R_A^T tau' R_A - phi_s0 p Jbar I = phi_s0 tauhat_s`. **Correct.**
- Energy `W_s = W_A(a) + phi_s0 Wbar_s(Fbar)` (19); objectivity `Wbar_s(a^{-1/3}R_A^T F) = Wbar_s(a^{-1/3}F)` (20).
- Return identities `tau' = (dW_A/dln a) I + phi_s0 dev tau_s^bar` (21) and
  `dW_A/dln a = (phi_s0/3) tr tau_s^bar + phi_s0 p Jbar` (22). Verified these are algebraically the
  trace/dev split of (12) and hence mutually consistent; `dW_A/dln a = tr tau'/3` also checks.
- Volumetric work (23): `delta W_s = (1/3) tr tau' delta ln a + (phi_s0/3) tr sig_s^bar delta Jbar`
  for `delta Fbar Fbar^{-1} = I delta Jbar/(3 Jbar)`. **Correct**, including the `phi_s0` factor.

### 2.3 Logarithmic Hooke laws, drained restriction, compliance

- Logarithmic strains (24)–(26): `epsbar = eps - (1/3) ln a I`. **Correct.**
- `K = (1/9) I:C^d:I`, `K_s = (1/9) I:C_s:I` (30). Spherical drained matching
  `K ln J = phi_s0 K_s ln Jbar` (31), `ln a = (1 - K/(phi_s0 K_s)) ln J` (32), and
  `W_A(a) = K/(2(1-K/(phi_s0 K_s))) (ln a)^2` (33). **Correct.**
- Total energy (34)–(35): I expanded `(1/2) epsbar:C_s:epsbar` with
  `epsbar = dev eps + (ln Jbar/3) I` and recovered the four terms of (35) with the correct
  coefficients, including the coupling term `(phi_s0/3) ln Jbar I:C_s:dev eps`. **Correct.**
- Pressure derivative (36) and mineral-volume equation (37): verified term-by-term that
  `d/dJbar [W_s]|_F = -phi_s0 p` reproduces (36) and that collecting terms gives (37). **Correct.**
- Drained distention (39): `ln a = (1/(3K_s))(1-K/(phi_s0 K_s)) I:C_s:eps` follows from (37) at `p=0`. **Correct.**
- Drained stiffness restriction (40): I verified independently (SymPy-equivalent numeric check) that
  `C^d:eps = phi_s0 C_s:epsbar` holds identically with
  `C^d = phi_s0 C_s - (phi_s0/(9K_s))(1-K/(phi_s0 K_s))(C_s:I)⊗(C_s:I)`, using
  `ln a = (1/(3K_s))(1-K/(phi_s0 K_s)) I:C_s:eps`. For the example matrix
  (`experiments.tex:9` eq. (83)) this gives `K_s = 28` and `C^d` normal components
  `(20.2969, 26.0668, 31.8918)`, shear `(12, 14.4, 16.8)`; positive definite. **Correct.**
- Compliance restriction (43): verified by the Sherman–Morrison identity, symbolically:
  with `M = phi_s0 C_s`, `w = C_s:I`, `C^d = M - c w⊗w`, `c = (phi_s0 K_s - K)/(9 K_s^2)`,
  `w:M^{-1}w = 9K_s/phi_s0`, so `(C^d)^{-1} = M^{-1} + [c/phi_s0^2]/[K/(phi_s0 K_s)] I⊗I
  = (phi_s0 C_s)^{-1} + (1-K/(phi_s0 K_s))/(9K) I⊗I`. **Correct.** Numerically the difference
  `(C^d)^{-1} - (phi_s0 C_s)^{-1}` equals `coef · I⊗I` to machine precision for the example matrix.
- Reference solid storage (58)–(60): verified
  `S_s = -phi_s0 dJbar/dp|_{F=I,p=0} = (phi_s0/K_s)(1-K/(phi_s0 K_s))` and that the third form
  `= phi_s0 I:C_s^{-1}:I - I:C_s^{-1}:C^d:C_s^{-1}:I` reduces to `9c` = the same value. **Correct.**

### 2.4 Finite-deformation Biot tensor and the fixed-pressure stresses

- Reduced energies (44)–(45) and primed stresses (46)–(48): verified
  `P'' = P' - phi_s0 p dJbar/dF|_p`, i.e. `P' = P'' + phi_s0 p dJbar/dF|_p` (48). **Correct.**
- `sig = sig'' - p B`, `B = I - (phi_s0/J) dJbar/dF|_p F^T` (49). Derived: `P' = P'' + phi_s0 p dJbar/dF`
  and `sig = sig' - p I` give `B = I - (phi_s0/J) dJbar/dF F^T`. **Correct.**
- Pore-volume variation (50): verified `B:(delta F F^{-1}) = (delta J - phi_s0 delta Jbar)/J` at `delta p = 0`. **Correct.**
- Mineral fixed-pressure derivative (51) and explicit Biot tensor (52): I re-derived (51) from (37)
  and then (52). Key step: using the appendix relation
  `d(T:eps)/dF = F[∂logC/∂C : T]` with `𝕃 = ∂logC/∂C`, and `𝕃:I = C^{-1}`, I obtain
  `∂[I:C_s:dev eps]/∂F = F[𝕃:dev(C_s:I)]` (the `3K_s F^{-T}` terms cancel exactly). Substituting into
  `B = I - (phi_s0 Jbar/J)(1/D) dln Jbar/dF F^T`, `D = K_s + (1-K/(phi_s0 K_s))p Jbar`, reproduces (52)
  term for term. Isotropic reduction of (52) gives exactly (62). **Correct.**
- Total-stress check (53) `sig = (phi_s0/J) tau_s^bar - (1-phi_s)p I`: verified via
  `phi_s/Jbar = phi_s0 Jbar/(J Jbar) = phi_s0/J`. **Correct.**
- Pressure envelope and tangent (54)–(55): verified `dW'/dp|_F = phi_s0 Jbar` by chain rule, and
  `dsig/dp|_F = -B` via Young's theorem and `dsig''/dp = p dB/dp` (both sides computed). **Correct.**
- Integrated response (56) and its stated interpretation of `sig''`'s pressure dependence. **Correct.**
- Reference Biot relation (57) `B_0 = I - C^d:C_s^{-1}:I`: verified that evaluating (52) at `F = I, p = 0`
  (with `𝕃 = 𝕀_sym`) gives `(1-K/K_s) I + (phi_s0 K_s - K)/(3K_s^2) dev(C_s:I)`, which equals
  `I - C^d:C_s^{-1}:I` identically. Numerically for the example matrix, the normal components are
  `0.7000, 0.7583, 0.7917`, matching `experiments.tex:20` exactly.

### 2.5 Logarithmic-derivative / spatial-stress conversion (appendix A)

- (101)–(103) `delta W = T:delta eps = {F[∂logC/∂C:T]}:delta F`, `tau = F[∂logC/∂C:T]F^T`. Verified.
- Spectral form (104), self-adjointness, and (105)–(106) `tr tau = tr T`. Verified
  `C:[𝕃:T] = sum_i lambda_i (T_ii/lambda_i) = tr T`. Also verified `𝕃:C = I` and `𝕃:I = C^{-1}`,
  hence `tau = F[𝕃:I]F^T = F C^{-1}F^T = I` for `T = I`. **Correct.**

### 2.6 Pore-fabric distention law (`sections/pore_fabric.tex`)

- Kinematics (65)–(70): `A = R_A G^{1/2}`, `G = A^T A`, `a = (det G)^{1/2}`, `H = (det G)^{-1/3}G`,
  `G = a^{2/3}H`. Verified `Cbar = F^T R_A G^{-1} R_A^T F` (68) and exact reduction to (2)–(3) when
  `G = a^{2/3}I`. **Correct.**
- Virtual work (73)–(74): I re-derived the push-forward bookkeeping, obtaining
  `G^{1/2} tau~ G^{-1/2} : (delta Fbar Fbar^{-1})` for the mineral term and
  `tau~:[delta(G^{1/2})G^{-1/2}]` for the distention term with `tau~ = R_A^T tau' R_A`. This matches
  (74) exactly, and the conformal limit `G^{1/2} = a^{1/3}I` recovers (18). **Correct.**
- Equilibrium (75), and its reduction on the conformal submanifold to (22). **Correct.**
- **Fabric-adapted basis `e_1..e_6`:** I verified orthonormality under tensor contraction for an
  arbitrary orientation (`m` random unit, `p_1,p_2` an orthonormal basis of the plane normal to `m`):
  Gram deviation from identity `2.2e-16`. Traces: `tr e_1 = sqrt 3`, `tr e_2 = tr e_3 = tr e_4 = tr e_5 = tr e_6 = 0`.
  Norms with the `sqrt2` normalizations are exactly 1 (`e_1 = I/sqrt3`,
  `e_2 = sqrt(3/2)(m⊗m - I/3)`, `e_3 = (p_1⊗p_1 - p_2⊗p_2)/sqrt2`,
  `e_4 = sqrt2 sym(m⊗p_1)`, `e_5 = sqrt2 sym(m⊗p_2)`, `e_6 = sqrt2 sym(p_1⊗p_2)`).
  All cross terms zero. **Correct.**
- Retained subspace `range D = span(e_1,e_2)` and its four-dimensional complement: verified that a
  rank-two `D` on `span(e_1,e_2)` annihilates `e_3,e_4,e_5,e_6` to `1e-16`. **Correct.**
- Compliance (78) `(C^d)^{-1} = (phi_s0 C_s)^{-1} + D^+`, with `D^+` the Moore–Penrose inverse:
  proved generally (`E = phi_s0 D^+ C_s:(eps-E)` follows by applying `D^+` to the stationarity
  condition `D:E = phi_s0 P_D C_s:(eps-E)`, since `D^+D` is the orthogonal projector onto
  `range D`), and verified numerically for a random anisotropic `C_s` and random `m`:
  `|(C^d)^{-1} T - eps| <= 2e-17` over three trials. Reduction to the rank-one spherical
  restrictions (43) when `D ∝ I⊗I`. **Correct.**
- **Uniqueness/scoping of the stationary point:** the argument is now correctly scoped to the
  *reference quadratic model*, requiring `D + phi_s0 C_s` positive definite on `range D`, which the
  manuscript states and the compiled material enforces (positive-definite 2x2 block). The
  complementary modes are explicitly dropped from the minimization rather than equilibrated, and the
  text says this is a modelling choice. This is stated, not overclaimed. **Acceptable.**
- Transverse isotropy (79)–(82): verified `det H = 1`; `E_dis = (ln a/3) I + ln h (1/2 I - 3/2 m⊗m)` (80)
  and `exp(2 E_dis) = a^{2/3}[h^{-2} m⊗m + h(I-m⊗m)] = G`; the identity
  `1/2 I - 3/2 m⊗m = -sqrt(3/2) e_2` gives `ln a = sqrt3 x_1`, `ln h = -x_2/sqrt(1.5)`, matching the
  compiled law. Shape balance (81) is independent of `p` because `Jbar` is independent of `h`. **Correct.**
- Conformal limit: `D ∝ I⊗I`, `D^+` the rank-one inverse on the volume direction, reducing (78) to (43). **Correct.**

### 2.7 Notation paragraph (prime/double-prime and bar rules)

`main.tex:215–254` now covers, and is consistent with, every symbol it is applied to: bar on
kinematic/energetic quantities = mineral state (1); bar on intrinsic density `rho_xi^bar = rho_xi/phi_xi`;
bar on a stress = mixture-frame representation vs hat = true frame; the *two different* barred-stress
normalizations (`sig_s^bar` per current mineral volume, `tau_s^bar = Jbar sig_s^bar` per reference
mineral volume); the work-conjugate distention pair (`Sdis_bar` conjugate to `G`, `Sdis` conjugate to
`E_dis`, both per reference mixture volume in the intermediate frame); bar on a boundary datum (`Q_f^bar`);
single prime = effective stress carrying the full pore pressure; double prime = fixed-pressure stress,
explicitly naming the reduced energies `W''` of (44) and `W'` of (45); superscript `d` = drained, with
the explicit warning that `d` never means distention; subscript `dis` for distention quantities
including `W_dis` and `W_A`. I found **no symbol in the manuscript whose bar/prime/double-prime usage
contradicts this paragraph**. The label collision between the fabric basis `e_1..e_6` and Mandel
component indices is explicitly disclaimed in `pore_fabric.tex:322`. **PASS.**

### 2.8 Limiting cases and their stated scopes

- Reference state (57)–(60), isotropic mineral (61)–(62), finite unjacketed path (63)–(64). I re-derived
  the unjacketed consistency through (37) (the `I:C_s:dev eps` term is nonzero and cancels the
  `(K_s - K/(phi_s0 K_s)) ln J` term identically at first order), so (63)–(64) are consistent on the
  selected branch. **Correct.**
- Gajo correspondence for (61) is stated as the volumetric law only, with the drained shear condition
  (`G = phi_s0 mu_s`) called out from (40). Scoped correctly.
- Every numerical/demonstration claim is scoped: the constant-tangent FE verification is distinguished
  from the nonlinear law, and the fabric law is stated to be checked "at the material point against a
  separate re-implementation of its equations, which shares the section's modelling conventions"
  (`finite_elements.tex:277–280`). **Honest and correctly scoped.**

### 2.9 Code / validation traceability

- `validation/equation_to_moose_map.yml` and `validation/theory_traceability.yml`: every equation label
  they cite resolves to a real `\label` in the snapshot (no undefined references; confirmed by
  extracting all `\label`/`\eqref`/`\cref` and by a clean `build/main.log` with no undefined-reference
  warnings).
- `moose_app/src/kernels/ReferenceBalance.C`: `ReferenceMomentum` residual `sum_j grad_test(j)*P(i,j)`
  = weak momentum (95); `ReferenceFluidMass` residual `test*(m-m_old)/dt - grad_test·flux` = (96). Match.
- `moose_app/include/utils/ConformalLaw.h` / `ConformalMaterial.C`: `cd[i][j] = phi*cs[i][j] -
  phi*alpha/(9 Ks)*(C_s:I)_i (C_s:I)_j` matches (40) with `alpha = 1-K/(phi Ks)`;
  `B = I - (phi I - phi alpha/(3Ks) C_s:I)` matches `I - C^d:C_s^{-1}:I` (57) and the isotropic limit (62);
  the finite path solves (37) by implicit differentiation and forms `B` per (52); `mass = rho0*exp(p/Kf)*(J-phi*Jbar)`
  matches (87)–(88); `flux = -mobility*J*rho*F^{-1}F^{-T}Grad p` matches (91); `P = J*sig*F^{-T}` matches (86).
  Storage `(1-phi)/Kf + phi*alpha/Ks` matches (94) with (59). Match.
- `moose_app/include/utils/FabricLaw.h`: basis, `E_dis`, equilibrium `(Dd + phi G)x = phi(g + p sqrt3 e1_hat)`,
  Moore–Penrose restriction (78), and `B = I - C^d:C_s^{-1}:I` all match section 7. Match.

### 2.10 Numerical claims re-checked from the frozen artifacts (not re-run)

- MMS spatial orders from `fe-evidence/runs/mms_space_*`: recomputed adjacent orders
  `p 2.00/2.00`, `ux 2.99/2.96`, `uy 3.00/2.96` — match `finite_elements.tex:205–207`.
- Fixed-mesh successive-difference temporal orders from `fe-evidence/mms-convergence.json`:
  `nx16 (1.093, 0.978, 1.015)`, `nx32 (1.397, 1.018, 1.125)`, `nx64 (1.396, 1.076, 1.252)`;
  range 0.98–1.40 — matches `finite_elements.tex:208`.
- Linear step refinement: `linear_time_0.001` / `linear_time_0.002` normalized pressure errors
  `3.658e-3` / `7.104e-3`, ratio `1.94` — matches `finite_elements.tex:210`.
- Finite-load floor: `nonlinear_load_0.0001` normalized pressure error `3.221e-3` — matches
  the "about 3.2e-3" claim (`finite_elements.tex:213`).
- Fabric evidence (`build/fabric/fabric-verification.json`): `H` reconstruction `2.220e-16`;
  `det H - 1 = -3.331e-16`; `||D:e_3|| = 1.58e-16`, `D:e_6 = 0`; rotation invariance `2.497e-16`;
  worst probe difference `4.885e-15`; conformal cross-check max `1.87e-14` — all match
  `finite_elements.tex:272–280` (2.2e-16, -3.3e-16, 1.6e-16, 0, 2.5e-16, 4.9e-15, 1.9e-14).
- Conformal suite `checks_passed = 186`, `legacy_identities_rechecked = 67 = 65 + 2`,
  max constitutive identity error `2.455e-9` — matches `experiments.tex:181–188`.
  Tensor suite `total_states = 273 = 13 x 21` — matches `experiments.tex:192`.
- Mandel reference (`site/reports/mandel-reference.json`): `G = 0.75`, `alpha = 0.6`,
  storage `17/80` (analytically re-derived); matches `finite_elements.tex:161–166`.
- Fabric probe / contour figures (`figures/fe_fabric_probe.csv`, `figures/fe_fabric_contours.csv`):
  peak centre pressures `3.616e-5 / 4.363e-5 / 4.990e-5 / 5.521e-5` and refined contour peaks
  `3.606e-5 / 4.349e-5 / 4.973e-5 / 5.503e-5`, `u_mag_max 5.183e-5 / 5.137e-5 / 2.382e-5 / 5.259e-5`;
  all match `finite_elements.tex:265–268` and `295–301`.
- Example reference Biot components `0.7000 / 0.7583 / 0.7917` recomputed (see 2.4); isotropic
  comparison shear `16.8 K_*` = mean of the five deviatoric stiffness modes of `C_s` divided by two
  (recomputed deviatoric eigenvalues `20, 24, 28, 42.967, 53.033`, mean `33.6`) — match `experiments.tex:20–24`.

---

## 3. REQUIRED changes

None. Every audited derivation closes, every stated normalization is consistent with the equation that
defines it, the fabric basis and its `sqrt2` normalizations are correct, the generalized compliance
restriction with the Moore–Penrose inverse is correct, the notation rules cover every symbol they are
applied to, and every numerical claim I could recompute from the frozen artifacts matches. I found no
place where the revised prose asserts something the equations do not support.

## 4. OPTIONAL notes

**R1-O1 (optional).** *Incompressible-phase statement is absent.* `main.tex:258–262` (eqs. (4)–(5)) give
`Jbar = rho_s0^bar / rho_s^bar` but the manuscript nowhere states that this forces `Jbar = 1` for an
incompressible solid phase, nor does it discuss the `K_s -> infinity` (incompressible-mineral) limit.
If a prior revision asserted `rho_bar/rho_bar0 = 1` for incompressible phases as part of the
decomposition discussion, that sentence did not survive into this snapshot. Recommendation: if the
incompressible limit is considered in scope, add one sentence after eq. (5) noting `Jbar = 1` for
incompressible phases and that the present construction is the compressible generalization; otherwise
no action. No associated error: nothing in the paper relies on an incompressible phase.

**R1-O2 (optional).** *Normalization of `W_A` and `W_dis` is inferable, not stated.* The notation
paragraph (`main.tex:245–253`) states the normalizations of the barred stresses and of `W^d`, but not
explicitly that `W_A(a)` and `W_dis(G)` are per reference mixture volume. This follows from
`W_s = W_A + phi_s0 Wbar_s` (19)/(71) with `W_s` per reference mixture volume, so it is not
inconsistent — only implicit. A half-sentence would close the gap.

**R1-O3 (optional).** *Conformal limit in the compiled law is a stiff-mode approximation.* The
manuscript states the conformal limit as `D ∝ I⊗I` (rank one). `FabricLaw.h` realizes it by freezing the
axial mode with a large finite modulus (`axial_modulus = 1e12`) rather than a singular `D`, so the
reported `1.9e-14` agreement with `ConformalMaterial` documents agreement with an approximation of the
limit rather than the exact limit. The manuscript's wording ("In the volume-only limit the same material
reproduces the conformal material ... to `1.9e-14`") is accurate; a parenthetical that the conformal
limit is enforced by a large axial modulus would make the provenance fully explicit. No correction required.

**R1-O4 (optional).** *"Kinematically frozen" wording.* `pore_fabric.tex:283` says the complementary
modes "are kinematically frozen to the mineral". This is correct in the intended sense (the distention
`E_dis` carries zero component on the complement, so the mineral strain retains it and the mineral
carries it at its own compliance), but "kinematically frozen" could be misread as freezing the
deformation rather than the distention. Consider "the complementary distention modes are set to zero and
carried by the mineral at its own compliance." Clarity only.

---

VERDICT: ACCEPT

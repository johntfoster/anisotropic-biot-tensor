# SIMULATED AI PEER REVIEW — Reviewer 1

**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Snapshot:** `.agent-runtime/review-snapshots/round-31` (frozen, read-only)
**Declared SNAPSHOT_ID:** `09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84`
**Emphasis:** derivation and correctness (reference/push-forward algebra, distention decomposition, volume-fraction-weighted phase stress, volumetric energy, pressure-coupling tensor, drained compliance, isotropic and isotropic-mineral reductions, index/factor/rank/symmetry/objectivity, limiting cases, quoted values).
**Date:** 2026-09-21
**Note:** simulated review, not a journal acceptance decision.

---

## 1. MANDATORY FIRST CHECKS

### 1.1 Snapshot identity

```
$ cd .../anisotropic-biot-tensor
$ sha256sum .agent-runtime/review-snapshots/round-31/source-manifest.json
09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84  .../round-31/source-manifest.json
```

**Result: MATCH.** The digest equals the declared SNAPSHOT_ID and equals the contents of
`round-31/SNAPSHOT_ID` (`09a606a7...d113c84`).

### 1.2 Re-hash of every manifest entry (on a temporary copy)

Commands: `cp -r .agent-runtime/review-snapshots/round-31 /tmp/r31/snap` (then `chmod -R u+w`), followed by a
SHA-256 recomputation of every path in `source-manifest.json` against the copy, plus a walk of the copy to
enumerate files present but unlisted. Nothing was written inside the snapshot.

| Quantity | Result |
|---|---|
| Entries listed in `source-manifest.json` | **606** |
| Hashes recomputed and equal | **606** |
| Hash mismatches | **0** |
| Listed files missing on disk | **0** |
| Files present on disk but not listed | **0** (excluding `source-manifest.json` and `SNAPSHOT_ID`, which are not self-listed) |

**PASS** — the snapshot is internally consistent and complete with respect to its manifest.

### 1.3 Independence declaration

- I did **not** open any file under `reviews/`. I issued one `ls reviews/` on the temporary copy, which
  returned only the filename `README.md`; no `reviews/` content (README, LAUNCH-STATE, reviewer-2,
  reviewer-3, or any prior round) was read. I subsequently issued a second `ls` of the repository's
  `reviews/round-31/` to confirm where to write my report; that listing returned only filenames
  (`LAUNCH-STATE.md`, `reviewer-2.md`, `reviewer-3.md`) and no file content. **Self-reported accidental
  exposure: filename visibility only; zero bytes of any other report or response were read.**
- I did **not** open any other `.agent-runtime/review-snapshots/round-*` directory. I ran one
  `ls -d .agent-runtime/review-snapshots/round-*` only to confirm which snapshot is current; it listed
  directory names (round-8 … round-31) and read no file inside any of them.
- All manuscript content was read from `/tmp/r31/snap` (the copy of round-31), never from the working tree.
- No held numerical suite was run. `validation/` and `examples/verify_*.py` were not executed; only frozen
  CSV/JSON artifacts were read and independently recomputed (Mandel `6×6` algebra in NumPy).

---

## 2. RE-DERIVATION AND CORRECTNESS

I re-derived each step from its stated starting point. Notation: `X:M = tr(X^T M)`; Mandel 6-vector for the
identity tensor is `v = (1,1,1,0,0,0)`, so `I⊗I ≡ v v^T`; `𝕁 = (1/3) I⊗I`, `𝕂 = I_s − 𝕁`.

### 2.1 The two checks the manuscript claims as its cross-validation

**V1.** `main.tex:216-246` (notation) and the derivation in `:233-247`. Using `τ' = Jσ'` and
`Jφ_s = φ_s0 J̄` (`eq:distention`), `σ' = φ_s(σ̄_s + pI)` gives exactly
`τ' = φ_s0(τ̄_s + p J̄ I)` (`eq:constitutive-kirchhoff-phase-stress`). **Consistent, including the
normalization conversion** required by the bar rule (`σ̄_s` per current mineral volume, `τ̄_s = J̄σ̄_s` per
reference mineral volume, `τ'` per reference mixture volume).

**V2.** I re-derived the rotation in `eq:rotated-mineral-kirchhoff` independently. For `F = A F̄` the mixed
push-forward is `τ^i_j = (A^{-1})_{li} τ̂^l_m A_{jm}`. With `A = a^{1/3} R_A` the factors
`a^{-1/3}·a^{1/3}` cancel, giving `τ̄_s = R_A τ̂_s R_A^T` — i.e. the rotation changes components only. **Correct.**

**V3 (work/energy equivalence).** `eq:phase-work-substitution` → `eq:distention-mineral-energy-work`: the
skew increment `δR_A R_A^T` drops against symmetric `τ'`; the pressure term cancels *because* of the phase
balance, and the mineral work is weighted by `φ_s0`. Re-checked independently with
`φ_s0 W̄_s(F̄)`: `φ_s0(∂W̄_s/∂F̄):δF̄ = φ_s0 τ̂_s:(δF̄F̄^{-1})`. **Correct.**

**V4.** `eq:energy-returned-effective-stress` + `eq:energy-returned-pressure-balance`: taking the trace of
`eq:constitutive-kirchhoff-phase-stress` gives `tr τ' = φ_s0(tr τ̄_s + 3p J̄)`; substituting into
`τ' = (∂W_A/∂ln a)I + φ_s0 dev τ̄_s` reproduces the full phase balance with shear terms intact.
**Self-consistent, and the dev-projection is right** (the mineral mean stress is *not* double-counted: the
`(φ_s0/3)tr τ̄_s` piece is absorbed into `∂W_A/∂ln a`).

### 2.2 Energies, EOS, and drained response

**V5.** `eq:equivalent-volumetric-work` (`(1/3)tr τ' δln a + (φ_s0/3)tr σ̄_s δJ̄`) follows from the
purely volumetric mineral variation `δF̄F̄^{-1} = I δJ̄/(3J̄)` with `τ̂_s/J̄ = σ̂_s`, `tr σ̂_s = tr σ̄_s`. **Correct.**

**V6.** Spherical-path matching `K ln J = φ_s0 K_s ln J̄`, `ln a = (1 − K/(φ_s0K_s)) ln J`, and
integration to `W_A(a) = K/[2(1 − K/(φ_s0K_s))] (ln a)^2` (`eq:distention-energy`). Curvature positive under
the stated `0 < K < φ_s0K_s`. The two energy expansions (`eq:equivalent-anisotropic-energy`,
`eq:equivalent-volumetric-energy`) expand to exactly the printed terms, including `(φ_s0K_s/2)(ln J̄)^2` and
the volume–shape coupling `(φ_s0/3) ln J̄ I:ℂ_s:dev ε` that vanishes for an isotropic mineral. **Correct.**

**V7.** `eq:anisotropic-mineral-eos` was obtained by differentiating the energy at fixed `F` and then
collecting terms. I verified the algebra by back-substitution: the expression
`K_s ln J̄ + (1 − K/(φ_s0K_s)) p J̄ − (K/φ_s0) ln J + (1/3)(1 − K/(φ_s0K_s)) I:ℂ_s:dev ε` collapses
identically to zero (the anisotropic shape term cancels exactly), so the EOS is consistent with
`eq:anisotropic-energy-pressure-derivative`; the isotropic limit is `eq:reconstructed-isotropic-source-eos`.
**Correct.**

**V8 (drained compliance/stiffness duality).** I recomputed in Mandel form with the manuscript's own
example `ℂ_s` (`main.tex:eq:example-mineral-stiffness` → `experiments.tex:16-22`), `φ_s0 = 0.6`, `K = 7K_*`:

```
K_s = (1/9) v·ℂ_s·v            = 28.0
ℂ^d = φ_s0ℂ_s − (φ_s0/9K_s)(1 − K/(φ_s0K_s)) (ℂ_s:v)(ℂ_s:v)^T      (eq:drained-stiffness-restriction)
max | (ℂ^d)^{-1} − [ (φ_s0ℂ_s)^{-1} + (1 − K/(φ_s0K_s))/(9K) v v^T ] |
   = 1.39e-17                                                    (eq:drained-compliance-restriction)
(1/9) v·ℂ^d·v = 7.000000000000000  (= K)
```

**The two forms are exact inverses of one another.** The claimed *rank-one, spherical* nature of the
additional compliance is confirmed, and the factor `1/9` (not `1/3`) is correct.

**V9 (reference Biot).** `B_0 = I − ℂ^d:ℂ_s^{-1}:I` (`eq:reference-biot-compatibility`) evaluated
numerically gives `(0.70000000, 0.75833333, 0.79166667, 0, 0, 0)`, i.e. the quoted
`0.7000, 0.7583, 0.7917` (`experiments.tex:26-27`). I also confirmed analytically that this equals the
`F = I, p = 0` limit of `eq:anisotropic-biot-explicit`:
`(1 − K/K_s)I − φ_s0(1 − K/(φ_s0K_s))I + (φ_s0/(3K_s))(1 − K/(φ_s0K_s))(ℂ_s:I)`, since
`1 − K/K_s − φ_s0(1 − K/(φ_s0K_s)) = 1 − φ_s0`. **Two independent routes agree.**

**V10 (explicit pressure-coupling tensor).** `eq:mineral-fixed-pressure-derivative` was re-derived by
differentiating `eq:anisotropic-mineral-eos` at fixed `p` (`∂J̄/∂F = J̄ F^{-T}`); the coefficient
`K_s + (1 − K/(φ_s0K_s)) p J̄` and the RHS `(K/φ_s0)F^{-T} − (1/3)(1 − K/(φ_s0K_s)) ∂(I:ℂ_s:dev ε)/∂F`
follow. Using `B = I − (φ_s0/J)(∂J̄/∂F|_p)F^T` and the appendix identity
`∂(I:ℂ_s:dev ε)/∂F = F[∂log C/∂C : dev(ℂ_s:I)]`, the prefactor `J̄/(J[K_s + (1 − K/(φ_s0K_s))pJ̄])` and
the bracket `K I − (φ_s0/3)(1 − K/(φ_s0K_s)) F[∂log C/∂C:dev(ℂ_s:I)]F^T` are **exactly as printed**.
Symmetry (self-adjoint log-derivative) and objectivity (`B(QF,p) = Q B(F,p) Q^T`) statements hold.
The cubic-symmetry remark (`dev(ℂ_s:I) = 0 ⟹ B` spherical) is correct.

**V11 (storage).** `S_s = −φ_s0 ∂J̄/∂p|_{F=I,p=0}` gives `(φ_s0/K_s)(1 − K/(φ_s0K_s))` from the EOS
(`∂ln J̄/∂p = −(1 − K/(φ_s0K_s))/K_s`), and this equals
`φ_s0 I:ℂ_s^{-1}:I − I:ℂ_s^{-1}:ℂ^d:ℂ_s^{-1}:I`. Mandel example: `S_s = 0.2`, total storage
`(1−0.9)/8 + 0.2 = 17/80 = 0.2125` — matches `finite_elements.tex:283-285` and
`site/reports/mandel-reference.json` (`M = 80/17`).

**V12 (appendix).** From `eq:log-frechet-spectral-form`,
`C:[∂log C/∂C:T] = Σ_i λ_i (T_ii/λ_i) = tr T`, so `tr τ = tr T` (`eq:logarithmic-stress-trace`).
The repeated-eigenvalue branch (`T_ij/λ_i`) is the correct continuous limit. **Correct.**

### 2.3 Section 7.4 (the mandated re-check) and the fabric construction

**V13 (7.3 fabric phase work, `pore_fabric.tex:150-191`).** I re-derived
`δFF^{-1} = δR_AR_A^T + R_A[δ(G^{1/2})G^{-1/2}]R_A^T + R_AG^{1/2}(δF̄F̄^{-1})G^{-1/2}R_A^T` and contracted.
Using `X:M = tr(X^TM)` (so the conjugate of `M = δF̄F̄^{-1}` is the transpose of the trace expression), the
mineral + pressure terms reduce to `φ_s0 G^{1/2}τ̂_sG^{-1/2} : (δF̄F̄^{-1})` — **ordering exactly as printed**
(the apparent `G^{±1/2}` swap is a convention artifact, not an error). In the conformal limit
`G^{1/2} = a^{1/3}I` this returns `eq:distention-mineral-energy-work` identically.

**V14 (7.4 equilibrium, `pore_fabric.tex:194-236`).** The stationarity functional
`∂/∂G [ W_dis(G) + φ_s0 W̄_s(F̄) + φ_s0 p J̄ ] = 0` (`eq:fabric-equilibrium`, line 204) is the correct one:
`∂W_s/∂J̄ = −φ_s0 p` makes `W_s + φ_s0 p J̄` stationary at pressure equilibrium, and positivity of
`φ_s0 p J̄ = φ_s0 p J (det G)^{-1/2} = φ_s0 p J e^{−tr E_dis}` supplies the required convexity of the
retained problem. Restricting to `G = a^{2/3}I` I confirmed the two derivative pieces

```
δ[φ_s0 W̄_s]  = −(φ_s0/3) tr τ̄_s  δ ln a
δ[φ_s0 p J̄]  = −φ_s0 p J̄          δ ln a
⇒  ∂W_A/∂ln a = (φ_s0/3) tr τ̄_s + φ_s0 p J̄     (:= eq:energy-returned-pressure-balance)
```

so the claimed reduction is **exactly correct**. The restriction to `range 𝔻`, the statement that
`𝔻` vanishes on the complement, the "dropped from the minimization by construction and frozen to the
mineral rather than equilibrated" caveat, strict convexity/uniqueness on the retained subspace, and
the explicit identification of the retained (volumetric–axial) degrees of freedom are all stated as
modelling choices and are internally consistent. The objectivity argument
(`A ↦ QA ⇒ G = A^TA` invariant; `W_dis` an isotropic scalar function of `G`, hence of
`tr G, tr G², tr G³`) is correct.

**V15 (fabric compliance and its conformal reduction, `pore_fabric.tex:265-296`).** Re-derived from the
constrained minimization over `E_dis ∈ range 𝔻`: stationarity gives `𝔻:E_dis = σ_∥` hence
`E_dis = 𝔻⁺σ`, and `ε = ε̄ + E_dis` with `ε̄ = (φ_s0ℂ_s)^{-1}σ` yields
`(ℂ^d)^{-1} = (φ_s0ℂ_s)^{-1} + 𝔻⁺` (`eq:fabric-compliance-restriction`). For the conformal case
`W_dis = ½c(ln a)²` with `c = K/(1 − K/(φ_s0K_s))`, `𝔻 = c v v^T` and
`𝔻⁺ = (1/(9c)) v v^T = (1 − K/(φ_s0K_s))/(9K) I⊗I` — **exactly the rank-one term of
`eq:drained-compliance-restriction`** (numerically identical to `1.7e-18`). The claimed reduction is exact.

**V16 (the `e_1…e_6` basis, `pore_fabric.tex:300-320`).** With `m` an arbitrary unit axis and
`p_1, p_2` orthonormal and normal to `m`, I formed
`e_1 = I/√3`, `e_2 = √(3/2)(m⊗m − I/3)`, `e_3 = (p_1⊗p_1 − p_2⊗p_2)/√2`,
`e_4 = √2 sym(m⊗p_1)`, `e_5 = √2 sym(m⊗p_2)`, `e_6 = √2 sym(p_1⊗p_2)`. The Gram matrix is `I_6` to machine
precision; all six norms are exactly 1. **The basis is orthonormal as claimed, including the `√2` on the
two axial-shear members `e_4, e_5` (and on `e_6`), and the `1/√2` on `e_3`.** The count is right: 2 retained
(volumetric, axial) + 4 complementary (the in-plane pair `e_3, e_6` and the axial shears `e_4, e_5`).

**V17 (minimization cross-reference points at the potential).** The only minimization references are
`pore_fabric.tex:198` (7.4, "the equilibrium that minimizes the potential over **G**" → `eq:fabric-equilibrium`,
line 204, whose bracket *is* the potential), `:207-213`, and `:276-282` (7.5, "The minimization in
`eq:fabric-equilibrium`"). **All point at the potential stationarity equation**, none at the distention-stress
definition. **Satisfied.**

**V18 (bar rule vs. section 7).** `main.tex:218-245` was read against every barred/hatted symbol in section 7:
`W̄_s` (per reference mineral volume), `F̄`, `J̄`, `ρ̄_s`, `ρ̄_s0`, `τ̄_s` (mixture frame, per reference mineral
volume), `τ̂_s` (true frame), and `S̄_dis` — which is explicitly carved out as the one exception ("a bar
instead denotes that stress in the intermediate frame, normalized per reference mixture volume", `:229-231`;
`pore_fabric.tex:137-141` says the same). `W_dis, E_dis, S_dis` carry the `dis` subscript, and the text states
that `d` never means distention. **The general bar rule matches every section 7 use; the barred-stress
normalizations are consistent, including the `φ_s0` weight that converts per-mineral-volume to
per-mixture-volume quantities.** I also verified the bar-rule definition of the prescribed boundary datum
`Q̄_f`.

**V19 (nontrivial limiting case, `pore_fabric.tex:388-393`).** Claim: with the volume–axial coupling modulus
zero and an isotropic mineral, the drained compliance is transversely isotropic while `B` stays spherical.
I re-derived it: if `𝔻⁺ = α e_1e_1 + β e_2e_2` with no `e_1–e_2` coupling, then with isotropic
`ℂ_s`, `(ℂ^d)^{-1} = c_1 𝕁 + c_2 e_2e_2 + (1/(2μ_sφ_s0))𝕂_rest`; since `e_2:I = 0` and `𝕂:I = 0`,
`ℂ^d:I = (1/c_1)I` with `c_1 = 1/(K_sφ_s0) + α/3`, so
`B_0 = [1 − 1/(K_s c_1)]I` is **spherical**, while `(ℂ^d)^{-1}` remains transversely isotropic.
This matches the frozen records `no_coupling_isotropic_biot` and `frozen_shape_isotropic_biot`
(`build/fabric/fabric-verification.json`: `B_par = B_per = 0.8838709677419355`, anisotropy ≈ `1.1e-16`)
versus `coupling_gives_anisotropy` (`0.85065442 / 0.91026998`). **Correct.**

### 2.4 Index / factor / rank / symmetry / objectivity summary

No defect found in: index bookkeeping (mixed-tensor push-forward and its inverse), the `a^{1/3}` cancellation,
the `φ_s0` / `J̄` / `J` weights, the `1/3` trace factors in the logarithmic split, the `1/9` in the compliance
restriction, the rank-one character of the conformal additional compliance, the symmetry of `B` and of the
distention stress, or the objectivity statements for both energies. The `nxn=1` (Mandel `v·v = 3`) factors in
the Moore–Penrose inverse are handled correctly (`𝔻⁺ = (1/9c)vv^T`), which is the step most easily gotten
wrong.

---

## 3. QUOTED VALUES vs. FROZEN ARTIFACTS

All quoted numbers were recomputed or read from the frozen artifacts named in the manuscript. Every one matches.

| Manuscript claim | Location | Frozen artifact | Verified |
|---|---|---|---|
| reference Biot `0.7000, 0.7583, 0.7917` | `experiments.tex:26-27` | recomputed `I − ℂ^d:ℂ_s^{-1}:I` | `0.70000000 / 0.75833333 / 0.79166667` |
| `K_s = 28K_*`; isotropic-comparison `μ_s = 16.8K_*` = ½ × mean of the five deviatoric modes | `experiments.tex:24-33` | recomputed | modes `20, 24, 28, 42.96678, 53.03322`; mean `33.6`; half `16.8` |
| Mandel `G = 0.75`, `B = 0.6`, total storage `17/80` | `finite_elements.tex:283-285` | `site/reports/mandel-reference.json` | `G = φ_s0μ_s = 0.75`; `1 − K/K_s = 0.6`; storage `17/80`; `M = 80/17` |
| conformal suite `186` checks; `65` per-state identities (5 × 13) + 2 reference relations; max constitutive error `2.5e-9` | `experiments.tex:184-189` | `build/conformal/verification.json`, `site/reports/conformal-verification.json` | `checks_passed = 186`, `legacy_identities_rechecked = 67`, `max_constitutive_identity_error = 2.4549890e-09` |
| spherical-gauge suite `273` states across `13` mineral stiffnesses | `experiments.tex:190-191` | `site/reports/tensor-verification.json` | `materials = 13`, `states_per_material = 21`, `total_states = 273` |
| MMS spatial orders `p 2.00/2.00`, `u_x 2.99/2.96`, `u_y 3.00/2.96` | `finite_elements.tex:311-315` | `fe-evidence/mms-convergence.json`, `site/reports/mms-convergence.json` | `p 1.99663/2.00081`; `ux 2.99167/2.95848`; `uy 2.99826/2.95999` |
| temporal successive-difference orders at `nx=16/32/64` lie between `0.98` and `1.40` | `finite_elements.tex:316-319`, `main.tex:591` | same | min `0.97830`, max `1.39690` (9 values) |
| linear step refinement `3.7e-3`, `7.1e-3`; ratio `1.94` | `main.tex:587-589`, `finite_elements.tex:320-321` | `figures/fe_mandel_refinement.csv`, `.../linear_time_0.001|0.002/analysis.json` | `0.00365796`, `0.00710392`; ratio `1.9421` |
| floor `3.2e-3` at `nx=20, dt=1e-3` | `main.tex:585-586`, `finite_elements.tex:322-324` | `figures/fe_load_limit.csv`, `.../nonlinear_load_0.0001/analysis.json` | `0.00322092` (loads `1e-3`: `0.003448`; `1e-2`: `0.005706`) |
| fabric reconstruction `2.2e-16`, `det H − 1 = −3.3e-16`, `‖𝔻:e_3‖ = 1.6e-16`, `𝔻:e_6 = 0`, rotation invariance `2.5e-16` | `finite_elements.tex:399-404` | `build/fabric/fabric-verification.json` | `2.2204e-16`, `−3.3307e-16`, `1.5823e-16`, `0.0`, `2.4965e-16`; `H` eigenvalues `h^{-2},h,h` |
| NumPy re-implementation worst absolute difference `4.9e-15` | `finite_elements.tex:404-409` | same (`worst_probe_abs_diff`) | `4.8850e-15` |
| volume-only limit `1.9e-14` | `finite_elements.tex:416-417` | same (`conformal_cross_check`) | max `1.8742e-14` |
| coupled peaks `4.36`, `4.99`, `5.52`, `3.62` `×10^{-5}` | `finite_elements.tex:449-453` | `figures/fe_fabric_mandel_peak.csv` | `4.3628e-5`, `4.9901e-5`, `5.5211e-5`, `3.6164e-5` |
| refined contour peaks `3.61`, `4.35`, `4.97`, `5.50` `×10^{-5}`; max on `X_1=0`, zero at `X_1=1` | `finite_elements.tex:461-466` | `figures/fe_fabric_contours.csv` | `3.6062e-5`, `4.3491e-5`, `4.9737e-5`, `5.5031e-5`; `p_max_x = 0.0` |
| displacement magnitudes `5.18`, `5.14`, `2.38`, `5.26` `×10^{-5}` | `finite_elements.tex:466-469` | same (`u_mag_max`) | `5.1826e-5`, `5.1372e-5`, `2.3818e-5`, `5.2587e-5` |
| reconstruction suite: work equivalence, finite unjacketed compression | `experiments.tex:191-192` | `site/reports/reconstruction-verification.json` | compliance `1.4e-16`, work equivalence `5.0e-10`, unjacketed `5.1e-14`, minimization `2.7e-9`, `20/20` incompatible pairs rejected |

No quoted value was found to disagree with a frozen artifact.

---

## 4. REQUIRED CHANGES

**None.** I found no derivation, index, factor, rank, symmetry, objectivity, or limiting-case error, and no
quoted value that disagrees with the frozen artifacts. The specific items the review emphasis asked me to
re-check (7.4 justification; bar rule vs. section 7; barred-stress normalizations; orthonormality of
`e_1…e_6` including the `√2` members; the minimization cross-reference) are all now stated correctly, and the
independent checks I performed reproduce the manuscript's own consistency claims. Because there is nothing
that must change, this section is empty by design.

## 5. OPTIONAL NOTES

**R1-O1 — `main.tex:236-238` (cross-reference precision).** "a double prime denotes the fixed-pressure stress
of `\eqref{eq:cauchy-pressure-tangent}`" points at the pressure-tangent equation
(`main.tex:540`, `∂σ/∂p|_F = −B`), which is not where the double-prime stress is introduced. `σ''` is defined
by `eq:fixed-pressure-stress` (`main.tex:450`) and the relation `σ = σ'' − pB` by `eq:finite-biot-tensor`
(`main.tex:462`). Consider citing `eq:fixed-pressure-stress`/`eq:finite-biot-tensor` here. The notation is
unambiguous from §5, so this is presentational.

**R1-O2 — `main.tex:242-244` (enumeration completeness).** "The distention quantities instead carry the
subscript `dis`: `W_dis`, `E_dis`, and `S_dis`" omits the barred work-conjugate `S̄_dis`, which is established
separately at `main.tex:229-231` and `pore_fabric.tex:137-141`. Adding it to the enumeration (or wording the
sentence as non-exhaustive) would prevent a reader from concluding that every distention stress is unbarred.

**R1-O3 — `main.tex:225-231` (sentence scope).** "The barred stresses also carry different normalizations:"
introduces two normalization cases and then one *frame* case (`S̄_dis`). Separating the sentence into a
normalization clause and a frame clause would read more cleanly.

**R1-O4 — `pore_fabric.tex:210` (wording).** "On the complement `𝔻` vanishes" is correct in meaning but reads
as if the complement is the domain; "On its complement, `𝔻` vanishes" removes the ambiguity.

**R1-O5 — `pore_fabric.tex:313-318` (order of presentation).** The four complementary modes are introduced as
`e_3`, `e_6`, then `e_4`, `e_5`. Listing them in index order (`e_3, e_4, e_5, e_6`) would make the
orthonormality claim easier to check against the definitions (the mathematics is correct as written — verified
in V16).

**R1-O6 — `main.tex:230`, `pore_fabric.tex:140` (terminology).** `S̄_dis = 2∂W_dis/∂G` is conjugate to
`G = A^TA`, a right Cauchy–Green (material/reference-type) tensor; calling it "the intermediate frame" is
loose, since the intermediate configuration is where `F̄` acts. Since both locations use the same term
consistently, this is a terminology refinement only ("the distention (material) frame"). If that reading is
intended, the `S̄_dis` entry in the bar rule is fully consistent with the general rule.

---

## 6. RECOMMENDATION SUMMARY

The derivation chain — multiplicative decomposition and conformal specialization; the volume-fraction-weighted
phase stress and its Kirchhoff form; the reversible-work/energy equivalence and the pressure cancellation; the
volumetric and distention energies; the anisotropic mineral equation and the explicit pressure-coupling
tensor; the drained stiffnes s/compliance duality and the reference Biot tensor; the isotropic and
isotropic-mineral reductions; the unjacketed path; and the tensorial fabric extension with its equilibrium,
compliance, and transverse-isotropic limit — was re-derived from its stated starting points and independently
cross-checked numerically where closed forms exist. The section 7.4 justification, the bar rule, the barred
normalizations, the `e_1…e_6` orthonormality, and the minimization cross-reference are now correct, and all
quoted values agree with the frozen artifacts. Only presentational notes remain.

VERDICT: ACCEPT

# Round 18 — Reviewer 1 (mathematics and correctness)

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work*
**Snapshot:** round-18, `SNAPSHOT_ID 810b503058701b0d3f43ef39cba2c6952e28a5e8b0728321849b0129a60e3625`
**Scope:** mathematics and correctness. Independent full pass; no prior-round verdict read.

---

## 1. Snapshot identity and manifest

- **Identity check — PASS.** `sha256(source-manifest.json)` =
  `810b503058701b0d3f43ef39cba2c6952e28a5e8b0728321849b0129a60e3625`,
  equal to `SNAPSHOT_ID`.
- **Manifest re-hash — PASS.** All 438 entries re-hashed in the snapshot:
  **438 OK, 0 missing, 0 mismatch.**
- Reviewed only the frozen snapshot; nothing edited, committed, or pushed.

---

## 2. Re-derivations (all reproduced; no defects found)

Every displayed relation was re-derived from the sources independently of the
package scripts. Each agreed with the manuscript.

1. **Kinematics / distention, `eq:spherical-distention`, `eq:conformal-mineral-metric`.**
   With `F = A F̄`, `A = a^{1/3} R_A` (`R_A` proper rotation),
   `F̄ = a^{-1/3} R_A^T F`, one gets `C̄ = a^{-2/3} C` and `Ū = a^{-1/3} U`.
   Correct.

2. **Phase stress balance.** `σ = φ_s σ̄_s − (1−φ_s)p I` implies
   `σ' = σ + p I = φ_s(σ̄_s + p I)`; with `Jφ_s = φ_s0 J̄`,
   `τ' = φ_s0(τ̄_s + p J̄ I)`. Correct.

3. **Work equivalence.** The virtual-deformation decomposition
   `δF F^{-1} = (1/3)δln a·I + δR_A R_A^T + R_A(δF̄ F̄^{-1})R_A^T`
   with skew `δR_A R_A^T` contracting to zero against symmetric `τ'` gives
   `δW_s = (1/3)tr τ'·δln a + φ_s0 τ̂_s:(δF̄ F̄^{-1})`. The identity
   `R_A^T τ' R_A − φ_s0 p J̄ I = φ_s0 τ̂_s` is correct; the fluid-pressure work
   cancels without requiring coaxiality of mineral stress and strain. Correct.

4. **Energy-returned effective stress, `eq:energy-returned-effective-stress`,
   `eq:energy-returned-pressure-balance`.** Differentiating
   `W_s = W_A(a) + φ_s0 W̄_s(F̄)` at fixed `J̄` returns
   `τ' = (∂W_A/∂ln a) I + φ_s0 dev τ̄_s`; the pressure balance
   `∂W_A/∂ln a = (φ_s0/3)tr τ̄_s + φ_s0 p J̄` substitutes to recover
   `τ' = φ_s0(τ̄_s + p J̄ I)`. Both verified term-for-term.

5. **Logarithmic strain split, `eq:constrained-mineral-logarithmic-strain`.**
   `ε̄ = ε − (ln a/3)I` and `ε̄ = dev ε + (ln J̄/3)I`. Correct.

6. **Spherical drained path and distention energy.** Trace of
   `τ' = φ_s0 τ̄_s` at `p=0` gives `K ln J = φ_s0 K_s ln J̄`, hence
   `ln a = (1−r)ln J` with `r = K/(φ_s0 K_s)`, and
   `W_A = K/(2(1−r))(ln a)^2`. Correct.

7. **Anisotropic mineral EOS, `eq:anisotropic-mineral-eos`.** Applying
   `∂W_s/∂J̄|_F = −φ_s0 p` to the expanded energy reproduces
   `0 = K_s ln J̄ + (1−r)p J̄ − (K/φ_s0)ln J + (1/3)(1−r) I:C_s:dev ε`.
   The intermediate `eq:anisotropic-energy-pressure-derivative` and its
   "collecting terms" step are both correct. The strict-monotonicity /
   unique-positive-root argument and the negative-pressure branch condition
   `eq:trace-mineral-stability-domain` are correct.

8. **Drained anisotropic distention, `eq:drained-anisotropic-distention`.**
   `ln a = (1−r)/(3K_s) I:C_s:ε` — reproduced both from the EOS at `p=0`
   and from `I:C^d:ε = (K/K_s) I:C_s:ε`. Correct.

9. **Drained stiffness restriction, `eq:drained-stiffness-restriction`, and
   compliance restriction, `eq:drained-compliance-restriction`.** From
   `C^d:ε = φ_s0 C_s:ε̄` with `ε̄ = ε − (ln a/3)I` and
   `ln a = (1−r)/(3K_s) I:C_s:ε`, one obtains
   `C^d = φ_s0 C_s − (φ_s0/9K_s)(1−r)(C_s:I)⊗(C_s:I)`. The compliance form
   follows from `ε = ε̄ + (ln a/3)I` with
   `ln a = (1−r)/(3K) I:C^d:ε` (`eq:drained-distention-from-stress`), giving
   `(C^d)^{-1} − (φ_s0 C_s)^{-1} = (1−r)/(9K) I⊗I`. The rank-one / spherical
   interpretation is exact.

10. **Finite Biot tensor, `eq:finite-biot-tensor`, and pore-volume identity,
    `eq:biot-pore-volume-variation`.** From
    `P' = P'' + φ_s0 p (∂J̄/∂F)|_p` with `σ' = σ + p I` and the push-forwards,
    `σ = σ'' − p B` with `B = I − (φ_s0/J)(∂J̄/∂F)|_p F^T`. The identity
    `δ(J − φ_s0 J̄)/J = B:(δF F^{-1})` (δp = 0) follows by direct
    differentiation. Both correct.

11. **Explicit Biot tensor, `eq:anisotropic-biot-explicit`.** Differentiating
    the EOS at fixed `p` reproduces `eq:mineral-fixed-pressure-derivative`
    exactly, and the identity
    `∂_F[I:C_s:dev ε]·F^T = F[∂logC/∂C:dev(C_s:I)]F^T` holds (verified in
    components via the spectral form in `eq:log-frechet-spectral-form`). The
    cubic-symmetry statement `dev(C_s:I)=0` is correct.

12. **Reference Biot, `eq:reference-biot-compatibility`.** At `F=I, p=0` the
    explicit tensor reduces to `B_0 = I − C^d:C_s^{-1}:I`, and to the closed
    form `B_0 = (1−φ_s0)I + (φ_s0(1−r)/3K_s)(C_s:I)` — both agree. Isotropic
    limit `(1−K/K_s)I` correct.

13. **Reference solid storage, `eq:reference-solid-storage`,
    `eq:reference-storage-compatibility`.** `S_s = (φ_s0/K_s)(1−r)` equals
    `φ_s0 I:C_s^{-1}:I − I:C_s^{-1}:C^d:C_s^{-1}:I` exactly (verified by
    Woodbury structure; the `I⊗I` term makes the two equal even for
    anisotropic `C_s`). Total storage `(1−φ_s0)/K_f + S_s` is the standard
    Biot storage.

14. **Cauchy-pressure tangent, `eq:cauchy-pressure-tangent`.** From the mixed
    second derivative of `W'`, `∂P'/∂p|_F = φ_s0 (∂J̄/∂F)|_p`, hence
    `∂σ/∂p|_F = −B`. Consistent with `σ = σ'' − p B` despite `σ''` itself
    depending on pressure (the two pressure dependences exactly cancel, as the
    manuscript states). Correct.

15. **FE weak forms, `eq:fe-total-first-piola`, `eq:fe-momentum-residual`,
    `eq:fe-fluid-residual`, and fluid closure.** `P = J σ F^{-T}`; referential
    fluid mass `m_f = ρ̄_f(J − φ_s0 J̄)`; storage `eq:fe-fluid-storage`;
    deformation coupling `δm_f|_p = ρ̄_f J B:(δF F^{-1})` (via
    `eq:biot-pore-volume-variation`); reference Darcy law
    `Q_f = −(J ρ̄_f k/μ_f) F^{-1}F^{-T} Grad p`. All correct, and the total
    reference storage `eq:fe-reference-total-storage` reduces to
    `(1−φ_s0)/K_f + S_s`. No spurious effective-stress correction is applied,
    consistent with `P` already containing the fluid term.

---

## 3. Published numbers recomputed from raw data

| Claim | Artifact | Value found | Match |
|---|---|---|---|
| Reference Biot components 0.7000 / 0.7583 / 0.7917 | `experiments.json` + closed form | 0.7 / 0.758333 / 0.791667 (exact) | ✓ |
| `K_s = 28K_*`, `K = 7K_*`, `φ_s0 = 0.6` | `experiments.json` | `(1/9)I:C_s:I = 28`, given 7, 0.6 | ✓ |
| Isotropic comparison `μ = 16.8K_*` | eigenvalue analysis of `eq:example-mineral-stiffness` | mean of 5 deviatoric modes = 33.6 → /2 = 16.8 | ✓ |
| Drained shear `G = 0.75`; reference Biot 0.6; storage 17/80 | `mandel-reference.json` | `G=0.75`, `α=0.6`, `M=80/17` | ✓ |
| MMS spatial orders ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00 | `mms-convergence.json` | 2.9917/2.9585, 2.9983/2.9600, 1.9966/2.0008 | ✓ |
| MMS temporal difference orders | `mms-convergence.json` | nx16 1.093/0.978/1.015; nx32 1.397/1.018/1.125; nx64 1.396/1.076/1.252 | ✓ |
| Mandel peak overshoot 5.4659% at t=0.01516535 | `mandel-reference.json` | ratio 1.0546586…, t=0.01516535… | ✓ |
| Load-limit floor ≈3.2e-3 at nx=20, dt=1e-3 | `figures/fe_load_limit.csv` | 3.2209197e-3 (load 1e-4) | ✓ |
| Conformal suite max identity error 2.5e-9 | `conformal-verification.json` | `max_constitutive_identity_error` 2.4549890e-9 | ✓ |
| 186 named checks; 65 (=5×13) + 2 reference | `conformal-verification.json` | `checks_passed` 186; `legacy_identities_rechecked` 67 | ✓ |
| 273 states across 13 stiffnesses | `tensor-verification.json` | `total_states` 273, `materials` 13 | ✓ |
| 110 fluid checks, max scaled error 8.09e-9 | `fluid-coupling-verification.json` | `count` 110, `maximum_scaled_error` 8.0867e-9 | ✓ |
| C++–Python agreement 6.4e-14 over 41 states | `cpp-python-constitutive.json` | 6.3948846e-14, 41 states | ✓ |

All recomputed values agree with the published figures (differences are
rounding of the stated significant figures only).

---

## 4. Notation clause in §2 (bar convention)

The new one-line clause — "A bar on a prescribed boundary datum, such as the
mass flux `\bar Q_f` of `\eqref{eq:fe-fluid-residual}`, denotes its prescribed
value on that boundary" — is **consistent** with the notation actually used:

- `\bar Q_f` (scalar prescribed datum) vs `Q_f` (referential mass-flux vector)
  is used exactly this way in `eq:fe-fluid-residual` and in the boundary
  statement `Q_f · N = \bar Q_f` on `Γ_Q`. No conflict.
- The other three declared rules (kinematic/energetic → mineral state;
  intrinsic density → per-phase-volume value; stress → mixture frame vs hat →
  true frame) are each applied consistently across `main.tex` §2 and
  `sections/finite_elements.tex`. In particular `ρ̄_f`, `ρ̄_f0` conform to the
  intrinsic-density rule; `F̄, J̄, C̄, Ū, ε̄, W̄_s` to the mineral-state rule;
  `σ̄_s, τ̄_s` vs `σ̂_s, τ̂_s` to the stress-frame rule.
- The forward reference `\eqref{eq:fe-fluid-residual}` and the reference
  `\eqref{eq:rotated-mineral-cauchy}` both resolve to defined targets.

The bar/hat convention carries four documented meanings (a mild surface
tension), but each is explicitly declared and applied consistently; this
introduces no mathematical or referencing error.

---

## 5. Findings

**REQUIRED: none.** I found no mathematical or correctness defect, and no
published number that I could not reproduce against its listed artifact.

**Optional observations (non-blocking, not required for acceptance):**

- **NOTE 1** — `\pder{W'}p`, `\pder{\mathbf\sigma}p`, and
  `\pder{\bar J}p` in the finite-Biot section leave the second `\pder`
  argument unbraced. They render correctly because each argument is a single
  token, but this is inconsistent with the braced style used elsewhere.
- **NOTE 2** — The MMS temporal "successive-difference orders" at nx=32/64
  give ux ≈ 1.4, above the asserted backward-Euler value of 1. The manuscript
  and `evidence.json` both state this honestly and explicitly claim "no order
  above one"; the wording is defensible, but a reader could misread the
  ≈1.4 values as a superconvergence claim without the surrounding explanation.
- **NOTE 3** — The `3.2×10^{-3}` floor is the *smallest-load* value; the
  load-sequence (1e-2 → 5.71e-3, 1e-3 → 3.45e-3, 1e-4 → 3.22e-3) is
  monotone decreasing but the floor is reached only at the smallest load
  tested. The wording "floors at about 3.2×10^{-3}" is accurate.

---

## VERDICT: ACCEPT

Required corrections:

1. *(none)*

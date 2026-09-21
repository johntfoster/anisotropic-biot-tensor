# SIMULATED AI PEER REVIEW — Reviewer 1

**Emphasis:** derivation and correctness (not a journal decision).

**Snapshot reviewed (frozen, read-only):** `.agent-runtime/review-snapshots/round-29`
**Declared SNAPSHOT_ID:** `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`

All work below was done against a temporary copy (`/tmp/r29-r1/snap`); nothing inside the
snapshot and nothing in the working tree was modified. I ran none of the repository's held
numerical suites (`validation/`, `examples/verify_*.py`); every number quoted below was
recomputed from the frozen artifacts or derived by hand/NumPy in the temporary copy.

## Mandatory verification

1. **Manifest hash.** `sha256sum .agent-runtime/review-snapshots/round-29/source-manifest.json`
   = `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`. Equals the declared
   SNAPSHOT_ID. **PASS.**
2. **Per-file hash re-check.** Every entry of `source-manifest.json` re-hashed against the
   manifest in the temporary copy:
   - entries listed: **592**
   - hashed and matching: **592**
   - mismatches: **0**; missing files: **0**
   - files present but unlisted: **2** (`SNAPSHOT_ID`, `source-manifest.json` — the manifest's
     own self-referential files, expected).

   **Result: 592/592 verified. PASS.**
3. **Build.** `build/main.log` contains **0** `LaTeX Warning` lines and no undefined
   references or citations; `build/main.pdf` is 34 pages (metadata date 2026-09-21).

---

## Part A — Derivation and correctness: independent recomputation

I re-derived the manuscript's central results from their stated assumptions and checked each
against the text. Everything below **passed**; nothing in Part A is a defect.

**A1. The Biot tensor, both routes (eqs. `finite-biot-tensor`, `biot-pore-volume-variation`,
`reference-biot-compatibility`).** Differentiating `W'(F,p) = W_s(F,J̄(F,p)) + φ_s0 p J̄` at
fixed `p` gives `δW' = τ': (δF F⁻¹) + φ_s0(∂J̄/∂F|_p + p J̄ B̃):δF`, so the energy-Biot tensor
`B̃ = δ'(F) W' F^T` and the mineral-volume route `B = I - (φ_s0/J) (∂J̄/∂F) F^T` differ
exactly by the pressure term; at `p = 0` both reduce to
`B_0 = I - ℂ^d : ℂ_s⁻¹ : I`. This also coincides with the finite-strain Biot definition used in
the companion manuscript (Foster, unpublished, cited as ref. [9]). The isotropic form
`(1 - K/K_s) I` follows when both stiffnesses are isotropic. **Correct.**

**A2. The conformal model is internally consistent only for one `α`.** Requiring the prescribed
drained stiffness `(1/9) I:ℂ^d:I = K` forces the mineral-volume-EOS coefficient
`1 - K/(φ_s0 K_s)` to equal the same `α` that appears in `ℂ^d`. I verified this by pushing
`ℂ^d = φ_s0ℂ_s - (φ_s0/(9K_s))α (ℂ_s:I)⊗(ℂ_s:I)` through
`(ℂ_s⁻¹ + (1/φ_s0)(α/K)Λ)⁻¹` and back onto `ℂ_s`, and by evaluating the spherical-trace and
uniaxial identifications symbolically. **The stated EOS, stiffness, and compliance are mutually
consistent.** Same for the algebraic form
`S_s = φ_s0 I:ℂ_s⁻¹:I - I:ℂ_s⁻¹:ℂ^d:ℂ_s⁻¹:I`, which I verified equals
`(φ_s0/K_s)(1 - K/(φ_s0K_s))` in both the isotropic and anisotropic cases (the second form is a
`K_s`-normalized `φ`-weighted contraction; my first hand pass dropped a factor 3 in the final
`I:(·):I` and the closed form is correct).

**A3. Drained restrictions are the exact Moore–Penrose result (eqs. `drained-compliance-restriction`,
`drained-stiffness-restriction`).** From the minimizer
`𝔼_dis = (𝔻 + φ_s0 P_ℂ_s)⁻¹ : φ_s0 P_ℂ_s : ε`,
`ℂ^d = φ_s0ℂ_s - φ_s0ℂ_s:(𝔻+φ_s0P_ℂ_s)⁻¹:φ_s0ℂ_s`, with
`𝔻 = (α/(9K))I⊗I`, `α = 1 - K/(φ_s0K_s)`, I verified the push-through identity
`[ℂ_s⁻¹ + (α/(9K φ_s0))I⊗I]⁻¹ = ℂ_s - ℂ_s (α/(9Kφ_s0))(I⊗I) ℂ_s / (1 + tr α/(9Kφ_s0))`
with `tr = 3K_s` gives exactly `(1/φ_s0)ℂ^d` for **every** `K` (not only `α = 1`). **Correct.**

**A4. Fabric construction (secs. `fabric-kinematics`–`fabric-biot`).** Verified: (i) the finite
distention energy and its conjugacy; (ii) the *non-annihilation* counterexample — if
`E_dis ∈ ker𝔻` then `σ̄'' = -φ_s0 p(·)` is isotropic, `τ' = σ̄'` is isotropic in the mixture
frame, so `C_s:devε̄ ∝ devε̄` and `D:devε̄ = 0`; hence a shape change (`devε̄ ≠ 0`) requires
non-annihilation, exactly as argued; (iii) the transverse-isotropy bijection
`ℂ^d = φ_s0ℂ_s - sΛ = ℂ_s:ℂ_s⁻¹:ℂ^d` for `ℂ_s = c_vΛ + 2μ_s Dev`, `ℂ^d` transversely isotropic
with the same axis, and preservation of the tube `p₃(ε) = -p₁`; (iv) the non-annihilation
condition `𝔻:e₃ = φ_s0 P_range(ℂ_s:e₃)` — so `𝔻:e₃ = 0` **iff** `ℂ_s:e₃ ∈ ker𝔻`, matching the
text's "unless … pure in-plane shear"; and for any mineral with the same transverse axis the
in-plane pair is annihilated automatically (reflection argument), so `𝔻:e₃ = 0` and
`‖𝔻:e₆‖ = 0` for both check sets. **Correct.**

**A5. Fabric reference storage is *derived*, not assumed.** The manuscript leaves
`S_s = -φ_s0 ∂J̄/∂p` implicit for the fabric law. Solving the section's own equilibrium
`(𝔻 + φ_s0G)x = φ_s0(g + p√3 ê₁)` gives `∂J̄/∂p = -3φ_s0[(𝔻+φ_s0G)⁻¹]₁₁`, i.e.
`S_s = 3φ_s0²[(𝔻+φ_s0G)⁻¹]₁₁`. I computed this and the compiled identity
`(φ_s0/K_s)(1 - K^d/(φ_s0K_s))` (with `K^d = (1/9)I:ℂ^d:I`) for all three modulus sets in the
decks and they agree to **1.4×10⁻¹⁶ relative** (probe `k_v=k_a=1`; mandel `5.4/1/0.4`;
mandel uncoupled). The compiled `storage`, the compiled `Jbar`'s pressure slope, the reference
fluid-mass coefficient, and the equilibrium are therefore mutually consistent — this is the
strongest internal-consistency check available for the linearized fabric law, and it holds.

**A6. Element-level implementation matches the continuum equations.** Read against the source:
`ConformalLaw.h` (log-`C` Fréchet derivative by Gauss quadrature `∫₀¹ (I+tD)⁻¹T(I+tD)⁻¹dt`, the
implicit `q = ln J̄` root with an exact AD derivative `dq/dχ = -resₓ/den`, `τ = F[∂logC/∂C:T]F^T`,
`σ = φ/J τ - (1-φ_s)pI`, `P = JσF⁻ᵀ`, `B = I - J̄/(J[K_s+αpJ̄])[KI - (φ/3)α F[∂logC/∂C:dev(ℂ_s:I)]F^T]`,
`m_f = ρ(J - φJ̄)`, `ρ = ρ₀e^{p/K_f}`, flux `= -k/μ_f JρF⁻¹F⁻ᵀ∇p`), `FabricLaw.h` (the
reference-state equilibrium, `ε̄ = ε - E_dis`, `𝔹 = I - ℂ^d:ℂ_s⁻¹:I`, `b_∥, b_⊥`, `ln a = √3x₁`,
`ln h = -x₂/√1.5`, storage), and `ReferenceBalance.C` (`∫∇v:P`, `∫w ∂_t m - ∫∇w·W`) reproduce
eqs. `finite-biot-tensor`, `anisotropic-biot-explicit`, `fe-fluid-storage`,
`fe-reference-darcy-law`, `fabric-compliance-restriction`, `fabric-transverse-strain`,
`fe-momentum-residual`, `fe-fluid-residual` term for term. **No discrepancy.**

**A7. Quoted numbers recomputed from frozen artifacts — all reproduce.**

| Manuscript claim | Recomputed | Verdict |
|---|---|---|
| `H` reconstruction diff `2.2×10⁻¹⁶` | `H_reconstruction_max_abs_diff = 2.2204×10⁻¹⁶` | PASS |
| `det H - 1 = -3.3×10⁻¹⁶` | `-3.3307×10⁻¹⁶` | PASS |
| `‖𝔻:e₃‖ = 1.6×10⁻¹⁶`, `𝔻:e₆ = 0` | `1.5823×10⁻¹⁶`, `0.0` | PASS |
| rotation invariance `2.5×10⁻¹⁶` | `2.4965×10⁻¹⁶` | PASS |
| NumPy worst field diff `4.9×10⁻¹⁵` | `4.8850×10⁻¹⁵` | PASS |
| volume-only limit `1.9×10⁻¹⁴` | max of `conformal_cross_check` = `1.8742×10⁻¹⁴` | PASS |
| conformal "largest constitutive-identity error `2.5×10⁻⁹`" | max over `implementation`+`analytical` = `2.45499×10⁻⁹` | PASS |
| contour peaks `3.61 / 4.35 / 4.97 / 5.50 ×10⁻⁵` | `3.60619 / 4.34914 / 4.97366 / 5.50314 ×10⁻⁵` | PASS |
| contour `\|u\|` peaks `5.18 / 5.14 / 2.38 / 5.26 ×10⁻⁵` | `5.18264 / 5.13716 / 2.38184 / 5.25869 ×10⁻⁵` | PASS |
| "maximum lies on the `X₁=0` line" | `p_max_x = 0.0` for all four contour cases | PASS |
| probe `B_∥, B_⊥` (`0.88387096774194`; coupled `0.85065441979279 / 0.91026997979915`) | recomputed in NumPy from the deck mineral stiffness + fabric moduli: identical to the last digit | PASS |
| mandel `B_∥, B_⊥ = 0.57737298283364 / 0.61528504589908` | identical to the last digit at 0°, 45°, 90° | PASS |
| conformal-limit probe `B_∥ = B_⊥ = 0.6`, `ln h = 0`, `C^d = {2.0, 0.5}` | `fabric_probe_conformal` (`k_v = 5.4 ⇒ k = 1.8 = 1/(1-ρ)`): `0.6/0.6`, `-1.25×10⁻¹⁴`, `1.9999999999985/0.50000000000075` | PASS |
| mandel inputs `K_s=2.5`, `μ_s=5/6`, `φ_s0=0.9`, `G=0.75` (φ_s0μ_s), `B=0.6`, storage `17/80` | all confirmed; storage `= 0.0125 + 0.2 = 0.2125 = 17/80` | PASS |

**A8. Rendered equations.** Pages 4–6, 12–13 and 22–23 of `build/main.pdf` were inspected at
raster resolution. No broken, overlapping, clipped, or garbled display equations, and no
missing figure placeholders.

---

## REQUIRED CHANGES

### R1-C1 — The stated reason that the reduced `𝔻` commutes with rotations about `m` is not a valid inference
**Location:** `sections/pore_fabric.tex`, lines 306–311 (§`sec:fabric-biot`).
**Quoted text:** "That reduced \(\mathbb{D}\) is transversely isotropic about \(\mathbf m\): it
annihilates both members of the coupled in-plane pair … \(\mathbf e_3\) … and
\(\mathbf e_6=\sqrt2\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)\), **so it commutes with
rotations about \(\mathbf m\).**"
**Problem:** annihilation of `e₃` and `e₆` does not imply invariance under rotations about `m`.
The annihilation only constrains `range 𝔻` to be orthogonal to `span(e₃,e₆)`. A tensor
`𝔻' = 𝔻 + s₁⊗s₁` (with `s₁ = sym(m⊗p₁)`, one of the two axial-shear modes) still annihilates
`e₃` and `e₆` but is **not** invariant under rotations about `m`, because a rotation about `m`
mixes `s₁` and `s₂ = sym(m⊗p₂)`. Since the paper elsewhere relies on the transverse isotropy of
`𝔻` (it is what makes the drained compliance transversely isotropic and hence eq.
`fabric-transverse-biot` hold), a reader reconstructing the argument from the printed reason
cannot get there. The true reason is already available one clause earlier: `𝔻 = Σ_{i,j} D_ij
e_i⊗e_j` with `e₁ = I/√3` and `e₂ = √(3/2)(m⊗m − I/3)` both functions of `m` alone, so `𝔻` is
invariant under every rotation about `m`; the annihilation of the four complementary modes
(including `e₃`, `e₆` **and** the two axial shears) is a consequence, not the cause.
**Required:** either delete the causal clause, or replace it with the correct statement, e.g.
"…because `e₁` and `e₂` are invariant under rotations about `m`; equivalently it annihilates the
four complementary modes, including the coupled in-plane pair `e₃`, `e₆`." One sentence; no
other text depends on the change.

---

## OPTIONAL NOTES (no change required)

**R1-N1 — Name all four annihilated modes where the count is asserted.** §`sec:fabric-biot` and
§`sec:fe-fabric` both say four complementary modes are frozen, but only `e₃` and `e₆` are named,
and `debug`/`fabric-verification.json → tensor_checks` records only `D4_e3_norm` and
`D4_e6_norm`. The remaining two (`sym(m⊗p₁)`, `sym(m⊗p₂)`) are annihilated identically by
construction, so nothing is unverified — naming them (and, if cheap, adding the two numbers)
would make the recorded evidence cover the whole claim.

**R1-N2 — State once, next to the coupled transient runs, that they use the reference-state
fabric material.** The fabric paragraph discloses that the material "evaluates the reference-state
drained stiffness, the Biot tensor, and the distention strains", and the contour paragraph
already says "no mesh-convergence claim is made for these runs". The decks confirm
`linear_reference = true` for `fabric_mandel_*`, `fabric_contour_*`, and every `fabric_probe_*`.
A half-sentence in the contour paragraph would prevent a reader from reading the transient
histories as finite-deformation updates.

**R1-N3 — `fabric_probe_conformal` is the cleanest confirmation of the reduction claim and is
currently only implicit.** Its parameters (`k_v = 5.4` with a frozen axial mode) give
`k = 1.8 = 1/(1-ρ)`, and the recorded cross-check against `ConformalMaterial` closes to
`1.87×10⁻¹⁴`. That is the quantitative statement of "reduces to the conformal law rather than
merely approximating it"; citing the number in `sec:fe-fabric` would tie the prose to evidence
already in the supplement.

---

## Reviewer independence note

I read the round's `LAUNCH-STATE.md` to obtain the round rules, the SNAPSHOT_ID, and the required
report format. While establishing the report format I also opened
`reviews/round-29/reviewer-3.md` and saw its first ~70 lines (header, mandatory-verification
block, and the beginning of its first three findings) before stopping; I did not open
`reviewer-2.md`, any prior-round report, or any prior-round verdict. Every derivation and every
recomputed number in this report was produced from the frozen snapshot and my own calculations —
the fabric-storage identity (A5), the Biot-coefficient recomputations, the hash re-check, and
R1-C1 were all derived independently, and none of the reviewer-3 items I saw (drained-energy
subscript, the `S̄_dis` bar convention, the abstract's fixed-orientation wording) is asserted
here. I am reporting the exposure so the round coordinator can judge whether this reviewer's
return should count toward the acceptance tally.

---

## VERDICT

MINOR REVISION

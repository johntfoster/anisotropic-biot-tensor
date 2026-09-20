# Round 17 — Reviewer 1 (mathematics and correctness)

Manuscript: *An anisotropic Biot tensor from mineral stress and distention work*
Frozen snapshot: `.agent-runtime/review-snapshots/round-17`
Working copy: `/tmp/r17r1` (read-only copy) and `/tmp/r17work` (writable copy).
No prior-round report or vote was read; `reviews/README.md` policy only.

## 1. Snapshot identity and manifest

**Identity check — PASS.**
`sha256(source-manifest.json) = faa3a2f488c5f117474072bb2de41b8de8e78a7cffbc8b51b449edec76292959`
which equals the value in `SNAPSHOT_ID`.

**Manifest re-hash — PASS.** All 438 entries in `source-manifest.json` were
re-hashed in the copied tree: **438 OK, 0 missing, 0 mismatch.**

## 2. Re-derivations of the displayed results (all reproduced)

I re-derived the following from the sources independently of the package
scripts. Every one agreed with the manuscript.

1. **Drained stiffness restriction, eq. (40).**
   With `C^d:ε = φ_s0 C_s:ε̄` at p=0 and `ε̄ = ε − (ln a/3)I`,
   plus `ln a = (1−r)/(3K_s) I:C_s:ε` (r = K/(φ_s0K_s)), one obtains
   `C^d = φ_s0 C_s − (φ_s0/9K_s)(1−r)(C_s:I)⊗(C_s:I)`.
   Self-consistency check added: `(1/9)I:C^d:I` returns `K` **exactly**
   (algebraically and to machine precision numerically).
2. **Drained compliance restriction, eq. (43).** Substituting the strain split
   into `ε = ε̄ + (ln a/3)I` gives
   `(C^d)^{-1} − (φ_s0C_s)^{-1} = (1−r)/(9K) I⊗I`.
   Numerically for the example: relative residual **3.9e-16**, and the
   difference tensor has **rank 1**.
3. **Anisotropic mineral EOS, eq. (51).** From `∂W_s/∂J̄|_F = −φ_s0 p` applied
   to eq. (48) the EOS
   `0 = K_s ln J̄ + (1−r)pJ̄ − (K/φ_s0)ln J + (1/3)(1−r) I:C_s:dev ε`
   is recovered term-for-term. The strict-monotonicity / unique-positive-root
   argument (and the negative-pressure branch condition eq. (52)) is correct.
4. **Drained anisotropic distention, eq. (44)** `ln a = (1−r)/(3K_s) I:C_s:ε`:
   reproduced from the EOS and from `I:C^d:ε = (K/K_s) I:C_s:ε`.
5. **Explicit anisotropic Biot tensor, eq. (52).** Differentiating the EOS at
   fixed p reproduces eq. (50) exactly, and pushing
   `B = I − (J̄/(J[K_s+(1−r)pJ̄])){K I − (φ_s0/3)(1−r)F[∂logC/∂C:dev(C_s:I)]F^T}`
   reproduces the source. The identity `∂_F[I:C_s:dev ε]·F^T = F[∂logC/∂C:dev(C_s:I)]F^T`
   holds; `dev(C_s:I)=0` for cubic symmetry is correct.
6. **Finite Biot tensor eq. (49) and pore-volume identity eq. (50).**
   I verified `σ = σ'' − pB` with `B = I − (φ_s0/J)(∂J̄/∂F)F^T` using the
   effective-stress convention `σ' = J^{-1}P'F^T` (not `σ = J^{-1}P'F^T`;
   the extra `pI` is what makes the `I` term appear). The identity
   `δ(J−φ_s0J̄)/J = B:(δF F^{-1})` follows directly. Reference limit gives
   `B_0 = (1−K/K_s)I` for an isotropic mineral.
7. **Reference relations, eqs. (57), (59), (60).**
   `B_0 = I − C^d:C_s^{-1}:I` equals the explicit F=I form
   `(1−φ_s0 r)I + (φ_s0(1−r)/3K_s)dev(C_s:I)` — identical to machine precision.
   `S_s = φ_s0/K_s(1−r)` equals
   `φ_s0 I:C_s^{-1}:I − I:C_s^{-1}:C^d:C_s^{-1}:I` (the `I⊗I` structure makes
   this exact even though `I` is not an eigenvector of an anisotropic `C_s`).
8. **Isotropic reduction eqs. (61)–(62)** and **finite unjacketed path
   eqs. (63)–(64)**: reproduced; on the unjacketed branch `σ̄_s = −pI`,
   `σ' = 0`, `σ = −pI`, `φ_s = φ_s0`.
9. **Integrated pressure response, eq. (56)**: `∂σ/∂p|_F = −B` from the mixed
   second derivative of `W'`, and Schwarz symmetry gives `∂W'/∂p|_F = φ_s0J̄`.

Numerical support: a from-scratch NumPy implementation of the equations above
(own `logm`, own Fréchet derivative) agrees with `examples/conformal_model.py`
over five structured + seven random finite states:
max ‖Δσ‖ = **3.4e-14**, max ‖ΔB‖ = **3.8e-16**, max |ΔW| = **2.7e-15**,
max |ΔJ̄| = **1.3e-15**.

## 3. Numerical claims checked against listed artifacts

Every claim below was recomputed from the package artifacts (or from the
recorded source), not merely read.

| Claim (location) | Artifact | Result |
| --- | --- | --- |
| Reference Biot 0.7000 / 0.7583 / 0.7917 (experiments.tex:25) | `build/conformal/experiments.json` | 0.7000000 / 0.7583333 / 0.7916667 |
| Drained stiffness shear = φ_s0 × mineral shear (limits.tex:56) | `experiments.json` | 12 / 14.4 / 16.8 = 0.6·(20,24,28) |
| K_s = 28K_*, K = 7K_*, φ_s0 = 0.6, μ̄_avg=16.8 (experiments.tex:8–27) | `experiments.json` | exact |
| 186 named checks; 65 per-state (=5×13) + 2 reference (experiments.tex:180–184) | `build/conformal/verification.json` | checks_passed 186; legacy 67 = 65 + 2 |
| Largest constitutive identity error 2.5e-9 (experiments.tex:186) | `verification.json` | 2.4549890331732928e-09 |
| Two-step refinement → second order (experiments.tex:187) | `step_refinement.csv`, `observed_orders` | 2.00039/2.00010/2.00002/2.00001 (energy), etc. |
| 273 finite states across 13 mineral stiffnesses (experiments.tex:191) | `site/reports/tensor-verification.json` | total_states 273, materials 13 |
| 110 fluid checks, max scaled error 8.09e-9 (evidence.json) | `site/reports/fluid-coupling-verification.json` | count 110, 8.086725789e-09 |
| C++ vs independent Python 6.4e-14 over 41 states (evidence.json) | `site/reports/cpp-python-constitutive.json` | 6.394884621840902e-14, 41 states |
| Assembled-Jacobian FD target 1e-6, recorded maxima | `fe-evidence/runs/jacobian_*` | max relative difference 2.39892e-07 / 2.38797e-07 / 2.39529e-07, all < 1e-6 |
| MMS spatial orders ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00 | `fe-evidence/mms-convergence.json`, `figures/fe_mms_convergence.csv` | 2.9917/2.9585, 2.9983/2.9600, 1.9966/2.0008 |
| MMS temporal difference orders (evidence.json) | `mms-convergence.json` | nx16 1.0932/0.9783/1.0152; nx32 1.3969/1.0183/1.1252; nx64 1.3964/1.0762/1.2519 |
| Mandel reference 38 self-checks, overshoot 5.4659% at 0.01516535 | `validation/mandel_reference.py --self-check` | 38 checks pass; ratio 1.054658607 → **5.4658607%**, t = 0.015165352 |
| Mandel inputs G=0.75, α=0.6, S=17/80, Ku=229/85, c=3.821656, ν=0.2, ν_u=0.3726274 | `validation/reference-data/README.md` | all reproduced |
| Finite-load pressure floor ≈3.2e-3 at nx=20, dt=1e-3 (main.tex:503) | `figures/fe_load_limit.csv` | 3.220919735602341e-3 (load 1e-4) |
| Deck parameters φ_s0=0.9, K=1, K_f=8, mobility=1.5, μ_s=5/6 (finite_elements.tex:161) | `fe-evidence/runs/linear_space_20/input.i` | mineral_stiffness = 3.6111/1.9444/1.6667 isotropic, matches |
| Rotated-anisotropy & partial decks use φ_s0=0.6, K=7 (evidence.json note) | `fe-evidence/runs/anisotropic_30/input.i` | confirmed |
| MMS stiffness rotated 30° (finite_elements.tex:191) | `validation/mms_reference.py`, `mms-reference.md` | +30° active rotation; `B0` is the 30°-rotated reference Biot |
| Figure sample counts 121 / 161 / 1° / 121 / 121 | `build/conformal/*.csv` | 121+121, 161+161, 361×3, 121+121, 121+121 |
| Equation cross-references: (65), (43), (57), (58)–(60), (40) | compiled `main.aux` | all match the reference documents |

The manuscript also **compiles cleanly**: `latexmk -lualatex` on the copy
produced `main.pdf`, 22 pages, 552170 bytes — byte-identical size to the
snapshot's `build/main.pdf`, with no errors and one underfull hbox.

### The three (five) published numbers recomputed with relative differences

1. Reference Biot components (paper 0.7000 / 0.7583 / 0.7917):
   got 0.70000000 / 0.75833333 / 0.79166667;
   relative differences **0**, **4.4e-5**, **4.2e-5** (pure decimal rounding of
   the paper's 4-digit values).
2. Mandel peak overshoot (paper 5.4659% at t = 0.01516535):
   got 5.4658607% at t = 0.015165352;
   relative differences **7.2e-6** (overshoot), **1.3e-7** (time).
3. Finite-load pressure floor (paper ≈3.2e-3 at nx=20, dt=1e-3):
   got 3.2209197e-3; relative difference **6.5e-3** against the paper's
   two-significant-figure "about 3.2e-3".
4. Conformal suite maximum constitutive identity error (paper 2.5e-9):
   got 2.4549890e-9; relative difference 1.8e-2 against the paper's
   2-significant-figure rounding.
5. C++–Python agreement (paper 6.4e-14): artifact 6.3948846e-14;
   relative difference **8.0e-4**.

## 4. Kernel / material source fidelity

- `ConformalMaterial.C` + `ConformalLaw.h` reproduce eqs. (49)–(52),
  (35), the fluid EOS (54) and reference Darcy law (57) exactly. The
  F=I linear branch reproduces the linearized EOS/storage/Biot.
  The mineral pushforward in `ConformalLaw.h` computes
  `τ = F[∂logC/∂C : (C_s:ε̄)]F^T` from the *skeleton* metric `C = F^TF`;
  I confirmed the scalar-scaling identity
  `a^{-2/3} ∂log C̄/∂C̄ = ∂log C/∂C` for `C̄ = a^{-2/3}C`, so this equals the
  manuscript's `R_A τ̂_s R_A^T`, i.e. it is not a missing-frame error.
- `ReferenceBalance.C` residuals are `grad_test·P` and
  `test·(m_f − m_f^old)/dt − grad_test·Q_f`, matching eqs. (77)–(78).
- The C++–Python oracle comparison (`verify_constitutive.py`) rebuilds σ, B and
  `P = JσF^{-T}` from the independent NumPy model; the recorded 6.4e-14
  maximum is over full tensors including noncoaxial states.
- `equation_to_moose_map.yml` and `theory_traceability.yml` are consistent
  with the sources; the linear-reference mode is correctly labelled as a
  separate tangent mode.

## 5. Findings

**REQUIRED: none.**

I found no substantive mathematical or correctness defect, and no number that
I could not reproduce against its listed artifact.

**NOTES (optional/editorial):**

- **NOTE 1** — `main.tex:455` `\pder{W'}p`, `main.tex:457`
  `\pder{\mathbf\sigma}p`, `sections/limits.tex:20` `\pder{\bar J}p`: the
  second `\pder` argument is unbraced. It happens to render correctly because
  the argument is a single token, but it is inconsistent with every other
  `\pder` use in the manuscript. Brace them for robustness/style.
- **NOTE 2** — main.tex:503 and the abstract say the finite-load normalized
  pressure discrepancy "floors at about 3.2e-3". The recorded sequence is
  non-monotone at the small-load end (load 1e-2 → 5.71e-3, 1e-3 → 3.45e-3,
  1e-4 → 3.22e-3); the 3.2e-3 value is the smallest-load value. The wording
  is defensible but could state that the floor is reached only at the
  smallest load tested.
- **NOTE 3** — `sections/experiments.tex:180–184` enumerates 65 + 2 of the
  186 checks and leaves the other 119 lumped as "additional checks". This is
  accurate (verified in `verification.json`) but the reader cannot itemize
  them from the text; optionally name the analytical/branch/quadrature groups.
- **NOTE 4** — `validation/reference-data/mms-reference.md` hard-codes
  equation numbers (43, 57, 60, 65). All four currently match the compiled
  numbering (checked against `main.aux`), so no action is required; these
  hard numbers will need re-checking if the equation order changes.

## 6. Verdict

VERDICT: ACCEPT

Required corrections: (none).

Optional observations (not required for acceptance): NOTES 1–4 in §5.

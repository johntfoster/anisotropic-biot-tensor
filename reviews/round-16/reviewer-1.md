# Round-16 review 1 of 3 — Mathematics and correctness

## (1) Reviewed version, snapshot identity, integrity

- Repository: `anisotropic-biot-tensor`; frozen snapshot
  `.agent-runtime/review-snapshots/round-16` (read-only), copied verbatim to
  `/tmp/r16rev1` for all work.
- Declared `SNAPSHOT_ID` = `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`.
- Recomputed `sha256(source-manifest.json)` = `c621378778d49f8875679440cf874a74aef3caa5d9b04b8936ad319fb57f885f`.
  **Exact match** to the declared identity.
- Re-hashed every path listed in `source-manifest.json` against the frozen
  snapshot bytes: **listed 438 ok 438 mismatch 0 missing 0**.
- Review policy was read only from `reviews/README.md`. No other round's
  reports, no `reviews/round-*/` contents, and no prior verdict were consulted.
  Prior-round verdicts did not inform this review.
- The frozen snapshot was not modified. The post-write re-verification of
  `sha256(source-manifest.json)` is unchanged (see completion note).

## (2) Independent recomputation evidence

All work below was recomputed from the shipped sources/data, not read from the
recorded numbers. Python was run under `conda activate moose`.

**Derivations re-derived from source and checked against code.**
- Drained-stiffness restriction (eq. `drained-stiffness-restriction`) and its
  rank-one compliance form (eq. `drained-compliance-restriction`): I verified the
  equivalence algebraically via Sherman–Morrison
  (`(φC_s)^{-1} = φ^{-1}C_s^{-1} + (1-K/(φK_s))/(9K) I⊗I`), including the Mandel
  factor bookkeeping in `ConformalLaw.h` (`cd[i][j]=phi*cs[i][j]-phi*alpha/(9*Ks)*ci*cj`).
- Mineral EOS (eq. `anisotropic-mineral-eos`): re-derived by differentiating the
  equivalent energy at fixed `F` and multiplying by `J̄`; confirmed against the
  code residual `Ks*(q-target)+alpha*p*exp(q)` and against the fixed-pressure
  derivative (eq. `mineral-fixed-pressure-derivative`, coefficient `K/φ`), where
  I checked the identity `K = φK_s(1-α)` that links the two forms.
- Explicit Biot tensor (eq. `anisotropic-biot-explicit`): re-derived
  `σ=σ''-pB` from `P'=P''+φp ∂J̄/∂F|_p` together with the pore-volume variation;
  confirmed the code's `B = I - J̄/(J·stability)·(K I - (φα/3) F[∂logC/∂C:dev(C_s:I)]F^T)`.
- Reference relations: `B_0 = I - C^d:C_s^{-1}:I` and
  `S_s = φ I:C_s^{-1}:I - I:C_s^{-1}:C^d:C_s^{-1}:I` re-derived and checked
  against the code's `tensorRowCdInverseCs` and `storage=phi*alpha/Ks`.
- Pore-volume identity `δ(J-φJ̄)/J = B:(δF F^{-1})` re-derived by index algebra.
- **Numerical confirmation that σ″ is not the effective stress:** finite-difference
  evaluation of `W''=W_s(F,J̄(F,p))` at `F=I,p=2` and `F(0.65),p=2,4` gives
  `‖σ_model-(σ″-pB)‖ ≤ 2.1e-9`, while `‖σ_model-(σ″+pI-pB)‖ = 3.46–6.93`. The
  manuscript's `σ=σ''-pB` is correct (σ″ differs from σ′ by `p(I-B)`).

**Numeric claims recomputed from shipped data.**
- Reference Biot components: `0.7000, 0.7583, 0.7917` reproduced exactly from
  `K_s=28, φ=0.6, K=7` (Mandel `C_s` as shipped).
- Example invariants: `K_s=28`, `α=7/12≈0.583333`, `K_a=12`, isotropic-comparison
  shear modulus `μ=16.8`, drained Mandel diag `(22.8, 25.7278, 29.7278, 12, 14.4, 16.8)`
  for the unrotated mineral — all reproduced.
- FE reference inputs: `φ=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, k/μ_f=1.5` give
  `G=0.75`, reference Biot `0.6`, total storage `17/80=0.2125`, `M=80/17`,
  `K_u=2.69412`, `ν=0.2`, `ν_u=0.3726274`, Skempton `1.04803` — all reproduced.
- `build/conformal/verification.json`: I re-ran `examples/verify_conformal.py`
  from the extracted supplement and reproduced `checks_passed=186`,
  `max_constitutive_identity_error=2.4549890331732928e-09` (the manuscript's
  "2.5e-9"), and the same second-order refinement orders; `5 states × 13
  identities = 65` per-state identities plus the 2 reference relations = the 67
  legacy checks.
- `site/reports/tensor-verification.json`: `13 materials × 21 = 273` states confirmed
  as recorded. `reconstruction-verification.json`: 20 materials, 20 incompatible
  pairs rejected. `fluid-coupling-verification.json`: `110` checks, max scaled
  error `8.0867e-9`. `cpp-python-constitutive.json`: 41 states, `6.39e-14`.
- MMS convergence (`fe-evidence/mms-convergence.json`): the space norms and the
  naive/successive-difference orders were recomputed from the per-run
  `analysis.json` files (ux 2.9917/2.9585, uy 2.9983/2.9600, p 1.9966/2.0008);
  the time series at fixed mesh uses successive-difference orders (≈1.09, 0.98,
  1.02 at nx=16) exactly as recorded. `site/evidence.json` describes this
  honestly, including that successive-difference orders exceed one at finer meshes
  (ux ≈1.40) and that no order above one is claimed.
- **MMS forcing re-derived independently.** I rebuilt the rotated fourth-order
  stiffness (`30°` about z), the drained `C^d`, the reference Biot tensor, and the
  linear mass/flux operators in NumPy, then recomputed the strong-form body force
  and mass source from the exact prescribed fields. They reproduce the deck's
  `body_x, body_y, mass_source` (`1.701011, 0.877913`, source `0.0477265`) to the
  digits carried in the deck. I also brute-force rotated the full fourth-order
  tensor and confirmed the C++ rotation convention in `ConformalLaw.h` matches the
  independent `validation/mms_reference.py` (max difference `1.4e-14`). The MMS
  decks set `linear_reference = true`, consistent with the stated "constant
  reference tangent" scope.
- `validation/mandel_reference.py`: I re-ran it; the derived constants and the
  `mandel-probes.csv` / `mandel-profiles.csv` artifacts reproduce **byte-identically**
  (matching SHA-256), and the peak overshoot `1.0546586` at `t=0.0151654` (5.4659%)
  reproduces.
- FE load-limit floor: `figures/fe_load_limit.csv` gives
  `pressure_max_normalized = 0.0032209` at `load=1e-4, nx=20, dt=1e-3` — matching the
  manuscript's "about 3.2e-3 ... floors ... rather than decaying".
- Discrete identities: the force-relative and discrete-mass-mobilized-relative maxima
  are `~1e-10`–`1e-12` in `site/reports/finite-deformation-summary.json`; the
  one-element drained/undrained analyses reproduce their expected reference values
  to `≤4e-15` with the recorded pass flags.
- Assembled-Jacobian study: the three perturbation steps give relative differences
  `2.1004e-7 … 2.3953e-7`, all below the `1e-6` target, with no monotone trend —
  consistent with the recorded note.

**Numerical supplement archive `build/conformal-2026-09-20-v1.zip`.**
- Extracted: 33 payload files resolve inside the archive; all 33 `manifest.json`
  digests match; 0 mismatch, 0 missing.
- The archive payload is byte-identical to the shipped snapshot for
  `build/conformal/verification.json`, `experiments.json`, all five figure CSVs,
  `examples/conformal_model.py`, and `examples/verify_conformal.py`.
- The archive `verification.json` `source_sha256` entries for
  `examples/conformal_model.py` and `examples/verify_conformal.py` match both the
  archive payload and the shipped sources.

## (3) Findings

**No required corrections. No wrong factors, signs, or unreproducible numbers were
found in the mathematics, the constitutive law, or the recorded artifacts.**

- **Observational — prose imprecision in the isotropic-comparison modulus.** The
  manuscript states the isotropic comparison's shear modulus is "the mean of the
  five deviatoric stiffness modes of `C_s`, divided by two". The code computes
  `mu_average = trace(P_dev @ cs)/10 = 16.8`, i.e. the Mandel-projected deviatoric
  average. The mean of the five deviatoric *eigenvalues* of `C_s` is `33.154/2 =
  16.577`, which is different. The shipped value `16.8` is internally consistent
  (code, `experiments.json`, manuscript), and the construction is a legitimate
  "average deviatoric stiffness", but a reader recomputing from the eigenvalues
  would not obtain `16.8`. This is a wording issue only; no result depends on it.
- **Observational — field/panel context for the pressure-integral error.** The
  recorded `instantaneous_times_pressure_error = 0.23887` is evaluated at the
  sheared state `F(0.65)` at `p=6`, whereas the manuscript attributes that check
  to the fixed-deformation pressure panel (`F=I`). At `F=I` the corresponding
  component error is `0.1618`. The manuscript quotes no number for this, so no
  numerical claim is contradicted; only the implied context differs.
- **Observational — scope of the Jacobian evidence.** The assembled-Jacobian
  comparison is an assembled-versus-matrix-free finite-difference check; as a
  residual/Jacobian self-consistency test it is correctly scoped as implementation
  evidence in the manuscript and `site/evidence.json`, and is not presented as
  independent physical verification.

## (4) Required corrections

None.

## (5) Optional suggestions

- In Section "Numerical examples" (experiments.tex), state the deviatoric-average
  definition explicitly, e.g. "the mean of the five deviatoric diagonal entries of
  the Mandel deviatoric projection of `C_s`, halved", so `16.8` is reproducible
  from the stiffness matrix without ambiguity.
- Optionally relabel or footnote the `instantaneous_times_pressure_error` field to
  record the state (`F(0.65), p=6`) at which it is computed, to avoid implying it is
  the `F=I` panel quantity.

## (6) Review limitations

- No compiled MOOSE binary ships with the snapshot, so the C++ was audited by source
  fidelity, independent re-implementation of the same formulas, and the recorded run
  artifacts (per-run provenance pins 12 source files whose SHA-256 match the shipped
  sources). The C++ was not executed.
- The FE field data are not shipped (`solution.csv` holds only scalar postprocessor
  history), so the reported MMS L2 orders and the Mandel discrepancy floor were
  verified from the shipped scalar histories and reference series rather than by
  re-solving the FE problem.
- The Jacobian and residual tests could not be re-executed for lack of a binary; the
  `-snes_test_jacobian` values were checked for internal consistency and against their
  stated target.
- Physics/source-fidelity and prose/notation are other reviewers' charges and were not
  assessed here beyond what mathematics required.

VERDICT: ACCEPT

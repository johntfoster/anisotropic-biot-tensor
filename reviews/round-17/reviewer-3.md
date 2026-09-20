# Round 17 — Reviewer 3 (prose, notation, significance, claim-vs-artifact consistency)

Snapshot reviewed: `.agent-runtime/review-snapshots/round-17`
SNAPSHOT_ID: `faa3a2f488c5f117474072bb2de41b8de8e78a7cffbc8b51b449edec76292959`
Reviewer: independent (depth 1/5). Prior-round verdicts carried no weight; I did
not read reviewer-1.md / reviewer-2.md or any earlier report before reaching my
own conclusions.

## 1. Snapshot verification

- `sha256(source-manifest.json)` = `faa3a2f488c5f117474072bb2de41b8de8e78a7cffbc8b51b449edec76292959`
  — **matches** the required SNAPSHOT_ID and the contents of `SNAPSHOT_ID`.
- Manifest entries: **438**. Re-hashed every one: **438 OK, 0 missing, 0 mismatch**.
- No file present on disk outside the manifest (the only unlisted entries are
  `source-manifest.json` and `SNAPSHOT_ID` themselves).
- **Package identity and content integrity verified.**

## 2. Scope of this review

Prose, notation, significance, and claim discipline. Concretely: (a) bar/hat
symbol conventions declared in `main.tex` §2; (b) scope accuracy of abstract,
introduction, discussion and conclusions against `site/evidence.json` and the
section files; (c) every quantitative claim traceable to a listed artifact;
(d) citation and cross-reference resolution; (e) broken sentences, dangling
references, duplicated text; (f) statements stronger than their evidence.

## 3. Findings

### REQUIRED

**R1. `\bar Q_f` is a fourth, undeclared bar meaning.**
`main.tex` §2 declares exactly three bar meanings plus the hat:

> "Throughout, a bar on a kinematic or energetic quantity denotes the mineral
> state reached by removing the distention… A bar on an intrinsic density
> denotes the per-phase-volume value… A bar on a stress denotes its
> representation in the mixture frame, whereas a hat denotes the true frame."

`sections/finite_elements.tex` then introduces a prescribed boundary flux
`\bar Q_f` that falls under none of the three rules (it is not a
kinematic/energetic quantity, not an intrinsic density, and not a stress):

- "reference traction `\mathbf t_0`, and outward mass flux `\bar Q_f`";
- "`+\int_{\Gamma_Q} w\bar Q_f\,\dd A_0`";
- "on `\Gamma_Q`, `\mathbf Q_f\cdot\mathbf N = \bar Q_f`."

`\mathbf Q_f` is the referential mass-flux field; `\bar Q_f` is its prescribed
boundary value. This is a standard weak-form "prescribed datum" notation, but it
is not declared anywhere in the snapshot, and the word "Throughout" in §2
implies the bar convention is exhaustive. Every other bar/hat symbol in the
package conforms (verified below), so this is the single outlier. The fix is a
one-line edit of the author's choosing, e.g. add a clause ("a bar on a
prescribed boundary flux denotes its prescribed value") or rename the datum
(`\bar Q_f \to Q_f^{\mathrm{bc}}` or `Q_f^\star`).

### OPTIONAL (not required for acceptance)

**N1. "in the same limit" is terse and can be misread.**
The abstract and Introduction say the FE implementation "is verified against a
manufactured solution for the constant reference tangent and, in the same
limit, the constant-coefficient consolidation reference". The intended reading
is "the constant-tangent limit" (the linear, constant-coefficient Mandel
reference — genuinely verified by the `linear_space_*` / `linear_time_*` family
in `figures/fe_mandel_refinement.csv`, pressure error ≈ 2.1e-3 / 4.6e-4 /
6.4e-4 at h = 0.1 / 0.05 / 0.025). But "the same limit" could be misread as
"the small-load limit", which the artifacts explicitly say does **not**
reproduce the reference: `figures/fe_load_limit.csv` shows the nonlinear
pressure error *flooring* at ≈3.2e-3 rather than decaying as load → 0, and
`site/evidence.json` marks the small-load Mandel case `pending`. The body
(§"Scope of these results" and the Discussion) already hedges this correctly
("constant reference tangent", "constant-tangent limit"), so the abstract/intro
are not wrong — only slightly ambiguous. Suggest naming the limit explicitly
("in the constant-tangent limit").

## 4. Checks performed and found clean (no finding)

- **Snapshot integrity** — as in §1.
- **Citation resolution** — extracted 22 distinct `\cite*` keys from
  `main.tex`, `sections/*.tex`, `provenance/*.tex`; `references.bib` has 22
  keys; exact one-to-one match (no dangling, no uncited). `build/main.log`
  shows no undefined-citation warning.
- **Cross-references** — 106 `\label`s; every `\eqref`/`\ref`/`\cref` target
  resolves; no undefined-reference warning in `build/main.log`. No dangling or
  orphaned equation/figure/section reference.
- **Notation (bar/hat)** — all symbols except `\bar Q_f` (R1) obey the declared
  convention:
  - mineral state (kinematic/energetic): `\bar J, \bar{\mathbf F},
    \bar{\mathbf C}, \bar{\mathbf U}, \bar{\mathbf\varepsilon}, \bar W_s`;
  - per-phase intrinsic density: `\bar\rho_s, \bar\rho_{s0}, \bar\rho_\xi,
    \bar\rho_f, \bar\rho_{f0}`;
  - mixture-frame stress: `\bar{\mathbf\sigma}_s, \bar{\mathbf\tau}_s`;
  - true-frame stress: `\widehat{\mathbf\sigma}_s, \widehat{\mathbf\tau}_s`.
  Fourth-order tensors in `\mathbb{}`, second-order in upright `\mathbf{}`, as
  declared. The hat↔bar rotation `\bar\sigma_s = R_A\hat\sigma_s R_A^T` and its
  Kirchhoff analogue are applied consistently; I checked the work substitution
  in §3 (`R_A^T\tau' R_A - \phi_{s0}p\bar J I = \phi_{s0}\hat\tau_s`) and the
  energy-returned stress `\tau' = \partial W_A/\partial\ln a\, I + \phi_{s0}
  \mathrm{dev}\bar\tau_s`; both are algebraically consistent.
- **Constitutive symbols** — re-derived independently:
  - `K_s = \tfrac19 I:\mathbb C_s:I = 252/9 = 28 K_*` and `K = 7 K_*`, with
    `0 < K < \phi_{s0}K_s = 16.8` satisfied;
  - reference Biot `B_0 = I - \mathbb C^d:\mathbb C_s^{-1}:I
    = (0.7000, 0.7583, 0.7917)` — matches `sections/experiments.tex` and the
    `p=0` row of `build/conformal/pressure_response.csv`
    (0.7 / 0.75833 / 0.79167);
  - isotropic comparison shear `\mu_s = 16.8 K_*` = (mean of five deviatoric
    stiffness modes)/2 = `trace(P\mathbb C_s)/10 = 168/10` (code:
    `mu_average = trace((I - 1/3 11^T) @ C_s)/10`), matching the text;
  - drained shear entries `= \phi_{s0}\times` mineral shear (12, 14.4, 16.8)
    from `\eqref{eq:drained-stiffness-restriction}`.
- **FE reference numbers** — `\phi_{s0}=0.9, K_s=2.5, \mu_s=5/6, K=1, K_f=8,
  \bar\rho_{f0}=1, k/\mu_f=1.5` → `G=0.75`, Biot `0.6`, total storage
  `(1-\phi_{s0})/K_f + S_s = 0.2125 = 17/80` (all confirmed); `a=1, b=0.1`,
  top resultant `2a q_L` confirmed.
- **Quantitative claims ↔ artifacts**
  - "186 named checks" = `conformal-verification.json` `checks_passed=186`.
  - "65 per-state identities (five states × thirteen)" = five
    `legacy_state0..4` × 13 identities = 65; "two reference Biot and rank-one
    compliance relations" = `legacy_reference_biot` +
    `legacy_reference_rank_one_compliance_identity` (65+2 =
    `legacy_identities_rechecked=67`).
  - "largest absolute error … 2.5×10⁻⁹" = `max_constitutive_identity_error
    = 2.45499e-9` (rounds to 2.5e-9).
  - "273 finite states across 13 mineral stiffnesses" =
    `tensor-verification.json` (`total_states=273`, `materials=13`,
    `states_per_material=21`).
  - "second-order convergence" of energy/pore-volume/pressure =
    `observed_orders` ≈ 2.000/2.000/2.000 before cancellation.
  - "floors at about 3.2×10⁻³ at nx=20, dt=10⁻³" = `figures/fe_load_limit.csv`
    `nonlinear_load_0.0001, nx=20, dt=0.001, pressure_max_normalized =
    0.0032209`.
  - "121 / 161 / one-degree" sampling — `build/conformal/pressure_response.csv`
    (243 rows = 2 materials × 121 + header), `shear_response.csv` (323 = 2 × 161
    + header, γ ∈ [−0.8, 0.8]), `rotation_response.csv` (243 = 2 × 121 + header,
    θ ∈ [0°, 180°]), `directional_response.csv` (1084 = 3 curves × 361 + header).
  - "Lambert-function solutions … negative-pressure … large positive-pressure"
    = `branch_pressure_{-13,-14,800}_lambert_volume` checks.
- **Scope wording (claim discipline)** — the abstract's "no quantitative
  finite-deformation verification and no experimental validation are claimed
  for those demonstrations" agrees with `site/evidence.json`
  (`finite_deformation.status = pending`, `physical_validation.status =
  not_performed`). The withdrawn reference-normalized numbers for the
  rotated-anisotropy and partial-drainage runs are **absent** from both the
  manuscript and the site; the body correctly reports only mass-balance and
  platen-equality diagnostics. The Discussion's conformal-restriction paragraph
  and the "synthetic parameters / no laboratory comparison" limitation match
  `site/evidence.json` limitations verbatim. I found no statement stronger than
  its supporting artifact; the "mineral anisotropy alone need not give
  directional pressure coupling (cubic symmetry)" claim follows correctly from
  `\dev(\mathbb C_s:I)=0`.
- **Prose/flow** — no broken sentences, no dangling references, no duplicated
  or contradictory text across abstract / introduction / discussion /
  conclusions (checked by sentence-level duplicate scan and full read). The
  abstract, introduction, and conclusion are mutually consistent on what is
  "verified" versus "demonstrated".

## Summary

The manuscript is carefully scoped, notationally disciplined (one outlier), and
its quantitative claims are each traceable to a listed, hash-verified artifact.
Citations and cross-references resolve completely. The single substantive
finding is the undeclared `\bar Q_f` bar usage (R1), a one-line notation fix;
N1 is a wording polish.

## VERDICT: MINOR REVISION

### Required corrections
1. Resolve the undeclared `\bar Q_f` boundary-flux notation: either extend the
   §2 bar convention with a clause covering a prescribed boundary value, or
   rename the datum (e.g. `Q_f^{\mathrm{bc}}` or `Q_f^\star`) so that every
   bar symbol in the package obeys the declared convention.

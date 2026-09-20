# Reviewer 1 — Mathematics and correctness

Round 12 independent review. Charge: mathematics and correctness of the finite-element
verification evidence and of `sections/finite_elements.tex`.

## 1. Reviewed version, snapshot ID, integrity result

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Immutable reviewed snapshot: `.agent-runtime/review-snapshots/round-12`
- SNAPSHOT_ID (sha256 of `source-manifest.json`):
  `1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e`

Commands and result:

```
$ cd .agent-runtime/review-snapshots/round-12 && sha256sum source-manifest.json
1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e  source-manifest.json
```

```
files_checked: 338 of 338
missing (in manifest but absent on disk): 0
mismatches: 0
extra_files_on_disk_not_in_manifest: 0
```

Every one of the 338 files listed in the manifest was re-hashed with a streaming
SHA-256 read and matched its recorded digest. No missing, no mismatched, and no
unlisted file was found (excluding `source-manifest.json` and `SNAPSHOT_ID`
themselves). **Integrity: PASS (338/338).**

All independent recomputation below was performed against the frozen snapshot; all
scratch output was written under `/tmp`. Nothing inside the snapshot was modified.

## 2. Independent recomputation evidence

### 2.1 MMS order script vs shipped JSON

```
$ python3 fe-evidence/compute_mms_order.py --runs fe-evidence/runs --out /tmp/r1-mms.json
EXIT=0   (wrote /tmp/r1-mms.json)
```

Programmatic comparison against the shipped `fe-evidence/mms-convergence.json`,
ignoring only the environment-dependent `runs_dir` field:

```
METHOD equal: True
required_runs equal: True
EXACT VALUE EQUALITY (all other keys): True
```

Every norm, naive order, norm deficit, difference order, level and config is
**bit-for-bit equal** to the shipped file.

Failure-path tests (must fail loudly and never write a partial table):

```
(a) --runs /tmp/does-not-exist        ->  EXIT=2 ; output file NOT created
(b) scratch dir containing only mms_space_4
                                      ->  EXIT=2 ; output file NOT created
(c) scratch dir with mms_space_4 present but no analysis.json
                                      ->  EXIT=2 ; output file NOT created
```

In (b) and (c) stderr lists all 12 missing required runs and states
"Refusing to emit a partial convergence table." The output write occurs only after
the completeness check, so no partial evidence file can be emitted. (Running with
no `--runs` still succeeds because the script's self-relative search finds the
sentinel; that is its documented fallback, not a silent partial.)

### 2.2 Applied-resultant plate force balance (independent recompute)

I recomputed `force_relative` directly from each raw `solution.csv` with my own code,
deriving the expected resultant from the deck geometry (`xmax-xmin`) and the traction
in the `FunctionNeumannBC` load function, not from the JSON.

| run | x-range | width | q | expected (derived) | JSON expected | JSON force_relative | recomputed | rel. diff |
|---|---|---|---|---|---|---|---|---|
| anisotropic_30 | [-1,1] | 2 | 0.7 | -1.4 | -1.4 | 2.142889e-12 | 2.142889e-12 | 0.00e+00 |
| partial_30_fine | [-1,1] | 2 | 0.7 | -1.4 | -1.4 | 3.671428e-11 | 3.671428e-11 | 0.00e+00 |
| linear_space_20 | [0,1] | 1 | 1e-4 | -1e-4 | -1e-4 | 8.115999e-11 | 8.115999e-11 | 0.00e+00 |
| nonlinear_load_0.01 | [0,1] | 1 | 0.01 | -0.01 | -0.01 | 8.999745e-13 | 8.999745e-13 | 0.00e+00 |

Final-time residuals: `top_reaction - applied` = 0.0, 9.0e-13, 9.0e-17, 1.0e-16
respectively. Convention confirmed: quarter domain (`case=mandel`, width `a=1`) →
`-a*q_L`; full/partial domain (width `2a=2`) → `-2*a*q_L`. `force_relative` is a
genuine equilibrium residual: it is the max over positive times of
`|top_reaction(t) - applied_resultant(t)| / |expected_force|`, i.e. how well the
discrete vertical plate reaction balances the instantaneous applied traction.

### 2.3 Discrete mass balance and platen equality

Recomputed from raw columns (`mass`, `mass_reaction`, `platen_min`, `platen_max`):

| run | mass_absolute (JSON / recomputed) | mass_rel (JSON / recomputed) | platen_equality (JSON / recomputed) |
|---|---|---|---|
| anisotropic_30 | 5.944030e-14 / 5.944030e-14 | 1.237090e-11 / 1.237090e-11 | 1.699162e-15 / 1.699162e-15 |
| partial_30_fine | 1.810418e-13 / 1.810418e-13 | 1.275599e-10 / 1.275599e-10 | 4.000272e-14 / 4.000272e-14 |
| linear_space_20 | 5.127097e-16 / 5.127097e-16 | 1.852083e-09 / 1.852083e-09 | 4.754700e-15 / 4.754700e-15 |
| nonlinear_load_0.01 | 5.695585e-16 / 5.695585e-16 | 2.175189e-11 / 2.175189e-11 | 6.001059e-17 / 6.001059e-17 |

All identical to the shipped values. The balance error is ≤ ~1e-13 in absolute
terms on a total fluid mass of O(1e-1) to O(1e-2), and the platen is equal to
≤ 4e-14 across the top boundary, consistent with the kinematic equal-value
constraint.

### 2.4 MMS spatial and temporal orders

Spatial (fixed dt=1e-4, nx=4,8,16):

```
ux_l2 naive=[2.9917, 2.9585]  difference=[2.9965]
uy_l2 naive=[2.9983, 2.9600]  difference=[3.0038]
p_l2  naive=[1.9966, 2.0008]  difference=[1.9952]
```

Consistent with Q2 displacement (~3) and Q1 pressure (~2). Temporal difference
orders (`log2` of successive norm deficits):

```
nx16: ux=1.0932  uy=0.9783  p=1.0152   (naive ux = [0.00264, 0.00124])
nx32: ux=1.3969  uy=1.0183  p=1.1252
nx64: ux=1.3964  uy=1.0762  p=1.2519
```

The nx=16 triple bounds the temporal order near one (max 1.093 ≤ "about 1.1"),
consistent with backward Euler. The naive temporal ratios are ~1e-3 and are not
quoted as the order. The nx=64 values (ux 1.40, p 1.25) are explicitly flagged in
`site/evidence.json` as residual spatial-floor contamination, **not** as a higher
achieved order. No order greater than 1 is claimed as achieved anywhere.

I independently checked that the shipped JSON is arithmetically self-consistent
(naive orders = log2 of successive norms; deficits = successive norm differences;
difference orders = log2 of successive deficits) for all space and time series: PASS.

### 2.5 Equations in `sections/finite_elements.tex` vs `moose_app` sources

| Paper relation | Code location | Result |
|---|---|---|
| `P = J σ F^{-T}` (eq:fe-total-first-piola) | `ConformalLaw.h`: `s.P=s.J*s.sigma*F.inverse().transpose()` | match |
| `ρ̄_f = ρ̄_f0 exp(p/K_f)` (eq:fe-fluid-eos) | `ADReal rho=rho0*exp(p/Kf)` | match |
| `m_f = ρ̄_f (J - φ_s0 J̄)` (eq:fe-reference-fluid-mass) | `s.mass=rho*(s.J-phi*s.y)` | match |
| `Q_f = -(J ρ̄_f k/μ_f) F^{-1}F^{-T} Grad p` (eq:fe-reference-darcy-law) | `s.flux=-mobility*s.J*rho*(invF*invF.transpose())*gradp` | match |
| momentum residual `∫ Grad v : P` (eq:fe-momentum-residual) | `ReferenceBalance.C`: `grad_test(j)*P(component,j)` | match |
| fluid residual `∫ w ṁ_f - ∫ Grad w · Q_f` (eq:fe-fluid-residual) | `test*(mass-old)/_dt - grad_test*flux` | match |
| backward Euler (eq:fe-conservative-time-step) | `(_mass-_old)/_dt` | match |
| mineral EOS `K_s ln J̄ + (1-K/(φ_s0 K_s)) p J̄ - (K/φ_s0) ln J + (1/3)(1-K/(φ_s0K_s)) I:C_s:dev ε = 0` (stress_reconstruction.tex, eq:anisotropic-mineral-eos) | `Ks*(q0-target)+alpha*p*y0`, `target=K/(phi*Ks)*log(J)-alpha/(3*Ks)*tr(Cs:dev)`, `alpha=1-K/(phi*Ks)` | match (sign and every factor) |
| storage `(1/ρ̄_f0)∂m_f/∂p|_{F=I,p=0}=(1-φ_s0)/K_f+S_s` (eq:fe-reference-total-storage) | `S_s=(φ/Ks)(1-K/(φKs))`; storage `=(1-phi)/Kf+phi*alpha/Ks` | match |

Reference constants quoted in `finite_elements.tex` (§"Reference problems"):
- Reference Biot coefficient 0.6 = `1 - K/K_s` = `1 - 1/2.5`. The code's internal
  `alpha = 1 - K/(φ K_s) = 0.5556` is an intermediate; the resulting isotropic
  reference tensor is `B_0 = [1 - φ(1-alpha)] I = (1 - K/K_s) I = 0.6 I`. Consistent.
- Total storage 17/80 = 0.2125 = `(1-0.9)/8 + S_s`, with
  `S_s = (0.9/2.5)(1 - 1/2.25) = 0.2`. Consistent.
- Drained shear modulus G = 0.75 = `φ μ_s = 0.9·(5/6)`. Consistent.

MMS deck cross-check (`mms_space_4`, `mms_time_0.01`, `mms_time_fine32_0.01`,
`mms_time_fine64_0.01`): unit square, `angle=30`, amplitude 0.01 (`U=P0=0.01`),
Q2 displacement / Q1 pressure, exact Dirichlet data and `ElementL2Error`
postprocessors, as stated in the text. PASS.

## 3. Findings with severity

- **F1 (Info, severity low) — `runs_dir` provenance is non-portable.** The shipped
  `fe-evidence/mms-convergence.json` records an absolute `runs_dir` pointing to
  `.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs`, outside the
  snapshot. This is metadata only; all values reproduce exactly from the snapshot
  runs. Not a correctness defect.
- **F2 (Info) — schema reduction between copies.** `site/reports/mms-convergence.json`
  omits `norms`, `levels`, and `required_runs` relative to
  `fe-evidence/mms-convergence.json`. All retained quantities match exactly, and
  the site copy's SHA-256 matches the artifact record in `site/evidence.json`. No
  value discrepancy.
- **F3 (Info) — spatial orders quoted are naive ratios.** The spatial numbers in
  `site/evidence.json` ("ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00") are the naive
  error-ratio orders. They coincide with the difference-method orders
  (2.9965 / 3.0038 / 1.9952) to three decimals at the measured levels, so the
  quoted spatial order is sound. The summary's statement that naive ratios are
  "never reported as temporal order" is accurate for the temporal measurement.
- **F4 (Info, severity low) — incompletely scoped "finer meshes" parenthetical.**
  The elevated temporal difference order for ux appears at **both** nx=32 (1.3969)
  and nx=64 (1.3964), but the summary cites only "nx=64 ux 1.40, p 1.25". The
  interpretation (spatial-floor contamination, not achieved order) is correct and
  applies equally to nx=32; only the enumeration is incomplete.

No equation/implementation mismatch, no factor error, and no unreproducible number
was found. Every quoted diagnostic (force, mass, platen, MMS order) was recomputed
to 0 relative difference.

## 4. Required corrections

None.

All mathematical and correctness claims in the reviewed material reproduce exactly
from the frozen snapshot, the failure paths of the evidence script are loud and
partial-write-free, and the equations in `sections/finite_elements.tex` match the
`moose_app` implementation with correct signs and factors. F1–F4 are informational
or editorial only and do not require correction for correctness.

## 5. Optional suggestions

- **O1.** Regenerate/record `runs_dir` in `fe-evidence/mms-convergence.json` as a
  snapshot-relative path (or drop it), so the evidence file is self-contained and
  portable. No numeric impact.
- **O2.** Add the raw `norms` (and `levels`) to the published
  `site/reports/mms-convergence.json` so readers can verify the orders without the
  private run tree; the deficits are present but the norms are not.
- **O3.** Extend the "finer meshes" parenthetical in `site/evidence.json` to name
  nx=32 as well as nx=64 for the elevated ux difference order.
- **O4.** State the element-order→rate mapping explicitly (Q2 displacement →
  h^3 in L2, Q1 pressure → h^2) next to the observed spatial orders, so the
  "consistent with" claim is checkable at a glance.

## 6. Verdict

VERDICT: ACCEPT

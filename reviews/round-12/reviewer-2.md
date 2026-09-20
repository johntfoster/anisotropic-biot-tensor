# Reviewer 2 — Physics/Source Fidelity and Packaging

**Round:** 12
**Charge:** constitutive and coupling fidelity, analytical reference reproduction,
comparability honesty, physical checks, packaging completeness.
**Reviewed by:** independent reviewer 2 (not the author; no other reviewer's report or
prior-round material under `reviews/` was read).

---

## 1. Reviewed version, snapshot ID, integrity

| Item | Value |
|---|---|
| Live repository | `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor` |
| Immutable snapshot | `.agent-runtime/review-snapshots/round-12` (mode 444/555) |
| `SNAPSHOT_ID` file | `1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e` |
| `sha256sum source-manifest.json` | `1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e` |
| Evidence version | `moose-fe-pending-2026-09-20` (`site/evidence.json`) |
| Recorded `provenance.source_revision` | `ecfe4a22a094d3b346ea89287f9a23e1917f017c` |
| Supplement archive | `build/conformal-2026-09-20-v1.zip` |

**Integrity result: PASS — manifest hash equals SNAPSHOT_ID.**

```
$ cd .agent-runtime/review-snapshots/round-12 && sha256sum source-manifest.json
1797085484aca549014a3b3c8685a37c3bb892461b9e165635c61774513e2a9e  source-manifest.json
```

Full hash verification of every listed file:

```
listed files: 338   ok: 338   missing: 0   mismatch: 0
extra files not in manifest: 2  (SNAPSHOT_ID, source-manifest.json — expected)
```

**File count: 338 / 338 listed files hash-match.** No modification was made inside the
snapshot; all scratch work used `/tmp/r2scratch`.

---

## 2. Independent verification evidence

### 2.1 Constitutive and coupling fidelity (kernels/materials vs theory)

I mapped `moose_app/include/utils/ConformalLaw.h` and
`moose_app/src/kernels/ReferenceBalance.C` to the stated equations and then re-derived the
key relations from `main.tex` / `sections/stress_reconstruction.tex` /
`sections/limits.tex` with an **independent numpy implementation** (not the repo's
`conformal_model.py`):

```
Command: python3 (independent implementation of eq:spherical-strain-stiffnesses,
         eq:drained-stiffness-restriction, eq:reference-biot-compatibility,
         eq:reference-solid-storage, eq:reference-total-storage)

Ks = 28.0
K_drained = (1/9) I:Cd:I = 7.0
B0 mandel components (11,22,33,shears): [0.700  0.758333  0.791667  0  0  0]
S_s = 0.0125  == phi*I:Cs^-1:I - I:Cs^-1:Cd:Cs^-1:I  (equal to 1e-15)
iso: K_drained=1.0, drained shear G=0.75, Biot coeff=[0.6 0.6 0.6 0 0 0],
     total storage = 0.2125 == 17/80
```

Every number reproduces the theory statements exactly:

* **Distention/deformation split.** `Law::evaluate` sets `C=F^T F`, `logC` via a
  Gauss–Legendre/Newton resolvent integral, `e = ½ logC`, and solves a mineral scalar
  equation with `q = ln J̄`. The residual `Ks*(q0 - target) + alpha*p*y0` with
  `target = K/(phi*Ks)*ln J - alpha/(3Ks)*tr(Cs:dev e)` is exactly
  `eq:anisotropic-mineral-eos` (multiplied through by `Ks`). Mineral log-strain
  `em = dev e + (q/3) I` matches `eq:constrained-mineral-logarithmic-strain`. **Traceable.**
* **Anisotropic Biot tensor.** `s.B = I - y/(J*stab) * (K I - phi*alpha/3 * F*LB*F^T)`
  with `stab = Ks + alpha*p*y` and `LB` built from `dev(Cs:I)` through the matrix-log
  derivative. This is `eq:anisotropic-biot-explicit` with
  `alpha = 1 - K/(phi*Ks)`. Linear branch `B = I - Cd:Cs^{-1}:I` matches
  `eq:reference-biot-compatibility`. **Traceable.**
* **Total stress, not drained pB.** Finite-deformation branch uses
  `s.sigma = phi/J * tau - (1 - solid) p I`, i.e. `eq:total-stress-phase-energy`; the
  momentum residual consumes `first_piola = J*sigma*F^{-T}` (`eq:fe-total-first-piola`)
  with no extra effective-stress correction. The drained tangent
  `sigma = Cd:sym(grad u) - B0 p` exists **only** in the explicitly separated
  `linear_reference` mode, documented as such in `validation/theory_traceability.yml`.
  No conflation of drained `pB` with the total stress. **Correct.**
* **Fluid EOS and permeability law.** `rho = rho0*exp(p/Kf)`,
  `mass = rho*(J - phi*y)`, `flux = -mobility*J*rho*(F^{-1}F^{-T})*grad p` match
  `eq:fe-fluid-eos`, `eq:fe-reference-fluid-mass`, `eq:fe-reference-darcy-law`. Spatial
  permeability stays isotropic (`sections/finite_elements.tex` states this is deliberate).
  **Correct.**
* **Symmetry / scope statements.** Reference Biot `B0` is symmetric and reduces to
  `(1-K/Ks)I` isotropically; the implementation exports the off-diagonal `B12`, which is
  the qualitative feature claimed in `sections/experiments.tex`. Scope language in the
  abstract, `sections/finite_elements.tex` "Scope of these results", and
  `sections/experiments.tex` consistently disclaims finite-deformation quantitative
  verification and experimental validation.

**No implementation was found that fails to trace to a stated equation.**

### 2.2 Analytical reference reproduction

```
$ python3 validation/mandel_reference.py --self-check --output-dir /tmp/r2scratch/refout
category: analytical-reference-only   passed: True
n_checks: 38   failed: []
central_overshoot: {'ratio': 1.0546586069998425, 'time': 0.015165352045764979, 'passed': True}
series_tail_bound: {'value': 9.21e-14, 'passed': True}
geometry a,b: 1.0 0.1
```

* **Self-check count: 38 — confirmed** (claimed 38).
* **Peak overshoot: 1.0546586 → 5.4659 % — confirmed** (claimed 5.4659 %), at
  **t = 0.01516535 — confirmed** (claimed 0.01516535).
* **Reference geometry a = 1, b = 0.1 slender domain — confirmed.**
* The stored `site/reports/mandel-reference.json` reproduces the identical overshoot and
  its `source_sha256` (`e5cf969c…be7a`) equals the live script hash.

### 2.3 Comparability honesty

```
$ grep -E "xmin|xmax|ymin|ymax" fe-evidence/runs/{anisotropic_30,partial_0,isotropic}/input.i
anisotropic_30: xmin=-1 xmax=1 ymin=-0.1 ymax=0.1
partial_0:      xmin=-1 xmax=1 ymin=-1   ymax=1
isotropic:      xmin=-1 xmax=1 ymin=-0.1 ymax=0.1
```

```
$ grep -rho "reference_comparable[^,}]*" . | sort | uniq -c
  17 reference_comparable": true
   4 reference_comparable": false
```

* **Partial-drainage family genuinely uses the square domain `[-1,1]×[-1,1]`** (the
  `partial` branch of `decks.py` sets `h = 1`, full domain), while the reference is the
  slender `[-1,1]×[-0.1,0.1]`. `partial_0`, `partial_30`, `partial_30_coarse`,
  `partial_30_fine` are exactly the four runs with `reference_comparable: false`, and
  their `analysis.json` carries **no** `*_normalized` metrics (verified: empty set) plus
  an explicit `reference_note`. Omitting reference-normalized metrics for these runs is
  **correct and honest.**
* **Anisotropic family domain matches the reference geometry**: full slender
  `[-1,1]×[-0.1,0.1]`, same as `isotropic`.
* **No run with `reference_comparable=false` hides behind a verification claim.** Only
  `analytical`, `implementation`, and `convergence` are marked `passed` in
  `site/evidence.json`; none cites a partial-drainage artifact. `finite_deformation` is
  `pending` with `evidence: []`, and both `site/evidence.json` and
  `sections/finite_elements.tex` explicitly label the partial family "not comparable"
  and excluded from verification claims. The three `cases[]` entries are all `pending`.

### 2.4 Physical checks

One-element drained / undrained (`fe-evidence/runs/one_element_*/analysis.json`):

```
drained:   pass=true  absolute_error=1.55e-16
undrained: pass=true  absolute_error=3.80e-15  mass_change=-1.01e-16
```

The `expected` values in `run_one_element.py` are computed by the **independent Python
`conformal_model.py`** (scipy root), not by the FE binary, so these are genuine
cross-implementation checks. The drained limits (ex≈1.327e-3, ey≈-5.291e-3) sit
within ~0.5 % of the linear small-strain prediction from my own drained stiffness
(Kd=1, G=0.75), consistent with the finite log-strain model; the undrained state
(ux≈2.477e-3, p≈4.783e-3) sits within ~0.5 % of the linear Mandel initial state
(2.484e-3, 4.795e-3). Physically sensible.

Finite-load-limit floor (`figures/fe_load_limit.csv`):

```
nonlinear_load_0.0001 pressure_max_normalized = 0.0032209   (≈3.2e-3)
nonlinear_load_0.001  pressure_max_normalized = 0.0034479
nonlinear_load_0.01   pressure_max_normalized = 0.0057060
```

**Floor claim (~3.2e-3) confirmed**; the statement that it does not decay toward the
linear reference as load → 1e-4 but plateaus at a discretization floor (nx=20, dt=1e-3)
is supported by the data.

Mass conservation (`discrete_mass_absolute` / `_mobilized_relative` over all
`fe-evidence/runs/*/analysis.json`):

```
max discrete_mass_absolute = 1.15e-12   max discrete_mass_mobilized_relative = 7.80e-11
force_relative range 9.0e-13 … 1.6e-9   expected_force = -1.4 = -2*a*q_L (a=1, q_L=0.7)
```

**Mass-conservation claims hold.** The stated corrected plate resultant
`-2*a*q_L` reproduces `expected_force = -1.4` with equilibrium residuals ≤ ~1e-9.

### 2.5 Packaging completeness

```
site/evidence.json artifacts:          19 checked, 0 problems (exists + SHA-256 match)
site/scientific-snapshot.json files:   33 checked, 0 problems (exists + SHA-256 match)
all evidence id references resolve; all figure-list references resolve
```

Supplement archive:

```
$ sha256sum build/conformal-2026-09-20-v1.zip
cec4b5ff171ecec27c2c0d8d797afef8f0b65f79ac899b1d4b60ce4313535d4d  (matches source-manifest.json)
zip entries: 34; internal manifest.json {version, sha256}; payload verification: 33/33 match
```

All five figures cited in the manuscript resolve and exist:

```
OK build/conformal/constrained_layer.pdf
OK build/conformal/directional_response.pdf
OK build/conformal/pressure_response.pdf
OK build/conformal/rotation_response.pdf
OK build/conformal/shear_response.pdf
```

`passed` categories are backed: `analytical` ← `mandel-reference`
(38 checks, reproduced); `implementation` ← `fluid-coupling-verification`
(110 checks, max scaled error 8.087e-9), `conformal-verification` (186 checks, max
identity error 2.455e-9), `tensor-verification` (273 states / 13 minerals),
`reconstruction-verification` (20 incompatible pairs rejected); `convergence` ←
`mms-convergence` (spatial ux 2.99/2.96, uy 3.00/2.96, p 2.00/2.00; temporal nx=16
ux 1.093, uy 0.978, p 1.015 — all match the reported values). **No unbacked `passed`
category found.**

---

## 3. Findings with severity

| # | Severity | Finding |
|---|---|---|
| F1 | **Minor** | `site/reports/mandel-reference.json` declares `artifacts` with SHA-256 for `mandel-probes.csv` and `mandel-profiles.csv`, but neither file is present anywhere inside the reviewed snapshot. The report backs the `analytical: passed` category. The declared hashes are real (they match the live runtime copies in `.agent-runtime/moose-fe-goal-2026-09-20/reference/`), so this is an omission from the package, not fabricated data. The `verification` block itself is self-contained and fully reproducible (I reproduced all 38 checks), so the `passed` claim is not unbacked — only the two data artifacts are dangling. |
| — | Info | `.agent-runtime/…` and `solution_profile_*.csv` / `solution.e` references inside `fe-evidence/plot-manifest.json` and per-run `provenance.json` are **runtime provenance pointers** to the original working directory, not packaged-artifact declarations. This is a normal, acceptable provenance convention; no action needed. |

No critical or major findings. Every physical, numerical, and comparability claim I
tested was reproduced exactly; nothing I could not reproduce was accepted.

---

## 4. Required corrections

1. **Resolve the two dangling artifact declarations in `site/reports/mandel-reference.json`.**
   Either ship `mandel-probes.csv` and `mandel-profiles.csv` inside the snapshot alongside
   the report, or remove them from the report's `artifacts` map (or re-emit the report
   without the artifacts block).
   *Why required:* a report that backs a `passed` category currently advertises SHA-256
   values for two files a package reader cannot obtain from the package, which is a
   packaging-consistency defect against the same standard applied to
   `site/evidence.json` and `site/scientific-snapshot.json` (whose references all
   resolve). The fix is small and does not touch any scientific claim.

---

## 5. Optional suggestions

1. **Clarify the `reference_comparable` flag semantics.** For the anisotropic family the
   flag is `true` (geometric comparability: slender domain matches the reference), yet the
   reported normalized differences are large (pressure_max ≈ 0.75, edge_ux ≈ 1.7). The
   accompanying text correctly calls these "demonstrations of the anisotropic-versus-isotropic
   material response, not verification", but a one-line comment that `reference_comparable`
   denotes *geometry compatibility only, not agreement within tolerance* would prevent
   misreading by a downstream consumer of the JSON.
2. **Annotate the finite-deformation metric ranges in `site/evidence.json`.** The stated
   anisotropic-family ranges (`pressure_max 0.73–0.86`, `profile max 0.74–0.88`) are
   reproduced only when the isotropic slender-domain run is included (0.7291 / 0.7362);
   over the six anisotropic-only runs the actual ranges are 0.755–0.858 and 0.755–0.875.
   Noting the set over which the range is taken would make the summary self-contained.
3. **Add a manuscript pointer to the FE figures.** `figures/fe_*.png` and the six
   JSON reports in `site/reports/` are packaged and hashed but are not referenced from
   `main.tex` (which cites only the five `build/conformal/*.pdf`). A sentence in
   `sections/finite_elements.tex` or the code/data-availability paragraph naming the
   evidence file would connect the paper text to its packaged evidence.

---

## 6. Verdict

```
VERDICT: MINOR REVISION
```

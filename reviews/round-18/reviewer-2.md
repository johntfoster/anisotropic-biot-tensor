# Reviewer 2 — Physics, source fidelity, packaging

**Round:** 18
**Snapshot:** `.agent-runtime/review-snapshots/round-18`
**SNAPSHOT_ID:** `810b503058701b0d3f43ef39cba2c6952e28a5e8b0728321849b0129a60e3625`

Independent review. Prior-round verdicts do not carry.

---

## 1. Snapshot integrity

- `sha256(source-manifest.json)` = `810b5030…60e3625`, exactly equal to the
  pinned `SNAPSHOT_ID`. **Pass.**
- Re-hashed all **438** files listed in `source-manifest.json` against the
  snapshot working tree: **0 missing, 0 hash mismatches.** **Pass.**

## 2. Artifact presence and hash fidelity

Every shipped document's referenced artifacts were located and re-hashed:

| Referenced artifact set | Files | Result |
|---|---|---|
| `fe-evidence/manifest.json` payload | 202 | all present, sha256 + byte size match |
| `site/evidence.json` `artifacts` allowlist | 23 | all present, sha256 match |
| `site/scientific-snapshot.json` `files` | 33 | all present, sha256 match |
| embedded supplement (PDF attachment) | 1 ZIP | present, sha256 matches shipped archive |

- The `scientific-snapshot` artifact's declared sha256
  (`250ed9d5…6059b`) equals the on-disk hash of
  `site/scientific-snapshot.json`. **Pass.**
- All 23 evidence artifacts (figures, reports, data CSVs, provenance) hash
  as declared; none missing. **Pass.**

## 3. Supplement packager reproducibility

Re-ran `python3 tools/package_numerical_supplement.py` on an unmodified copy
of the snapshot. The regenerated `build/conformal-2026-09-20-v1.zip` has
sha256 `b635be76…649f981`, **byte-identical** to the shipped archive
(same digest, 34 payload files). The internal `manifest.json` version
`conformal-2026-09-20-v1` and its 34 file hashes are self-consistent.
**Pass.**

## 4. PDF embedded attachment

`build/main.pdf` contains exactly one embedded file,
`conformal-2026-09-20-v1.zip`; `pdfdetach`-extracted bytes hash to
`b635be76…649f981`, identical to the shipped archive. **Pass.**

## 5. PDF build currency

`build/main.pdf` is **22 pages** (pdfinfo and `main.log` both confirm
`Output written on main.pdf (22 pages, 552403 bytes)`). Build log shows no
LaTeX errors, no undefined citations, and a stable `main.out` checksum.
PDF mtime (18:19:54) is newer than `main.tex` (18:19:45) and all
`sections/*.tex`, so it is the latest build against current sources.
**Pass.**

## 6. Force / mass / platen balance claims vs raw run data

Cross-checked `site/reports/finite-deformation-summary.json` against every
per-run `fe-evidence/runs/<case>/analysis.json`:

- All 11 runs (anisotropic 0/30/30-coarse/30-fine/45/90, isotropic,
  partial 0/30/30-coarse/30-fine) agree field-for-field on
  `peak_pressure`, `peak_time`, `force_relative`,
  `discrete_mass_absolute`, `discrete_mass_mobilized_relative`, and
  `platen_equality_absolute` — **0 discrepancies** at machine precision.
- Family aggregates (anisotropic `force_relative_max` 1.276e-10, mass
  2.470e-10; isotropic 3.214e-12 / 7.587e-12; partial 2.052e-10 /
  4.636e-10) recompute exactly from the member runs.
- Independently recomputed `force_relative` from raw `solution.csv`
  (`top_reaction` vs `-q_L·width·ramp`) for sampled cases and matched the
  recorded `analysis.json` values to ~1e-18.
- The force convention (`-a q_L` quarter / `-2a q_L` full domain, a=1) is
  stated consistently in `analyze_mandel.py`, every `analysis.json`, and
  the manuscript, and the corrected plate resultant is correctly described
  as an equilibrium residual, not a force-balance failure.

**Pass — claims are measured, not asserted.**

## 7. Partial-drainage family vs slender Mandel reference

Confirmed non-comparability is explicitly recorded at three levels:

- Each of `partial_0/30/30_coarse/30_fine` `analysis.json` carries
  `reference_comparable: false` and a `reference_note` stating the square
  domain `[-1,1]×[-1,1]` differs from the slender Mandel reference
  `[-1,1]×[-0.1,0.1]`.
- `site/evidence.json` case `"Partial-boundary drainage"` states the
  reference-normalized comparison "is not comparable and is omitted".
- The manuscript `sections/finite_elements.tex` (Scope paragraph) states the
  partial-drainage comparison "is therefore reported as not comparable and
  is excluded from the verification claims."

No reference-normalized discrepancy is emitted for the partial family, and
no stale `reference_comparison.csv` is present (the `not_applicable` list in
the fe-evidence manifest covers exactly these). **Pass.**

## 8. Source fidelity (spot physics audit)

- `moose_app/include/utils/ConformalLaw.h` implements the Mandel-basis
  mineral stiffness with rotation, the matrix-logarithm (Gauss–Legendre)
  integral, the implicit mineral-volume root, the phase-weighted stress
  `σ = φ_s/J · τ̄_s − (1−φ_s) p I`, the reference mass `ρ_f(J − φ_s0 Ȳ)`,
  and the explicit Biot tensor `B = I − Ȳ/(J·stability)·(K I − φ_s0 α/3 · F·LB·Fᵀ)`,
  matching `eq:constitutive-phase-stress-sum`,
  `eq:fe-reference-fluid-mass`, and `eq:anisotropic-biot-explicit`.
- `validation/equation_to_moose_map.yml` and
  `validation/theory_traceability.yml` map kernels/materials to numbered
  equations and record the reference-tangent Mandel mode as distinct from
  the finite-deformation model.
- C++ vs independent Python constitutive evaluation: 6.39e-14 max value
  error over 41 finite states (`cpp-python-constitutive.json`), consistent
  with the manuscript's claim.
- Manuscript numeric claims verified against reports: 186 named checks
  (conformal suite), 273 finite states / 13 stiffnesses (tensor suite),
  max constitutive identity error 2.45e-9, 110 fluid-coupling checks at
  8.09e-9, MMS orders (spatial ux/uy/p ≈ 2.99/3.00/2.00; temporal
  successive-difference ≈ 1.0–1.4 reported as measurements), Mandel
  reference 38 self-checks with 5.4659% overshoot at t=0.01516535.
- Small-load floor claim ("normalized pressure discrepancy floors at about
  3.2e-3 at nx=20, dt=1e-3") matches `linear_load_reference`
  (3.1957e-3) and `nonlinear_load_0.0001` (3.2209e-3).

**Pass — kernel-to-equation traceability is maintained and claims are
honestly labeled (demonstration vs verification; `physical_validation`
correctly `not_performed`).**

## 9. Minor observations (non-blocking)

1. `site/reports/mms-convergence.json` embeds an absolute `runs_dir`
   (`…/.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs`). The
   report is self-contained (all orders/norms inline), so this is cosmetic
   provenance leakage, not a correctness defect. Optional cleanup only.

---

## Verdict

VERDICT: ACCEPT

The snapshot is internally consistent end-to-end: every manifest, artifact,
scientific snapshot, supplement archive, and embedded PDF attachment hashes
as declared; the packager reproduces the shipped archive byte-for-byte; the
force/mass/platen diagnostics are measured in the raw run data; the
partial-drainage family is correctly marked not comparable to the slender
Mandel reference and excluded from verification claims; and the 22-page PDF
is the current build. No required corrections.

**Required corrections:** none.

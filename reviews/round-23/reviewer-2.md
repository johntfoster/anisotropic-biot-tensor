# Reviewer 2 — Round 23 (physics, source fidelity, packaging)

Snapshot reviewed: `.agent-runtime/review-snapshots/round-23`
SNAPSHOT_ID: `53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5` (556 files)
Scope: frozen snapshot only; read-only. No prior-round reviews consulted.

## Step 1 — Integrity

- OK. `sha256(source-manifest.json)` equals the declared SNAPSHOT_ID
  (`source-manifest.json` is a flat `path -> sha256` map, 556 entries).
- Re-hashed all 556 listed files: **556 OK, 0 missing, 0 mismatch**.
- Integrity passes; review proceeds.

## Step 2 — Packaging and source fidelity

**2a. `fe-evidence/manifest.json`** — declares 53 `cases`, 53 `runs` entries,
293 `files` entries, 28 `not_applicable`. Every declared digest verifies:
**293/293 OK, 0 missing, 0 bad** (byte length and sha256 both match). No
bad or missing digest. Only `README.md` and `manifest.json` itself are
undeclared (self-describing files) — see optional note O4.

**2b. `site/evidence.json`** — 35 declared artifacts; all resolve and hash as
declared: **35/35 OK, 0 missing, 0 mismatch**. `site/scientific-snapshot.json`
— 43 declared files, **43/43 OK, 0 missing, 0 mismatch**. The generic
`source_sha256` maps inside the reports also resolve and match the shipped
`examples/*.py` sources (no mismatches in the sweep).

**2c. `site/reports/*.json` currency vs the shipped runs** — recorded values are
current:
- `fabric-verification.json` `moose`/`independent` fields reproduce exactly when
  `examples/verify_fabric.py` is run from the extracted archive (see 2d).
- `finite-deformation-summary.json` per-run `peak_pressure`/`force_relative`/
  `discrete_mass_*`/`platen_equality_absolute` match the corresponding
  `fe-evidence/runs/<case>/analysis.json` values (spot-checked `anisotropic_0`,
  `anisotropic_90`).
- `mandel-reference.json`: 38 checks, all `passed`; `central_overshoot`
  ratio `1.0546586069998425` at `t = 0.015165352` ⟹ 5.4659% at t = 0.01516535,
  matching the `site/evidence.json:14` summary.
- `mms-convergence.json`, `conformal-verification.json` (186 checks,
  max constitutive identity error 2.455e-9), `tensor-verification.json`
  (273 states / 13 materials), `fluid-coupling-verification.json` (110 checks)
  all match their manuscript citations.

**2d. Supplement archive `build/anisotropic-biot-2026-09-20-v2.zip`** — extracted
outside the checkout (`/tmp/rev2zip`). Internal `manifest.json`: **57/57 entries
verify, 0 missing, 0 mismatch** (self-consistent; only itself undeclared).
Ships byte-identical to the snapshot:
- `moose_app/include/utils/FabricLaw.h`, `moose_app/src/materials/FabricMaterial.C`,
  `moose_app/include/materials/FabricMaterial.h`,
  `moose_app/inputs/fabric_probe.i`, `moose_app/inputs/fabric_mandel.i`,
  `moose_app/inputs/conformal_probe.i`,
  `examples/verify_fabric.py`, `examples/plot_fabric_results.py`,
  `build/fabric/fabric-verification.json` — all SAME.
- All 15 fabric/conformal `fe-evidence/runs/*/solution.csv` — all SAME.
- Reproduction: `python3 examples/verify_fabric.py` runs and reproduces the
  shipped probe values and residuals; `python3 examples/plot_fabric_results.py
  --runs fe-evidence/runs --output …` regenerates `fe_fabric_mandel_history.csv`,
  `fe_fabric_mandel_peak.csv`, `fe_fabric_probe.csv` **byte-identical** to
  `figures/` in the snapshot. (PNG/PDF bytes differ, as the archive README
  explicitly permits for platform metadata.)

**2e. `build/main.pdf` embedded attachment** — extracted with
`pdfdetach -saveall`; the embedded `anisotropic-biot-2026-09-20-v2.zip` is
**byte-identical** to the on-disk archive (both
`bf99380cdf82940ed806d814e0f921efd1a16c1057a8eb7647272364e1eff3e2`, `cmp` clean).
Archive name consistency: `main.tex:26-27` (`filespec=anisotropic-biot-2026-09-20-v2.zip`,
`build/anisotropic-biot-2026-09-20-v2.zip`) and `README.md:45,48`
(`build/anisotropic-biot-2026-09-20-v2.zip`) both name the shipped archive.

## Step 3 — Physics and source fidelity

- **Coupled Mandel peak centre pressures** — `sections/finite_elements.tex:313-315`
  states 4.38e-5 (X1), 4.98e-5 (45°), 5.50e-5 (other in-plane axis), vs 3.65e-5
  uncoupled. `figures/fe_fabric_mandel_peak.csv` records `4.3760733643082e-05`,
  `4.9825794324732e-05`, `5.497926837564e-05`, `3.6523250981799e-05`. All four
  round correctly and the anisotropy trend is monotone increasing with fabric
  angle. `fabric_mandel_coup_a45/analysis.json` `center_pressure` =
  `4.9825794324732e-05` confirms the peak is the final recorded state
  (`sections/finite_elements.tex:316-317`), with `peak_stability 2.5`.
- **Fabric probe numbers** — `sections/finite_elements.tex:271-288` quotes
  reconstruction 2.2e-16, det-1 −3.3e-16, ‖D:e3‖ 1.6e-16, rotation invariance
  2.5e-16, worst abs diff 4.9e-15, conformal reduction 1.9e-14. The shipped
  `examples/verify_fabric.py` run prints 2.2204e-16, −3.3307e-16, 1.5823e-16,
  2.4965e-16, 4.885e-15, 1.874e-14 — all round correctly. `fabric_probe_*.csv`
  B_par/B_per/ln_h/sigma22 match `fabric-verification.json` exactly.
- **NDIR** — code ships `moose_app/include/utils/FabricLaw.h:61`
  `static constexpr unsigned NDIR = 2;`, and all narrative text consistently
  describes the two-dimensional (volumetric–axial) retained subspace. No text
  anywhere describes a five-direction (NDIR=5) law; the only "five" occurrences
  (`sections/experiments.tex:29,181`; `site/README.md:90`) are unrelated
  (five deviatoric modes, five states, five categories). No stale-law drift.
- **Contradiction scan** — no manuscript number was found that its own shipped
  figure/CSV contradicts: MMS orders (p 2.00/2.00, ux 2.99/2.96, uy 3.00/2.96)
  match `mms-convergence.json`; `main.tex:566-571` load floor 3.2e-3
  (`fe_load_limit.csv` 0.003221), step refinement 3.7e-3 / 7.1e-3 ratio 1.94
  (`linear_time_0.001` 0.003658 → `linear_time_0.002` 0.007104), temporal orders
  0.98–1.40 (measured 0.978–1.397) all match.
- **Overclaim discipline** — honest and consistent. `main.tex` abstract,
  `sections/finite_elements.tex:339-371` ("Scope of these results"), the
  archive `README.md`, and `site/evidence.json` (`finite_deformation: pending`,
  `physical_validation: not_performed`) all state that the coupled/anisotropic/
  partial/rotated-fabric runs are finite-load **demonstrations**, not
  quantitative verification, and that parameters are synthetic with no
  experimental validation. No validation claim is present anywhere.

## REQUIRED items

1. **Duplicate limitation entry shipped in `site/evidence.json`.**
   `site/evidence.json:482` and `:483` are the same limitation ("The pore-fabric
   extension relaxes the drained-compliance restriction …"), with `:483` merely
   extended. The `limitations` array (7 entries) therefore presents one
   limitation twice; the second should be merged/replaced with the intended
   distinct entry (or removed). This is a reader-visible defect in a
   published-adjacent artifact and should be de-duplicated.

2. **Duplicate note entry shipped in `fe-evidence/manifest.json`.**
   `fe-evidence/manifest.json:5442` and `:5443` are the same `runs/fabric_*`
   note, `:5443` adding the `conformal_probe_ref` clause. The `notes` array
   repeats itself; replace `:5442` with `:5443` (i.e. keep only the more
   complete wording).

3. **Machine-specific absolute path shipped in a public report.**
   `site/reports/mms-convergence.json:3` and `fe-evidence/mms-convergence.json:3`
   record
   `"runs_dir": "/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs"`.
   A public artifact should not embed an absolute path into a private
   `.agent-runtime/…` working directory; record it relative to the repository
   root (or drop the field). (Related but lower priority: the same
   `.agent-runtime/moose-fe-goal-2026-09-20/…` build/output paths are recorded
   in every `fe-evidence/runs/*/provenance.json`, e.g.
   `fe-evidence/runs/anisotropic_0/provenance.json:19,21,22`; recording the
   original build directory is legitimate provenance, but leaking the internal
   runtime directory name is avoidable.)

## Optional notes

- **O1.** `examples/verify_fabric.py` and the compiled `FabricLaw.h` share the
  distention basis and reported-`ln_h` sign convention; the manuscript already
  labels this correctly as an implementation check rather than an independent
  re-derivation (`sections/finite_elements.tex:285-291`). No change required;
  the wording is appropriately hedged.
- **O2.** The zip `README.md` documented suite was only partially executed here
  (the fabric path: `verify_fabric.py` + `plot_fabric_results.py`). The
  remaining documented commands (`weighted_stress.py`, `verify_reconstruction.py`,
  `verify_tensor.py`, `verify_conformal.py`, `conformal_experiments.py`) were not
  re-run because their outputs are already digest-pinned and the fabric path is
  the round's focus; a full end-to-end run would strengthen the reproduction
  claim.
- **O3.** The zip internal `manifest.json` and `fe-evidence/manifest.json` do not
  declare themselves (and the former not its `README.md`). This is conventional
  for a self-hashing manifest; noting it only for completeness.
- **O4.** `site/test_builder.py:54` contains path-traversal test literals
  (`../secret.json`, `/tmp/a.json`, `validation/.env`, …). These are inputs to a
  path-sanitization test, not data, so no action is needed — flagged only so the
  strings are not mistaken for a leak during future audits.
- **O5.** `site/evidence.json` provenance records an underlying source revision
  (`ecfe4a22…`) older than the working revision. The accompanying note already
  discloses this ("The base commit predates this working revision"), so the
  disclosure is adequate.

## Summary

Integrity passes (556/556). Every declared digest in `fe-evidence/manifest.json`
(293/293), `site/evidence.json` (35/35) and `site/scientific-snapshot.json`
(43/43) resolves. The supplement archive is self-consistent, ships sources and
fabric run data byte-identical to the snapshot, and its documented commands
reproduce the shipped fabric CSVs byte-for-byte. The PDF's embedded attachment
is byte-identical to the on-disk archive and the archive name matches
`main.tex`/`README.md`. Every quantitative claim checked (coupled Mandel peaks,
fabric probe residuals, MMS orders, load floor, step ratio, temporal orders)
matches the shipped figures/CSVs, the anisotropy trend direction is correct, no
stale NDIR=5 text survives, and overclaim discipline is honest. Three low-severity
packaging defects (two duplicated array entries and one leaked absolute
internal path) require cleanup.

VERDICT: MINOR REVISION

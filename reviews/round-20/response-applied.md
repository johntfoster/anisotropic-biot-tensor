# Round 20 — fixes applied (round-21 prepared)

This records, per review item, the file:line change, the re-run evidence, and the
build/reproduction results. The next review round (round 21) is frozen from the
rebuilt tree.

Frozen snapshot: `.agent-runtime/review-snapshots/round-21`
`SNAPSHOT_ID f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`, 549 files, 0 missing.

## Required items

### B1 — `ln_h` sign convention (R1-required-1)

Applied by flipping the sign at the source so the reported `ln_h` equals the
paper's `ln h` (fixed by `½I − 3/2 m⊗m = −√(3/2) e₁`).

- `moose_app/include/utils/FabricLaw.h:607` — `s.ln_h = -xi / std::sqrt(1.5)`
  (was `+xi / std::sqrt(1.5)`). The header comment (lines 14–18) now restates
  the convention `ln h = −x₂/√1.5` because `½I − 3/2 m⊗m = −√(3/2) e₂`.
- `examples/verify_fabric.py:152` — `"ln_h": float(-x[1] / np.sqrt(1.5))`
  (was `+x[1]/√1.5`).
- `moose_app/src/materials/FabricMaterial.C:67,105` — unchanged; it copies
  `s.ln_h` verbatim, so it inherits the corrected sign.

Re-run evidence:

- Rebuilt `moose_app/anisotropic_biot-opt`; the resulting binary hashes to
  `ff0272fc279fcf91f6acd0c4a2e0ce436e8b165ad68b15549c27e6845dfdd31e`, which is
  the `application_sha256` recorded in every affected run's `provenance.json`
  (the flip is therefore genuinely in the executed binary).
- Re-ran every fabric deck (probe, mandel, and shape families). The probe
  `solution.csv` histories now record the paper sign, e.g.
  `fabric_probe_iso` `ln_h = −0.005` (was `+0.005`), and the coupled mandel
  `ln_h_max`/`ln_h_min` columns are the negative of their pre-fix values while
  `center_pressure` and every other physical field are unchanged (nothing
  physical depends on the sign, as the reviewer noted).
- Re-ran `examples/verify_fabric.py` against the re-run tree:
  `worst probe-field absolute difference = 4.885e-15`; the independent and
  compiled `ln_h` columns agree to ~1e-17. `build/fabric/fabric-verification.json`
  now records the paper-sign `ln_h` for all ten probe cases.

### B2 — shape-probe evidence (R1-required-2, R2-required-1)

- Materialized the three run histories `fe-evidence/runs/fabric_probe_a0`,
  `fabric_probe_a45`, `fabric_probe_a90` (each with `input.i`, `provenance.json`,
  `run.log`, `solution.csv`). Their `provenance.json` records
  `application_sha256 ff0272fc…` (the flipped binary) and
  `command_overrides: ["Materials/law/fabric_angle=0/45/90"]`.
- Registered them in `fe-evidence/manifest.json`: cases 50→53, files 278→293,
  runs 50→53, via `tools/register_fabric_evidence.py`.
- Shipped them in the supplement archive:
  `tools/package_numerical_supplement.py:20` `FABRIC_RUN_CASES` now includes
  `fabric_probe_a0`, `fabric_probe_a45`, `fabric_probe_a90`.
- Regenerated `figures/fe_fabric_probe.pdf/png/csv` and
  `figures/fe_fabric_mandel.pdf/png` (+ `_history.csv`, `_peak.csv`) from the
  shipped tree via `examples/plot_fabric_results.py --runs fe-evidence/runs
  --output build/fabric-plots`; the plotter now reports `"missing": []` and
  panel (c) is drawn from the three shape runs. `figures/fe_fabric_probe.csv`
  carries the three `fabric_probe_a0/a45/a90` rows with full data.

Reproducibility proof: extracted `build/anisotropic-biot-2026-09-20-v2.zip`
into a fresh temporary directory and ran the documented command there —

```
python3 examples/verify_fabric.py                        # worst 4.885e-15
python3 examples/plot_fabric_results.py \
  --runs fe-evidence/runs --output build/fabric-plots    # figures=2, missing=[]
```

— which produced the same figure (panel (c) included) and the same three shape
rows. The documented regeneration no longer reports "Shape-response probes
absent".

## Optional items

### O1 (R1-optional-1) — frozen `D` modes

Applied: `sections/pore_fabric.tex` (lines 258–266) now states explicitly that
the five-modulus transversely isotropic `𝔻` is full rank on the volumetric,
axial, in-plane-deviatoric, and two shear directions but leaves the in-plane
shear `sym(p₁⊗p₂)` frozen to the mineral compliance through the zero eigenvalue
of the Moore–Penrose inverse `𝔻⁺` on that mode. The "full-rank `D`" phrasing now
agrees with the implemented rank-5-in-6 tensor.

### O2 (R1-optional-2) — `verify_fabric.py` implementation check

Applied: `sections/finite_elements.tex:220–224` now notes that the material-point
agreement "is an implementation check, not an independent derivation", because
`examples/verify_fabric.py` re-derives the section equations but shares their
modelling conventions (the distention basis, the equilibrium, and the reported
sign convention for `ln h`) with the compiled material.

### O3 (R1-optional-3) — `3.2e-3` attribution wording

Aligned: `main.tex:556–558` now calls the `3.2×10⁻³` floor "a discretization
floor attributable to the fixed-step backward-Euler temporal error", matching
`site/evidence.json` (which already used "a discretization floor … attributable
to the fixed-step backward-Euler temporal error"). The `nx=20`, `dt=1e-3`
value (`0.0032209…`) is unchanged and still resolves to
`fe-evidence/runs/nonlinear_load_0.0001/analysis.json`.

### R2-opt-1 — NumPy version agreement

Applied: `site/reports/tensor-verification.json` is byte-identical to
`build/weighted-stress/tensor-verification.json`; both record `numpy 2.2.6`
(the stale site copy had `1.26.4`).

### R2-opt-2 — default `--runs`

Applied: `examples/plot_fabric_results.py:40` and `examples/verify_fabric.py:37`
default `DEFAULT_RUNS` to `fe-evidence/runs`, the shipped evidence tree (the
previous default was the unshipped `.agent-runtime/anisotropic-fabric-goal-…/runs`).

### R2-opt-3 — `dehghanipentamerodio2019` issue year

Checked against Crossref (`10.1088/2053-1591/aaf5b9`): `journal-issue`
`published-online 2019-03-01` (volume 6, issue 3); the article itself carries an
online-first date of `2018-12-19`. `references.bib` `year = {2019}` is the
correct **issue** year. No correction needed.

### R2-opt-4 — Drumheller §8.9 and Gajo (3.27)/(3.32)/(3.34) anchors

Checked against the source PDFs in `references/pdfs/`:

- `drumheller-2000-…`: section **8.9 "Symmetry of the distention gradient"**
  is present and is the correct location for the equilibrium similarity
  transformation; it concludes `A_S = a_S^{1/3} R_S`. The manuscript's
  "commute with `A^T A`" is the author's own framing of that symmetry
  condition and is consistent with §8.9. Anchor confirmed; no correction.
- `gajo-2010-…`: eqs. **(3.27)** (logarithmic-volumetric effective Kirchhoff
  stress), **(3.32)** (`J_s = J_{s-m} J_{s-f}`), and **(3.34)** (the two
  constituent-volume relations) are present and are the equations needed to
  eliminate the two constituent volume factors and recover the isotropic
  mineral-volume equation. Anchors confirmed; no correction.

## Build and reproduction results

- **Manuscript**: `latexmk -lualatex -interaction=nonstopmode -halt-on-error
  -outdir=build main.tex` → 28 pages; **0 undefined references, 0 undefined
  citations**, 0 overfull boxes, 1 cosmetic underfull box in the bibliography.
- **Supplement archive**: `tools/package_numerical_supplement.py` →
  `build/anisotropic-biot-2026-09-20-v2.zip`, 58 files,
  sha256 `f24b3d01b0a6d08363231618503a353edd77ccc9321afc0c20b4976a47a9ed24`.
  The archive name is unchanged, so the `\embedfile` filespec in `main.tex`
  needed no edit. The embedded attachment is byte-identical to the on-disk
  archive.
- **Verification site**: `tools/build_verification_site.py` → 32 artifacts,
  link check passed.
- **Review snapshot**: `tools/build_review_snapshot.py round-21` →
  `SNAPSHOT_ID f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`,
  549 files, 0 missing.

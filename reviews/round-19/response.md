# Round 19 — author response and revision matrix

Snapshot reviewed: `.agent-runtime/review-snapshots/round-19`
(`SNAPSHOT_ID ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682`, 534 files).

Verdicts: Reviewer 1 MINOR REVISION · Reviewer 2 MINOR REVISION · Reviewer 3 MINOR REVISION.

Stop criterion (**>=2 exact ACCEPT**) is **not met**; this round produced no ACCEPT.
All three reports found the physics, mathematics and evidence sound, and confined every
required item to notation, packaging or documentation. No scientific defect was reported.
A revised snapshot must be reviewed in a new round (round 20); votes are not carried across.

## Required findings (all accepted; none rebutted)

| ID | Reviewers | Location | Issue | Disposition |
| --- | --- | --- | --- | --- |
| A1 | R1-F1, R2-01, R3-11 | `sections/experiments.tex` availability ¶; `README.md:45` | Supplement named `conformal-2026-09-20-v1.zip`; shipped/embedded archive is `anisotropic-biot-2026-09-20-v2.zip` | APPLIED — both strings updated to the shipped name |
| A2 | R2-02 | `examples/verify_fabric.py:29` | Hard-coded checkout-only run path; documented command fails from the extracted archive | APPLIED — accepts `--runs`, defaults to the shipped evidence tree; documented command verified from an extracted archive |
| A3 | R2-03 | `fe-evidence/manifest.json` | 11 `runs/fabric_*` case directories absent from `cases`/`files`/`runs` | APPLIED — fabric runs registered in the evidence manifest |
| A4 | R1-F2, R3-01 | `sections/stress_reconstruction.tex` vs `sections/pore_fabric.tex` | `W_d` denotes the drained skeleton energy in §4 and the distention energy in the fabric section | APPLIED — drained skeleton energy renamed; fabric section keeps `W_d` (consistent with `S_d`, `E_d`, `D`) |
| A5 | R3-02 | `sections/finite_elements.tex:153-157` | `a` reused for the distention volume ratio and the Mandel rectangle half-width | APPLIED — Mandel half-widths renamed; distention ratio `a` unchanged |
| A6 | R3-04 | `sections/finite_elements.tex` figures | The two new fabric figures are never cited from the text | APPLIED — both figures now `\ref`d in the pore-fabric subsection |
| A7 | R3-10 | `sections/pore_fabric.tex` / `main.tex` introduction | Novelty claim not differentiated from Cowin's fabric-tensor poroelasticity | APPLIED — explicit differentiation added: Cowin assigns anisotropic elastic constants to the solid; here the fabric tensor enters the *distention* energy and thereby the Biot tensor |
| A8 | R3-12 | `sections/experiments.tex` availability ¶ | Claims the finite-element implementation is absent from the supplement, but the archive ships `FabricLaw.h`, `FabricMaterial.{h,C}` and the fabric decks | APPLIED — availability text corrected to state what the archive does ship |
| A9 | R1-F3 | `main.tex` conclusion | `3.2e-3` discrepancy described as a model floor; it is dominated by fixed-`dt` temporal error | APPLIED — attributed to discretization error at the stated `nx`, `dt`, not to the model |

## Optional findings

| ID | Reviewer | Disposition |
| --- | --- | --- |
| R2-04 | validation maps omit `FabricMaterial` | APPLIED — fabric entry added to `validation/equation_to_moose_map.yml` |
| R2-05 | nonlinear fabric equations have reference-state code trace only | NOTED — equation-site scope note added; general finite-deformation fabric equilibrium remains explicitly out of implementation scope |
| R2-06 | coexisting `v1`/`v2` labels | APPLIED — site manifest version aligned to the article supplement family |
| R2-07 | `plot_fabric_results.py` default run emits no figures | APPLIED — site reproduction command passes `--runs` |
| R1 optional | non-monotone Mandel spatial refinement; check-count wording; single-sample temporal order estimate; truncated 5-mode fabric stiffness; manifest hash-description wording | NOTED — wording clarifications where the snapshot already contains the supporting data; no claim changed |

## Verification

The revision pass rebuilds the manuscript, re-runs the fabric verification and the
supplement packaging, and records per-item `file:line` confirmation plus the build
result in the appended verification block. The next review round is frozen from that
rebuilt tree.

## Verification (applied)

All commands were run from the repository root; every result below was observed.
Per-item before/after records are in `reviews/round-19/revision-notes.md`.

### Build

| Command | Result |
| --- | --- |
| `python3 -m pip install -r examples/requirements.txt` | satisfied (numpy 2.2.6, scipy 1.15.3, matplotlib 3.10.8) |
| `python3 examples/weighted_stress.py` | exit 0 |
| `python3 examples/verify_reconstruction.py` | exit 0 |
| `python3 examples/verify_tensor.py` | exit 0 (`materials 13`, `total_states 273`) |
| `python3 examples/verify_conformal.py` | exit 0 |
| `python3 examples/conformal_experiments.py` | exit 0 |
| `python3 examples/verify_fabric.py` | exit 0, `worst_probe_abs_diff = 4.885e-15` |
| `python3 tools/register_fabric_evidence.py` | exit 0 (`fe_cases 49`, `fe_files 273`, `fe_runs 49`) |
| `python3 tools/package_numerical_supplement.py` | exit 0 (55 archive files) |
| `latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex` | exit 0 |

- `grep -ci "undefined" build/main.log` = 0; no unresolved citation or reference
  warning; page count 28.
- `grep -c "Overfull" build/main.log` = 0 (no new overfull boxes relative to the
  prior 0).

### A2 — extracted-archive reproduction

```sh
rm -rf /tmp/r19rev-final-extract && mkdir -p /tmp/r19rev-final-extract
unzip -q build/anisotropic-biot-2026-09-20-v2.zip -d /tmp/r19rev-final-extract
cd /tmp/r19rev-final-extract && python3 examples/verify_fabric.py
```

exit 0; wrote `build/fabric/fabric-verification.json` with
`worst_probe_abs_diff = 4.884981308350689e-15` (≈4.885e-15).

### Embedded archive and final digests

```
pdfdetach -list build/main.pdf      ->  1: anisotropic-biot-2026-09-20-v2.zip
pdfdetach -saveall build/main.pdf   ->  embedded bytes sha256 == on-disk archive
                                        (bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53, both)
```

```
sha256sum build/main.pdf build/anisotropic-biot-2026-09-20-v2.zip
51d236a3c966b108581d730f0bf5161aef9b8ccdd1408908ae1c8f159e307966  build/main.pdf
bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53  build/anisotropic-biot-2026-09-20-v2.zip
```

`site/evidence.json` (32 artifacts, 9 figures) and `site/scientific-snapshot.json`
(41 files) digests all resolve after regeneration; `fe-evidence/manifest.json`
(49 cases, 273 files, 49 runs) digests all resolve.

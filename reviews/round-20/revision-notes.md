# Round 20 revision notes — single-writer pass

Repo: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Base commit: `ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c`
Source of items: `reviews/round-20/response.md` (B1, B2, O1–O3, R2-opt-1…4).

Fabric application binary sha256 after rebuild:
`ff0272fc279fcf91f6acd0c4a2e0ce436e8b165ad68b15549c27e6845dfdd31e`
(the executable bytes are unchanged because the header-only law is compiled into
`lib/libanisotropic_biot-opt.so.0.0.0`, sha256
`f909618d312afd3a89d9f5dc7a8d6d5e98710b4fde4a0365c9309255ff825008`; behaviour is
changed and verified below).

## Required items

| ID | file:line | before → after | verification command | observed result |
| --- | --- | --- | --- | --- |
| B1 | `moose_app/include/utils/FabricLaw.h:607` | `s.ln_h = xi / std::sqrt(1.5);` → `s.ln_h = -xi / std::sqrt(1.5);` | `./moose_app/anisotropic_biot-opt -i moose_app/inputs/fabric_probe.i Outputs/file_base=/tmp/.../solution Materials/law/fabric_coupling=0` | recorded `ln_h = -0.005` (was `+0.005`); paper's `ln h` for `eps=diag(0.01,-0.005,0)` |
| B1 | `moose_app/include/utils/FabricLaw.h:14-19` | header restated `E_d` but not the reported scalars → added the convention block `ln a = sqrt(3) x1`, `ln h = -x2/sqrt(1.5)` because `1/2 I - 3/2 m⊗m = -sqrt(3/2) e2` | header read + `git diff` | comment now matches the formula and the code |
| B1 | `examples/verify_fabric.py:152` | `float(x[1] / np.sqrt(1.5))` → `float(-x[1] / np.sqrt(1.5))` | `python3 examples/verify_fabric.py` | exit 0; independent `ln_h` now equals recorded `ln_h`; worst probe difference `4.885e-15` |
| B1 | `examples/verify_fabric.py:14-16` (O2) | added docstring note that it is an implementation check sharing the modeling and sign conventions | read | note present |
| B1 | `examples/verify_fabric.py:186-189` | added `fabric_probe_a0/a45/a90` to `CASES` so panel (c) families get a genuine independent check | `python3 examples/verify_fabric.py` | worst difference unchanged at `4.885e-15`; a45 `ln_h=-0.0005`, a90 `ln_h=0.004` reproduced by the NumPy code |
| B1 | `examples/plot_fabric_results.py:212` | caption `"ln_h, the deviatoric distention"` → `"ln h, the fabric shape (deviatoric) distention"` | read | plotted quantity named per the paper |
| B1 | `sections/finite_elements.tex:222,236-239` | (c) called "deviatoric distention" → `Fabric shape distention \(\ln h\) (the manuscript convention …); the plotted quantity is the paper's \(\ln h\), not its negative` | `latexmk …` | builds clean; caption matches the data |
| B2 | `fe-evidence/runs/fabric_probe_a0|a45|a90/` | absent → materialized with the exact `fabric_probe_iso` file set: `input.i`, `provenance.json`, `analysis.json`, `solution.csv`, `run.log` | `ls fe-evidence/runs/fabric_probe_a*` | 5 files each; provenance uses `application_sha256`, `git_revision`, `input_deck`, `command_overrides`, `recorded_utc`, `exit_status`, `source` |
| B2 | `fe-evidence/manifest.json` | 50 cases / 278 files / 50 runs, 3 dirs unregistered → 53 cases / 293 files / 53 runs, 0 unregistered | independent audit (below) | run dirs 53 = registered cases 53; unregistered files `[]`; digest/resolve failures `[]` |
| B2 | `figures/fe_fabric_probe.{pdf,png,csv}` | regenerated from `fe-evidence/runs`; panel (c) previously absent (`20085` B, `Shape-response probes absent`) | `python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots` | `missing: []`; panel (c) drawn; CSV now has 11 lines with populated shape rows |
| B2 | `tools/package_numerical_supplement.py` | `FABRIC_RUN_CASES` lacked the shape family → added `fabric_probe_a0/a45/a90` | `python3 tools/package_numerical_supplement.py` | archive now ships `fe-evidence/runs/fabric_probe_a{0,45,90}/solution.csv` (58 files) |
| B2 | `tools/register_fabric_evidence.py` | only refreshed `fabric_*` dirs, leaving `conformal_probe_ref` and stale digests → refreshes case names + digests for **every** directory under `fe-evidence/runs`; fabric-style run records for the fabric families + `conformal_probe_ref` | `python3 tools/register_fabric_evidence.py` | exit 0; digest-mismatch failure on `conformal_probe_ref/provenance.json` resolved |

## Optional items

| ID | file:line | before → after | verification command | observed result |
| --- | --- | --- | --- | --- |
| O1 | `sections/pore_fabric.tex:258-266` | "A full-rank \(\mathbb{D}\) relaxes …" → added that the five-modulus \(\mathbb{D}\) is full rank on its retained directions but leaves the in-plane shear \(\operatorname{sym}(\mathbf p_1\otimes\mathbf p_2)\) frozen to the mineral compliance (zero eigenvalue of \(\mathbb{D}^{+}\)) | read | agrees with `FabricLaw.h`'s five-direction basis |
| O2 | `examples/verify_fabric.py:14-16`; `sections/finite_elements.tex:222` | added "implementation check … shares the section's basis and reported-scalar sign conventions" in both the script and `sec:fe-fabric` | read | done |
| O3 | `main.tex:556-562`; `site/evidence.json:15` | `main.tex` "dominated by … rather than by an irreducible model discrepancy" vs site "a discretization floor" → both now say **floors at about 3.2e-3, a discretization floor attributable to the fixed-step backward-Euler temporal error**, citing the linear step-refinement `3.658e-3`/`7.104e-3` (ratio 1.94) and MMS temporal orders 0.98–1.40 | numbers re-read from `fe-evidence/runs/linear_time_*/*.json` and `fe-evidence/mms-convergence.json` | engine quotes match; wording aligned |
| R2-opt-1 | `site/reports/tensor-verification.json:19` | `"numpy": "1.26.4"` → `"2.2.6"` (matches the archived `build/weighted-stress/tensor-verification.json`) | `diff` vs build copy | only the numpy line differed; now identical |
| R2-opt-2 | `examples/plot_fabric_results.py:40-41` | `DEFAULT_RUNS = .agent-runtime/…` → `fe-evidence/runs`; default output → `build/fabric-plots` | `python3 examples/plot_fabric_results.py` (no `--runs`) | reads shipped evidence by default |
| R2-opt-3 | `references.bib:164-173` | check only (no edit) | Crossref `10.1088/2053-1591/aaf5b9` | entry `year=2019`, `volume=6`, `number=3`, `page=035404` reproduce IOP's issue citation; Crossref `issued`/`published-online` = `2018-12-19` (online-first). Issue year **2019 confirmed**; no change |
| R2-opt-4 | `main.tex:600`; `sections/limits.tex:51` | check only (no edit) | `pdftotext` of Drumheller 2000; Gajo 2010 text | Drumheller §8.9 is titled **"Symmetry of the distention gradient"** (Eqs. 116–119: `A_S T_S^e A_S^{-1}`, symmetry ⇒ `A_S = a_S^{1/3} R_S`), matching the cited transformation; Gajo **(3.27)**, **(3.32)**, **(3.34)** all exist and are the logarithmic volumetric relations (`K = K(ln J − ln J_{s−f})I + m dev B̄`; `J_s = J_{s−m} J_{s−f}`; `K_vol = K_s ln J_{s−m}`, `J_s p_w = −K_s ln J_{s−f}`). Both anchors **confirmed**; no change |

Files I did **not** touch (already modified in the working tree before this pass):
`README.md`, `references.bib`, `sections/experiments.tex`,
`sections/stress_reconstruction.tex`, `tools/build_review_snapshot.py`,
`validation/equation_to_moose_map.yml`.

## Build and verification block

```
$ eval "$(~/miniconda3/bin/conda shell.bash hook)"; conda activate moose
$ export MOOSE_DIR=~/.local/moose
$ export LD_LIBRARY_PATH=~/.local/moose/framework:$LD_LIBRARY_PATH
$ (cd moose_app && make -j$(nproc))                          # exit 0

# re-ran every ln_h-bearing deck (probe iso/coup_a0/a45/a90/conformal/stiffaxial/
# softaxial + shape a0/a45/a90, conformal_probe_ref, 4 mandel cases) — all rc=0

$ python3 examples/verify_fabric.py                          # exit 0
worst probe-field absolute difference = 4.885e-15
$ python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots
{"figures": 2, "missing": [], "files": [ ... 7 files ... ]}   # exit 0
$ python3 tools/register_fabric_evidence.py                  # exit 0
snapshot_files 41 · artifacts 32 · fe_cases 53 · fe_files 293 · fe_runs 53
$ python3 tools/package_numerical_supplement.py              # exit 0
archive build/anisotropic-biot-2026-09-20-v2.zip
sha256 f24b3d01b0a6d08363231618503a353edd77ccc9321afc0c20b4976a47a9ed24 (58 files)
$ latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
                                                             # exit 0
```

Recorded checks:

| Check | Command | Observed |
| --- | --- | --- |
| Undefined references/citations | `grep -ci undefined build/main.log` | `0` |
| Overfull boxes | `grep -c "Overfull \\hbox" build/main.log` | `0` |
| Page count | `pdfinfo build/main.pdf` | 28 |
| Embedded archive bytes | `pdfdetach -saveall build/main.pdf` vs `build/*.zip` | identical `f24b3d01…9ed24` |
| Manifest coverage | independent audit of `fe-evidence/manifest.json` | run dirs 53 = cases 53; unregistered files `[]`; digest/resolve failures `[]`; runs records 53 |
| Site digests | audit `site/evidence.json` (32 artifacts) + `site/scientific-snapshot.json` (41 files) | 0 bad |
| Archive reproduction (`/tmp/archive-final`) | `python3 examples/verify_fabric.py` | exit 0 |
| Archive figure reproducibility | `python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots` | `missing: []`, no "Shape-response probes absent" |
| Figure byte identity (archive vs shipped) | `sha256sum` | `fe_fabric_probe.pdf` `97a0d596…`, `.png` `07f1e14b…`, `.csv` `5fae30eb…`, `fe_fabric_mandel.pdf` `03f520e1…` all **identical** |

Note: the PDF figures were made byte-stable by omitting the PDF `CreationDate`/
`ModDate` metadata (`examples/plot_fabric_results.py:119`), so the documented
reproduction now reproduces the shipped figure exactly rather than only in content.

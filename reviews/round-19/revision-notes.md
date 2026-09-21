# Round 19 — revision notes (single-writer pass)

Applied by the round-19 revision pass. One row per required item (A1–A9) and per
applied optional item (R2-04, R2-06, R2-07). Every listed command was run from
the repository root unless stated otherwise; every listed result was observed.

## Required items

| ID | File:line | Before → After | Verification command | Observed result |
| --- | --- | --- | --- | --- |
| A1 | `sections/experiments.tex:211-212`; `README.md:45` | `conformal-\allowbreak2026-\allowbreak09-\allowbreak20-\allowbreak v1.zip` → `anisotropic-\allowbreak biot-\allowbreak2026-\allowbreak09-\allowbreak20-\allowbreak v2.zip` (LaTeX `\allowbreak` line-breaking macros kept); README `build/conformal-2026-09-20-v1.zip` → `build/anisotropic-biot-2026-09-20-v2.zip` | `grep -rn "conformal-2026-09-20-v1" --include=*.tex --include=*.md --include=*.py --include=*.json --include=*.yml . \| grep -v '^./reviews/' \| grep -v '^./build/'` | no hits outside `reviews/` history and `build/`; only `.agent-runtime/` historical snapshots retain the old name (not sources) |
| A2 | `examples/verify_fabric.py:33` (`DEFAULT_RUNS`), `:181` (`--runs`); `tools/package_numerical_supplement.py:20,35-36,48-50` (`FABRIC_RUN_CASES`, ship run inputs) | hard-coded `ROOT/".agent-runtime/anisotropic-fabric-goal-2026-09-20/runs"` → `ROOT/"fe-evidence/runs"` with an argparse `--runs` override and a clear error; the 12 recorded `solution.csv` inputs the two fabric scripts read are now added to the supplement archive | `rm -rf /tmp/r19rev-final-extract && mkdir -p /tmp/r19rev-final-extract && unzip -q build/anisotropic-biot-2026-09-20-v2.zip -d /tmp/r19rev-final-extract && cd /tmp/r19rev-final-extract && python3 examples/verify_fabric.py` | exit 0; wrote `build/fabric/fabric-verification.json` with `worst_probe_abs_diff = 4.884981308350689e-15` (≈4.885e-15) |
| A3 | `tools/register_fabric_evidence.py:167-214` | script extended to register the 11 `fe-evidence/runs/fabric_*` case directories (cases + file digests + run records) and to assert every recorded digest resolves; JSON never hand-edited | `python3 tools/register_fabric_evidence.py` then `python3 -c` digest walk of `fe-evidence/manifest.json` | `fe_cases=49` (38 existing + 11 fabric), `fe_files=273` (202 existing + 71 fabric), `fe_runs=49`; digest walk `bad=[]` (all resolve) |
| A4 | `sections/stress_reconstruction.tex:34,45,49,201` | drained skeleton energy `W_d` → `W_{\mathrm{dr}}` (4 occurrences); fabric `W_d` and all of `S_d`, `E_d`, `D` unchanged | `grep -n "W_{\\\\mathrm{dr}}" sections/stress_reconstruction.tex`; `grep -c "W_d" sections/pore_fabric.tex main.tex` | `W_{\mathrm{dr}}` at lines 34, 45, 49, 201; fabric `W_d` occurrences intact (16 in `pore_fabric.tex`, 1 in `main.tex`) |
| A5 | `sections/finite_elements.tex:153,154,157` | Mandel rectangle half-widths `a`,`b` → `L_x`,`L_y` (`[-L_x,L_x]\times[-L_y,L_y]`, `L_x=1`, `L_y=0.1`, `2L_x q_L`) in §fe-reference-problems only; distention volume ratio `a` untouched everywhere | `grep -n "L_x\|L_y" sections/finite_elements.tex`; inspect `sections/limits.tex:62` and `main.tex:178` | `L_x`/`L_y` at lines 153-157 only; `limits.tex:62` still reads `a=1,\;J=\bar J` (unjacketed path) and `main.tex:178` still reads `a=\det\mathbf A` — both are the distention volume ratio, not the Mandel geometry, and are unchanged |
| A6 | `sections/finite_elements.tex:222,247` | added `\Cref{fig:fe-fabric-probe}` and `\Cref{fig:fe-fabric-mandel}` in-text references in §fe-fabric | `grep -n "Cref{fig:fe-fabric" sections/finite_elements.tex`; `grep -ci "undefined" build/main.log` | both `\Cref`s present (lines 222, 247); 0 undefined references; build log has no unresolved-reference warning |
| A7 | `main.tex:112-115` (fabric-literature paragraph), `:136-140` (gap paragraph) | added a short differentiation: Cowin-type fabric formulations assign fabric-dependent elastic/poroelastic coefficients to the solid directly and at small strain; here the fabric enters the distention (pore-volume/shape) energy and the anisotropic Biot tensor follows through the mineral-volume response — a distinct constitutive route, not a restatement | `grep -n "assigning\|distinct from the fabric" main.tex`; LaTeX build | text present at lines 112 and 136-140; compiles cleanly (no new overfull) |
| A8 | `sections/experiments.tex:220-231` | "The coupled finite-element implementation … is not part of that archive" → corrected: the archive does ship `FabricLaw.h`, `FabricMaterial.h`, `FabricMaterial.C`, and the `fabric_probe.i`, `conformal_probe.i`, `fabric_mandel.i` decks plus the recorded run histories they read; "the rest of the coupled finite-element implementation" (remaining application sources, deck inputs, per-run analyses, figure data, verification-evidence file) stays in the repository. Honest scope statements preserved | `grep -n "The archive does ship\|The rest of the coupled" sections/experiments.tex`; compare with `unzip -l build/anisotropic-biot-2026-09-20-v2.zip` | corrected text at lines 220-231; archive listing contains all six named fabric sources/decks and 12 shipped run histories |
| A9 | `main.tex:555-557` | "…floors at about \(3.2\times10^{-3}\) at \(nx=20\), \(dt=10^{-3}\) rather than decaying to it" → "…at \(nx=20\), \(dt=10^{-3}\) their normalized pressure discrepancy remains about \(3.2\times10^{-3}\), dominated by the fixed-step backward-Euler temporal error rather than by an irreducible model discrepancy" (number unchanged) | `grep -n "3.2\\\\times10^{-3}" main.tex` | reworded at line 556; the value `\(3.2\times10^{-3}\)` and the `nx=20`, `dt=10^{-3}` identification are unchanged |

Note (A4 conditional): §2 of `main.tex` (notation conventions paragraph) does not list the drained skeleton energy, so no notation-inventory entry was added. The §2 paragraph lists only the four bar-accent meanings, none of which is `W_d`.

## Applied optional items

| ID | File:line | Change | Verification command | Observed result |
| --- | --- | --- | --- | --- |
| R2-04 | `validation/equation_to_moose_map.yml:11-17` | added a `FabricMaterial` object with its equation list, consumed/produced fields, the linearized reference-state derivative note, and an approximation note recording that the general finite-deformation fabric equilibrium is out of implementation scope | `grep -n "FabricMaterial" validation/equation_to_moose_map.yml` | entry present at line 11 |
| R2-06 | `tools/register_fabric_evidence.py:97`; `site/evidence.json:3` | site manifest version `fabric-2026-09-20-v1` → `anisotropic-biot-2026-09-20-v2`, aligned with the article supplement family | `python3 -c "import json;print(json.load(open('site/evidence.json'))['version'])"` | `anisotropic-biot-2026-09-20-v2` |
| R2-07 | `tools/register_fabric_evidence.py:147-154`; `site/evidence.json` `reproduction[4]` | site reproduction command now passes `--runs` (and an output dir) to `plot_fabric_results.py`; the entry is updated in place rather than only appended | `python3 -c "import json;print(json.load(open('site/evidence.json'))['reproduction'][4]['command'])"`; `python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots` | command = `python3 examples/verify_fabric.py && python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots`; the plot script emits 2 figures (`fe_fabric_probe`, `fe_fabric_mandel`) |

## Build and verification (recorded)

All commands run from the repository root unless stated.

```sh
python3 -m pip install -r examples/requirements.txt          # numpy 2.2.6, scipy 1.15.3, matplotlib 3.10.8
python3 examples/weighted_stress.py                           # exit 0
python3 examples/verify_reconstruction.py                     # exit 0
python3 examples/verify_tensor.py                             # exit 0 (materials 13, total_states 273)
python3 examples/verify_conformal.py                          # exit 0
python3 examples/conformal_experiments.py                     # exit 0
python3 examples/verify_fabric.py                             # exit 0, worst_probe_abs_diff 4.885e-15
python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots   # 2 figures
python3 tools/register_fabric_evidence.py                     # exit 0
python3 tools/package_numerical_supplement.py                 # exit 0, 55 archive files
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex   # exit 0
```

- `latexmk` exit 0; `grep -ci "undefined" build/main.log` = 0; 28 pages; `grep -c "Overfull" build/main.log` = 0 (no new overfull relative to the prior 0). Two initial overfull boxes introduced by the A1/A8 rewording were removed by rewording the availability paragraph before the final build.
- The archive embeds `anisotropic-biot-2026-09-20-v2.zip`; `pdfdetach -saveall` bytes hash to `bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53`, equal to the on-disk archive.
- `site/evidence.json` (32 artifacts, 9 figures) and `site/scientific-snapshot.json` (41 files) digests all resolve; `fe-evidence/manifest.json` (49 cases, 273 files, 49 runs) digests all resolve.

## Not applied / notes

- No required item needed to be stopped: none of A1–A9 required a change to equations, numbers, claims, or provenance beyond the listed edits.
- The A2 default run tree is the recorded evidence tree that ships with the repository (`fe-evidence/runs`), which is also what the archive now ships; `.agent-runtime/...` is no longer referenced by any shipped script's default.
- Observation (out of A3 scope, unchanged): the paired `fe-evidence/runs/conformal_probe_ref/` reference deck is also present on disk and is likewise not listed in `fe-evidence/manifest.json`. A3 specified the 11 `runs/fabric_*` directories, so only those were registered; `conformal_probe_ref` is the one remaining unregistered run directory and is flagged here for the next round.

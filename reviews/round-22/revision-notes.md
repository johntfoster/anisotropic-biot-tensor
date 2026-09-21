# Round-22 revision notes — single-writer pass

Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
Reviewed freeze: `.agent-runtime/review-snapshots/round-21`
(SNAPSHOT_ID `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`)
Base commit: `ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c` (`git rev-parse HEAD`)
Source items: `reviews/round-21/reviewer-1.md` (MAT-1..MAT-3), `reviewer-3.md` (R3-1..R3-5), `reviewer-2.md` (optional only).

Path taken: **reduction** — the implemented distention was restricted to `span(e1, e2)`
(`D` positive definite on the volumetric–axial block, zero on the four complementary modes).
See `reviews/round-22/response.md` for why and for the per-item evidence.

Build log: `reviews/round-22/build.log` (copy of the final `latexmk` transcript; the in-tree log
is `build/main.log`).

---

## 1. sha256 before → after, per edited source file

"before" = the working tree as received at the start of this pass (= the reviewed round-21
content plus the three retained Foster prose edits); "after" = the file as it stands at the end.

| file | before | after |
| --- | --- | --- |
| `main.tex` | `c67c00b8a17aaf0ecaa314857f66fc99e95324996587804c1b87807254a5d334` | `4d2b75d11ccca155c7da59725be210e5f380c5b7716d3d393175b6e8b63787af` |
| `sections/pore_fabric.tex` | `31a5a9fc0b644fd698f7d49b17d08278a16122e1f3916c316dd29d7d24f4daf6` | `3392d1d50562e5b2c6bc58a9392044462e99e62a8d1ba4b8d4563a8a787a76c0` |
| `sections/finite_elements.tex` | `ee24fa81182649e33d81b6a316b5c9b1b2f6a9f4b6bce7b8de600c2c8931c9f4` | `f6df90ea0b7256cff33a17fb85904c79cf79e6d942b263610a986a60f71671bc` |
| `sections/experiments.tex` | `a452cf5dd67bb9aa76d40a7833116bdc77d172eafddc348be699822155333b86` | `c82c9512672d58bbdc6d4ab5355f5f4562cc0edb20f4f17d79f2f90e2f774ee6` |
| `validation/equation_to_moose_map.yml` | `ad9ebec32cd614578592dff49225d916161ffd1f77afdfed3fe99b44c794d343` | `b3811254b1f68b5e51b9cdb38adf504f3a844f7fbc73f4c76feb5a1b9e723c45` |
| `validation/theory_traceability.yml` | `dd18414ccf37a8aa0ae7ff0af02800ee4f9357fc249f17edc89ddd52cb11b048` | `184b4f3f91ce14ece3c1656cd3b4de7f5acc0339b4f75989f08051c4e629a980` |
| `moose_app/include/utils/FabricLaw.h` | `e57f4bdf2e78e042d76767bc26905017ffded46a08c26d383660197666184406` | `2953669c61af15c4aac3d7a73854793674995b647a6a7433c78b2d3b6a9a9857` |
| `moose_app/src/materials/FabricMaterial.C` | `fd343519b7aa71dcfae29405500719d9616fb669cb9284e09688e0b6394139f6` | `9abcfab637c610ac9645105d72dcfd63ff19e550305bf8d772981f00ecc030c2` |
| `moose_app/inputs/fabric_probe.i` | `00ca5c61787579e05419b5878d9bac1c876ad943387c2032f4323da78256d0ca` | `49ae9a76eb30982778873dbb30cfb4943994a5684849d4118072040b17e679cf` |
| `moose_app/inputs/fabric_mandel.i` | `89be4736f77c865610720643ab93782ceb5f475b77057d37fa16da3d8692dfe7` | `a1ae9148583b4209b16922f0c52425fe33825f7635ffadd3ad008a79d564b867` |
| `examples/verify_fabric.py` | `d9194f7cd5fd1da254b04f7aca0b6466fb9602b1859e93bbc52d147a5be18d7d` | `d62657882696aca5e6687effa2217071c80431c1aea5b7b8017a891abaa1d709` |
| `examples/plot_fabric_results.py` | `ed4b81bd5575ae9888edbcc8cee613f4c126d7fa3ba55dd71307366532369128` | unchanged |
| `tools/register_fabric_evidence.py` | `ea0698ec1f42f9877ab16e014a98d964c7f7bd74b0b9ad7d141520d98a6e3c8c` | `ac1cf71f9fc53fa7946ff4464b2602301d83c83cc9e8099473a6d2b8e81cb2d0` |
| `tools/package_numerical_supplement.py` | `1d7a3027f48003df9095a1a66f667d0ac66df5df0cfb04a9ba0551dfb18eff11` | `a0cd2ba0c7795d7b7b5188fc833224f0d1873c8997abb854f2984c57253160c2` |
| `README.md` | `96a6b585fc654b7a4e537fe341c74fc1248c6d7a2fefc3b4203a6adb39cd9bf2` | `fbda410ee3eb2ffef87af83eabc166e9d0576451896b582230cc2b62b6422ea5` |
| `moose_app/inputs/conformal_probe.i` | `fbd86fc45328a05fb317f8981423fcb3d6fc54bad8cdd0715a2cc41420322a7a` | unchanged |

New files created in this pass:

| file | sha256 |
| --- | --- |
| `examples/plot_fe_verification.py` | `132fa29062c7d439f78208f92b7982f98f28d01d04bd32ce3b748e8372da51b7` |
| `tools/rerun_fabric_decks.py` | `589e0f8ac16447584c04d832991fb2669995e7005035a1e0901427c0602da417` |
| `reviews/round-22/response.md` | this pass |
| `reviews/round-22/revision-notes.md` | this file |
| `reviews/round-22/build.log` | final latexmk transcript |

Regenerated evidence and outputs (final):

| artifact | sha256 |
| --- | --- |
| `moose_app/anisotropic_biot-opt` | `ff0272fc279fcf91f6acd0c4a2e0ce436e8b165ad68b15549c27e6845dfdd31e` (unchanged bytes) |
| `moose_app/lib/libanisotropic_biot-opt.so.0.0.0` | `859a34121b1628fb373ce4c5f882558799c19e5925cd93aba0cfbde6c484a81c` (changed: the header-only law compiles into the library) |
| `build/fabric/fabric-verification.json` | `66e3f5c4b1041acbf494db3dda591845d420b2680102d139a0c122b659326a1c` |
| `figures/fe_fabric_probe.csv` | `e7bc7406fa8a455def44323f0dc517cf80382c007235c4e17eeeb29fbede09a2` |
| `figures/fe_fabric_probe.pdf` / `.png` | `97a0d596acf43b40802a58822e32538f81deaeabb52e89a759fff4397a88666e` / `07f1e14b19b5ec30167c53c83c82e8eca33771a02ac187334d26ab1ade730e1c` |
| `figures/fe_fabric_mandel_peak.csv` | `59d60505273db81c2f6da559593a6441163c9dc2107de0ee87bd21f9265cd267` |
| `figures/fe_fabric_mandel.pdf` / `.png` | `a750a216f01e0811c8bb0dd3cc9cc9e38247f393b68b1cfda944af200a9b18ff` / `3ae0f4a09296fad424360dbd5d24a1dd181d9ae9048f93b30b9d42e5475cce9e` |
| `figures/fe_verification_convergence.pdf` / `.png` (new) | `12cdde8ebd569d5dab0f1598bfa93e392cd6908e573f5edeb9bf79288763d755` / `5a9387457be3716e75d395c0aff876e392d72ae054179a4254e5b0d1ab57d07e` |
| `figures/fe_reference_comparison.pdf` / `.png` (new) | `4d5a499c40824119b5b870984faa4d10bed92905f6cbe4ea87cb4e9b28e57550` / `3fa5d03e1225e68c3fa744e262f5ed9bc5e77b61eae6a5a49b830c8de25b57f2` |
| `site/evidence.json` | `0af66cb96d873b29d3a037abe2608ca101fa083b9282874dc70714717fb61538` |
| `site/scientific-snapshot.json` | `76bdf6c04b92c3243eed65862f6b9139e7938078f459aa5ded73f48b036dbb84` |
| `fe-evidence/manifest.json` | `4d3262e3bd9353b1ee3b5f4a6f84d4d0977e8863116407c0763d204b86af7b36` |
| `build/anisotropic-biot-2026-09-20-v2.zip` | `bf99380cdf82940ed806d814e0f921efd1a16c1057a8eb7647272364e1eff3e2` |
| `build/main.pdf` | `ec975573ccd6194e2d8701f63823a2b4ba21ee762a06113df590f1708964a831` |

The three retained Foster prose edits were preserved verbatim: `main.tex` abstract comma,
`main.tex` conclusions "a discretization floor" wording, `sections/pore_fabric.tex` missing copula.

---

## 2. Count integrity per edited `.tex`

Counted with `grep -oF` exactly as in `reviews/foster-fabric-cycle-1/counts-before.txt`
(so `\cite` also matches `\citep`/`\citet`, and `\Cref` is *not* counted in the `\cref` column).
"before" is the round-21 snapshot file `.agent-runtime/review-snapshots/round-21/<file>`;
"after" is the working tree.

| file | label | ref | cref | eqref | cite | `\begin{equation}` | `\begin{align}` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `main.tex` before | 41 | 0 | 3 | 18 | 24 | 17 | 10 |
| `main.tex` after | 41 | 0 | 5 | 19 | 24 | 17 | 10 |
| `sections/pore_fabric.tex` before | 25 | 0 | 5 | 28 | 2 | 16 | 2 |
| `sections/pore_fabric.tex` after | 25 | 0 | 9 | 31 | 2 | 16 | 2 |
| `sections/finite_elements.tex` before | 22 | 0 | 2 | 9 | 2 | 3 | 5 |
| `sections/finite_elements.tex` after | 24 | 0 | 3 | 11 | 2 | 3 | 5 |
| `sections/experiments.tex` before | 9 | 6 | 0 | 9 | 1 | 3 | 0 |
| `sections/experiments.tex` after | 9 | 6 | 0 | 9 | 1 | 3 | 0 |

No `\label` was removed or renamed in any file, so no previously valid reference can dangle.
The `\label` increase in `sections/finite_elements.tex` is the two new figure labels
(`fig:fe-verification`, `fig:fe-reference-comparison`); the `\cref`/`\eqref` increases are their
in-text references and the new symmetry-check references. `\begin{equation}`/`\begin{align}`
counts are unchanged everywhere (no equation was added or removed; `eq:fabric-compliance-restriction`
keeps its number but its right-hand side changed from `D⁻¹` to `D⁺`).

---

## 3. Build result

```
$ latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
EXIT=0
undefined references/citations : 0   (grep -ci undefined build/main.log)
overfull hboxes               : 0   (grep -c 'Overfull \hbox' build/main.log)
pages                         : 32  (pdfinfo build/main.pdf)
build/main.pdf sha256         : ec975573ccd6194e2d8701f63823a2b4ba21ee762a06113df590f1708964a831
```

Page count moved 28 → 31 → 32 as the two new finite-element displays were added and the
convergence display was expanded from three to four panels.

Embedded supplement verified against the on-disk archive:

```
$ pdfdetach -saveall -o /tmp/r22/pdfx2 build/main.pdf
bf99380cdf82940ed806d814e0f921efd1a16c1057a8eb7647272364e1eff3e2  /tmp/r22/pdfx2/anisotropic-biot-2026-09-20-v2.zip
bf99380cdf82940ed806d814e0f921efd1a16c1057a8eb7647272364e1eff3e2  build/anisotropic-biot-2026-09-20-v2.zip
```

Archive self-consistency and end-to-end reproduction from a clean extraction:

```
$ unzip -q build/anisotropic-biot-2026-09-20-v2.zip -d /tmp/r22/supp && cd /tmp/r22/supp
$ python3 -c "verify manifest.json hashes"     -> entries 57, bad [], extra []
$ python3 examples/verify_fabric.py            -> exit 0, worst probe-field difference 4.885e-15
$ python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots
                                               -> exit 0, 2 figures, missing []
```

Archive version name was **not** bumped (`anisotropic-biot-2026-09-20-v2.zip`), so `main.tex`'s
`\embedfile`, `tools/package_numerical_supplement.py`, and `README.md` all still agree.

---

## 4. Digit-literal reconciliation

Every number that changed, with its regenerated source.

| manuscript location | old | new | verified against (command output) |
| --- | --- | --- | --- |
| `sections/finite_elements.tex` peak centre pressure, fabric along `X1` | `6.28e-5` | **`4.38e-5`** | `figures/fe_fabric_mandel_peak.csv` = `4.3760733643082e-05` |
| same, `45°` | `5.10e-5` | **`4.98e-5`** | `4.9825794324732e-05` |
| same, other in-plane axis | `3.95e-5` | **`5.50e-5`** | `5.497926837564e-05` |
| same, uncoupled reference | `5.13e-5` | **`3.65e-5`** | `3.6523250981799e-05` |
| page count (recorded) | 28 | **32** | `pdfinfo build/main.pdf` |

Numbers **added** in this pass, each from a command run in this session:

| manuscript number | value | source |
| --- | --- | --- |
| `H` reconstruction error | `2.2e-16` | `verify_fabric.py` `H_reconstruction_max_abs_diff` = `2.220446049250313e-16` |
| `det H − 1` | `−3.3e-16` | `H_det_minus_one` = `−3.3306690738754696e-16` |
| `‖D:e3‖` | `1.6e-16` | `D4_e3_norm` = `1.5823112613210482e-16` |
| `D:e6` | `0` | `D4_e6_norm` = `0.0` |
| rotation invariance | `2.5e-16` | `rotation_invariance_norm` = `2.4965357070272594e-16` |
| MMS adjacent orders `p` | `2.00`, `2.00` | `fe-evidence/mms-convergence.json` `naive_orders` |
| MMS adjacent orders `ux` | `2.99`, `2.96` | same |
| MMS adjacent orders `uy` | `3.00`, `2.96` | same |
| step-refinement ratio | `1.94` | `figures/fe_mandel_refinement.csv` `0.0071039215708695895/0.003657958974355574` = `1.9420` |
| finite-load floor | `3.2e-3` | `figures/fe_load_limit.csv` `0.003220919735602341` |

Numbers checked and **unchanged** (re-verified from regenerated artifacts):

| claim | value | source |
| --- | --- | --- |
| worst probe-field difference | `4.9e-15` | `verify_fabric.py` worst = `4.885e-15` |
| conformal reduction vs `ConformalMaterial` | `1.9e-14` | `1.874e-14` |
| reference Biot components (`sections/experiments.tex`) | `0.7000`, `0.7583`, `0.7917` | `build/conformal/` (conformal suite untouched by this pass) |
| uncoupled probe Biot components | `0.88387` | `figures/fe_fabric_probe.csv` |
| coupled probe Biot components | `0.850654`, `0.910270` | `figures/fe_fabric_probe.csv` (insensitive to the removed modes) |
| conclusions temporal orders | `0.98`–`1.40` | `fe-evidence/mms-convergence.json` `difference_orders` span `0.978`–`1.397` |
| conclusions step refinement / floor | `3.7e-3`, `7.1e-3`, ratio `1.94`, floor `3.2e-3` | `figures/fe_mandel_refinement.csv`, `figures/fe_load_limit.csv` (non-fabric runs, unchanged) |
| conformal suite sizes | `186` checks, `273` states, `13` stiffnesses, `2.5e-9` | `build/conformal/verification.json`, `build/weighted-stress/tensor-verification.json` (unchanged) |

---

## 5. Evidence regeneration record

```
# 1. rebuild
cd moose_app && make -j$(nproc)                       # exit 0; lib sha 859a3412…
# 2. re-run every pore-fabric deck (15 cases)
python3 tools/rerun_fabric_decks.py                   # 15/15 success
# 3. independent check
python3 examples/verify_fabric.py                     # exit 0, worst 4.885e-15
# 4. per-run analysis records
python3 tools/rerun_fabric_decks.py --analysis-only   # 10 probe + 4 mandel + reference
# 5. figures
python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots
python3 examples/plot_fe_verification.py              # 2 figures, missing []
# 6. evidence manifests
python3 tools/register_fabric_evidence.py             # artifacts 35, figures 11, cases 5,
                                                      # snapshot 43, fe cases 53, fe files 293
python3 tools/build_verification_site.py --validate-only   # {"manifest": "valid", "artifacts": 35}
python3 tools/build_verification_site.py                   # link_check passed
# 7. supplement
python3 tools/package_numerical_supplement.py         # 58 files, sha bf99380c…
# 8. manuscript
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex   # exit 0
```

Independent self-consistency audit run after all regeneration: `fe-evidence/manifest.json`
53 cases / 293 files all resolve and hash-match; `site/evidence.json` 35 artifacts all resolve
and hash-match; `site/scientific-snapshot.json` 43 files all resolve and hash-match; every
`\includegraphics` target in `main.tex` and `sections/*.tex` exists. Result: **FAILS: none**.

No file under `.agent-runtime/review-snapshots/`, `reviews/round-19`, `reviews/round-20`,
`reviews/round-21`, `reviews/foster-cycle-*`, or `reviews/foster-fabric-cycle-*` was read-write
touched. No commit, push, or history rewrite was performed.

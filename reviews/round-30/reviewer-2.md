# SIMULATED AI PEER REVIEW — Reviewer 2 (numerical verification and source fidelity)

Manuscript: "An anisotropic Biot tensor from mineral stress and distention work"
Snapshot under review: `.agent-runtime/review-snapshots/round-30` (frozen; read-only)
SNAPSHOT_ID (declared): `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`

## Mandatory first checks — results

1. **Manifest self-hash.** `sha256sum .agent-runtime/review-snapshots/round-30/source-manifest.json`
   = `ade4ec319cd757abad15546bd307efe2d9f85b2df21aa075bd74fb9ba4f0658b`
   → **matches the declared SNAPSHOT_ID exactly.**

2. **Full manifest re-hash** (performed on a `cp -r` copy in `/tmp`, nothing written inside the snapshot):
   - Entries listed in `source-manifest.json`: **592**
   - Hash matches: **592 / 592**
   - Missing files: **0**; hash mismatches: **0**
   - Files present but not listed: **2** — `SNAPSHOT_ID` and `source-manifest.json` (expected runtime/metadata files, not payload)
   - **Result: PASS.** No mismatch, no missing listed file, no unexplained unlisted file.

This reviewer did not open any file under `reviews/`, and did not read any `.agent-runtime/review-snapshots/round-*` directory other than `round-30`.

---

## REQUIRED CHANGES

### R2-C1 — Pore-fabric run provenance names a revision that cannot contain the fabric source, and omits source/executable digests

**Location:** `fe-evidence/runs/fabric_*/provenance.json` (19 records), e.g. `fe-evidence/runs/fabric_probe_iso/provenance.json`, `fe-evidence/runs/fabric_contour_a45/provenance.json`, `fe-evidence/runs/fabric_mandel_coup_a90/provenance.json`.

**Exact values at issue.** Each of the 19 pore-fabric provenance records declares

```
"git_revision": "ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c"
```

and each omits both `source_sha256` and `binary_sha256` (verified: 0 of 19 carry either field).

At that revision the fabric source **does not exist**:

```
$ git cat-file -e ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c:moose_app/src/materials/FabricMaterial.C   -> ABSENT
$ git cat-file -e ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c:moose_app/include/utils/FabricLaw.h        -> ABSENT
$ git cat-file -e ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c:moose_app/include/materials/FabricMaterial.h -> ABSENT
$ git log --oneline --diff-filter=A -- moose_app/src/materials/FabricMaterial.C
  6385889 Extend the anisotropic Biot tensor with pore-fabric theory and verified FE evidence
```

`ab46ebe` (2026-09-20 18:50) is an ancestor of the pinned snapshot revision `97e862b` (2026-09-21 17:33), and the twelve fabric files (`FabricMaterial.C/.h`, `FabricLaw.h`, `fabric_probe.i`, `fabric_mandel.i`, `fabric_contour.i`, `conformal_probe.i`, plus the fabric plotting/verify scripts) are **added** on the path from `ab46ebe` to `97e862b`.

**Why this is required.** The manuscript presents these runs as evidence (`sections/finite_elements.tex` §"Pore-fabric demonstration": peak centre pressures `4.36e-5`, `4.99e-5`, `5.52e-5`, `3.62e-5`; contour peaks `3.61e-5`, `4.35e-5`, `4.97e-5`, `5.50e-5`; diffusion figure). The recorded revision therefore cannot have produced them, and because these records carry no `source_sha256`/`binary_sha256` there is **no digest anywhere in the frozen tree that links the shipped fabric results to the shipped fabric source**. The 38 non-fabric runs, by contrast, do record digests (see R2-C3), so the defect is specific to the fabric evidence the manuscript relies on for its newest claims.

**Required fix:** record the revision actually used (or the correct commit containing the fabric sources) for all 19 fabric runs, and add `source_sha256` for the fabric source files plus `binary_sha256`, as the older runs already do.

### R2-C2 — Two payload files declared as JSON are not JSON and embed absolute host paths

**Location:** `build/weighted-stress/derivation-scan.json`, `build/weighted-stress/display-scan.json`.

Both are declared with a `.json` extension in the supplement manifest and shipped in the archive:

```
build/weighted-stress/derivation-scan.json : 0807a839259aab8141d02c53b8194914cd654c271e2f7c2a1b50e604640d94fb
build/weighted-stress/display-scan.json    : f0c0a6760b9d82735d57aff22858c83c4db21231af8bf29f8405eb0b67517e91
```

Their declared digests **do** verify (see audit), but the file type is wrong:

```
$ file build/weighted-stress/derivation-scan.json
build/weighted-stress/derivation-scan.json: ASCII text
$ python3 -c "import json;json.load(open('build/weighted-stress/derivation-scan.json'))"
json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 1)
```

They are human-readable scan logs whose first lines are absolute local paths on a **different** host/user than the review environment:

```
== /home/john/projects/research/reactive_transport/anisotropic-biot-tensor/main.tex ==
```

**Why this is required.** `sections/experiments.tex` §"Independent verification and reproducibility" states the repository records its evidence "as JSON and CSV files"; a consumer that parses `*.json` in the supplement (a normal machine-readability expectation for a declared payload) fails, and the embedded `/home/john/...` path is a provenance/portability defect inside a distributable artifact.

**Required fix:** rename to a non-`.json` extension (e.g. `.txt`/`.log`) and update the supplement manifest, or emit valid JSON; sanitize the absolute paths.

---

## OPTIONAL NOTES

### R2-C3 — No run record carries both a revision and source digests

The 57 FE provenance records split into two disjoint schemas:

- 38 runs (`anisotropic_*`, `isotropic`, `linear_*`, `mms_*`, `jacobian_*`, `nonlinear_load_*`, `one_element_*`, `partial_*`): `source_sha256` (12 files) + `binary_sha256`, **no** `git_revision`.
- 19 runs (`conformal_probe_ref`, `fabric_*`): `git_revision` only, **no** `source_sha256`/`binary_sha256`.

No single record ties a revision to source digests. A uniform provenance schema (revision + source digests + executable digest in every record) would make R2-C1 untestable-in-the-future. All 456 `source_sha256` values across the 38 runs resolve, and all 38 `input_sha256` values match their `input.i`.

### R2-C4 — Two distinct copies of the manufactured-solution analysis

`site/reports/mms-convergence.json` (`87e1d95bb87b4535e5e5389d8d19bc4d5ca97d0a38e95ebc703bff6c5b977887`) differs from `fe-evidence/mms-convergence.json` (`de2ca677a47f3c7745a9cc748ad7be768e4884b7b6934878df853036508419a0`). Both digests are declared where they are used and both resolve (`site/evidence.json` declares the site copy; `figures/fe-verification-plot-manifest.json` declares the `fe-evidence/` copy). This is self-consistent, but two artifacts with the same name and different bytes invite confusion; a note confirming the intended distinction would help.

### R2-C5 — Export manifest names paths absent from the frozen tree

`provenance/manuscript-export.json` lists 13 paths; 4 are absent from the snapshot: `.latexmkrc`, `Makefile`, `agent_environment`, `agent_workflows` (9 present). If this manifest describes the public export repository rather than this manuscript repo, that should be stated explicitly; otherwise 4 of 13 declared paths do not resolve.

### R2-C6 — Bib key/year inconsistency in one entry

`references.bib`, `@article{braun2020, ...}` declares `year = {2021}` while the key says `2020`. The entry is only cited inside a multi-key `\citep{...}` group (`main.tex:102`) so no rendered year claim is currently affected, but the key/year mismatch should be reconciled.

### R2-C7 — `source_sha256` in the build reports uses bare filenames

`build/conformal/experiments.json` and `build/conformal/verification.json` key `source_sha256` by bare basenames (`conformal_model.py`, `conformal_experiments.py`) that resolve only under `examples/`. The digests are correct, but an unqualified key is ambiguous in a flat machine-readability context.

---

## Assessment

### Numerical recomputation (frozen artifacts only)

Every number quoted in the manuscript was recomputed from the frozen artifacts. **All 32 checked quantities agree.**

| # | Manuscript quote (location) | Recomputed value (source) | Status |
|---|---|---|---|
| 1 | conformal suite "186 named checks" (`experiments.tex:180`) | `checks_passed=186`; 186 `checks` entries (`build/conformal/verification.json`) | OK |
| 2 | "65 per-state identities (five states times thirteen)" (`:181`) | 5×13 = 65; `legacy_identities_rechecked=67` = 65 + the 2 stated reference relations | OK |
| 3 | "largest absolute error ... \(2.5\times10^{-9}\)" (`:186`) | `max_constitutive_identity_error=2.454989033173293e-9` → `2.45e-9` | OK |
| 4 | "273 finite states across 13 mineral stiffnesses" (`:191`) | `total_states=273`, `materials=13`, `states_per_material=21` (`site/reports/tensor-verification.json`) | OK |
| 5 | "110 checks, max scaled error \(8.09\times10^{-9}\)" (`main.tex:...`) | `count=110`, `maximum_scaled_error=8.086725789003e-9` (`fluid-coupling-verification.json`) | OK |
| 6 | "matches ... to \(6.4\times10^{-14}\) over 41 finite states" | `states=41`, `value_absolute_error=6.394884621841e-14` (`cpp-python-constitutive.json`) | OK |
| 7 | Mandel "38 self-checks (peak overshoot 5.4659% at t = 0.01516535)" (`site/evidence.json:14`) | 38 `checks`; `central_overshoot.ratio=1.0546586069998425` → 5.46586%; `time=0.015165352045764979` | OK |
| 8 | "discretization floor ... about \(3.2\times10^{-3}\)" (`finite_elements.tex:213,232`; `main.tex:573`) | `nonlinear_load_0.0001` `pressure_max_normalized=0.003220919735602341` (`figures/fe_load_limit.csv`) | OK |
| 9 | MMS spatial p "2.00 and 2.00" (`finite_elements.tex`) | `1.996629236`, `2.000807300` (`mms-convergence.json`) | OK |
| 10 | MMS spatial ux "2.99 and 2.96" | `2.991666866`, `2.958479240` | OK |
| 11 | MMS spatial uy "3.00 and 2.96" | `2.998261286`, `2.959985775` | OK |
| 12 | temporal nx=16 (ux 1.093, uy 0.978, p 1.015) | `1.093194822`, `0.978303798`, `1.015176716` | OK |
| 13 | temporal nx=32 (ux 1.397, uy 1.018, p 1.125) | `1.396877937`, `1.018345541`, `1.125199497` | OK |
| 14 | temporal nx=64 (ux 1.396, uy 1.076, p 1.252) | `1.396366310`, `1.076203845`, `1.251931280` | OK |
| 15 | step-refinement ratio "1.94" | `0.0071039215708695895 / 0.003657958974355574 = 1.9420` (`fe_mandel_refinement.csv`) | OK |
| 16 | fabric peaks 4.36 / 4.99 / 5.52 / 3.62 (×10⁻⁵) | `4.3627593400865e-5`, `4.9900848305106e-5`, `5.521105069019e-5`, `3.6163929824772e-5` (`fe_fabric_mandel_peak.csv`) | OK |
| 17 | contour peaks 3.61 / 4.35 / 4.97 / 5.50 (×10⁻⁵) | `3.606194309585106e-5`, `4.3491366180031454e-5`, `4.973659107895197e-5`, `5.503135423750668e-5` (`fe_fabric_contours.csv`) | OK |
| 18 | contour u_mag 5.18 / 5.14 / 2.38 / 5.26 (×10⁻⁵) | `5.1826395396202306e-5`, `5.13715515334801e-5`, `2.381836351578327e-5`, `5.258692042529596e-5` | OK |
| 19 | reference Biot 0.7000, 0.7583, 0.7917 (`experiments.tex:25`) | `B=[0.7, 0.7583333333333333, 0.7916666666666666]` (`build/weighted-stress/results.json`) | OK |
| 20 | "mineral shear modulus is \(16.8K_*\)" (`experiments.tex:29`) | `trace(P_dev @ cs)/10 = 168/10 = 16.8` (`conformal_model.py:78`) | OK |
| 21 | fabric reconstruction "differs ... by \(2.2\times10^{-16}\)" | `H_reconstruction_max_abs_diff=2.220446049250313e-16` | OK |
| 22 | "\(\det\mathbf H-1=-3.3\times10^{-16}\)" | `H_det_minus_one=-3.3306690738754696e-16` | OK |
| 23 | "\(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\) and \(\mathbb D:\mathbf e_6=\mathbf 0\)" | `D4_e3_norm=1.5823112613210482e-16`; `D4_e6_norm=0.0` | OK |
| 24 | rotation invariance "\(2.5\times10^{-16}\)" | `rotation_invariance_norm=2.4965357070272594e-16` | OK |
| 25 | NumPy re-implementation "worst absolute difference \(4.9\times10^{-15}\)" | `worst_probe_abs_diff=4.884981308350689e-15` | OK |
| 26 | conformal reduction "to \(1.9\times10^{-14}\)" | `conformal_cross_check` max abs diff `1.8741952434453424e-14` | OK |
| 27 | anisotropic peak centre pressure 0.2062–0.2158 at t = 0.002–0.004 | `0.20618076123919`–`0.21577360606411`, `peak_time` 0.002–0.004 (`finite-deformation-summary.json`) | OK |
| 28 | anisotropic `force_relative` ≤ 1.276e-10 | `1.2764297555431118e-10` | OK |
| 29 | mass residual ≤ 2.47e-10 | `2.4698697504736024e-10` | OK |
| 30 | isotropic 0.2238, `force_relative` 3.214e-12 | `0.22382672333431`, `3.2144128628682927e-12` | OK |
| 31 | partial 0.2005–0.2016, `force_relative` ≤ 2.052e-10 | `0.200515258783`–`0.20162857565873`, `2.0521425828487087e-10` | OK |
| 32 | supplement "expected 69 files" | 69 entries in the archive (68 payload + `manifest.json`) | OK |

No discrepancy was found between any manuscript-quoted number and its frozen source. The manuscript's own framing is consistently conservative: the values it flags as "measurements and no order above one is asserted" (ux ≈ 1.40 at nx=32/64) do reproduce, and every figure caption that disclaims verification/validation status is matched by a corresponding `limitations` entry in the plotting manifests.

### Digest audit summary

Every declared machine-readable digest in the shipped tree resolves to the file it names. **Zero unresolvable, missing, or stale digests.**

| Artifact / digest family | Declared | Resolved | Result |
|---|---|---|---|
| `source-manifest.json` (snapshot) | 592 | 592 | PASS (+2 unlisted metadata) |
| Supplement `manifest.json` payload (`sha256`) | 68 | 68 | PASS; declared set ≡ actual set |
| Supplement SHA-256 vs on-disk archive | 1 | 1 | PASS (`fa8c07a25f…146c`; 69 files) |
| PDF `\embedfile` attachment vs on-disk archive | 1 | 1 | **byte-identical** after FlateDecode |
| `figures/*-plot-manifest.json` `input_sha256` + `output_sha256` | 43 | 43 | PASS |
| `fe-evidence/manifest.json` file `sha256` (+`bytes`) | 317 | 317 | PASS (0 size mismatches) |
| `site/evidence.json` artifact `sha256` | 41 | 41 | PASS |
| `site/scientific-snapshot.json` file `sha256` | 47 | 47 | PASS |
| `build/**` report `source_sha256` | 4 | 4 | PASS (bare names resolve under `examples/`) |
| FE run `provenance.json` `source_sha256` (38 runs × 12) | 456 | 456 | PASS |
| FE run `provenance.json` `input_sha256` (38 runs) | 38 | 38 | PASS |
| **Total** | **~1,608** | **~1,608** | **PASS** |

Additional confirmations:

- **Supplement self-containment.** `build/anisotropic-biot-2026-09-20-v2.zip` declares `version` and a `sha256` map covering all 68 payload files; the declared set exactly equals the archive contents (no extras, none missing). `README.md` supplies the dependency step (`python3 -m pip install -r examples/requirements.txt`) and an explicit reproduction order (verification scripts first, then plot generation), and states no companion checkout is required. The manuscript's Code-and-data-availability paragraph is accurate on this point.
- **PDF attachment.** Object 120 (`/Type/EmbeddedFile`, `/Subtype application/zip`, `/Size 2277115`) decompresses to a stream whose SHA-256 is `fa8c07a25f853dd96a6ef8f101ee8d5ef25650e2d746aaedd9b5b78bfad0146c` — identical to the on-disk archive and to the declared digest, and `cmp` reports the extracted bytes byte-identical to `build/anisotropic-biot-2026-09-20-v2.zip`.
- **FE evidence tree.** 57 run directories, each with a `provenance.json`; the `fe-evidence/runs` set matches the 57 `cases` in `manifest.json`. All quoted convergence orders and values read from the frozen JSON/CSV.
- **`source_revision` vs `git_revision`.** `site/evidence.json` declares `source_revision=97e862b30e176b8fa1f223abef9adfef78d4cfc3`. This **is** internally consistent: every shipped source file tested hashes to its content at `97e862b` (e.g. `examples/plot_fabric_results.py` = `ed4b81bd…69128`, `moose_app/include/utils/FabricLaw.h` = `761334c6…497961`, `moose_app/src/materials/FabricMaterial.C` = `9abcfab6…030c2` all equal `git show 97e862b:<path>`), and all 47 `scientific-snapshot.json` digests resolve. The separate FE-run `git_revision` field is a different fact recorded at a different time; for the 19 fabric runs it is **not** consistent with the evidence it describes (R2-C1). No digest declared in either record fails to resolve.
- **Licensing/provenance.** `LICENSE` (Apache-2.0) is byte-identical in the repo, in the supplement, and to the digest declared in the supplement manifest (`cfc7749b…3d30`); `licenses/CC-BY-4.0.txt` is present; `LICENSES.md` matches the supplement copy. `build/conformal/verification.json` and `site/reports/conformal-verification.json`, and `build/fabric/fabric-verification.json` and `site/reports/fabric-verification.json`, are byte-identical pairs respectively.
- **Citations.** 36 `\cite*` keys in the text, 36 entries in `references.bib`; no cited-but-absent key and no uncited entry. Spot checks of attribution (Biot 1955, Biot–Willis 1957, Thompson–Willis 1991, de Buhan 1998, Gajo 2010, Foster–Xu 2025, Drumheller 2000, Gaston 2009 MOOSE, Walker 2023 for the Mandel series, Zha 1996 forsterite, Putnis/Altree-Williams dissolution–reprecipitation, Cowin/Turner-Moore fabric sequence) are supported by the entry titles/journals; the companion manuscript is correctly recorded as unpublished with a pinned source URL and inspected commit. Only the `braun2020` key/year mismatch (R2-C6) was found.

### Verdict rationale

The numerical content is fully reproducible from the frozen artifacts: every one of the 32 recomputed quantities matches the manuscript, and the digest audit is clean across ~1,608 declared digests, including a byte-identical PDF attachment. The required changes concern **provenance records and file naming**, not scientific results: R2-C1 removes a genuine reproducibility gap on the pore-fabric evidence the manuscript presents (recorded revision that cannot contain the fabric sources, plus absent source/executable digests), and R2-C2 corrects two payload files declared as JSON. Neither affects any quoted value or declared digest. This warrants a minor revision.

VERDICT: MINOR REVISION

# SIMULATED AI PEER REVIEW — Reviewer 2

**Emphasis:** numerical verification and source fidelity.
**Repository:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
**Snapshot (read-only):** `.agent-runtime/review-snapshots/round-31`
**Declared SNAPSHOT_ID:** `09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84`
**Report path:** `reviews/round-31/reviewer-2.md`

This report is the output of a *simulated* AI peer-review round. It is not a
journal decision and confers no acceptance. All reads were made against the
frozen snapshot; no manuscript file was edited. The held numerical suites
(`validation/`, `examples/verify_*.py`) were **not** run; every quoted number
was recomputed from the frozen CSV/JSON/Exodus artifacts.

---

## 1. Mandatory first checks

### Check 1 — snapshot identity

Command:

```
sha256sum .agent-runtime/review-snapshots/round-31/source-manifest.json
```

Result:

```
09a606a73d9f475ec624785b7b2a8483f989f2270eca7aeb405015205d113c84  .../round-31/source-manifest.json
```

`SNAPSHOT_ID` file content is the same string. **PASS** — matches the declared
`SNAPSHOT_ID` exactly.

### Check 2 — re-hash every listed file on a temporary copy

The snapshot was copied out first and never written in place:

```
rm -rf /tmp/r31-review-r2 && mkdir -p /tmp/r31-review-r2 \
  && cp -r <snapshot>/round-31 /tmp/r31-review-r2/snap \
  && chmod -R u+w /tmp/r31-review-r2/snap
```

Every entry of `source-manifest.json` was re-hashed under `/tmp/r31-review-r2/snap`
(Python `hashlib.sha256`, 1 MiB chunks), then every file on disk was walked and
compared against the manifest keys.

| Result | Count |
| --- | --- |
| entries in `source-manifest.json` | 606 |
| entries re-hashed | 605 |
| entries skipped | 1 |
| hash mismatches | **0** |
| listed files missing on disk | **0** |
| files present but not listed | **0** |

The one skipped entry is `reviews/README.md`. It was skipped deliberately so
that no file under `reviews/` was opened (see independence declaration). Hashing
that single entry is the only manifest check I did not perform; every other
entry, including all `fe-evidence/` binary Exodus files and the supplement
archive, verified byte-for-byte. **PASS** with that one stated exception.

### Check 3 — independence declaration

- I did **not** open any file under `reviews/` — not `README.md`, not
  `LAUNCH-STATE.md`, not any other reviewer report or response. The only
  `reviews/` interaction was (a) skipping the `reviews/README.md` manifest
  entry as described above, and (b) `mkdir -p`/writing this report. No
  accidental exposure occurred.
- I did **not** read any other `.agent-runtime/review-snapshots/round-*`
  directory. I ran `ls -la .agent-runtime/review-snapshots/` once, which lists
  sibling `round-*` **directory names** only (no file contents); no other round
  was entered or read. Reported here for completeness.
- Disclosure: to verify the declared `git_revision` in the FE provenance
  records I ran read-only `git cat-file` / `git ls-tree` / `git show` against
  the *repository object database* (the snapshot contains no `.git`). No
  working-tree manuscript file was opened or modified for this; only the
  content of the declared commit `b6d7272…` was read.

---

## 2. Numerical verification — every number the manuscript quotes

All values below were recomputed from the frozen artifacts. "Manuscript"
locations are file + line.

| # | Manuscript value | Location | Source artifact | Recomputed | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | reference Biot components `0.7000`, `0.7583`, `0.7917` | `sections/experiments.tex:25` | `build/conformal/experiments.json` — `B0 = I − C^d:(C_s)^{-1}:I` | `0.7`, `0.758333…`, `0.791667…` | **AGREE** |
| 2 | isotropic mineral shear modulus `16.8 K_*` = mean of five deviatoric modes ÷ 2 | `sections/experiments.tex:29` | `examples/conformal_model.py:78` `mu_average = trace(P_dev·C_s)/10` | `trace(P_dev·C_s)=168`; `168/5/2 = 16.8` | **AGREE** |
| 3 | conformal suite "186 named checks" | `sections/experiments.tex:180` | `build/conformal/verification.json` `checks_passed`, `len(checks)` | `186`, `186` | **AGREE** |
| 4 | "65 per-state identities (five states × thirteen identities)" | `sections/experiments.tex:180-182` | same — `legacy_state{0..4}_*` keys | 5 states × 13 = `65` (plus 121 non-state = 186) | **AGREE** |
| 5 | largest constitutive identity error `2.5e-9` | `sections/experiments.tex:186` | same — `max_constitutive_identity_error` | `2.454989…e-09` | **AGREE** |
| 6 | spherical-gauge suite "273 finite states across 13 mineral stiffnesses" | `sections/experiments.tex:191` | `build/weighted-stress/tensor-verification.json` | `total_states=273`, `materials=13`, `states_per_material=21` (13×21=273) | **AGREE** |
| 7 | FE reference `G=0.75`, `α=0.6`, storage `17/80` | `sections/finite_elements.tex:162-166` | `site/reports/mandel-reference.json`; recompute `S_s=(1−φ)/K_f + φ/K_s(1−K/(φK_s))` | `G=0.75`, `α=0.6`, `0.0125+0.2=0.2125=17/80` | **AGREE** |
| 8 | FE inputs φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, k/μ_f=1.5 | `sections/finite_elements.tex:159-163` | `fe-evidence/runs/linear_time_0.001/input.i` `mineral_stiffness`, `solid_fraction`, `drained_bulk`, `fluid_bulk`, `mobility` | `K_s=2.5`, `μ_s=5/6` (Mandel `C44=5/3`), rest exact | **AGREE** |
| 9 | MMS pressure orders `2.00`, `2.00` | `sections/finite_elements.tex:203` | `fe-evidence/mms-convergence.json` `space.orders.p_l2.naive_orders` | `1.9966`, `2.0008` | **AGREE** |
| 10 | MMS `u_x` orders `2.99`, `2.96` | same | `…ux_l2.naive_orders` | `2.9917`, `2.9585` | **AGREE** |
| 11 | MMS `u_y` orders `3.00`, `2.96` | same | `…uy_l2.naive_orders` | `2.9983`, `2.9600` | **AGREE** |
| 12 | temporal orders "between 0.98 and 1.40" | `sections/finite_elements.tex:205-206` | `…time.*.orders.*.difference_orders` | min `0.9783`, max `1.3969` | **AGREE** |
| 13 | linear step refinement ratio `1.94`; errors `3.7e-3`, `7.1e-3` | `sections/finite_elements.tex:210`, `main.tex:589` | `figures/fe_mandel_refinement.csv` + `linear_time_0.001/0.002` `analysis.json` | `0.00365796`, `0.00710392`, ratio `1.94205` | **AGREE** |
| 14 | pressure discrepancy floors at `3.2e-3` | `sections/finite_elements.tex:214,233`, `main.tex:586` | `figures/fe_load_limit.csv` `nonlinear_load_0.0001` | `0.003220920` | **AGREE** |
| 15 | fabric reconstruction differs by `2.2e-16` | `sections/finite_elements.tex:271` | `build/fabric/fabric-verification.json` `tensor_checks.H_reconstruction_max_abs_diff` | `2.22045e-16` | **AGREE** |
| 16 | `det H − 1 = −3.3e-16`, eigenvalues `h^-2,h,h` | `sections/finite_elements.tex:271` | same `H_det_minus_one`, `H_eigenvalues` | `-3.33067e-16`; `0.999286,1.000357,1.000357` | **AGREE** |
| 17 | `‖D:e3‖ = 1.6e-16`, `D:e6 = 0` | `sections/finite_elements.tex:273-274` | same `D4_e3_norm`, `D4_e6_norm` | `1.58231e-16`, `0.0` | **AGREE** |
| 18 | rotation invariance `2.5e-16` | `sections/finite_elements.tex:275` | same `rotation_invariance_norm` | `2.49654e-16` | **AGREE** |
| 19 | NumPy re-implementation worst diff `4.9e-15` | `sections/finite_elements.tex:279` | same `worst_probe_abs_diff` | `4.88498e-15` | **AGREE** |
| 20 | volume-only limit reproduces conformal to `1.9e-14` | `sections/finite_elements.tex:287` | `conformal_cross_check.*.abs_diff` max | `1.87420e-14` | **AGREE** |
| 21 | coupled peaks `4.36e-5` (0°), `4.99e-5` (45°), `5.52e-5` (90°), `3.62e-5` uncoupled; peak = final state | `sections/finite_elements.tex:312-315` | `fabric_mandel_coup_a{0,45,90}/analysis.json`, `fabric_mandel_iso`; `figures/fe_fabric_mandel_peak.csv` | `4.362759e-5`, `4.990085e-5`, `5.521105e-5`, `3.616393e-5`; history monotonically rises to t=0.003 | **AGREE** |
| 22 | refined contour peaks `3.61e-5` iso, `4.35`, `4.97`, `5.50e-5` | `sections/finite_elements.tex:326-328` | `figures/fe_fabric_contours.csv` + recomputed from `fe-evidence/runs/fabric_contour_*/solution.e` (nodal `p`) | `3.606194e-5`, `4.349137e-5`, `4.973659e-5`, `5.503135e-5` | **AGREE** |
| 23 | displacement-magnitude peaks `5.18e-5`, `5.14e-5`, `2.38e-5`, `5.26e-5` | `sections/finite_elements.tex:331-333` | `figures/fe_fabric_contours.csv` + recomputed `max‖(ux,uy)‖` from the Exodus files | `5.182640e-5`, `5.137155e-5`, `2.381836e-5`, `5.258692e-5` | **AGREE** |
| 24 | eleven evenly spaced field snapshots; common final time | `sections/finite_elements.tex:322-324` | `solution.e` `time_whole` | 11 values, `0 … 0.003` | **AGREE** |
| 25 | sampling counts 121 pressure states, 161 γ, one-degree directions, 121 angles, 121 layer points | `sections/experiments.tex:110,133,150,170,193` | `build/conformal/{pressure,shear,directional,rotation,constrained_layer}.csv` row counts | 242=2×121, 322=2×161, 1083=3×361, 242=2×121, 242=2×121 | **AGREE** |
| 26 | diffusion figure "six recorded times" | `sections/finite_elements.tex:339` | `figures/fe_fabric_diffusion.csv` | 6 rows per case (2 cases) | **AGREE** |
| 27 | `0 < K < φ_s0 K_s` with `K_s=28K_*`, `φ_s0=0.6` | `sections/experiments.tex:24` | arithmetic | `φ_s0 K_s = 16.8 > 7` | **AGREE** |

**Disagreements found among recomputed manuscript numbers: none.** Every number
quoted from the frozen artifacts reproduces to the stated precision.

---

## 3. Declared-digest audit

| Declared digest surface | Entries | Result |
| --- | --- | --- |
| snapshot `source-manifest.json` | 606 | 605/605 re-hash OK, 0 mismatch, 0 missing, 0 unlisted (1 entry skipped: `reviews/README.md`) |
| supplement `manifest.json` (in `build/anisotropic-biot-2026-09-20-v2.zip`) | 68 | 68/68 OK, 0 mismatch, 0 missing, 0 extras |
| supplement archive digest | 1 | `build/anisotropic-biot-2026-09-20-v2.zip` = `9643b64b…16`, matches `source-manifest.json:77` |
| `fe-evidence/manifest.json` | 317 | 317/317 OK (digests and `bytes`), 0 missing |
| `site/scientific-snapshot.json` | 47 | 47/47 OK |
| `site/evidence.json` `artifacts` | 41 | 41/41 OK |
| figure plot manifests — `figures/fe-verification-plot-manifest.json`, `figures/fabric-plot-manifest.json` | inputs+outputs | all OK |
| figure plot manifest — `figures/fe_fabric_contours-plot-manifest.json` | inputs+outputs | **4 input digests MISMATCH** (see R2-C1) |
| FE run provenance records | 19 | source/git/input all OK (see below) |

### 3.1 FE run provenance (`fe-evidence/runs/*/provenance.json`)

Note on the count: **19** records carry the full fabric provenance schema
(`git_revision`, `application_sha256`, `input_deck`, …). **18** directories are
named `fabric_*`; the nineteenth is `conformal_probe_ref`, the paired conformal
reference deck. `fe-evidence/README.md` describes exactly this pairing, and
`build/fabric/…`/`figures/fabric-plot-manifest.json` also list it, so this is a
naming convention, not a defect. All 19 were verified.

- **`git_revision` contains the fabric sources.** All 19 declare
  `b6d72721414a0c09aa6492465acd3a4c8d07e31b`. `git cat-file -t` → `commit`;
  `git ls-tree -r <rev>` returns `moose_app/include/utils/FabricLaw.h`,
  `moose_app/include/materials/FabricMaterial.h`,
  `moose_app/src/materials/FabricMaterial.C`. **PASS.**
- **`source_sha256` matches the shipped source at that revision.** 513 values
  (3 sources × 19 records — deduplicated per record) recomputed with
  `git show <rev>:<path> | sha256`, compared to each record. **513 checked,
  0 failures.**
- **`input_sha256` matches the shipped input deck.** All 19 compared against
  `moose_app/inputs/<input_deck>`; **19/19 OK**.
- **`binary_sha256` vs compiled-application digest.** The compiled binary is
  *not shipped* (`fe-evidence/README.md` states this; no `*-opt`/`.so` exists in
  the snapshot). What can be verified is internal consistency: `binary_sha256`
  equals `application_sha256` for all 19, with the single value
  `ff0272fc…d31e`; the paired `application_library_sha256` is `cdd1ebf6…6fbd`
  for all 19. **PASS** as far as the snapshot permits; a byte-level check of the
  binary digest is not possible from the snapshot alone (see R2-O2).

### 3.2 `build/weighted-stress/derivation-scan.txt` and `display-scan.txt`

- **Not declared as JSON.** Both are declared only under their `.txt` names:
  `source-manifest.json:106-107`. No JSON key (`…scan.json`) exists anywhere in
  the snapshot. **PASS.**
- **Shipped in the supplement under a non-JSON name.** `unzip -l
  build/anisotropic-biot-2026-09-20-v2.zip` lists
  `build/weighted-stress/derivation-scan.txt` (9876 B) and
  `build/weighted-stress/display-scan.txt` (673 B), and the supplement
  `manifest.json` hashes both under those names. **PASS.**
- **No foreign absolute host paths.** `grep -nE '(/home/|/Users/|/tmp/|/root/|/mnt/|[A-Za-z]:\\\\)'`
  over both files returns nothing; the only path-like tokens are
  repo-relative (`main.tex`, `sections/limits.tex`, …). **PASS.**

### 3.3 `provenance/manuscript-export.json` path resolution

The file declares **13** paths (`.latexmkrc`, `AGENTS.md`, `VISION.md`,
`README.md`, `LICENSES.md`, `Makefile`, `main.tex`, `references.bib`,
`references/`, `provenance/`, `agent_environment/`, `agent_workflows/`,
`tools/`). All **13 resolve inside the snapshot** (9 files, 4 directories).
**PASS.** The review brief refers to "the four paths"; the artifact declares
thirteen, all of which resolve. If the intent was that four previously-failing
paths now resolve, that is consistent — there are no unresolved paths. Recorded
as R2-O3 so the count discrepancy is not mistaken for a failure.

---

## 4. REQUIRED changes

### R2-C1 — `figures/fe_fabric_contours-plot-manifest.json` records stale `input_sha256` for the four contour Exodus files

**Location:** `figures/fe_fabric_contours-plot-manifest.json:46-49`.

The declared digests do not match the shipped `solution.e` bytes, nor the two
other manifests that hash the same files:

| File | plot-manifest declares | shipped bytes = `source-manifest.json` = supplement manifest |
| --- | --- | --- |
| `fe-evidence/runs/fabric_contour_iso/solution.e` | `7b79a565…80ac9` | `0f281f7a…2b9fd` |
| `fe-evidence/runs/fabric_contour_a0/solution.e` | `8fba1339…72221` | `ca9ad477…6e74d` |
| `fe-evidence/runs/fabric_contour_a45/solution.e` | `9dd70793…99478` | `36c8fb10…bd323` |
| `fe-evidence/runs/fabric_contour_a90/solution.e` | `f8f5f361…fe1e6` | `604d9fcc…85dfc` |

`source-manifest.json`, the supplement `manifest.json`, and the shipped bytes
all agree with each other; only this plot manifest disagrees, so it is the stale
record. The orphaned digests appear nowhere else in the snapshot
(`grep -rl` finds them only in this manifest). The figure's own `output_sha256`
entries (`fe_fabric_contours.csv/pdf/png`, `fe_fabric_diffusion.*`) *do* match
the shipped files, and the plotted values reproduce from the shipped `.e`
(Section 2, items 22-23) — so the *figure content* is sound; only the recorded
**input identity** is wrong. Because `site/README.md` states "the builder
rejects stale hashes", a stale declared digest in a shipped manifest is a
provenance-integrity defect regardless of whether any number changes.

**Fix:** re-record `input_sha256` for those four `solution.e` files from the
shipped bytes, or regenerate the manifest from the same run set that produced
the shipped Exodus files.

---

## 5. OPTIONAL notes

### R2-O1 — shipped Exodus files embed a foreign absolute host path in the `title` attribute

The four contour decks carry a transient absolute host path in the Exodus
`title` global attribute, e.g. `fe-evidence/runs/fabric_contour_iso/solution.e`
→ `/tmp/tmpzwc21mkj/solution.e` (also `tmpc9wg6ihp`, `tmp6l7inktx`, `tmpeo3zddn3`).
The two `*-scan.txt` files are clean (Section 3.2); this is a separate class of
shipped artifact. It affects no quoted number and no digest, but it is
foreign-host-path leakage in a published artifact. Setting a stable
`Outputs/file_base`/`title` before export removes it. Optional.

### R2-O2 — `binary_sha256` cannot be byte-verified from the snapshot

The compiled application is intentionally not shipped, so `binary_sha256`
`ff0272fc…d31e` is only internally consistent with `application_sha256`
(all 19 records) and is documented as such in `fe-evidence/README.md`. If a
future round wants this digest independently checkable, publishing the digest
of the build toolchain artifact (or a reproducibility note naming the exact
build command) would close the loop. Not required.

### R2-O3 — count wording in `provenance/manuscript-export.json`

The artifact declares 13 paths (all resolving) rather than the "four" referenced
in the review brief (Section 3.3). No action needed on the artifact; noting so
the discrepancy is not read as a partial failure.

---

## 6. Summary

- Snapshot identity and full re-hash: **clean** (605/605, 1 entry deliberately
  skipped for independence).
- Every number the manuscript quotes from the frozen artifacts: **reproduces** —
  27 checks, 0 disagreements.
- Supplement, `fe-evidence`, site, and plot manifests: **verify**, except the
  four stale `input_sha256` entries in `figures/fe_fabric_contours-plot-manifest.json`
  (R2-C1), which affect no figure value or scientific claim.
- 19 FE provenance records: declared revision contains the fabric sources,
  513/513 `source_sha256` and 19/19 `input_sha256` verify; `binary_sha256` is
  internally consistent but not byte-checkable (R2-O2).

The numerical and source-fidelity record is strong. One provenance manifest
carries stale input digests and must be corrected (R2-C1); the remaining items
are optional hygiene.

VERDICT: MINOR REVISION

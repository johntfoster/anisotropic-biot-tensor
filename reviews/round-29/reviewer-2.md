# SIMULATED AI PEER REVIEW — Reviewer 2 (numerical verification and source fidelity)

**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Snapshot reviewed:** `.agent-runtime/review-snapshots/round-29` (frozen; never the working tree)
**Declared SNAPSHOT_ID:** `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`
**Label:** SIMULATED AI PEER REVIEW — not a journal submission and not a journal decision.

## Mandatory checks (exact results)

1. **SNAPSHOT_ID check.**
   `sha256sum .agent-runtime/review-snapshots/round-29/source-manifest.json`
   = `8aff33630cf27ac2727729471b38529c10f23edb1d6a5f90f2553c5b7f8726d7`
   → **matches the declared SNAPSHOT_ID exactly.** (The snapshot's own
   `SNAPSHOT_ID` file contains the same string.)

2. **Full manifest re-hash** (performed on a `cp -r` copy at `/tmp/r29r2/snap`,
   never inside the snapshot):
   - Entries listed in `source-manifest.json`: **592**
   - Re-hashed and **matching: 592**
   - **Hash mismatches: 0**
   - **Listed but missing: 0**
   - Present but **not listed: 2** — `SNAPSHOT_ID` and `source-manifest.json`
     (self-referential; expected).

   **Hash-check result: PASS — 592/592 entries verified against the manifest, 0 mismatches, 0 missing.**

All other verification below was done from the frozen copy only. I did not read
`reviews/`, any prior-round verdict, any other `round-*` directory, or another
reviewer's report; I ran no `validation/` suite, no `examples/verify_*.py`, and
no MOOSE executable.

---

## REQUIRED CHANGES

### R2-C1 — Declared input digest in `figures/fe-verification-plot-manifest.json` does not resolve

**Location:** `figures/fe-verification-plot-manifest.json`, field
`input_sha256["fe-evidence/mms-convergence.json"]`.

**At issue:**

```
declared: 87e1d95bb87b4535e5e5389d8d19bc4d5ca97d0a38e95ebc703bff6c5b977887
actual  : de2ca677a47f3c7745a9cc748ad7be768e4884b7b6934878df853036508419a0
```

The actual digest of the frozen `fe-evidence/mms-convergence.json` is
`de2ca677…419a0`. That same value is what `fe-evidence/manifest.json` declares
(`files[].path = "mms-convergence.json"`, `sha256 = de2ca677…419a0`), so the
evidence-tree manifest is self-consistent and the plot manifest is the outlier.
Corroborating the staleness, this manifest's `versions` block records
`python 3.14.0 / numpy 2.4.2` while `figures/fabric-plot-manifest.json` and
`figures/fe_fabric_contours-plot-manifest.json` record `3.10.12 / 2.2.6`,
i.e. the manifest was written against a different (earlier) build of the file.

**Scope:** every other digest in all three figure manifests resolves (22 + 10 +
11 entries checked), all 317 `fe-evidence/manifest.json` payload digests resolve,
and no manuscript number depends on this field. The defect is one stale
declared digest — a broken digest in a machine-readable provenance artifact.

**Required fix:** regenerate (or refresh) the manifest so that
`input_sha256["fe-evidence/mms-convergence.json"]` equals the frozen file's
digest, and reconcile the `versions` block with the environment that produced
the shipped `mms-convergence.json`.

---

## OPTIONAL NOTES

### R2-N1 — Figure caption understates how many temporal orders exceed unity
**Locations:** `sections/finite_elements.tex:226` ("the values include one
above unity"); `figures/fe-verification-plot-manifest.json:16` (same caption);
generated at `examples/plot_fe_verification.py:171`.
The panel plots 3 fields × 3 meshes = 9 successive-difference orders. From
`fe-evidence/mms-convergence.json` the values are
nx=16: ux 1.0932, uy 0.9783, p 1.0152; nx=32: ux 1.3969, uy 1.0183, p 1.1252;
nx=64: ux 1.3964, uy 1.0762, p 1.2519 — **eight of the nine exceed unity**, only
`uy` at nx=16 lies below. The main text (`main.tex:571`) states this correctly
("including values above one"). Suggest "the values include values above unity"
in the caption for consistency. No number changes.

### R2-N2 — `tensor_checks.fabric_angle_deg` is a rotation angle, not the fabric orientation
**Location:** `build/fabric/fabric-verification.json`, `tensor_checks`
(`"fabric_angle_deg": 30.0` with `"reconstruction_case": "fabric_probe_coup_a45"`).
The `30.0` is the superposed-rotation angle of the invariance test
(`phi = np.radians(30.0)`, `examples/verify_fabric.py:246`), whereas the
reconstruction case is the 45° probe (`mt = [cos45°, sin45°, 0]`, verified by
`H_reconstruction_max_abs_diff = 2.22e-16`). The field name invites misreading;
a name such as `rotation_angle_deg` would be unambiguous. Not quoted in the
manuscript.

### R2-N3 — Base decks record default fabric parameters; overrides live in provenance
**Location:** e.g. `fe-evidence/runs/fabric_probe_coup_a45/input.i:209-210`
(`fabric_coupling = 0`, `fabric_angle = 0`), while
`fe-evidence/runs/fabric_probe_coup_a45/provenance.json` records
`command_overrides = ["Materials/law/fabric_angle=45",
"Materials/law/fabric_coupling=0.4"]`. This is documented and correct
(`tools/rerun_fabric_decks.py` lists deck+overrides per case), and the recorded
`solution.csv` does match the 45°/0.4 state (independent re-implementation diff
3.7e-15). A one-line pointer in `fe-evidence/README.md` from `input.i` to
`command_overrides` would prevent a reader from diffing the deck alone.

### R2-N4 — Mixed path conventions in `source_sha256` records
`build/conformal/experiments.json` uses bare basenames
(`"conformal_model.py"`, `"conformal_experiments.py"`; both resolve under
`examples/`), whereas `build/conformal/verification.json` uses repo-relative
paths (`"examples/conformal_model.py"`). Both resolve and match; a single
convention would make automated resolution unambiguous.

### R2-N5 — `site/evidence.json` names the scientific snapshot without a resolvable reference
`site/evidence.json` sets `provenance.scientific_snapshot = "scientific-snapshot"`
(a label) rather than a path or digest that resolves to
`site/scientific-snapshot.json`; the sibling 41 `artifacts[]` entries do carry
resolving `path`+`sha256`, so the convention already exists.

---

## Assessment of numerical-verification and source-fidelity quality

**Overall: strong, with one bookkeeping defect.** The frozen snapshot is
internally coherent to an unusual degree for a working draft. The full manifest
re-hashes cleanly (592/592), the numerical supplement is genuinely
self-contained and its payload manifest verifies, the PDF's embedded attachment
extracts byte-identically to the on-disk archive, and **every number I could
recompute from frozen artifacts reproduced**. Verification claims in the
manuscript are, importantly, scoped honestly: the MMS orders are stated as
measurements with a mesh–step cross term, the temporal orders are explicitly not
asserted above one, and the finite-load/rotated/partial-drainage/ pore-fabric
runs are labelled demonstrations rather than quantitative verification or
experimental validation.

**Supplement and embedding.** `build/anisotropic-biot-2026-09-20-v2.zip` has
sha256 `fa8c07a2…0146c` (matches the task's expected digest), 69 entries, the
expected 69-file count, and declares version `anisotropic-biot-2026-09-20-v2`, a
68-entry payload-hash manifest (`manifest.json` → `sha256{}`, all 68 digests
resolve), a dependency record (`examples/requirements.txt` plus recorded
versions in the reports), and a reproduction order in `README.md` (verification
before figure generation). I confirmed the documented commands' inputs are all
present in the archive (e.g. `verify_fabric.py` reads only the shipped
`fe-evidence/runs/*/solution.csv`; `plot_fabric_contours.py` reads the shipped
`solution.e`+`solution.csv`). `pdfdetach -saveall build/main.pdf` extracts
`anisotropic-biot-2026-09-20-v2.zip` with sha256 `fa8c07a2…0146c`, byte-identical
to the on-disk archive (`cmp` clean). Documents are 34 pages.

**FE evidence tree.** `fe-evidence/manifest.json` lists 57 cases and all 317
payload digests resolve with correct byte counts; each of the 57 run
directories carries `input.i`, `provenance.json`, `run.log`, `solution.csv`,
`analysis.json`; per-run `provenance.json` source digests resolve for 456/456
entries with 0 mismatches and 0 unresolved paths. Recorded
executable/library/git digests are present (e.g. `application_sha256`,
`application_library_sha256`, `git_revision = ab46ebe4…`, consistent with
`site/evidence.json` `provenance.source_revision`). Quoted convergence orders,
the step-refinement ratio, the finite-load floor, the 273-state/13-stiffness
gauge suite, the 186-check conformal suite, the fabric-reconstruction bounds,
and all peak-pressure/displacement values correspond exactly to the frozen
JSON/CSV.

**Citation fidelity.** All 36 `\cite*` keys used in `main.tex`, `sections/*.tex`,
`build/weighted-stress/*.tex` and `provenance/*.tex` resolve to
`references.bib`, and all 36 bib entries are cited (no orphans, no missing
entries). Every claim attributed to a cited work is a characterization of that
work's subject consistent with its title/scope; no citation is used to support a
claim outside its stated content and no uncited attribution appears in the
numerical sections. Spot checks against publisher records confirmed
`fosterxu2025` (JMPS **Vol. 204**, 2025, Article **106263** — the bib value is
correct) and `moesencardosocowin2012` (Mech. Mater. **54**:70–83, 2012);
`walker2023poroelasticity` (GJI 235(3):2442–2475, doi 10.1093/gji/ggad370) is
independently corroborated by the repository's own reference implementation
(`validation/mandel_reference.py` docstring cites the same DOI, Appendix D).
Two further metadata spot checks could not be completed because the search
provider returned a quota error, not because of any defect in the entries.

**Provenance and licensing.** `provenance/ai-use.yml`, `provenance/AI_USE.md`
and `provenance/ai_use_statement.tex` are mutually consistent (identical
tool/model lists and disclosure text). `LICENSES.md`/`LICENSE`/`licenses/CC-BY-4.0.txt`
are coherent (Apache-2.0 code, CC BY 4.0 manuscripts, third-party rights
reserved), and both are shipped inside the supplement with digests that resolve.
Companion-site manifests are internally consistent: all 41 `site/evidence.json`
artifacts and all 47 `site/scientific-snapshot.json` files resolve by digest
(41/41, 47/47), site artifact ids referenced by categories/cases/figures are all
defined, and the reported site-level checks reproduce (38 Mandel self-checks with
central overshoot 5.4659% at t = 0.01516535; 110 fluid-coupling checks with max
scaled error 8.09e-09; C++-vs-Python agreement 6.4e-14 over 41 states).

### Table — every number quoted in the manuscript, recomputed from frozen artifacts

| # | Location (file:line) | Quoted value | Recomputed value | Frozen source | Status |
|---|---|---|---|---|---|
| 1 | `sections/experiments.tex:25` | reference Biot components 0.7000, 0.7583, 0.7917 | 0.7, 0.7583333333333333, 0.7916666666666667 | `build/conformal/experiments.json` `highlights.reference_B` | ✔ |
| 2 | `sections/experiments.tex:29` | isotropic mineral shear modulus 16.8 K⋆ = ½·mean of five deviatoric modes | 16.8 (modes sum 168; 168/5/2) | `experiments.json` `isotropic_comparison.mu` | ✔ |
| 3 | `sections/experiments.tex:180` | 186 named checks | 186 | `build/conformal/verification.json` `checks_passed` | ✔ |
| 4 | `sections/experiments.tex:180-182` | 65 per-state identities (5 states × 13) | 65 (5 `legacy_states` × 13 keys each) | `verification.json` `checks`, `legacy_states` | ✔ |
| 5 | `sections/experiments.tex:186` | largest constitutive identity error 2.5e-9 | 2.4549890331732928e-09 | `verification.json` `max_constitutive_identity_error` | ✔ |
| 6 | `sections/experiments.tex:191` | 273 finite states across 13 stiffnesses | 273 states, 13 materials | `build/weighted-stress/tensor-verification.json` | ✔ |
| 7 | `sections/finite_elements.tex:200-203` params | φ_s0 0.9, K_s 2.5, μ_s 5/6, K 1, K_f 8, ρ̄_f0 1, k/μ_f 1.5 | same | `validation/mandel_reference.py` `MandelParameters` | ✔ |
| 8 | `sections/finite_elements.tex` G=0.75 | drained shear modulus 0.75 | φ_s0·μ_s = 0.9·5/6 = 0.75 | `mandel_reference.py` `G=0.75` | ✔ |
| 9 | `sections/finite_elements.tex` Biot 0.6 | reference Biot coefficient 0.6 | 1−K/K_s = 1−1/2.5 = 0.6 | `mandel_reference.py` `alpha=0.6` | ✔ |
| 10 | `sections/finite_elements.tex` storage 17/80 | total storage 17/80 | (1−φ_s0)/K_f+S_s = 0.0125+0.2 = 0.2125 = 17/80 | `M=80/17`; `experiments.json` `Ss` form | ✔ |
| 11 | `sections/finite_elements.tex:204` | MMS orders p 2.00/2.00, u_x 2.99/2.96, u_y 3.00/2.96 | p 1.9966/2.0008; ux 2.9917/2.9585; uy 2.9983/2.9600 | `fe-evidence/mms-convergence.json` `space.orders[*].naive_orders` | ✔ |
| 12 | `main.tex:571` | temporal orders 0.98–1.40 at nx=16/32/64 | min 0.9783 (uy,nx16), max 1.3969 (ux,nx32) | `mms-convergence.json` `time.*.difference_orders` | ✔ |
| 13 | `sections/finite_elements.tex:209`; `main.tex:569` | step-refinement ratio 1.94 | 0.0071039215708695895 / 0.003657958974355574 = 1.9421 | `figures/fe_mandel_refinement.csv`; `linear_time_*` analyses | ✔ |
| 14 | `main.tex:568` | 3.7e-3 at dt=1e-3 | 0.003657958974355574 | `linear_time_0.001/analysis.json` `pressure_max_normalized` | ✔ |
| 15 | `main.tex:568` | 7.1e-3 at dt=2e-3 | 0.0071039215708695895 | `linear_time_0.002/analysis.json` | ✔ |
| 16 | `sections/finite_elements.tex:213,232`; `main.tex:566` | finite-load pressure floor 3.2e-3 (nx=20, dt=1e-3) | 0.003220919735602341 (nx=20, dt=0.001, load=1e-4) | `nonlinear_load_0.0001/analysis.json` | ✔ |
| 17 | `sections/finite_elements.tex:314` | peak centre pressure 4.36e-5 (0°) | 4.3627593400865e-05 | `fabric_mandel_coup_a0/analysis.json` | ✔ |
| 18 | `sections/finite_elements.tex:315` | 4.99e-5 (45°) | 4.9900848305106e-05 | `fabric_mandel_coup_a45/analysis.json` | ✔ |
| 19 | `sections/finite_elements.tex:315` | 5.52e-5 (90°) | 5.521105069019e-05 | `fabric_mandel_coup_a90/analysis.json` | ✔ |
| 20 | `sections/finite_elements.tex:316` | 3.62e-5 (uncoupled) | 3.6163929824772e-05 | `fabric_mandel_iso/analysis.json` | ✔ |
| 21 | `sections/finite_elements.tex:312-313` | each peak coincides with final recorded state | peak == final (t=0.003) in all 4 cases | `figures/fe_fabric_mandel_peak.csv` | ✔ |
| 22 | `sections/finite_elements.tex:324` | eleven evenly spaced field snapshots | 11 times, 0→0.003 uniform | `fabric_contour_*/solution.e` `time_whole` | ✔ |
| 23 | `sections/finite_elements.tex:328` | refined peak pressure 3.61e-5 (iso) | 3.606194309585106e-05 | `figures/fe_fabric_contours.csv` `p_max` | ✔ |
| 24 | `sections/finite_elements.tex:329` | 4.35e-5 (0°), 4.97e-5 (45°), 5.50e-5 (90°) | 4.3491366180031454e-05, 4.973659107895197e-05, 5.503135423750668e-05 | `figures/fe_fabric_contours.csv` | ✔ |
| 25 | `sections/finite_elements.tex:333-334` | u-magnitude peaks 5.18e-5, 5.14e-5, 2.38e-5, 5.26e-5 | 5.1826395396202306e-05, 5.13715515334801e-05, 2.381836351578327e-05, 5.258692042529596e-05 | `figures/fe_fabric_contours.csv` `u_mag_max` | ✔ |
| 26 | `sections/finite_elements.tex:329-331` | max on X₁=0 symmetry line; p→0 at drained edge X₁=1 | p_max_x = 0.0 all cases; p_min ≈ 0 | `fe_fabric_contours.csv` | ✔ |
| 27 | `sections/finite_elements.tex:270` | reconstruction diff 2.2e-16 | 2.220446049250313e-16 | `fabric-verification.json` `tensor_checks` | ✔ |
| 28 | `sections/finite_elements.tex:270` | det H − 1 = −3.3e-16 | −3.3306690738754696e-16 | `fabric-verification.json` `tensor_checks` | ✔ |
| 29 | `sections/finite_elements.tex:272` | ‖D:e₃‖ = 1.6e-16, D:e₆ = 0 | 1.5823112613210482e-16, 0.0 | `fabric-verification.json` `tensor_checks` | ✔ |
| 30 | `sections/finite_elements.tex:274` | rotation invariance 2.5e-16 | 2.4965357070272594e-16 | `fabric-verification.json` `tensor_checks` | ✔ |
| 31 | `sections/finite_elements.tex:278` | NumPy re-implementation worst diff 4.9e-15 | 4.884981308350689e-15 | `fabric-verification.json` `worst_probe_abs_diff` | ✔ |
| 32 | `sections/finite_elements.tex:286` | volume-only limit vs conformal material 1.9e-14 | 1.8741952434453424e-14 | `fabric-verification.json` `conformal_cross_check` | ✔ |
| 33 | `site/evidence.json:14` (reports) | 38 Mandel self-checks, overshoot 5.4659% at t=0.01516535 | 38 checks; ratio 1.0546586069998425; t=0.015165352045764979 | `site/reports/mandel-reference.json` | ✔ |
| 34 | `site/evidence.json:20` (reports) | 110 checks, max scaled error 8.09e-09 | 110; 8.086725789002713e-09 | `site/reports/fluid-coupling-verification.json` | ✔ |
| 35 | `site/evidence.json:20` (reports) | C++ vs Python 6.4e-14 over 41 states | 6.394884621840902e-14, 41 states | `site/reports/cpp-python-constitutive.json` | ✔ |
| 36 | `main.tex` (data/code availability) | supplement self-contained, extractable via `pdfdetach` | extracts to sha256 `fa8c07a2…0146c` = on-disk archive | `build/main.pdf` attachment | ✔ |

**No quoted numerical value failed to reproduce.** The single required change
(R2-C1) is a declared-digest staleness in a generated plot manifest; it does not
alter any quoted number, figure value, or verification conclusion.

---

VERDICT: MINOR REVISION

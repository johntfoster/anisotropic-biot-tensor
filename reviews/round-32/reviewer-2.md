# SIMULATED AI PEER REVIEW — Reviewer 2 of 3 (numerical verification and source fidelity)

This is a simulated AI peer review. It is not journal peer review and confers no
acceptance. Verdict line at the end.

- **Snapshot reviewed:** `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-32` (read-only)
- **Declared SNAPSHOT_ID:** `2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44`
- **Emphasis:** numerical verification and source fidelity
- **Method:** every file was read from the frozen snapshot only. Nothing in the
  working tree was used as evidence. No file in the snapshot was modified; the
  only file I wrote is this report.
- **Boundaries honoured:** the held numerical suites (`validation/`,
  `examples/verify_*.py`) were **not** run. Numbers were recomputed from the
  frozen CSV/JSON artifacts and, for the field-location claims, read directly
  from the shipped Exodus files. `build/main.aux` is not shipped; equation
  numbering was not needed for any finding.

---

## 1. Mandatory first checks

### Check 1 — manifest digest equals the declared SNAPSHOT_ID

```
$ cd <snapshot> && sha256sum source-manifest.json
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44  source-manifest.json
$ cat SNAPSHOT_ID
2231ed2b9825fef48f1015be1b9b2a230c09bec424ad18a9ca8f32c5d0e8fa44
```

**Result: PASS.** `sha256(source-manifest.json)` equals the declared
SNAPSHOT_ID exactly, and `SNAPSHOT_ID` holds the identical string.
(`sha256(SNAPSHOT_ID)` = `0b4dfa162e86108388ecab70f065f3c8581a4fb38fec898279042beea349caa8`;
the `SNAPSHOT_ID` file is the identifier *contents*, so its own hash is not
expected to equal the ID.)

### Check 2 — re-hash every file listed in `source-manifest.json`

`source-manifest.json` is a flat mapping of repository-relative path → sha256.
A full independent walk (`os.walk`) plus re-hash of every listed entry gives:

| Measure | Result |
|---|---|
| manifest entry count | **608** |
| entries re-hashed | **608** |
| hash mismatches | **0** |
| listed files missing on disk | **0** |
| files present but unlisted | **2** — `SNAPSHOT_ID`, `source-manifest.json` |
| total files on disk | **610** |

**Result: PASS.** The only two unlisted files are exactly the two that cannot
list themselves. Zero mismatches, zero missing listed files, no other unlisted
files anywhere in the tree.

### Check 3 — independence declaration

I declare the following.

- I did **not** open any file under `reviews/`, including `reviews/README.md`.
  *(Accidental exposure, self-reported below.)*
- I did **not** read, list, glob or `find` any other
  `.agent-runtime/review-snapshots/round-*` directory.
- I did **not** read any other reviewer's report and did **not** read any
  verdict or acceptance count.

**Self-reported accidental exposure (full disclosure):**

1. Early in the session I ran `ls -la reviews` **in the working tree** (not in
   the snapshot) while establishing the repository layout. This listed
   directory *names* only (e.g. `round-1` … `round-30`, `foster-cycle-*`,
   `README.md`). No file inside any of them was opened, and no report content,
   verdict, or acceptance count was seen. This was the working tree, not a
   `review-snapshots/round-*` directory.
2. To write this report I created/`ls`-ed my own output directory
   `reviews/round-32/` and observed that it contains one pre-existing
   file, `LAUNCH-STATE.md`. I did **not** open it.
3. While auditing `source-manifest.json` I observed programmatically that its
   key set contains **exactly one** `reviews/` key, `reviews/README.md`. I did
   **not** open it. No other reviewer report is shipped in this snapshot under
   a `reviews/` path.

I term none of the above as reading another reviewer's report; my vote is not
invalidated on that basis, but I disclose it so the count can be assessed
independently.

---

## 2. Numerical verification — every value the manuscript quotes

Each value was located in the frozen artifact, recomputed where possible, and
compared. Unit note: the conformal/experiment section uses one arbitrary stress
unit `K_*`; pressure/energy are in `K_*`, strain and `B` dimensionless.

### 2.1 Conformal and experiment values (`sections/experiments.tex`, `build/conformal/`)

| # | Manuscript claim (location) | Artifact | Artifact value | Recompute | Verdict |
|---|---|---|---|---|---|
| 1 | 186 named checks | `build/conformal/verification.json:checks_passed` | `186`; `checks` dict len **186**; fails (error>tol) **0** | 186 keys, 0 over tolerance | **agree** |
| 2 | 65 per-state identities = 5 states × 13 identities | `verification.json:checks` `legacy_state{0..4}_*` | 5 × 13 = **65** names; `legacy_identities_rechecked = 67` | 65 + 2 = 67 | **agree** |
| 3 | two reference Biot / rank-one relations | `legacy_reference_biot`, `legacy_reference_rank_one_compliance_identity` | present, errors 1.9e-16, 1.4e-17 | — | **agree** |
| 4 | largest constitutive-identity error `2.5×10⁻⁹` | `verification.json:max_constitutive_identity_error` | `2.4549890331732928e-09` | rounds to 2.5e-9 (2 s.f.) | **agree** |
| 5 | `φs0=0.6`, `K=7K_*`, matrix of eq. (example-mineral-stiffness) | `build/conformal/experiments.json` | `phi_s0=0.6`, `K=7.0`, 6×6 matrix identical elementwise | — | **agree** |
| 6 | `K_s = 28K_*` | `experiments.json:Ks` | `28.0` | `I:C_s:I/9 = 252/9 = 28.0` | **agree** |
| 7 | isotropic mineral shear modulus `16.8K_*` = "mean of the five deviatoric stiffness modes, divided by two" | `experiments.json:isotropic_comparison.mu` | `16.8` | deviatoric projection of the normal 3×3 block: eig `PNP = {0, 42.9668, 53.0332}` (sum 96) plus shear diagonals `{20,24,28}` → mean 33.6 → /2 = **16.8** | **agree** (see R2-O1 on wording) |
| 8 | reference Biot components `0.7000, 0.7583, 0.7917` | `experiments.json:highlights.reference_B` | `0.7, 0.7583333…, 0.7916666…` | recomputed `B0 = I − C_d:C_s⁻¹:I` → `[0.7, 0.758333, 0.791667]` | **agree** |
| 9 | 121 pressure states | `experiments.json:loading`; `pressure_response.csv` | "121 points"; **242 data rows = 121×2** (anisotropic+isotropic) | — | **agree** |
| 10 | 161 equally spaced γ | `shear_response.csv` | **322 rows = 161×2** | — | **agree** |
| 11 | 121 angles (rotation) | `rotation_response.csv` | **242 rows = 121×2**, modes `internal frame`/`physical rotation` | — | **agree** |
| 12 | 121 points (constrained layer) | `constrained_layer.csv` | **242 rows = 121×2** | — | **agree** |
| 13 | directional "one-degree intervals" | `directional_response.csv` | **1083 rows = 361×3** states; `theta_deg` 0…360 | — | **agree** (361 samples/state) |
| 14 | second-order step refinement | `verification.json:observed_orders` | `energy_stress 2.00039`, `pore_volume 2.00021`, `pressure 1.99999` | — | **agree** |
| 15 | 273 finite states across 13 mineral stiffnesses | `build/weighted-stress/tensor-verification.json` | `total_states 273 = materials 13 × 21` | — | **agree** |
| 16 | reconstruction suite (work equivalence, finite unjacketed) | `build/weighted-stress/reconstruction-verification.json` | `work_equivalence 5.04e-10`, `unjacketed 5.09e-14`, `materials 20` | — | **agree** |
| 17 | all plotted states positive phase volume + scalar stability | `experiments.json` | `solid_fraction_range [0.4343, 0.6] ⊂ (0,1)`; `min_scalar_stability 28.0 > 0` | — | **agree** |
| 18 | negative-pressure branch + large positive state outside plotted range | `verification.json` | `branch_pressure_{-14,-13,800}_*` all pass | −14, −13 < 0; 800 ≫ plotted 6 | **agree** |

### 2.2 Finite-element values (`sections/finite_elements.tex`, `main.tex` §5, `fe-evidence/`, `figures/`)

| # | Manuscript claim (location) | Artifact | Artifact value | Verdict |
|---|---|---|---|---|
| 19 | MMS pressure orders `2.00`, `2.00` | `fe-evidence/mms-convergence.json:space.orders.p_l2.naive_orders` | `[1.996629, 2.000807]` | **agree** |
| 20 | MMS `u_x` orders `2.99`, `2.96` | same, `ux_l2.naive_orders` | `[2.991667, 2.958479]` | **agree** |
| 21 | MMS `u_y` orders `3.00`, `2.96` | same, `uy_l2.naive_orders` | `[2.998261, 2.959986]` | **agree** |
| 22 | temporal orders `0.98`–`1.40` at nx=16/32/64 | same, `time.*.orders.*.difference_orders` | min `0.97830` (nx16,uy), max `1.39688` (nx32,ux) | **agree** |
| 23 | linear step refinement errors `3.7×10⁻³` and `7.1×10⁻³` at dt=1e-3, 2e-3 | `figures/fe_mandel_refinement.csv` | `0.003657959`, `0.007103922` | **agree** |
| 24 | ratio `1.94`, first order in Δt | recompute `0.007103922/0.003657959` | `1.94205` | **agree** |
| 25 | pressure floor `3.2×10⁻³` at nx=20, dt=1e-3 | `figures/fe_load_limit.csv` (`load=0.0001`) | `0.003220919735602341` | **agree** |
| 26 | fabric reconstruction diff `2.2×10⁻¹⁶` | `build/fabric/fabric-verification.json:tensor_checks.H_reconstruction_max_abs_diff` | `2.220446049250313e-16` | **agree** |
| 27 | `det H − 1 = −3.3×10⁻¹⁶`, eig `h⁻²,h,h` | same, `H_det_minus_one`, `H_eigenvalues` | `−3.330669e-16`; `[0.9992863543052308, 1.000357013944851, 1.000357013944851]`; `h=1.000357013944851`, `h⁻²=0.9992863543052308` | **agree** |
| 28 | `‖D:e₃‖ = 1.6×10⁻¹⁶`, `D:e₆ = 0` | same, `D4_e3_norm`, `D4_e6_norm` | `1.5823112613210482e-16`, `0.0` | **agree** |
| 29 | rotation invariance `2.5×10⁻¹⁶` | same, `rotation_invariance_norm` | `2.4965357070272594e-16` | **agree** |
| 30 | NumPy re-implementation worst diff `4.9×10⁻¹⁵` | same, `worst_probe_abs_diff` | `4.884981308350689e-15` (max single field 3.66e-15 over 10 fields × 10 cases) | **agree** |
| 31 | conformal limit `1.9×10⁻¹⁴` | same, `conformal_cross_check.*.abs_diff` | max `1.874195e-14` (σ11) | **agree** |
| 32 | coupled peaks `4.36e-5`, `4.99e-5`, `5.52e-5`; uncoupled `3.62e-5` | `figures/fe_fabric_mandel_peak.csv` | `4.362759e-5`, `4.990085e-5`, `5.521105e-5`; iso `3.616393e-5` | **agree** |
| 33 | each peak coincides with the final state | same, `peak_center_pressure == final_center_pressure`, `final_time 0.003` | identical to 15 s.f. | **agree** |
| 34 | contour peaks `3.61e-5` (iso), `4.35`, `4.97`, `5.50e-5` | `figures/fe_fabric_contours.csv` | `3.606194e-5`, `4.349137e-5`, `4.973659e-5`, `5.503135e-5` | **agree** |
| 35 | displacement peaks `5.18e-5`, `5.14e-5`, `2.38e-5`, `5.26e-5` | same, `u_mag_max` | `5.182640e-5`, `5.137155e-5`, `2.381836e-5`, `5.258692e-5` | **agree** |
| 36 | max on `X₁=0` line; `p→0` at drained edge `X₁=1` | `fe_fabric_contours.csv:p_max_x=0.0` for all four; **independent re-read of `solution.e`** | `p_max` at `x=0.0` for all four; `max|p|` on `x=1` edge `2.2e-130 / 5.4e-136 / 1.0e-166 / 1.5e-127` | **agree** |
| 37 | "eleven evenly spaced field snapshots" | all four `solution.e`: `time_step=11`; `fabric_contour_a45/solution.csv` rows t=0…0.003 step 3e-4 | 11 snapshots | **agree** |
| 38 | diffusion "six recorded times" | `figures/fe_fabric_diffusion.csv` | 6 times/row-block | **agree** |
| 39 | refined `40×8` mesh of `1×0.1` strip | `fabric_contour_*/provenance.json:mesh`; `solution.e` `num_elem=320`, `num_nodes=1377` | 40×8=320 elements; (2·40+1)(2·8+1)=1377 nodes | **agree** |
| 40 | FE reference inputs `φs0=0.9, Ks=2.5, μs=5/6, K=1, Kf=8, ρf0=1, k/μf=1.5` | `site/reports/mandel-reference.json:parameters` | `K=1.0, G=0.75, alpha=0.6, M=4.705882352941177, mobility=1.5, a=1.0, b=0.1` | **agree** |
| 41 | drained shear modulus `G=0.75` | same | `G=0.75`; recompute `φs0·μs = 0.9·(5/6) = 0.75` | **agree** |
| 42 | reference Biot coefficient `0.6` | same | `alpha=0.6`; recompute `1−K/Ks = 1−1/2.5 = 0.6` | **agree** |
| 43 | total storage `17/80` | `mandel-reference.json:derived.M` etc. | recompute `(1−φs0)/Kf + (φs0/Ks)(1−K/(φs0Ks)) = 0.0125 + 0.2 = 0.2125 = 17/80` | **agree** |

**No numerical disagreement was found.** Every value quoted in `main.tex`,
`sections/experiments.tex`, `sections/finite_elements.tex`,
`sections/pore_fabric.tex`, `sections/stress_reconstruction.tex`,
`sections/limits.tex` and `sections/logarithmic_derivative.tex` that is a
recorded measurement traces to a frozen artifact at the stated precision.
All 186 recorded conformal checks pass their recorded tolerances
(0 failures at `error > tolerance`).

---

## 3. Digest-surface audit

Every declared digest surface was re-hashed from the shipped bytes.

| Surface | Entries | Mismatch | Missing | Notes |
|---|---|---|---|---|
| `source-manifest.json` | 608 | 0 | 0 | 2 unlisted files are the two self-excluded files |
| `fe-evidence/manifest.json` (`files[]`) | 317 | 0 | 0 | byte-size fields also all match (0 mismatches); unlisted = `README.md`, `manifest.json` |
| `fe-evidence/runs/*/provenance.json` (`input_sha256`, `source_sha256`) | 57 records | 0 | 0 | see §5 |
| `site/evidence.json` (`artifacts[]`) | 41 | 0 | 0 | includes all `site/reports/*` |
| `site/scientific-snapshot.json` (`files[]`) | 47 | 0 | 0 | |
| `build/anisotropic-biot-2026-09-20-v2.zip` internal `manifest.json` | 68 | 0 | 0 | 69 files on disk; only `manifest.json` unlisted (self-exclusion) |
| `figures/fabric-plot-manifest.json` | 15 in / 7 out | 0 | 0 | |
| `figures/fe-verification-plot-manifest.json` | 6 in / 4 out | 0 | 0 | |
| `figures/fe_fabric_contours-plot-manifest.json` | 5 in / 6 out | 0 | 0 | |

Two notes on path resolution. (i) The `output_sha256` keys in the three
`figures/*-plot-manifest.json` files are relative to `figures/`, while the
`input_sha256` keys are repository-relative; resolving the outputs against the
snapshot root shows spurious "missing" files that do not exist. With the
correct resolution all 17 output digests match. This is a manifest-path
convention, not a digest failure — flagged only so a future automated checker
does not fall into it. (ii) The `build/*.png` siblings of the `build/conformal/*.pdf`
figures are not declared in any manifest surface; they are unhashed by design
and are not referenced by the manuscript.

**Supplement archive.** `sha256(build/anisotropic-biot-2026-09-20-v2.zip)` =
`ab993ee75fd3e087e19114fed9d3cc50996b587b908472e5ac96bcfdb5ee4d04`. The PDF
attachment was extracted independently and is **byte-identical** to that
shipped zip (`cmp` clean, same sha256). The archive's internal
`manifest.json` covers 68 of its 69 files with 0 mismatches.

---

## 4. Figure-input provenance (Exodus)

`figures/fe_fabric_contours-plot-manifest.json` declares an `input_sha256`
entry for each of the four Exodus field files. Independent command:

```
$ sha256sum fe-evidence/runs/fabric_contour_{iso,a0,a45,a90}/solution.e
3dfe02ae921075727d0999c83fd9991562cbc1a660096e80ebfd35a7ebaedcad  .../fabric_contour_iso/solution.e
e615b78160aeb0fcc89cfae7f9d7ef94cf53177ed0f08e439aff927cd590ee52  .../fabric_contour_a0/solution.e
2ab3a3ca95c0023c54cc8fda56ea2092be0989fcd19359f63ceb81b4adb7fd53  .../fabric_contour_a45/solution.e
8eb00e29510deb943fef9c714a3a12c43eda15d4cdfc52c12c55e59704f75e00  .../fabric_contour_a90/solution.e
```

**Result: all four declared digests match the shipped bytes exactly**
(same strings as the manifest). The declared `examples/plot_fabric_contours.py`
input digest also matches. So the figure's claimed field inputs are the exact
files that ship, and the four contour figures are reproducible from the
snapshot's own bytes to the extent the generator is deterministic (see §6).

The nineteen `build/conformal/*.csv|pdf|json` inputs behind
`build/fabric/fabric-verification.json` are declared and all verify; the
`build/conformal/experiments.json` inputs to `figures/fabric-plot-manifest.json`
also verify (§3).

---

## 5. Run provenance

57 `fe-evidence/runs/*/provenance.json` records.

| Check | Result |
|---|---|
| `input_sha256` vs the shipped deck (cross-checked against both `moose_app/inputs/<deck>` and the run's own `input.i`) | **57/57 match, 0 mismatches** |
| `source_sha256` entries (160 individual source digests) vs shipped sources | **0 mismatches, 0 missing** |
| records carrying some binary/application digest | **57/57** |
| distinct declared `git_revision` | **2**: `40a49aee…` (42 records), `b6d72721…` (15 records) |

**Binary digest verifiability.** Every record declares
`binary_sha256` (38 non-fabric records) or `application_sha256` +
`application_library_sha256` (19 fabric records), but **no compiled binary or
`.so` ships in the snapshot** (`find` for `*-opt` / `*.so*` returns 0 files;
`moose_app/` contains sources, headers, inputs and scripts only). Therefore the
declared binary digests **cannot be verified from the snapshot** — they are
self-declared. This is disclosed in the evidence itself
(`fe-evidence/manifest.json` note: "The binary is not shipped…"), so it is a
documented re-derivation limit, not an undisclosed gap.

**Git revision verification (read-only).** Both declared revisions exist in the
repository object database:

```
40a49aee… 2026-09-21 18:04:55 -0500  Resolve the round-30 review findings…
b6d72721… 2026-09-21 17:48:15 -0500  Resolve the round-29 review findings…
```

For both revisions I extracted the recorded sources' blobs and hashed them:

| Path | `b6d72721` sha256 | `40a49aee` sha256 | recorded `source_sha256` |
|---|---|---|---|
| `moose_app/include/utils/FabricLaw.h` | `761334c6…` | `761334c6…` | `761334c6…` |
| `moose_app/include/materials/FabricMaterial.h` | `7e70dde1…` | `7e70dde1…` | `7e70dde1…` |
| `moose_app/src/materials/FabricMaterial.C` | `9abcfab6…` | `9abcfab6…` | `9abcfab6…` |
| `moose_app/inputs/fabric_contour.i` | `284f042c…` | `284f042c…` | `284f042c…` |
| `moose_app/inputs/fabric_mandel.i` | `a1ae9148…` | `a1ae9148…` | `a1ae9148…` |

**No record declares a revision whose tree does not contain the recorded
sources.** Every declared revision is present, and its blobs reproduce the
recorded digests exactly.

One internal-consistency point, not a defect: `site/evidence.json:provenance.source_revision`
is `40a49aee…`, while the snapshot's own commit (working tree HEAD,
`8d837260…`) is later. The site text says "The base commit predates this
working revision", and the review snapshot is declared authoritative, so the
pinned revision being an ancestor is expected.

---

## 6. Reproducibility of the recorded field files

**Determination: two runs of the same deck would NOT produce identical bytes.**
Evidence, from the shipped `solution.e` files themselves:

All four contour Exodus files carry an info record with a wall-clock stamp that
differs per run:

| File | `MOOSE Version` | `Current Time` | `Executable Timestamp` |
|---|---|---|---|
| `fabric_contour_iso` | git commit `abafb58b` on 2026-02-20 | `Mon Sep 21 18:20:51 2026` | `Sun Sep 20 23:20:55 2026` |
| `fabric_contour_a0` | same | `Mon Sep 21 18:21:04 2026` | same |
| `fabric_contour_a45` | same | `Mon Sep 21 18:21:16 2026` | same |
| `fabric_contour_a90` | same | `Mon Sep 21 18:21:29 2026` | same |

Two further observations:

- `num_info` differs between files of *identical* decks: 1639 for
  `a0/a45/a90`, 1640 for `iso`. The info record block is therefore
  content-dependent and not a constant-size header.
- The `Current Time` probe here is between *different* decks run minutes apart.
  Because the string is written from the process clock at file creation, two
  runs of the *same* deck likewise differ in that record, and hence in bytes.

**What is reproducible vs not reproducible in a recorded Exodus file:**

- **Not reproducible (differs byte-for-byte between two runs of the same deck):**
  the `info_records` line `Current Time: …` (wall-clock), and, across
  rebuilds, `Executable Timestamp: …` and the `MOOSE Version` commit string.
  Any archive-byte hash of the `.e` file is therefore run-dependent.
- **Structurally deterministic and expected to repeat:** the mesh
  (`coordx/coordy`, `connect1`, `node_num_map`), the block/side-set topology,
  the variable name tables (`name_nod_var` = `force_reaction, mass_reaction, p,
  ux, uy` in the contour runs), the timestep count (`time_step = 11`), and the
  `time_whole` values.
- **Numerically reproducible only under matched conditions:** the floating-point
  `vals_nod_var*` / `vals_elem_var*` / `vals_glo_var` payloads. They are
  deterministic in principle for a fixed binary, platform and BLAS/MPI thread
  count, but are exposed to summation-order and library-version differences.
  The shipped `.csv` histories (`solution.csv`, `figures/*.csv`) carry the same
  caveat but no wall-clock stamp, so they are the more portable record.

This is **not** a manuscript claim error: no text in `main.tex` or the sections
promises byte-identical field files. The shipped supplement `README.md` says
"Floating-point and PDF metadata differences between platforms need not
reproduce archive bytes" — accurate as far as it goes, but it attributes
non-reproducibility to *platform* differences and *PDF* metadata only, and does
not mention that the shipped Exodus files embed a run wall-clock. See R2-O2.

---

## 7. Do the recorded artifacts support the manuscript's scope claims?

| Scope claim | Where | Recorded support | Verdict |
|---|---|---|---|
| FE implementation "verified against a manufactured solution for the constant reference tangent" | abstract, §5 | `mms-convergence.json` space orders 2.00/2.00/2.99/2.96/3.00/2.96 over nx=4,8,16; 3 MMS decks ship with `analysis.json` | **supported** |
| "and, in the same limit, the constant-coefficient consolidation reference" | abstract, §5 | 10 `linear_*` runs ship `reference_comparison.csv`; `site/reports/mandel-reference.json` self-checks pass; comparison plotted with no interpolation | **supported** |
| "rotated-anisotropy and partial-drainage demonstrations at finite load; no quantitative finite-deformation verification and no experimental validation are claimed" | abstract, §5 | `site/evidence.json:categories.finite_deformation = pending`; each `anisotropic_*` / `partial_*` `analysis.json` sets `reference_comparable=false` with a `reference_note` explaining the domain/parameter mismatch; only mass-balance, platen-equality and force diagnostics are reported | **supported** |
| "fabric law … checked at the material point against a separate re-implementation of the section equations that shares the same modelling conventions" | abstract, §5 | `fabric-verification.json` compares compiled fields to an independent NumPy evaluation over 10 cases / 10 fields, worst 4.9e-15, and the `README`/site text states the shared conventions (distention basis, equilibrium, `ln h` sign) | **supported and honestly labelled** |
| "no experimental validation" | abstract, site | `site/evidence.json:categories.physical_validation = not_performed`; limitations list "Parameters are synthetic" | **supported** |
| "the coupled finite-element application sources … travel with the manuscript sources in the repository" | `sections/experiments.tex` (Code and data availability) | `moose_app/` ships sources + `Makefile` + inputs + scripts; the published companion is separate and declared | **supported** |
| tensorial law "implemented in its reference-state linearization" and demonstrated with pressure rotating with pore fabric | abstract, §5.4 | `fabric_mandel_*` peaks 4.36/4.99/5.52e-5 vs 3.62e-5 uncoupled behind an isotropic, unrotated mineral | **supported** |

The scope language is consistently more conservative than the data would
license, which is the correct direction.

---

## REQUIRED changes

**None.** No numerical claim disagrees with a frozen artifact; no declared
digest fails; no listed file is missing; no record declares an unverifiable or
absent revision; and every quoted check count and convergence order reproduces
exactly. I did not reach this by weakening any finding: I searched explicitly
for a contradiction in the two places the emphasis points at (the
"five deviatoric stiffness modes" number and the Exodus field provenance) and
could not produce one.

## OPTIONAL notes

- **R2-O1 — `sections/experiments.tex`, line ~150 ("Its mineral shear modulus is
  `16.8K_*`, the mean of the five deviatoric stiffness modes of `C_s`, divided by
  two").** The value is *correct* (`experiments.json:isotropic_comparison.mu =
  16.8`), but the phrase is not reproducible from the shipped artifacts alone:
  the five modes are never recorded, and two natural readings of "the five
  deviatoric stiffness modes" give a different answer — the two
  non-volumetric eigenvalues of the full normal 3×3 block
  (`41.98152417…`, `51.79003653…`) with the three shear diagonals
  (`20, 24, 28`) average `42.0` (→ `21.0`), whereas the deviatoric *projection*
  `P N P` with the same shear diagonals gives `{42.9668, 53.0332, 20, 24, 28}`,
  mean `33.6` (→ `16.8`, the recorded value). Suggestion: record the five
  modes in `build/conformal/experiments.json` (e.g. a `deviatoric_modes` field)
  or name the construction in the sentence. No manuscript number changes.
- **R2-O2 — supplement `README.md` (reproducibility paragraph) and
  `figures/fe_fabric_contours-plot-manifest.json` `limitations`.** The shipped
  `solution.e` files embed a per-run wall-clock `Current Time` info record, so
  the Exodus bytes are not reproducible even on a single platform. The README's
  remark covers platform floating-point and PDF metadata but not this. Suggest
  adding one clause: recorded Exodus files carry a run timestamp in their info
  records, so byte equality is not expected; the CSV histories are the portable
  record. Purely documentary — no claim is affected.
- **R2-O3 — `sections/finite_elements.tex`, lines ~272–274 ("the stiffness
  annihilates the coupled in-plane pair `‖D:e₃‖=1.6×10⁻¹⁶` and `D:e₆=0`…" and
  earlier "the four complementary modes are frozen to the mineral").**
  `fabric-verification.json:tensor_checks` records norms only for `e₃` and
  `e₆`; the two axial-shear modes `e₄`, `e₅` are covered by the transverse-
  isotropy argument but have no recorded norm. Suggest adding `D4_e4_norm` and
  `D4_e5_norm` for completeness. No quoted number is unsupported, so this is
  optional.

---

VERDICT: ACCEPT

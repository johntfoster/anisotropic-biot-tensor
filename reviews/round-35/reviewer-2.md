# SIMULATED AI PEER REVIEW — Reviewer 2 of 3

**This is a simulated AI peer review. It is not journal peer review and confers no acceptance.**

Manuscript: *An anisotropic Biot tensor from mineral stress and distention work* (John T. Foster)
Frozen snapshot: `.agent-runtime/review-snapshots/round-35`
Declared `SNAPSHOT_ID`: `3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886`
Emphasis: numerical verification and source fidelity (every quoted number and every declared digest re-checked against the frozen artifacts).

All reads were performed against the frozen snapshot (copied read-only to `/tmp/r35` only to obtain a writable scratch tree; the snapshot itself was never modified).

---

## 0. Independence declaration (mandatory check 3)

I did **not** open any file under `reviews/` (including `reviews/README.md`). I did **not** read, list, glob, or `find` any other `.agent-runtime/review-snapshots/round-*` directory, any other reviewer's report, or any verdict/acceptance count.

Self-report of exposure risk. My first command listed the repository root (`ls -la` of the *working tree*, not the snapshot) and the snapshot root directory itself. Those listings showed that directory names `reviews/` and `.agent-runtime/review-snapshots/round-35` exist, but no directory contents under `reviews/` were ever listed or opened, and no sibling `round-*` directory was ever listed or opened. Every subsequent read was confined to the `round-35` snapshot tree and to read-only `git` queries against the working-tree object database (permitted by the task). No other reviewer's report or verdict was seen. My vote is independent.

---

## MANDATORY FIRST CHECKS

### Check 1 — manifest digest equals the declared SNAPSHOT_ID

```
$ cd .agent-runtime/review-snapshots/round-35
$ sha256sum source-manifest.json
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886  source-manifest.json
$ cat SNAPSHOT_ID
3e56fad609d38c3a6dd65c10e6aff3959ec7deaff3c21ba2b86448074ad1d886
```

**Result: PASS.** The re-computed SHA-256 of `source-manifest.json` equals the declared `SNAPSHOT_ID` exactly, and the `SNAPSHOT_ID` file holds the identical string. (The declared file was not modified during review; a re-check of the manifest hash after all work would be expected to match, as the file is read-only in the snapshot.)

### Check 2 — re-hash every listed file and walk the tree

`source-manifest.json` is a flat mapping `repository-relative path -> sha256` with **608 entries**.

```
$ python3  # sha256 of each listed path + os.walk of the snapshot
entries listed:              608
re-hashed OK:                608
hash mismatches:             0
listed but missing on disk:  0
files present but unlisted:  0   (excluding source-manifest.json and SNAPSHOT_ID, which cannot list themselves)
```

**Result: PASS.** Entry count 608; re-hashed 608; 0 hash mismatches; 0 listed-but-missing; 0 present-but-unlisted.

### Check 3 — independence

See §0 above. No exposure; vote independent.

---

## SCOPE VERIFICATION — NUMBERS

Every numerical value quoted in `main.tex` and `sections/*.tex` was located in the frozen JSON/CSV/Exodus artifacts. Unless stated otherwise the quoted manuscript value agrees to the digits printed.

| # | Manuscript claim (location) | Frozen artifact evidence | Result |
|---|---|---|---|
| 1 | "186 named checks" — `sections/experiments.tex:181` | `site/reports/conformal-verification.json` → `checks_passed: 186`, `len(checks) = 186` | agree |
| 2 | "65 per-state identities (five states times thirteen identities)" — `experiments.tex:181–186` | `legacy_state0..4_*` keys: 5×13 = 65; `legacy_identities_rechecked: 67` = 65 + the 2 reference relations | agree |
| 3 | "two reference Biot and rank-one compliance relations" — `experiments.tex:186` | `legacy_reference_biot`, `legacy_reference_rank_one_compliance_identity` | agree |
| 4 | largest constitutive-identity error `2.5×10⁻⁹` — `experiments.tex:187` | `max_constitutive_identity_error = 2.4549890331732928e-09` | agree (2.455e-9) |
| 5 | `φ_s0 = 0.6`, `K = 7K_*`, `K_s = 28K_*` — `experiments.tex:10–22` | `build/conformal/experiments.json`: `phi_s0 0.6`, `K 7.0`, `Ks 28.0` (K_s = 252/9) | agree |
| 6 | mineral Mandel stiffness matrix — `experiments.tex:eq:example-mineral-stiffness` | `mineral_Mandel_stiffness` identical element-by-element | agree |
| 7 | reference Biot components `0.7000, 0.7583, 0.7917` — `experiments.tex:25` | `highlights.reference_B = [0.7, 0.758333…, 0.791666…]`; **independently recomputed** `B₀ = I − ℂᵈ:ℂ_s⁻¹:I` = `[0.7, 0.75833333, 0.79166667]` | agree |
| 8 | isotropic mineral shear modulus `16.8K_*` = mean of the five deviatoric modes ÷ 2 — `experiments.tex:29` | **independently recomputed** deviatoric spectrum of ℂ_s = {20, 24, 28, 42.9668, 53.0332}; mean 33.6; ÷2 = **16.8** | agree |
| 9 | drained stiffness "determined by the restriction" — `experiments.tex:23` | **independently recomputed** `ℂᵈ = φ_s0ℂ_s − (φ_s0/9K_s)(1−K/(φ_s0K_s))(ℂ_s:I)⊗(ℂ_s:I)` reproduces `drained_Mandel_stiffness` with max abs diff **0.0** | agree |
| 10 | pressure path "121 pressure states" — `experiments.tex:64` fig caption | `build/conformal/pressure_response.csv`: 243 rows = 2 materials × 121 + header | agree |
| 11 | shear path "161 equally spaced values of γ" — `experiments.tex:86` | `shear_response.csv`: 323 rows = 2 × 161 + header | agree |
| 12 | directional "one-degree intervals" — `experiments.tex:105` | `directional_response.csv`: 1084 rows = 3 × 361 + header (1° spacing) | agree |
| 13 | rotation "121 angles span zero to 180°" — `experiments.tex:143` | `rotation_response.csv`: 243 rows = 2 × 121 + header | agree |
| 14 | layer "121 points on 0≤p/K_*≤6" — `experiments.tex:158` | `constrained_layer.csv`: 243 rows = 2 × 121 + header | agree |
| 15 | "273 finite states across 13 mineral stiffnesses" — `experiments.tex:191` | `site/reports/tensor-verification.json`: `total_states 273`, `materials 13`, `states_per_material 21` | agree |
| 16 | reconstruction suite (work equivalence, finite unjacketed) — `experiments.tex:192` | `reconstruction-verification.json`: `work_equivalence`, `unjacketed`, `drained_energy`, `reference_storage`, `minimum_drained_eigenvalue 1.8415` | agree |
| 17 | FE reference inputs `φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, ρ̄_f0=1, k/μ_f=1.5` — `finite_elements.tex:206–211` | decks: `solid_fraction = 0.9`, `drained_bulk = 1`, `fluid_bulk = 8`, `mobility = 1.5`; `conformal_probe.i` mineral C₄₄ = 1.6667 = 2μ ⇒ μ = 5/6, λ = 1.9444 ⇒ K_s = 2.5 | agree |
| 18 | drained shear `G = 0.75`; reference Biot `0.6`; total storage `17/80` — `finite_elements.tex:212–214` | 0.9·(5/6) = 0.75; 1−K/K_s = 0.6; (1−φ_s0)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80; `mandel-reference.json` `M = 4.70588… = 1/0.2125` | agree |
| 19 | MMS spatial orders p `2.00/2.00`, u_x `2.99/2.96`, u_y `3.00/2.96` — `finite_elements.tex:246` | `fe-evidence/mms-convergence.json` (and `site/reports/mms-convergence.json`) naive_orders: p 1.9966/2.0008; ux 2.9917/2.9585; uy 2.9983/2.9600 | agree |
| 20 | temporal orders "0.98–1.40" at nx=16/32/64 — `finite_elements.tex:252`, `main.tex:613` | successive-difference orders: min 0.9783 (nx16,uy), max 1.3969 (nx32,ux) | agree |
| 21 | step-refinement `3.7×10⁻³`, `7.1×10⁻³` at dt=10⁻³/2×10⁻³, ratio `1.94` — `finite_elements.tex:256`, `main.tex:610` | `figures/fe_mandel_refinement.csv`: 3.65796e-3, 7.10392e-3; ratio 1.9421 | agree |
| 22 | load-limit floor `3.2×10⁻³` at nx=20, dt=10⁻³ — `finite_elements.tex:262`, `main.tex:608` | `figures/fe_load_limit.csv`: `nonlinear_load_0.0001` pressure_max_normalized = 3.22092e-3 | agree |
| 23 | fabric reconstruction `2.2×10⁻¹⁶`; `det H − 1 = −3.3×10⁻¹⁶`; eigenvalues `h⁻²,h,h`; `‖𝔻:e₃‖=1.6×10⁻¹⁶`; `𝔻:e₆=0`; rotation invariance `2.5×10⁻¹⁶` — `finite_elements.tex:271–275` | `fabric-verification.json` `tensor_checks`: 2.2204e-16; −3.3307e-16; [0.99928635, 1.00035701, 1.00035701] (= h⁻²,h,h for ln h = 3.5695e-4); 1.5823e-16; 0.0; 2.4965e-16 | agree |
| 24 | NumPy re-implementation worst diff `4.9×10⁻¹⁵` — `finite_elements.tex:279` | `worst_probe_abs_diff = 4.884981308350689e-15` | agree |
| 25 | volume-only limit reproduces conformal to `1.9×10⁻¹⁴` — `finite_elements.tex:287` | `conformal_cross_check` max abs diff = 1.8742e-14 | agree |
| 26 | coupled peaks `4.36, 4.99, 5.52 ×10⁻⁵`, uncoupled `3.62×10⁻⁵` — `finite_elements.tex:312–314` | `fabric_mandel_coup_a0/a45/a90` centre_pressure 4.3628e-5 / 4.9901e-5 / 5.5211e-5; `fabric_mandel_iso` 3.6164e-5 | agree |
| 27 | "each peak coincides with the final recorded state" — `finite_elements.tex:315` | `fe_fabric_mandel_peak.csv`: `peak_center_pressure == final_center_pressure`, `final_time = 0.003` for all four | agree |
| 28 | contour peaks `3.61, 4.35, 4.97, 5.50 ×10⁻⁵` — `finite_elements.tex:326` | `fe_fabric_contours.csv` p_max: 3.6062e-5, 4.3491e-5, 4.9737e-5, 5.5031e-5 | agree |
| 29 | displacement peaks `5.18, 5.14, 2.38, 5.26 ×10⁻⁵` — `finite_elements.tex:331` | `fe_fabric_contours.csv` u_mag_max: 5.1826e-5, 5.1372e-5, 2.3818e-5, 5.2587e-5 | agree |
| 30 | "maximum lies on the X₁=0 symmetry line … falls to zero at the drained edge X₁=1" — `finite_elements.tex:327` | CSV `p_max_x = 0.0` for all four; `p_min ~ −1e−127 … −5e−136` (≈0) | agree |
| 31 | "eleven evenly spaced field snapshots" — `finite_elements.tex:322` | Exodus `time_step = 11`, t = 0, 0.0003 … 0.003; provenance "11 field snapshots incl. initial" | agree |
| 32 | diffusion figure "six recorded times" — `finite_elements.tex:335` caption | `fe_fabric_diffusion.csv`: 12 rows = 2 cases × 6 times | agree |
| 33 | Step refinement "second-order convergence" — `experiments.tex:188` | `observed_orders`: energy {2.0004,2.0001,2.00002,2.000006}, pore_volume {2.0002,…}, pressure {1.99999,2.00028,2.00029,1.98915} | agree |
| 34 | negative-pressure/Lambert and large positive-pressure checks — `experiments.tex:196–197` | `branch_pressure_−14/−13/800_*` checks; 800 is outside the plotted 0–6 range | agree |
| 35 | positive phase volumes & scalar stability at plotted states — `experiments.tex:194` | `solid_fraction_range [0.4343, 0.6]`, `min_scalar_stability 28.0` | agree |
| 36 | fluid-coupling count/error (site claim) — `site/evidence.json` implementation summary | `fluid-coupling-verification.json`: `count 110`, `maximum_scaled_error 8.0867e-09` (site text 8.09e-09) | agree |
| 37 | C++ vs Python `6.4e-14` over 41 states — `site/evidence.json` | `cpp-python-constitutive.json`: `states 41`, `value_absolute_error 6.3949e-14` | agree |
| 38 | Mandel reference self-checks & overshoot — `site/evidence.json` analytical | `mandel-reference.json`: peak overshoot 5.4659 % at t = 0.01516535 | agree |
| 39 | FE finite-deformation diagnostic ranges — `site/evidence.json` finite_deformation | `finite-deformation-summary.json`: anisotropic peak 0.2062–0.2158, force_rel ≤1.276e-10, mass ≤2.47e-10; partial 0.2005–0.2016, ≤2.052e-10, ≤4.636e-10; isotropic 0.2238, 3.214e-12 | agree |

**No numerical disagreement was found. Every manuscript number was located in the frozen artifacts and agrees; several (rows 7, 8, 9) were re-derived from first principles rather than only matched to a stored scalar.**

---

## SCOPE VERIFICATION — DECLARED DIGEST SURFACES

| Surface | Entries | Mismatches | Missing | Unlisted | Result |
|---|---|---|---|---|---|
| `source-manifest.json` | 608 | 0 | 0 | 0 | PASS |
| `fe-evidence/manifest.json` `files[]` | 317 | 0 | 0 | 1 (`fe-evidence/README.md`, not self-listed) | PASS |
| `fe-evidence/runs/*/provenance.json` | 57 | 0 | 0 | — | PASS |
| `site/evidence.json` `artifacts` | 40 | 0 | 0 | — | PASS |
| `site/scientific-snapshot.json` `files` | 47 | 0 | 0 | — | PASS |
| `build/anisotropic-biot-2026-09-20-v2.zip` internal `manifest.json` | 68 | 0 | 0 | 0 | PASS |
| `figures/*-plot-manifest.json` (3 files) | 43 input+output digests | 0 | 0 | — | PASS |

Notes and independent re-checks:

- **Run provenance.** For all 57 runs, `input_sha256` was re-hashed against the shipped `input.i` (0 mismatches) and every `source_sha256` entry (`FabricLaw.h`, `FabricMaterial.h`, `FabricMaterial.C`) was re-hashed against the shipped sources (0 mismatches, 0 missing). `binary_sha256`/`application_sha256` are **not verifiable from the snapshot because the compiled binary is not shipped**; the manifest `notes` states this explicitly, so it is a disclosed limitation rather than an unmet claim.
- **Supplement archive.** The zip contains 69 files; its internal `manifest.json` lists 68 (it does not list itself) and all 68 re-hash exactly against the extracted bytes; 0 unlisted files; version `anisotropic-biot-2026-09-20-v2` matches `site/evidence.json` `version` and the `\embedfile` name in `main.tex`. The zip README is self-contained (ships `examples/*`, the fabric decks, the recorded run histories and the field files) and its reproduction commands reference files that are present in the archive.
- **Independent figure-input verification (Exodus).** Re-hashed with an independent command against the shipped bytes:

  ```
  fabric_contour_iso/solution.e  3dfe02ae921075727d0999c83fd9991562cbc1a660096e80ebfd35a7ebaedcad  OK
  fabric_contour_a0/solution.e   e615b78160aeb0fcc89cfae7f9d7ef94cf53177ed0f08e439aff927cd590ee52  OK
  fabric_contour_a45/solution.e  2ab3a3ca95c0023c54cc8fda56ea2092be0989fcd19359f63ceb81b4adb7fd53  OK
  fabric_contour_a90/solution.e  8eb00e29510deb943fef9c714a3a12c43eda15d4cdfc52c12c55e59704f75e00  OK
  ```

  All four declared `input_sha256` values equal the shipped bytes, and equal the values in the zip manifest and in `fe-evidence/manifest.json`.
- **Duplicate report copies are byte-identical**, so the copy chain is verifiable: `build/conformal/verification.json` ≡ `site/reports/conformal-verification.json`; `build/fabric/fabric-verification.json` ≡ `site/reports/fabric-verification.json`; `build/weighted-stress/tensor-verification.json` ≡ `site/reports/tensor-verification.json`.

### Run provenance — declared revisions against the repository object database

The snapshot has no `.git`, so read-only `git` was run against the working-tree object database:

| Declared `git_revision` | Runs | Commit present | Recorded sources in that tree |
|---|---|---|---|
| `40a49aeed3c02e074029f2ec6f75b4b444ded9a4` | 42 | yes (ancestor of HEAD) | `FabricLaw.h`, `FabricMaterial.h`, `FabricMaterial.C`, `fabric_contour.i` all present with SHA-256 **exactly equal** to the recorded `source_sha256`/`input_sha256` |
| `b6d72721414a0c09aa6492465acd3a4c8d07e31b` | 15 | yes (ancestor of HEAD) | same three sources present with identical recorded digests |

```
$ git show 40a49ae:moose_app/include/utils/FabricLaw.h | sha256sum
761334c6ce4919c1ff1dfb83b4b780ef4b9306f2e30dff4e4d63357cce497961   # == recorded
$ git show b6d72721:moose_app/src/materials/FabricMaterial.C | sha256sum
9abcfab637c610ac9645105d72dcfd63ff19e550305bf8d772981f00ecc030c2   # == recorded
```

**No record's revision tree fails to contain its recorded sources.** The `site/evidence.json` `provenance.source_revision` (`caac4069…`) also exists in the object database and is an ancestor of HEAD.

### Reproducibility of the recorded field files, and documentation of the residual

- The Exodus files **do** embed a run wall-clock string (e.g. `Current Time: Mon Sep 21 18:20:51 2026` in `fabric_contour_iso/solution.e`, echoed from the framework header). The shipped documentation states this accurately: `figures/fe_fabric_contours-plot-manifest.json` `limitations` says the raw bytes are not reproducible while the field arrays are, and the root `README.md` repeats it ("the raw file digest changes with the run time even though the fields do not, and the manifest is regenerated with them"). This is an honest, accurate description.
- I could not regenerate the decks (no compiled application is shipped, and the held numerical suites are out of scope), so the "field arrays bit-identical" claim is corroborated only by internal consistency: e.g. `fabric_contour_iso/solution.csv` final `center_pressure = 3.6061943087043e-05` equals `analysis.json` `center_pressure`, and the Exodus-derived `p_max = 3.606194309585106e-05` agrees to output precision. No contradiction was found.
- The finite-load residual/floor is described accurately and consistently in `main.tex:608`, `sections/finite_elements.tex:262`, `figures/fe-verification-plot-manifest.json`, and `site/evidence.json` (which correctly marks `finite_deformation` as `pending` and `physical_validation` as `not_performed`). This matches the manuscript's own "demonstration, not a verified limit" wording.

---

## FINDINGS

### REQUIRED

**R2-C1 — `fe-evidence/manifest.json`, `notes[0]` (line 5594): the note misstates which run outputs ship.**

The note reads:

> "Each runs/<case>/provenance.json enumerates the complete output set of the source run. Only the curated subset listed in files[] ships (**the Exodus solution.e and the per-step solution_profile_\*.csv dumps are intentionally not shipped because of size**); provenance_outputs_unshipped records the difference per case."

The parenthetical is contradicted by the same file's authoritative `files[]` list and by the shipped bytes:

- `files[]` lists **4** Exodus files — `runs/fabric_contour_{iso,a0,a45,a90}/solution.e` — and those four files are present on disk and are hashed by `figures/fe_fabric_contours-plot-manifest.json` and by the supplement archive.
- `files[]` lists **16** `solution_profile_*.csv` dumps (4 each for `runs/fabric_mandel_coup_{a0,a45,a90}` and `runs/fabric_mandel_iso`), and those files are present on disk.
- Only 38 of the 57 cases actually list `solution.e` in `provenance_outputs_unshipped`.

So the sentence is false as written for the 8 pore-fabric cases and over-broad for `solution_profile_*.csv`. Because this is the machine-readable record an auditor reads to learn what ships, and the review scope explicitly covers whether the shipped documentation describes the shipped record accurately, this should be corrected in the evidence record.

*Suggested fix:* scope the claim to the runs that omit them, e.g. "… Only the curated subset listed in files[] ships; for the source runs the large Exodus `solution.e` and per-step `solution_profile_*.csv` dumps are intentionally omitted, and `provenance_outputs_unshipped` records the difference per case (the refined `fabric_contour_*` field files and the `fabric_mandel_*` profile dumps are exceptions that do ship)."

**R2-C1 is the only required item. No numerical value and no declared digest is wrong; every other audited surface reconciles exactly.**

### OPTIONAL

**R2-O1 — `build/anisotropic-biot-2026-09-20-v2.zip` `README.md`: minor internal tension in the scope sentence.** The sentence "The models are synthetic constitutive calculations, not physical validation or finite-element simulations" is immediately followed by shipping recorded finite-element run histories. The following sentence ("The archive additionally ships recorded finite-element run histories…") resolves the intent, so this is only a wording nicety; consider "not physical validation, and its coupled examples are demonstrations rather than verified finite-element predictions."

**R2-O2 — `scripts/`-adjacent provenance: unverifiable binary digests.** `provenance.json` `binary_sha256`/`application_sha256` cannot be checked from the snapshot because the compiled application is not shipped. This is already disclosed in `fe-evidence/manifest.json` `notes`, and is not a defect; recorded here so the gap is visible in the audit trail. If a public release is desired, shipping the binary or a build-recipe hash that reproduces it would close the loop.

**R2-O3 — `site/evidence.json` `provenance.note`.** "The base commit predates this working revision" is only unambiguous for the site snapshot: `caac4069…` (2026-09-21 18:54) is a descendant of the run revision `40a49ae…` (18:04) and an ancestor of HEAD `01208754…` (19:04). The statement is consistent if "working revision" means HEAD, but a reader could misread it relative to the recorded run revision. Consider naming the commit explicitly.

---

## ASSESSMENT

The snapshot is internally consistent to an unusual degree: 608/608 manifest entries, 317/317 `fe-evidence` files, all 57 run provenance records, all 40 site artifacts, all 47 scientific-snapshot entries, all 68 zip-manifest entries, and all 43 figure-manifest digests re-hash exactly; every manuscript number traces to a frozen artifact and agrees; and the three key constitutive scalars (drained stiffness, reference Biot, isotropic comparison shear modulus) were re-derived independently rather than merely matched. The declared revisions are real commits whose trees contain the recorded sources byte-for-byte. The manuscript's scope claims (pending finite-deformation, not-performed physical validation, demonstration-only finite-load panels) are stated honestly and match the evidence manifest.

The only defect is a factual over-broad statement about which files ship in `fe-evidence/manifest.json` `notes[0]`, which is why the verdict is a minor revision rather than an accept. Fixing R2-C1 should require no re-run and no change to any number, digest, or figure.

---

VERDICT: MINOR REVISION

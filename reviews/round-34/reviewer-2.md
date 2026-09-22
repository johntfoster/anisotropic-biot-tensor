# SIMULATED AI PEER REVIEW — Reviewer 2 of 3

**Emphasis:** numerical verification and source fidelity
**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work* (John T. Foster)
**Frozen snapshot reviewed:** `.agent-runtime/review-snapshots/round-34`
**Declared SNAPSHOT_ID:** `a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e`
**Report:** `reviews/round-34/reviewer-2.md`
**Date:** 2026-09-21

This is a simulated AI peer-review exercise. It is not journal peer review and
confers no acceptance. All manuscript and evidence reads were taken from the
frozen snapshot only; the snapshot was never modified.

---

## 1. Mandatory first checks

### 1.1 SNAPSHOT_ID vs manifest hash — PASS

```
$ cd /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-34
$ sha256sum source-manifest.json
a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e  source-manifest.json
$ cat SNAPSHOT_ID
a2d99a3960d08ac9a8b1e9d333a0f77fb676a240b29e0ed528b9d1b308b3ea1e
```

`sha256(source-manifest.json)` equals the declared SNAPSHOT_ID exactly, and the
`SNAPSHOT_ID` file holds the same 64-hex string (no trailing whitespace). PASS.

### 1.2 Full re-hash of every listed file — PASS

`source-manifest.json` is a flat `repository-relative path -> sha256` mapping.
A python3/hashlib script read the mapping, re-hashed every listed path with
`hashlib.sha256(open(p,'rb').read()).hexdigest()`, then walked the tree with
`os.walk` to find files present but unlisted.

| Quantity | Result |
|---|---|
| entry count in manifest | **608** |
| entries re-hashed | 608 |
| hash mismatches | **0** |
| listed files missing on disk | **0** |
| files present on disk (walk) | 610 |
| files present but unlisted | **0** |

The two non-listed files on disk are exactly `source-manifest.json` and
`SNAPSHOT_ID`, which cannot list themselves, as the assignment notes. No other
file is unlisted. PASS.

### 1.3 Independence declaration

- I did **not** open any file under `reviews/`, including `reviews/README.md`.
- I did **not** read, list, glob, or `find` any other
  `.agent-runtime/review-snapshots/round-*` directory, any other reviewer's
  report, or any verdict/acceptance count.
- I did **not** open `build/main.aux` (it is not shipped); where equation-level
  context was needed I used the section sources and `build/main.log`/`main.pdf`
  only if required, which it was not.
- **Self-reported accidental exposure:** the mandatory tree walk in check 1.2
  (`os.walk` over the snapshot) enumerated file *names* under `reviews/` as a
  side effect of hashing the whole tree, and confirmed that every such file is
  listed in `source-manifest.json`. No `reviews/` file name was printed, and no
  `reviews/` file content (including any other reviewer's report) was read,
  displayed, or opened. Separately, the shipped repository `README.md` (lines
  75–76) *names* `reviews/README.md` and states that earlier reviews are not
  acceptance evidence; I did not follow that reference. My vote is not based on
  any exposure to another reviewer's work.

No other snapshot-listing tool was run against round-* directories.

---

## 2. Numerical verification: every quoted value vs the frozen artifacts

Every numerical value in `main.tex` and `sections/*.tex` was located in the
frozen JSON/CSV/Exodus artifacts and recomputed or re-read. **All values agree.**

### 2.1 Constitutive example data (`sections/experiments.tex`)

| Manuscript value | Location | Frozen source | Agreement |
|---|---|---|---|
| `phi_s0 = 0.6` | experiments.tex:7 | `build/conformal/experiments.json` `phi_s0` (snapshot also splits `phi=0.6` in `examples/conformal_model.py`) | exact |
| `K = 7 K_*` | experiments.tex:7 | `experiments.json` `K=7.0` | exact |
| mineral Mandel `C_s` 6×6 `(50,12,10;12,60,14;10,14,70;20,24,28)` | experiments.tex:44–52 (`eq:example-mineral-stiffness`) | `experiments.json` `mineral_Mandel_stiffness` — identical entries | exact |
| `K_s = 28 K_*` | experiments.tex:22 | `experiments.json` `Ks=28.0`; also recomputed `I:C_s:I/9 = 28.0` | exact |
| reference Biot `0.7000, 0.7583, 0.7917` | experiments.tex:25 | `experiments.json` `highlights.reference_B = [0.7, 0.7583333333333333, 0.7916666666666667]` | exact |
| isotropic mineral shear `16.8 K_*` | experiments.tex:29 | `experiments.json` `isotropic_comparison.mu = 16.8`; `examples/conformal_model.py:78` `mu_average = trace((I-ONE⊗ONE/3)·C_s)/10`; independently recomputed `trace(P·C_s)/10 = 16.8` | exact |
| 121 pressure states | experiments.tex:55 | `experiments.json` `loading.pressure = "F=I, p=0..6, 121 points"`; `build/conformal/pressure_response.csv` 242 rows = 2 materials × 121 | exact |
| 161 shear values | experiments.tex:86 | `loading.shear = "…161 points…"`; `shear_response.csv` 322 = 2 × 161 | exact |
| 121 rotation angles | experiments.tex:140 | `loading.rotation = "…theta=0..180 deg, 121 points"`; `rotation_response.csv` 242 = 2 × 121 | exact |
| 121 layer pressure points | experiments.tex:163 | `loading.layer = "…p=0..6,121 points"`; `constrained_layer.csv` 242 = 2 × 121 | exact |
| "one-degree intervals" (direction) | experiments.tex:115 | `loading.directional = "theta=0..360 deg"` (361); `directional_response.csv` 1083 = 3 × 361 | exact |
| conformal suite 186 named checks | experiments.tex:181 | `site/reports/conformal-verification.json` `checks_passed = 186` = `len(checks)` | exact |
| 65 per-state identities (5 × 13) | experiments.tex:181–183 | `checks` keys `legacy_state0..4` × 13 = 65 | exact |
| largest constitutive-identity error `2.5e-9` | experiments.tex:187 | `max_constitutive_identity_error = 2.4549890331732928e-9` | rounds to 2.5e-9 |
| tensor suite 273 states / 13 mineral stiffnesses | experiments.tex:192 | `site/reports/tensor-verification.json` `materials=13`, `total_states=273` (21 states/material) | exact |

Additional conformal checks audited: all **186** recorded checks satisfy
`error <= tolerance` (0 failures), which is what "186 named checks" plus the
`checks_passed` field assert. The largest *overall* error (`second_order_pressure
= 0.01085`, tolerance `0.06`) is a convergence check, not a constitutive
identity, and is correctly excluded from the `2.5e-9` claim. The 5-state × 13
identity set covers exactly the 8 listed families (rotation_orthogonality,
true_metric, log_strain, energy_rotation_independence,
rotated_mineral_stress, mixture_stress_rotation_independence,
(scalar) pressure_equilibrium, full_phase_balance_from_energy, pressure_tangent,
pressure_dependent_rotation_cancels, pore_volume_derivative,
zero_rotation_energy_derivative, full_virtual_work).

### 2.2 Finite-element reference values (`sections/finite_elements.tex`)

| Manuscript value | Location | Frozen source | Agreement |
|---|---|---|---|
| `phi_s0=0.9`, `K_s=2.5`, `mu_s=5/6`, `K=1`, `K_f=8`, `rho_f0=1`, `k/mu_f=1.5` | FE:161–163 | `site/reports/mandel-reference.json` `parameters` `{K:1.0, G:0.75, alpha:0.6, M:4.705882352941177, mobility:1.5, a:1.0, b:0.1}`; `K_f=8` from `fluid-coupling-verification.json` `fluid.bulk_modulus`; `mu_s = G/phi_s0 = 5/6` | exact |
| drained shear `G = 0.75` | FE:164 | `mandel-reference.json` `parameters.G = 0.75` | exact |
| reference Biot `0.6` | FE:165 | `parameters.alpha = 0.6` | exact |
| total storage `17/80` | FE:166 | `M = 80/17 = 4.70588…` ⇒ `1/M = 0.2125 = 17/80`; independently `(1-0.9)/8 + (0.9/2.5)(1-1/2.25) = 0.0125+0.2 = 0.2125` | exact |
| MMS `U=P_0=0.01` | FE:191 | `fe-evidence/runs/mms_space_16/input.i` expressions `0.01*sin(t)*sin(pi x)sin(pi y)`, etc. | exact |
| MMS mineral rotated `30°` | FE:192 | `mms_space_16/input.i:185 angle = 30`; `configuration.angle = 30` | exact |
| MMS orders p `2.00/2.00`, ux `2.99/2.96`, uy `3.00/2.96` | FE:204–205 | `fe-evidence/mms-convergence.json` `space.orders.*.naive_orders`: ux `[2.99167, 2.95848]`, uy `[2.99826, 2.95999]`, p `[1.99663, 2.00081]` | exact |
| temporal orders `0.98–1.40` at nx=16/32/64 | FE:208; main.tex:607 | `mms-convergence.json` `time.*.difference_orders`: nx16 `{ux 1.0932, uy 0.9783, p 1.0152}`, nx32 `{1.3969, 1.0183, 1.1252}`, nx64 `{1.3964, 1.0762, 1.2519}` ⇒ range [0.9783, 1.3969] | exact |
| step-refinement ratio `1.94`; errors `3.7e-3`, `7.1e-3` | FE:210; main.tex:604–605 | `figures/fe_mandel_refinement.csv` `linear_time_0.001 = 0.003657958974355574`, `linear_time_0.002 = 0.0071039215708695895`; ratio `= 1.9420` | exact |
| pressure floor `3.2e-3` at nx=20, dt=1e-3 | FE:214,233; main.tex:602 | `figures/fe_load_limit.csv` `nonlinear_load_0.0001 … 0.003220919735602341` | exact |
| fabric reconstruction diff `2.2e-16` | FE:271 | `site/reports/fabric-verification.json` `tensor_checks.H_reconstruction_max_abs_diff = 2.220446049250313e-16` | exact |
| `det H − 1 = −3.3e-16` | FE:271 | `tensor_checks.H_det_minus_one = -3.3306690738754696e-16` | exact |
| eigenvalues `h^{-2}, h, h` | FE:271 | `H_eigenvalues = [0.99928635…, 1.00035701…, 1.00035701…]` = `[h^-2, h, h]` with `h=1.00035701`, matching `H_eigenvalues_expected` | exact |
| `||D:e3|| = 1.6e-16` | FE:273 | `D4_e3_norm = 1.5823112613210482e-16` | exact |
| `D:e6 = 0` | FE:273 | `D4_e6_norm = 0.0` | exact |
| rotation invariance `2.5e-16` | FE:275 | `rotation_invariance_norm = 2.4965357070272594e-16` | exact |
| NumPy re-implementation worst diff `4.9e-15` | FE:279 | `worst_probe_abs_diff = 4.884981308350689e-15` | exact |
| volume-only limit `1.9e-14` | FE:287 | `conformal_cross_check.sigma11.abs_diff = 1.8741952434453424e-14` | exact |
| coupled Mandel peaks `4.36/4.99/5.52 e-5`, coupling-off `3.62e-5` | FE:312–314 | `fabric_mandel_coup_a0/a45/a90/iso` `analysis.json` `center_pressure = 4.3627593400865e-5 / 4.9900848305106e-5 / 5.521105069019e-5` vs `3.6163929824772e-5` | exact |
| "peak coincides with the final recorded state" | FE:315 | `figures/fe_fabric_mandel_peak.csv`: `peak_center_pressure == final_center_pressure` for all four cases | exact |
| refined contour peaks `3.61e-5` (iso) and `4.35, 4.97, 5.50 e-5` | FE:326–327 | `fabric_contour_*` `analysis.json` `center_pressure = 3.6061943087043e-5 / 4.3491366179057e-5 / 4.9726564036483e-5 / 5.5031354237468e-5` | exact |
| displacement peaks `5.18, 5.14, 2.38, 5.26 e-5` | FE:331–332 | `figures/fe_fabric_contours.csv` `u_mag_max = 5.1826395396202306e-5 / 5.13715515334801e-5 / 2.381836351578327e-5 / 5.258692042529596e-5` | exact |
| refined `40×8` mesh of `1×0.1` strip; **eleven** snapshots; final state `X_1=0` symmetry, zero at drained edge `X_1=1` | FE:318–331 | Exodus `fabric_contour_a0`: `num_elem=320` (40×8 QUAD9), `num_nodes=1377`, coordinates `[0,1]×[0,0.1]`, `time_step=11` at `0, 3e-4, …, 3e-3`; `p_max_x=0.0`, `p_min≈1e-130` | exact |
| diffusion figure "six recorded times" | FE:368 | `figures/fe_fabric_diffusion.csv` 6 rows per case | exact |
| rate `k/mu_f = 1.5` | FE:163 | `mandel-reference.json` `mobility = 1.5` | exact |
| "all plotted states satisfy positive phase volumes and the scalar stability condition" | experiments.tex:196 | `experiments.json` `solid_fraction_range [0.4343, 0.6000]` ⊂ (0,1); `min_scalar_stability = 28.0 > 0` | supported |
| Mandel reference "38 self-checks, peak overshoot 5.4659% at t=0.01516535" (site/evidence.json) | site/evidence.json:14 | `mandel-reference.json` `verification.checks` count 38; `central_overshoot = {ratio 1.0546586069998425, time 0.015165352045764979}` | exact (5.4659%, t=0.01517) |
| "fluid EOS … 110 checks, max scaled error 8.09e-09"; "C++ … 6.4e-14 over 41 finite states" (site/evidence.json) | site/evidence.json | `fluid-coupling-verification.json` `count=110`, `maximum_scaled_error=8.0867e-9`; `cpp-python-constitutive.json` `states=41`, `value_absolute_error=6.3949e-14` | exact |

**Independent recomputation of figure-input values.** From the shipped Exodus
bytes (netCDF4), not from the figure CSVs:

```
fabric_contour_iso: u_mag_max=5.182640e-05 (1,0.1) | p_max=3.606194e-05 (0,0.1)
fabric_contour_a0:  u_mag_max=5.137155e-05 (1,0.1) | p_max=4.349137e-05 (0,0.0125)
fabric_contour_a45: u_mag_max=2.381836e-05 (1,0)   | p_max=4.973659e-05 (0,0.1)
fabric_contour_a90: u_mag_max=5.258692e-05 (1,0.1) | p_max=5.503135e-05 (0,0.0125)
```

These match the manuscript and the figure CSVs to the printed precision.

**Isotropic shear modulus derivation (independent).** `trace(P·C_s)/10` with
`P = I − (1,1,1,0,0,0)⊗(1,1,1,0,0,0)/3` gives `168/10 = 16.8`; the five
eigenvalues of the deviatoric restriction are
`[20, 24, 28, 42.9668, 53.0332]`, whose mean is `33.6` and half is `16.8`. The
manuscript's "mean of the five deviatoric stiffness modes of `C_s`, divided by
two" is therefore exact under the deviatoric-restriction definition. Agreement: exact.

### 2.3 Conclusion of the number audit

No disagreement was found. Every quoted number reproduces from the frozen
artifacts at its stated precision.

---

## 3. Declared digest surfaces

All declared digests were re-hashed from the frozen bytes with an independent
`sha256sum`/`hashlib` invocation.

| Surface | Declared entries | Mismatches | Missing |
|---|---|---|---|
| `source-manifest.json` | 608 | 0 | 0 |
| `fe-evidence/manifest.json` `files[]` | 317 | 0 | 0 |
| `site/evidence.json` `artifacts[]` | 40 | 0 | 0 |
| `site/scientific-snapshot.json` `files[]` | 47 | 0 | 0 |
| `figures/fabric-plot-manifest.json` (in 15 / out 7) | 22 | 0 | 0 |
| `figures/fe_fabric_contours-plot-manifest.json` (in 5 / out 6) | 11 | 0 | 0 |
| `figures/fe-verification-plot-manifest.json` (in 6 / out 4) | 10 | 0 | 0 |
| supplement `build/anisotropic-biot-2026-09-20-v2.zip` internal `manifest.json` | 68 | 0 | 0 |

**Supplement archive.** `sha256 = ab993ee75fd3e087e19114fed9d3cc50996b587b908472e5ac96bcfdb5ee4d04`,
2 277 441 bytes, 69 members. The internal `manifest.json` declares 68 payload
digests; all 68 match the shipped bytes, none is declared-but-absent, and the
only unlisted member is `manifest.json` itself. Its `version` field is
`anisotropic-biot-2026-09-20-v2`, identical to `site/evidence.json` `version`.

**`fe-evidence/manifest.json` cross-checks.** `cases` (57) equals the 57
`runs/*` directories; `runs[]` has 57 entries; `not_applicable` (28) lists
run-local files deliberately not shipped. All 317 `files[]` entries verify.

---

## 4. Figure-input provenance (Exodus inputs), independent command

The four refined contour decks are the direct inputs of
`fe_fabric_contours`/`fe_fabric_diffusion`. Independent command:

```
$ sha256sum fe-evidence/runs/fabric_contour_iso/solution.e \
            fe-evidence/runs/fabric_contour_a0/solution.e \
            fe-evidence/runs/fabric_contour_a45/solution.e \
            fe-evidence/runs/fabric_contour_a90/solution.e
3dfe02ae921075727d0999c83fd9991562cbc1a660096e80ebfd35a7ebaedcad  …/fabric_contour_iso/solution.e
e615b78160aeb0fcc89cfae7f9d7ef94cf53177ed0f08e439aff927cd590ee52  …/fabric_contour_a0/solution.e
2ab3a3ca95c0023c54cc8fda56ea2092be0989fcd19359f63ceb81b4adb7fd53  …/fabric_contour_a45/solution.e
8eb00e29510deb943fef9c714a3a12c43eda15d4cdfc52c12c55e59704f75e00  …/fabric_contour_a90/solution.e
```

These match `figures/fe_fabric_contours-plot-manifest.json`
`input_sha256` entry-for-entry, and the declared output hashes
(`fe_fabric_contours.csv/.pdf/.png`, `fe_fabric_diffusion.csv/.pdf/.png`)
also match. Note that `source-manifest.json` itself lists these `solution.e`
files (they are the only Exodus files shipped), so the digest chain
snapshot → manifest → plot-manifest → figure CSV is closed end to end.

---

## 5. Run provenance

For each of the 57 `fe-evidence/runs/<case>/provenance.json` records I checked
declared source digests, the input-deck digest, the binary digest, and any
declared `git_revision`.

| Check | Result |
|---|---|
| `input_sha256` equals the shipped `runs/<case>/input.i` | **57 / 57 match** |
| `input_sha256` equals the shipped `moose_app/inputs/<input_deck>` where the deck and the `input_deck` field are both present (19 runs) | **19 / 19 match**; 38 runs declare no `input_deck`/overrides |
| declared `source_sha256` entries verified against the snapshot sources | **513 / 513 match**, 0 missing |
| `binary_sha256` verifiable from the snapshot | **not shipped** (documented in `fe-evidence/manifest.json` note 3 and `fe-evidence/README.md`) |
| distinct declared `git_revision` values | 2: `40a49aee…` (42 runs), `b6d72721…` (15 runs) |

**Revision verification (read-only git object-database queries).** Both
revisions exist as commits, and every declared source path in each revision's
declared set resolves in that revision's tree to bytes whose SHA-256 equals the
recorded digest:

```
$ git cat-file -t 40a49aeed3c02e074029f2ec6f75b4b444ded9a4   -> commit   (15 paths: problems none)
$ git cat-file -t b6d72721414a0c09aa6492465acd3a4c8d07e31b   -> commit   (3 paths:  problems none)
$ for f in moose_app/include/utils/FabricLaw.h \
           moose_app/include/materials/FabricMaterial.h \
           moose_app/src/materials/FabricMaterial.C; do
    git cat-file blob 40a49aee…:$f | sha256sum; done
761334c6…497961  FabricLaw.h        (recorded 761334c6…497961) ✓
7e70dde1…5f74    FabricMaterial.h   (recorded 7e70dde1…5f74)   ✓
9abcfab6…30c2    FabricMaterial.C   (recorded 9abcfab6…30c2)   ✓
```

No record declares a revision whose tree lacks the recorded sources. The
`git_revision_basis` field honestly states that the harness did not record a
revision at run time, so the pin is "the revision whose sources match, not
necessarily the revision the run was made from"; the "sources match" part is
verified true.

**`site/evidence.json` `source_revision`.** The declared
`a0e268c81daf1a59f78201a98778a7d542c444fe` exists
(`commit`, dated 2026-09-21) and its tree contains the shipped FE/figure sources
byte-for-byte (`FabricMaterial.C`, `FabricLaw.h`, `examples/verify_fabric.py`
all re-hash equal). The manuscript's claim (experiments.tex:213–216) that the
evidence file "records the inspected source revision and pins the SHA-256 hashes
of the files it reports" is therefore supported.

---

## 6. Reproducibility of the recorded field files

What is and is not reproducible across runs, with evidence from the frozen bytes:

**Not reproducible (environment/time dependent):**
1. **Run wall clock.** Every shipped `solution.e` carries a `Current Time:`
   information record (e.g. `Mon Sep 21 18:21:04 2026` for `fabric_contour_a0`).
2. **Executable timestamp.** An `Executable Timestamp:` record (`Sun Sep 20
   23:20:55 2026`) plus a `MOOSE Version` line (`git commit abafb58b on 2026-02-20`).
3. **Absolute host path of the deck.** An `Input File(s):` record holds
   `  /home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/...`
   (truncated to the 80-char line width). Because the path is absolute, the raw
   bytes differ across machines and checkouts as well as across runs.

Consequently the raw `sha256` of each Exodus file is not stable across
regenerations, which is exactly why `fe_fabric_contours-plot-manifest.json`
records the *current* Exodus digests and is regenerated with the decks.

**Stable by construction:** the Exodus `title` attribute is the literal string
`solution.e` in all four files (the decks write with a relative output base), so
the title is not a temporary host path; the mesh, timesteps, and field arrays
(`p`, `ux`, `uy`, `force_reaction`, `mass_reaction`, element `J`, `Jbar`,
`energy`, `sigma11/22`, `solid_fraction`, `stability`) are pure solver output;
the companion histories (`solution.csv`, `figures/*.csv`) are plain-text
full-precision records and reproduce the numeric fields.

**Documentation accuracy.** The shipped documentation describes the residual
but does not describe it completely:

- `figures/fe_fabric_contours-plot-manifest.json` `limitations[4]` says the
  Exodus files "embed a per-run wall-clock line in their information records, so
  their raw bytes are not reproducible across runs". True, but incomplete: the
  same records also embed the executable timestamp, the MOOSE version, and an
  absolute host path, so the bytes are also not reproducible across *machines*.
- `README.md:105–110` explains the relative output base / stable `title` and the
  wall-clock digest change, but likewise does not mention the embedded absolute
  path.
- `README.md:107` asserts "The recorded field arrays are bit-identical across
  regenerations". This cannot be independently confirmed from the frozen
  snapshot, which contains exactly one generation per file; it is an asserted
  property, not frozen evidence. (It is plausible and consistent with the fixed
  solver, deck, and binary, but it is not verifiable here.)

Neither statement is false as written (each names a sufficient cause), so this is
a completeness matter, not a correctness defect — see **R2-O1**.

---

## 7. Do the recorded evidence support each scope claim?

The manuscript's scope-limiting claims were checked against the artifacts:

| Scope claim | Evidence | Supported |
|---|---|---|
| Constitutive/material-point and FE *implementation* verification only; "no quantitative finite-deformation verification and no experimental validation" (abstract; FE §*Scope of these results*) | `materialize`/`README` states these are synthetic; `finite-deformation-summary.json` note; `fe-evidence/README.md`; `site/evidence.json` `finite_deformation="pending"`, `physical_validation="not_performed"` | yes |
| The finite-load floor is a discretization floor, not a verified limit | `fe_load_limit.csv` non-decaying `pressure_max_normalized` 0.00322→0.00345→0.00571 as load increases; quantified as such | yes |
| Temporal orders reported as measurements, no order above one asserted | `mms-convergence.json` difference orders 0.978–1.397; `fe-verification-plot-manifest.json` `limitations[1]`; `site/evidence.json` convergence summary explicitly withdraws any order above one | yes |
| The fabric law is checked at the material point against a re-implementation sharing the modelling conventions, not an independent derivation | `fabric-verification.json` + `fe-evidence/README.md`; FE:279–282 states the shared-convention caveat; `site/reports/fabric-verification.json` `source_sha256` points to `examples/verify_fabric.py` | yes |
| Pore-fabric runs are force-controlled demonstrations on synthetic, uncalibrated moduli, not validation | `provenance.json` `command`/`configuration`; `finite-deformation-summary.json` note; FE §*Scope of these results* | yes |
| Rotated-anisotropy/partial-drainage runs are equilibrium demonstrations; partial family uses a square domain and is "not comparable" and excluded | `partial_0/30` `configuration.nx=ny=12` (square); `anisotropic_*` `nx=16, ny=4`; `site/evidence.json` `finite_deformation` text | yes |
| Note the shipped evidence is the authoritative frozen artifact over the repository `site/` copy | the `site/` copies hash-match their declares here | yes |

No scope claim oversells the recorded evidence. Where the manuscript claims
verification, the claim is exactly the constant-reference-tangent / MMS /
material-point checks that the artifacts record.

---

## REQUIRED changes

**None.** I found no numerical disagreement, no digest mismatch, no missing or
unlisted file (beyond the two self-exclusion cases), no provenance record whose
revision fails to contain its sources, and no scope claim unsupported by the
recorded evidence. The frozen snapshot is internally consistent to the
precision the manuscript reports.

## OPTIONAL notes

- **R2-O1 — `figures/fe_fabric_contours-plot-manifest.json` `limitations[4]`
  (and `README.md:105–110`).** The reproducibility residual is under-described.
  Beyond the per-run wall-clock line, each shipped Exodus also embeds an
  `Executable Timestamp`, the MOOSE version, and an **absolute host path** in an
  `Input File(s):` record (verified in
  `fe-evidence/runs/fabric_contour_a0/solution.e`, info record 12). Adding
  "and an absolute input-path record" to the limitation would make the
  environment dependence (across machines/checkouts, not only across runs)
  explicit.
- **R2-O2 — `README.md:107`.** "The recorded field arrays are bit-identical
  across regenerations" is asserted but not evidenced in the frozen snapshot
  (one generation per file). If retained, consider marking it as an asserted
  reproduction property, or ship a second-generation field-array hash to
  substantiate it.
- **R2-O3 — `fe-evidence/manifest.json` `notes`.** Notes 5 and 7 (0-based
  indices 4 and 6) both describe the `runs/fabric_*` records and conflict on one
  point: one says their `provenance.json` records `application_sha256` "rather
  than `binary_sha256`", while the other says they record "the compiled binary
  digest". All 19 fabric/conformal `provenance.json` records in fact carry both
  `application_sha256` and `binary_sha256` (equal, e.g. `ff0272fc…`). The
  near-duplicate notes should be reconciled to a single accurate statement.
- **R2-O4 — `sections/experiments.tex:29`.** "the mean of the five deviatoric
  stiffness modes of `C_s`, divided by two" is exact (= 16.8) under the
  deviatoric-*restriction* definition used by `examples/conformal_model.py:78`
  (`trace(P·C_s)/10`), but is ambiguous: the mean of the five *largest-eigenvalue-
  complement* kernel eigenvalues of the 6×6 Mandel matrix gives 16.58. A half-
  clause ("the five eigenvalues of the deviatoric restriction of `C_s`") would
  remove the ambiguity. Purely presentational; no value changes.
- **R2-O5 — `site/evidence.json` `provenance.source_revision`.** The pinned
  revision `a0e268c8…` predates the current manuscript HEAD and its subject line
  references round 32. It is internally honest ("The base commit predates this
  working revision") and its tree contains the shipped sources byte-for-byte, so
  the FE attribution is sound; but a reader cannot map the evidence to the
  manuscript revision from this field alone. Consider also recording the
  manuscript revision the evidence file was regenerated against.

---

VERDICT: ACCEPT

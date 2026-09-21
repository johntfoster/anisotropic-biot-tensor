# SIMULATED AI PEER REVIEW — Reviewer 2

**Role:** Reviewer 2 of 3, final manuscript acceptance review (numerical verification and source fidelity).
**Nature:** This is a simulated AI peer review. It is not journal peer review and confers no acceptance.
**Frozen snapshot reviewed:** `.agent-runtime/review-snapshots/round-33`
**Declared SNAPSHOT_ID:** `7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53`
**Report path:** `reviews/round-33/reviewer-2.md`

---

## 1. Mandatory first checks

### 1.1 Snapshot hash equals the declared SNAPSHOT_ID

Command and result:

```
$ sha256sum source-manifest.json
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53  source-manifest.json

$ cat SNAPSHOT_ID
7e75f419a105318fb1bec98caa19469a63f34efd25d41b79fb8ae055f37e3e53
```

**PASS.** `sha256(source-manifest.json)` equals the declared `SNAPSHOT_ID` exactly, and the `SNAPSHOT_ID` file holds the identical 64-hex string.

### 1.2 Re-hash of every `source-manifest.json` entry

`source-manifest.json` is a flat `path -> sha256` mapping. Every listed path was read from the frozen snapshot and re-hashed with `hashlib.sha256`; the tree was then walked for unlisted files.

```
manifest type: dict
entry count: 608
re-hashed ok: 608
missing on disk: 0
mismatches: 0
files present: 610
unlisted count: 0
```

**PASS.** 608/608 entries re-hash to the declared value; 0 listed files missing; 0 mismatches; 610 files present on disk = 608 manifest entries + `source-manifest.json` + `SNAPSHOT_ID` (which cannot list themselves); **0 files present but unlisted** anywhere in the tree.

### 1.3 Independence declaration

I declare:

- I did **not** open, read, `cat`, `less`, or grep the contents of any file under `reviews/`, including `reviews/README.md`.
- I did **not** read, list, glob, or `find` any **other** `.agent-runtime/review-snapshots/round-*` directory. The only snapshot directory touched was `.../round-33` and its contents.
- I did **not** read any other reviewer's report and did **not** read any verdict line or acceptance count.

Self-reported incidental exposure (no report content read):

- The filename `reviews/README.md` is itself an entry of the snapshot `source-manifest.json`, and therefore appeared in the mandatory manifest read of §1.2. Its **contents were not opened**.
- During the mandatory tree walk of §1.2 and one `grep -rln` scoped to the round-33 snapshot root, the path `reviews/README.md` was printed as a filename. Only the filename was exposed; no content was read.
- While creating my own output path I listed the **working-tree** directory `reviews/` (which contains `round-*` subdirectory names and `foster-cycle-*` names). This was a directory listing only: **no file was opened**, and no reviewer report, verdict, or acceptance count was read. I did not open `reviews/round-33/LAUNCH-STATE.md` or any other file there.

No reviewer report or acceptance/verdict information was exposed to me. My vote is independent.

---

## 2. Scope for this reviewer's emphasis: numerical verification and source fidelity

All amounts below were recomputed independently from the frozen artifacts. Independent recomputation used `numpy` (matrix algebra for the constitutions) and `netCDF4` (Exodus inspection); no held numerical suite (`validation/`, `examples/verify_*.py`) was executed.

### 2.1 Constitutive and reference values (`sections/experiments.tex`, `sections/limits.tex`)

| Manuscript value | Location | Independent recomputation | Result |
|---|---|---|---|
| Reference Biot components 0.7000, 0.7583, 0.7917 | experiments.tex:25 | `B0 = I - C^d:C_s^-1:I` with `C_s` from eq (example-mineral-stiffness), `C^d` from eq (drained-stiffness-restriction) | **agree** (0.7, 0.7583333, 0.7916667) |
| `K_s = 28 K_*` | experiments.tex:22 | `(1/9) I:C_s:I = 252/9` | **agree** |
| `K = 7 K_*`, `phi_s0 = 0.6`, `0<K<phi_s0 K_s` | experiments.tex:20–22 | `(1/9) I:C^d:I = 7`; `16.8 = phi_s0 K_s > 7` | **agree** |
| Isotropic mineral shear modulus `16.8 K_*` = mean of five deviatoric modes / 2 | experiments.tex:29 | `trace(P_dev C_s P_dev)/5/2 = 240/5/2` | **agree** |
| Isotropy preservation (`K_s`, `K`, `phi_s0` shared) | experiments.tex:27–30 | isotropic `C_s` has `Ks=28`, `mu=16.8` (`conformal/experiments.json`) | **agree** |

### 2.2 Conformal verification-suite counts and error (`sections/experiments.tex`)

| Manuscript value | Location | Artifact | Result |
|---|---|---|---|
| 186 named checks | experiments.tex:181 | `site/reports/conformal-verification.json` `checks_passed=186`, `checks` dict has 186 entries | **agree** |
| 65 per-state identities = 5 states × 13 | experiments.tex:182 | 5 `legacy_state{0..4}` × 13 identity names = 65 | **agree** |
| two reference Biot / rank-one compliance relations | experiments.tex:183–184 | `legacy_reference_biot`, `legacy_reference_rank_one_compliance_identity` | **agree** |
| largest constitutive-identity error `2.5e-9` | experiments.tex:187 | `max_constitutive_identity_error=2.4549890331732928e-09` | **agree** |
| 273 finite states across 13 mineral stiffnesses (spherical gauge) | experiments.tex:192 | `tensor-verification.json`: `materials=13`, `states_per_material=21`, `total_states=273` | **agree** |
| second-order step refinement (energy, pore volume, pressure) | experiments.tex:188–189 | `observed_orders` ≈ 2.0000 (finest pressure 1.989) | **agree** |
| reconstruction suite (work equivalence, finite unjacketed) | experiments.tex:193 | `reconstruction-verification.json` `errors.work_equivalence=5.04e-10`, `errors.unjacketed=5.09e-14` | **agree** |
| Lambert checks on admissible negative- and large positive-pressure states | experiments.tex:205–207 | `branch_pressure_-14`, `branch_pressure_-13`, `branch_pressure_800` in conformal report | **agree** |

### 2.3 Sampling and snapshot counts

| Manuscript value | Location | Artifact | Result |
|---|---|---|---|
| 121 pressure states, `0 ≤ p/K_* ≤ 6` | experiments.tex:55 | `build/conformal/pressure_response.csv` = 1 header + 242 = 121×2 | **agree** |
| 161 equally spaced `gamma` values | experiments.tex:86 | `shear_response.csv` = 161×2 rows | **agree** |
| directional response at one-degree intervals | experiments.tex:115 | `directional_response.csv` = 361×3 rows | **agree** |
| 121 angles 0–180° | experiments.tex:140 | `rotation_response.csv` = 121×2 rows | **agree** |
| 121 layer pressure points | experiments.tex:163 | `constrained_layer.csv` = 121×2 rows | **agree** |
| eleven evenly spaced field snapshots | finite_elements.tex:322 | Exodus `time_step` dim = 11, `time_whole = 0…0.003` step 0.0003 | **agree** |
| six recorded times (diffusion) | finite_elements.tex:369 | `fe_fabric_diffusion.csv` = 6 times (0, .0006, .0012, .0018, .0024, .003) | **agree** |
| refined `40×8` mesh on the `1×0.1` strip | finite_elements.tex:320 | Exodus `num_elem=320`, QUAD9; provenance `mesh="nx=40 ny=8 on [0,1] x [0,0.1] (QUAD9)"` | **agree** |

### 2.4 Finite-element reference values and convergence (`sections/finite_elements.tex`)

| Manuscript value | Location | Artifact | Result |
|---|---|---|---|
| `phi_s0=0.9, K_s=2.5, mu_s=5/6, K=1, K_f=8, rho_f0=1, k/mu_f=1.5` | finite_elements.tex:160–163 | `site/reports/mandel-reference.json` (`G=0.75`, `alpha=0.6`, `mobility=1.5`, `a=1, b=0.1`) | **agree** |
| drained shear `G=0.75` | finite_elements.tex:164 | `phi_s0 mu_s = 0.9·(5/6)=0.75` | **agree** |
| reference Biot `0.6` | finite_elements.tex:165 | `1 - K/K_s = 1 - 1/2.5 = 0.6` | **agree** |
| total storage `17/80` | finite_elements.tex:166 | `Ss=0.2`, `(1-phi)/K_f=0.0125`, sum `0.2125 = 17/80`; `M=4.70588=80/17` | **agree** |
| MMS orders: p 2.00/2.00, ux 2.99/2.96, uy 3.00/2.96 | finite_elements.tex:203–205 | `mms-convergence.json` `space.orders.*.naive_orders` | **agree** (1.9966/2.0008, 2.9917/2.9585, 2.9983/2.9600) |
| temporal orders 0.98–1.40 | finite_elements.tex:208 | `time.*.difference_orders` over nx=16/32/64 | **agree** (min 0.97830, max 1.39688) |
| step-refinement 3.7e-3 and 7.1e-3, ratio 1.94 | finite_elements.tex / main.tex:600–601 | `figures/fe_mandel_refinement.csv` (`linear_time_0.001`=3.65796e-3, `linear_time_0.002`=7.10392e-3, ratio 1.9420) | **agree** |
| pressure floor ≈ 3.2e-3 at load 1e-4 | finite_elements.tex / main.tex:598 | `figures/fe_load_limit.csv` (`nonlinear_load_0.0001`=3.22092e-3; 1e-3→3.44787e-3; 1e-2→5.70599e-3) | **agree** (monotone toward a nonzero floor) |

### 2.5 Fabric reconstruction and coupled peaks (`sections/finite_elements.tex`)

| Manuscript value | Location | Artifact | Result |
|---|---|---|---|
| `H` reconstruction differs by `2.2e-16` | finite_elements.tex:271 | `tensor_checks.H_reconstruction_max_abs_diff=2.220446049250313e-16` | **agree** |
| `det H - 1 = -3.3e-16`, eigenvalues `h^-2, h, h` | finite_elements.tex:271–272 | `H_det_minus_one=-3.33067e-16`; eigenvalues `[0.99928635, 1.00035701, 1.00035701]` | **agree** |
| `||D:e3|| = 1.6e-16`, `D:e6 = 0` | finite_elements.tex:273 | `D4_e3_norm=1.58231e-16`, `D4_e6_norm=0.0` | **agree** |
| rotation invariance `2.5e-16` | finite_elements.tex:275 | `rotation_invariance_norm=2.49654e-16` | **agree** |
| independent NumPy worst difference `4.9e-15` | finite_elements.tex:279 | `worst_probe_abs_diff=4.88498e-15` | **agree** |
| volume-only limit `1.9e-14` | finite_elements.tex:287 | `conformal_cross_check` max abs diff `1.87420e-14` | **agree** |
| coupled peaks 4.36/4.99/5.52e-5 vs 3.62e-5 uncoupled; peak = final state | finite_elements.tex:312–315 | `fe_fabric_mandel_peak.csv` (4.36276e-5, 4.99008e-5, 5.52111e-5, 3.61639e-5; peak≡final for all) | **agree** |
| contour peaks 3.61/4.35/4.97/5.50e-5; max on `X1=0`; zero at `X1=1` | finite_elements.tex:326–329 | `fe_fabric_contours.csv` (3.60619e-5, 4.34914e-5, 4.97366e-5, 5.50314e-5; `p_max_x=0.0`; `p_min≈0`) | **agree** |
| displacement peaks 5.18/5.14/2.38/5.26e-5 | finite_elements.tex:331–332 | `fe_fabric_contours.csv` (5.18264e-5, 5.13716e-5, 2.38184e-5, 5.25869e-5) | **agree** |

No quoted number disagreed with its artifact.

---

## 3. Digest-surface audit

Every declared digest surface was re-hashed from the frozen bytes.

| Surface | Entries | Result |
|---|---|---|
| `source-manifest.json` | 608 | 608 OK, 0 mismatch, 0 missing, 0 unlisted (§1.2) |
| `fe-evidence/manifest.json` `files[]` | 317 | 317 OK (sha256 **and** byte size), 0 missing; only `fe-evidence/README.md` present-but-unlisted locally (it is listed in `source-manifest.json`) |
| `fe-evidence/runs/*/provenance.json` `outputs` | 3533 declared | 114 shipped: **114/114 OK**; 3419 declared-but-unshipped (see §4) |
| `fe-evidence/runs/*/provenance.json` `source_sha256` | 513 records / 15 distinct paths | 513 OK, 0 mismatch, 0 missing |
| `fe-evidence/runs/*/provenance.json` `input_sha256` | 57 | 57 OK (all equal the shipped `input.i`) |
| `site/evidence.json` `artifacts[]` | 40 | 40 OK, 0 mismatch, 0 missing |
| `site/scientific-snapshot.json` `files[]` | 47 | 47 OK, 0 mismatch, 0 missing |
| supplement `build/anisotropic-biot-2026-09-20-v2.zip` internal `manifest.json` | 68 | 68/68 OK; only `manifest.json` itself unlisted (cannot self-hash) |
| `figures/fabric-plot-manifest.json` | 15 in / 8 out | all OK |
| `figures/fe_fabric_contours-plot-manifest.json` | 5 in / 6 out | all OK |
| `figures/fe-verification-plot-manifest.json` | 6 in / 4 out | all OK |
| report-embedded `source_sha256` (conformal, fluid-coupling, mandel) | 5 | all OK against shipped sources |
| report-embedded artifact digests (mandel-probes/profiles) | 2 | OK |

**No digest mismatch was found on any surface.**

### 3.1 Figure-input provenance for the four contour Exodus files

Independent command (`sha256sum`), compared with the declared `input_sha256` in `figures/fe_fabric_contours-plot-manifest.json`:

```
e615b78160aeb0fcc89cfae7f9d7ef94cf53177ed0f08e439aff927cd590ee52  fe-evidence/runs/fabric_contour_a0/solution.e
2ab3a3ca95c0023c54cc8fda56ea2092be0989fcd19359f63ceb81b4adb7fd53  fe-evidence/runs/fabric_contour_a45/solution.e
8eb00e29510deb943fef9c714a3a12c43eda15d4cdfc52c12c55e59704f75e00  fe-evidence/runs/fabric_contour_a90/solution.e
3dfe02ae921075727d0999c83fd9991562cbc1a660096e80ebfd35a7ebaedcad  fe-evidence/runs/fabric_contour_iso/solution.e
```

All four match the manifest exactly. **PASS.**

### 3.2 Run provenance and revision fidelity

- Each `provenance.json` declares `source_sha256`, `input_sha256`, and `binary_sha256` (or `application_sha256` for the fabric runs).
- **Source digests:** all 15 distinct recorded source paths were extracted read-only from the repository object database at the recorded `git_revision` `40a49aeed3c02e074029f2ec6f75b4b444ded9a4` and hashed. 15/15 equal the recorded values; no recorded revision's tree lacks a recorded source.
- **Input-deck digests:** 57/57 match the shipped `input.i`.
- **`git_revision`:** `40a49ae` resolves, is a commit, and is an ancestor of `HEAD` (`a0e268c`). The provenance itself honestly qualifies it (`git_revision_basis`: "the revision whose sources match, not necessarily the revision the run was made from").
- **Binary digest:** `binary_sha256 = ff0272fc…` is declared but the binary is **not shipped**, so it is not verifiable from the snapshot. This is disclosed in `fe-evidence/manifest.json` notes ("The binary is not shipped").
- The FE source blobs are byte-identical at `40a49ae`, at the site's `provenance.source_revision` `8d83726`, and at `HEAD` for all 15 files, so the two recorded revision strings do not disagree about source content.

---

## 4. Reproducibility of the recorded field files (Exodus)

**What is not reproducible:** each Exodus `solution.e` embeds run wall-clock strings in its information records. Verified by reading the frozen bytes with `netCDF4`:

```
fabric_contour_iso: 'Current Time:            Mon Sep 21 18:20:51 2026'
                    'Executable Timestamp:    Sun Sep 20 23:20:55 2026'
fabric_contour_a0:  'Current Time:            Mon Sep 21 18:21:04 2026'
fabric_contour_a45: 'Current Time:            Mon Sep 21 18:21:16 2026'
fabric_contour_a90: 'Current Time:            Mon Sep 21 18:21:29 2026'
```

So the raw file digest changes per run even when the numerics do not.

**What is reproducible:** the time grid (`time_whole` = 0 … 0.003, 11 steps) and the field arrays (`vals_nod_var*`, `vals_elem_var*`, `coordx/coordy`, connectivity, maps) are deterministic given identical binary, inputs, and thread count; the Exodus `title` is the stable relative string `solution.e`.

**Does the shipped documentation describe this residual accurately?** Yes, in two places:

- `figures/fe_fabric_contours-plot-manifest.json` `limitations`: "The recorded Exodus files embed a per-run wall-clock line in their information records, so their raw bytes are not reproducible across runs; the recorded CSV histories and the field arrays are."
- `README.md` (repo root): "The recorded field arrays are bit-identical across regenerations; the framework header echoed into the Exodus information records carries the run wall clock, so the raw file digest changes with the run time even though the fields do not…".

The supplement archive `README.md` states the general point more weakly ("Floating-point and PDF metadata differences between platforms need not reproduce archive bytes"), but the specific Exodus residual is documented where it matters (the manifest that hashes those files). The description is **accurate**.

An incidental observation (does not affect any manuscript claim): `num_info` differs by one line between `fabric_contour_iso` (1640) and the other three (1639). Since the information records are not hashed into any claim and the field arrays are what the figures read, this is immaterial.

---

## 5. Whether the recorded evidence supports each scope claim

| Scope claim | Location | Supporting evidence | Result |
|---|---|---|---|
| FE implementation verified against a manufactured solution for the constant reference tangent | abstract, finite_elements.tex | `mms_space_*` decks are `linear=true, angle=30`, exact-field MMS; measured orders match | **supported** |
| Constant-coefficient consolidation reference in the same limit | finite_elements.tex §fe-reference-problems | `linear_space_*`, `linear_time_*` quarter-domain decks; `mandel-reference.json` independent series (`passed=true`) | **supported** |
| No *quantitative* finite-deformation verification claimed | abstract, finite_elements.tex §scope | finite-load panels reported as floor/demonstration only (`fe_load_limit.csv`) | **supported (honest restriction)** |
| Rotated-anisotropy, partial-drainage are demonstrations, not comparable to the slender reference | finite_elements.tex §scope | `finite-deformation-summary.json` note; `not_applicable` / `reference_note` fields | **supported** |
| Fabric law checked at the material point vs a separate re-implementation sharing conventions | finite_elements.tex:275–287 | `fabric-verification.json` `worst_probe_abs_diff=4.88e-15`; conformal cross-check `1.87e-14` | **supported** |
| Pore-fabric coupling demonstrated in a coupled calculation | finite_elements.tex:312 | `fe_fabric_mandel_peak.csv` directional spread (3.62→5.52e-5) | **supported** |
| Synthetic parameters; no experimental validation | abstract, evidence.json limitations | `site/evidence.json` limitations list | **supported** |
| Repository records parameters, paths, residuals, versions, figure data | experiments.tex:194–196 | `provenance.json`, `analysis.json`, manifests, `versions` blocks; all digests verified | **supported** |

---

## 6. REQUIRED changes

None. I found no numerical error, no digest mismatch, no unsupported claim, and no misleading statement in the frozen snapshot within this reviewer's emphasis.

## 7. OPTIONAL notes

- **R2-O1 (`site/evidence.json`, `provenance` block).** The site declares `source_revision = 8d8372606cab…`, while every run record declares `git_revision = 40a49ae…`. Both trees contain byte-identical FE sources (verified), and the accompanying `note` explains the distinction, so this is not a defect. It could still read more clearly if the note stated explicitly that the recorded run revision predates the site's base commit and that the sources are unchanged between them.
- **R2-O2 (`fe-evidence/manifest.json`, notes).** 3419 of 3533 declared per-run outputs are intentionally unshipped, so their declared digests cannot be confirmed from the snapshot. This is disclosed ("provenance_outputs_unshipped records the difference per case") and the 114 shipped outputs all verify; no action needed beyond keeping the disclosure.
- **R2-O3 (provenance records).** `binary_sha256` is declared but the binary is not shipped, so it is unverifiable; already disclosed. If bit-level binary reproducibility ever becomes an acceptance claim, a checksummed binary or a build recipe with pinned toolchain would be required.
- **R2-O4 (Exodus `num_info`).** The one-line difference in information-record count between the isotropic and coupled contour files is immaterial to all claims; noting it only for completeness.
- **R2-O5 (self-report).** As recorded in §1.3, my only exposure to non-reviewed paths was filename-level (manifest entry, tree walk, and a working-tree directory listing). No report content, verdict, or acceptance count was read.

---

## 8. Summary

- Snapshot integrity: 608/608 manifest entries re-hash exactly; declared `SNAPSHOT_ID` confirmed twice; 0 unlisted files.
- Every manuscript-quoted number recomputes to the recorded artifact value: reference Biot components, `K_s`, the five-mode isotropic shear modulus 16.8, check counts (186/65/273/13), the `2.5e-9` largest constitutive error, sampling and snapshot counts, the FE reference values, the MMS/temporal orders, the 1.94 step-refinement ratio, the `3.2e-3` pressure floor, the pore-fabric reconstruction residuals and eigenvalues, the coupled and contour peaks, and the displacement peaks.
- Every declared digest surface (manifests, provenance, site evidence, scientific snapshot, supplement archive, plot manifests, report-embedded digests) verifies against shipped bytes; the four Exodus figure inputs verify independently.
- Revision fidelity holds: recorded source digests match the repository tree at the recorded revision, and the revision exists and is an ancestor of `HEAD`.
- The Exodus reproducibility residual is stated accurately in the shipped documentation.
- The recorded evidence supports each scope claim, and the manuscript correctly restricts its finite-deformation and validation claims.

VERDICT: ACCEPT

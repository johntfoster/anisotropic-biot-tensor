# Reviewer 2 report — ROUND 36 (simulated AI peer review)

Seat: **numerical verification and source fidelity**.
Snapshot under review: `.agent-runtime/review-snapshots/round-36`
Declared `SNAPSHOT_ID`: `c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d`
This is a simulated review; it confers no acceptance.

All manuscript, evidence, and code reads were taken from the frozen snapshot. No manuscript,
evidence, or code file was modified.

---

## Mandatory first checks

### Check 1 — snapshot identity

```
$ cd .../review-snapshots/round-36
$ cat SNAPSHOT_ID
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d
$ sha256sum source-manifest.json
c1f6210d5e2649986693d3dc0c26dccc072434c166148bbdc89e3f874ce4644d  source-manifest.json
```

Both equal the declared `SNAPSHOT_ID`. **PASS.**

### Check 2 — full re-hash of the manifest and tree walk

```
$ python3  # (script: hash every source-manifest.json path; walk tree excluding reviews/)
entries listed: 608
re-hashed OK:   608
hash mismatches: 0
listed-but-missing: 0
present files (excl. reviews/ subtree): 609
present-but-unlisted: SNAPSHOT_ID, source-manifest.json
```

Result: **PASS.** Every one of the 608 listed paths re-hashed to its recorded digest; no
mismatch and no missing file. The only two files present but unlisted are `SNAPSHOT_ID` and
`source-manifest.json` themselves, which are necessarily self-referential. No other unlisted
file exists outside `reviews/`.

### Check 3 — independence

I did not open, read, glob, or find any file *content* under `reviews/`, and I did not open any
other `.agent-runtime/review-snapshots/round-*` directory. To satisfy Check 2 the manifest loop
computed the SHA-256 of `reviews/README.md` (the single `reviews/` path that appears in the
snapshot manifest) by digest only; its bytes were never displayed or read. The tree walk for
"present-but-unlisted" deliberately pruned the whole `reviews/` subtree.

**Self-reported accidental exposure:** while creating my output directory I ran
`ls -la .../reviews/`, which printed the top-level directory *names* of the working-tree
`reviews/` folder (`foster-cycle-1/`, `foster-r24-cycle-1/`, …). Only names were shown; no
report file was opened and no other reviewer's verdict, report text, or acceptance count was
seen. I did not read or list anything inside those directories, and the listing is not used
anywhere in this report.

---

## Verification performed (all reads from the snapshot)

### A. Numerical claims in `main.tex` and `sections/*.tex` vs frozen artifacts

Every quoted number, range, and figure value I could locate in the frozen artifacts agrees.

| Claim (location) | Quoted | Frozen artifact | Agrees |
|---|---|---|---|
| Reference Biot components `experiments.tex:25` | 0.7000 / 0.7583 / 0.7917 | recomputed from printed matrix | yes |
| Isotropic mineral shear modulus `experiments.tex:29` | 16.8 K* | mean of 5 deviatoric modes ÷ 2 (recomputed = 16.8) | yes |
| K_s `experiments.tex:22` | 28 K* | `I:C_s:I/9` = 28 | yes |
| Pressure states `experiments.tex:55` | 121 | `build/conformal/pressure_response.csv` = 121/material | yes |
| Shear samples `experiments.tex:86` | 161 | `shear_response.csv` = 161/material | yes |
| Rotation angles `experiments.tex:140` | 121 over 0–180° | `rotation_response.csv` = 121/mode | yes |
| Conformal suite size `experiments.tex:181` | 186 named checks | `build/conformal/verification.json` `checks_passed`=186 | yes |
| Per-state identities `experiments.tex:182` | 65 (5×13) | 65 `legacy_state*` keys, 13 each | yes |
| Max constitutive error `experiments.tex:187` | 2.5×10⁻⁹ | `max_constitutive_identity_error`=2.4549890…e-09 | yes |
| Tensor suite `experiments.tex:191` | 273 states / 13 stiffnesses | `tensor-verification.json` 13×21=273 | yes |
| FE parameters `finite_elements.tex:161-163` | φ_s0=0.9, K_s=2.5, μ_s=5/6, K=1, K_f=8, ρ_f0=1, k/μ_f=1.5 | `validation/reference-data/README.md:70` | yes |
| Drained shear `finite_elements.tex:164` | G=0.75 | φ_s0·μ_s (recomputed) = 0.75 | yes |
| Reference Biot FE `finite_elements.tex:165` | 0.6 | 1−K/K_s (recomputed) = 0.6 | yes |
| Total storage `finite_elements.tex:166` | 17/80 | recomputed 0.2125; `M`=1/(17/80)=4.705… | yes |
| MMS spatial orders `finite_elements.tex:203-205` | p 2.00/2.00, ux 2.99/2.96, uy 3.00/2.96 | `fe-evidence/mms-convergence.json` `naive_orders` | yes |
| Temporal orders `finite_elements.tex:207` | 0.98–1.40 | nx16 1.093/0.978/1.015, nx32 1.397/1.018/1.125, nx64 1.396/1.076/1.252 | yes |
| Step-refinement ratio `finite_elements.tex:210`, `main.tex:611-612` | 1.94 (3.7e-3, 7.1e-3) | `figures/fe_mandel_refinement.csv` linear_time = 0.003658, 0.007104 → 1.942 | yes |
| Load-limit floor `main.tex:609`, `finite_elements.tex:214` | 3.2×10⁻³ at nx=20, dt=1e-3 | `figures/fe_load_limit.csv` = 0.0032209 | yes |
| Fabric peak pressures `finite_elements.tex:311-316` | 4.36/4.99/5.52/3.62 ×10⁻⁵ | `figures/fe_fabric_mandel_peak.csv` | yes |
| Refined contours `finite_elements.tex:326-332` | 3.61/4.35/4.97/5.50 ×10⁻⁵; u 5.18/5.14/2.38/5.26 ×10⁻⁵ | `figures/fe_fabric_contours.csv` | yes |
| Fabric reconstruction `finite_elements.tex:269-275` | 2.2e-16, −3.3e-16, 1.6e-16, 2.5e-16 | `site/reports/fabric-verification.json` `tensor_checks` | yes |
| Fabric NumPy agreement `finite_elements.tex:279` | 4.9e-15 | `worst_probe_abs_diff`=4.885e-15 | yes |
| Fabric conformal limit `finite_elements.tex:286` | 1.9e-14 | `conformal_cross_check` max = 1.874e-14 | yes |
| Mandel reference `site/evidence.json:14` | 38 checks, overshoot 5.4659% at 0.01516535 | `mandel-reference.json` 38 checks; ratio 1.0546586, t=0.015165352 | yes |
| Fluid-coupling report `site/evidence.json:23` | 110 checks, 8.09e-09 | `fluid-coupling-verification.json` count=110, max=8.0867e-09 | yes |
| C++/Python agreement `site/evidence.json:23` | 6.4e-14 over 41 states | `cpp-python-constitutive.json` states=41, 6.3949e-14 | yes |
| Finite-deformation ranges `site/evidence.json:46` | p 0.2062–0.2158; force ≤1.276e-10; mass ≤2.47e-10; partial 0.2005–0.2016 etc. | `site/reports/finite-deformation-summary.json` | yes |

**Independent recomputation (not merely matching stored scalars).** From the printed
`C_s` matrix and φ_s0=0.6, K=7, I recomputed: K_s=28; the drained stiffness `C^d` via
eq. `drained-stiffness-restriction` (shear block = 12/14.4/16.8); `B_0 = I − C^d:C_s⁻¹:I` =
(0.70000, 0.75833, 0.79167); the five deviatoric eigenvalues of `C_s` (20, 24, 28, 42.9668,
53.0332) whose mean÷2 = 16.8; and from the FE section parameters G = φ_s0 μ_s = 0.75,
B = 1−K/K_s = 0.6, storage = (1−φ_s0)/K_f + S_s = 17/80, M = 1/storage = 4.70588,
Ku = 2.69412, Skempton = 1.04803, ν = 0.2, ν_u = 0.37263, c = 3.82166 — all equal to the
recorded values. The shipped `examples/conformal_model.py:21-22` carries the same printed
matrix, and its own `mu_average` (`:78`) = trace(P_dev·C_s)/10 = 16.8.

### B. Declared digest surfaces (all verified byte-for-byte)

| Surface | Result |
|---|---|
| `source-manifest.json` | 608/608 hashed OK (Check 2) |
| `fe-evidence/manifest.json` `files[]` | 317/317 hash **and** byte-length OK; 0 missing; only `README.md`, `manifest.json` unlisted (self/readme) |
| `fe-evidence/runs/*/provenance.json` | 57 files; `source_sha256` 513/513 OK; `input_sha256` 57/57 = shipped `input.i`; shipped `outputs` 114/114 OK |
| `site/evidence.json` `artifacts` | 40/40 OK |
| `site/scientific-snapshot.json` `files` | 47/47 OK |
| supplement archive (`build/anisotropic-biot-2026-09-20-v2.zip`) internal `manifest.json` | 68/68 OK; payload↔manifest exactly 1:1 (no extras, no omissions) |
| `figures/*-plot-manifest.json` (3 files) | all `input_sha256` and `output_sha256` OK; declared `missing` empty |
| report-local digests (`mandel-reference.json` artifacts, `source_sha256` in conformal/fluid reports) | all OK |

Machine-readable claims about shipped bytes are accurate: `manifest.json` `runs[]`
`provenance_outputs_total`/`_unshipped` reproduce the true shipped/unshipped split for all 57
runs (0 anomalies); the two MMS copies differ only in `runs_dir` exactly as the manifest note
states and carry identical `space`/`time` data; the four `fabric_contour_*/solution.e` and the
sixteen `fabric_mandel_*/solution_profile_*.csv` exceptions ship as stated; and every
`analysis.json` present-flag matches disk.

---

## REQUIRED items

### R2-C1 — `site/evidence.json` references a nonexistent artifact and a shipped report is unregistered; the versioned file fails its own validator

**Location:** `site/evidence.json:25` (implementation category `evidence[]`), and
`tools/build_verification_site.py:108-110`.

**Defect.** The `implementation` category lists the evidence id `"fluid-coupling-verification"`,
but no artifact with that `id` exists (the 40 declared artifact ids contain none containing
"fluid", and no declared artifact `path` contains "fluid"). Consequences:

1. The machine-readable claim at `site/evidence.json:23` — "fluid EOS and reference-mass
   derivatives (110 checks, max scaled error 8.09e-09)" — is backed by a report that is
   *not* listed among the artifacts, while the category simultaneously cites an id that
   resolves to nothing.
2. The shipped report `site/reports/fluid-coupling-verification.json` exists in the snapshot
   (it is listed in `source-manifest.json`) but is **unregistered** in `site/evidence.json`,
   so it is invisible to the artifact-checksum/download surface.
3. `site/evidence.json` **fails its own validation**. The builder explicitly rejects unknown
   evidence ids.

**Evidence (exact command and output):**

```
$ python3 tools/build_verification_site.py --validate-only
Site build failed: Unknown evidence artifact: implementation
EXIT=1
```

Root cause isolated in scratch space (no repository file edited): copying
`site/evidence.json` to `/tmp`, deleting only the id `fluid-coupling-verification` from
`categories.implementation.evidence`, and re-validating gives:

```
$ python3 tools/build_verification_site.py --validate-only --manifest /tmp/ev_fixed.json
{"manifest": "valid", "artifacts": 40, "scientific_checks_executed": false}
EXIT=0
```

So the single dangling id is the whole cause. This is a self-inconsistent shipped record:
the README (`site/README.md:5-8`) states that `passed` categories are "backed by the listed
artifacts", yet the check behind the cited fluid-coupling claim is neither listed nor
registered, and the documented validation command fails on the snapshot.

**Required fix:** add a `fluid-coupling-verification` artifact entry (kind `report`, path
`site/reports/fluid-coupling-verification.json`, correct `sha256`), or change
`site/evidence.json:25` to the correct existing id, then re-run `--validate-only` to green.

*Note:* this is a record-keeping defect; it does not alter any scientific number in the
manuscript. The fluid-coupling report itself is present and its own contents (110 checks,
8.09e-09) are internally consistent and match `site/evidence.json:23`.

---

## OPTIONAL notes

### R2-O1 — `fe-evidence/README.md` wording about `reference_note`

`fe-evidence/README.md:11` says "a `reference_note` in each non-comparable `analysis.json`".
Checked against the shipped bytes: every `analysis.json` that carries `reference_comparable:
false` (`anisotropic_*`, `isotropic`, `partial_*`) does carry a `reference_note`; the
`mms_*`, `jacobian_*`, `one_element_*`, `fabric_*`, and `conformal_probe_ref`
`analysis.json` files carry neither `reference_comparable` nor `reference_note`. The sentence
is therefore defensible if "non-comparable" means exactly the `reference_comparable:false`
set, but it could be read as covering the MMS/Jacobian/one-element decks that
`manifest.json:notes` also calls non-comparable. Consider scoping the wording (e.g.
"...each run whose analysis records `reference_comparable:false`"). No incorrect digest or
number is involved.

### R2-O2 — external-revision manifest digest mismatch (investigated, not a snapshot defect)

A broad scan flagged `references/notes/weighted-stress-source-manifest.json:6`, which records
`AGENTS.md` = `9138064e…`, whereas the snapshot's `AGENTS.md` hashes to `618ec2de…`. The same
file's other keys (`paper/main.tex`, `paper/defs.tex`, `all.bib`) and its `companion_commit`
(`e62234c8…`) identify the *companion* manuscript revision, not this repository's layout, so
the digest describes a different source tree and is not a stale digest of this snapshot. No
action implied; recorded for transparency.

### R2-O3 — positive verification summary

All three mandatory checks pass. All declared digest surfaces (source manifest, FE evidence
manifest, 57 provenance files, site evidence artifacts, scientific snapshot, supplement
archive internal manifest, three figure plot manifests, report-local digests) verify
byte-for-byte. Every numeric value I could locate in `main.tex` and `sections/*.tex` agrees
with its frozen artifact, and the key constitutive scalars were independently recomputed from
the printed matrix and parameters rather than merely matched against stored values. The one
required item above is a self-consistency defect in a shipped evidence record; the science
and its numbers are unaffected.

---

VERDICT: MINOR REVISION

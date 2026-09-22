# Reviewer 2 — numerical verification and source fidelity

**Manuscript:** *An anisotropic Biot tensor from mineral stress and distention work* (John T. Foster)
**Snapshot:** `round-37`, `SNAPSHOT_ID = 0d75448ba758ff51c9f4e43423c120ffba6eaa1088442206436692c957fd2189`
**Scope of this review:** digest-surface verification, independent recomputation of printed scalars, and
traceability of every quoted number to a frozen artifact. All reads were taken from the immutable
snapshot only. All paths below are relative to the snapshot root.

---

## 1. Mandatory checks

### 1.1 Snapshot identity — **PASS**

```
$ sha256sum source-manifest.json
0d75448ba758ff51c9f4e43423c120ffba6eaa1088442206436692c957fd2189  source-manifest.json
```

This equals the declared `SNAPSHOT_ID` exactly. `SNAPSHOT_ID` (65 bytes) also contains the same string.

### 1.2 Manifest re-hash against disk — **PASS**

```
listed entries: 608
MISSING:  0
MISMATCH: 0
files on disk (excluding reviews/): 609
UNLISTED: 2  ->  SNAPSHOT_ID, source-manifest.json   (both expected)
```

All 608 listed paths hash byte-for-byte to their declared SHA-256. The only present-but-unlisted files
are the two self-referential metadata files the brief identifies as expected. No listed-but-missing file.

---

## 2. Declared digest surfaces verified byte-for-byte — all **PASS**

| Surface | What was checked | Result |
|---|---|---|
| `source-manifest.json` | 608 paths, SHA-256 + presence | 0 mismatch, 0 missing |
| `fe-evidence/manifest.json` (`files[]`) | 317 entries, SHA-256 **and** byte length | 0 mismatch, 0 missing |
| `fe-evidence/runs/*/provenance.json` | every `outputs[].sha256`, and all **513** `source_sha256` entries re-hashed on disk | 0 mismatch, 0 missing |
| `figures/fabric-plot-manifest.json`, `figures/fe-verification-plot-manifest.json`, `figures/fe_fabric_contours-plot-manifest.json` | every `input_sha256` and `output_sha256` (34 digests) | 0 mismatch, 0 missing |
| `site/evidence.json` (`artifacts[]`) | 41 artifact digests | 0 mismatch, 0 missing |
| `site/scientific-snapshot.json` (`files[]`) | 47 source digests | 0 mismatch, 0 missing |
| Site validator | `python3 tools/build_verification_site.py --validate-only` | `{"manifest": "valid", "artifacts": 41, "scientific_checks_executed": false}`, exit 0 |
| `build/anisotropic-biot-2026-09-20-v2.zip` internal `manifest.json` | 68 declared digests vs archive bytes; payload completeness (69 entries − `manifest.json`) | 0 mismatch; payload ⊂ declared and declared ⊂ payload (exact) |
| report-local digests | `site/reports/mandel-reference.json` → `artifacts` (`mandel-probes.csv`, `mandel-profiles.csv`) | both match |

`fe-evidence/manifest.json` is also internally consistent with the tree: 57 `runs[]` cases = 57 `cases[]`
= 57 run directories on disk (exact set equality), and the 28 `not_applicable` entries correspond to the
decks that carry no reference comparison.

---

## 3. Independent recomputation of printed scalars

I recomputed these from the printed matrices/parameters rather than matching stored values.

| Quantity | Source claim | My recomputation | Verdict |
|---|---|---|---|
| `K_s` from the printed Mandel matrix | `sections/experiments.tex:22` — \(K_s=28K_*\) | \(\tfrac19\,\mathbf I:\mathbb C_s:\mathbf I = 252/9 = 28\) | **MATCH** |
| \(\mathbb C_s\) positive definite | `sections/experiments.tex:22` | eigenvalues \(20,24,28,41.98,51.79,86.23\) all \(>0\) | **MATCH** |
| Reference Biot components | `sections/experiments.tex:25` — \(0.7000, 0.7583, 0.7917\) | \(B_0=\mathbf I-\mathbb C^d:\mathbb C_s^{-1}:\mathbf I\) with `eq:drained-stiffness-restriction` → \(0.700000, 0.758333, 0.791667\); shear comps \(0\) | **MATCH** |
| Drained spherical modulus recovery | `eq:drained-stiffness-restriction` | \(\tfrac19\mathbf I:\mathbb C^d:\mathbf I = 7.000000\) | **MATCH** |
| Isotropic comparison shear modulus | `sections/experiments.tex:29` — \(16.8K_*\) = mean of five deviatoric modes ÷ 2 | modes \(43,53,20,24,28\), mean \(33.6\), ÷2 \(=16.8\) | **MATCH** |
| FE drained shear | `sections/finite_elements.tex:164` — \(G=0.75\) | \(\phi_{s0}\mu_s = 0.9\cdot(5/6) = 0.75\) | **MATCH** |
| FE reference Biot | `sections/finite_elements.tex:165` — \(0.6\) | isotropic \(B_0=1-K/K_s = 1-1/2.5 = 0.6\) (`sections/limits.tex:20`) | **MATCH** |
| FE total storage | `sections/finite_elements.tex:166` — \(17/80\) | \((1-\phi_{s0})/K_f + S_s = 0.0125+0.2 = 0.2125 = 17/80\) | **MATCH** |

Note: the isotropic reference Biot is \(1-K/K_s\), not \(1-K/(\phi_{s0}K_s)\); using the latter would give
\(0.5556\). The manuscript states the correct form in `sections/limits.tex:20`, consistent with the
printed \(0.6\). No error.

---

## 4. Every quoted number located in a frozen artifact

| Quoted value | Location | Frozen artifact | Verdict |
|---|---|---|---|
| floor \(\approx 3.2\times10^{-3}\) at \(nx=20,\ dt=10^{-3}\) | `main.tex:625`; `sections/finite_elements.tex:214,233` | `figures/fe_load_limit.csv` → `nonlinear_load_0.0001 … 0.003220919735602341` | **MATCH** |
| step-refinement \(3.7\times10^{-3}\), \(7.1\times10^{-3}\) | `main.tex:627-628` | `figures/fe_mandel_refinement.csv` → `0.003657958974355574`, `0.0071039215708695895` | **MATCH** |
| ratio \(1.94\) | `main.tex:628`; `sections/finite_elements.tex:210` | \(0.0071039215/0.0036579590 = 1.94198\) | **MATCH** |
| temporal orders \(0.98\)–\(1.40\) at \(nx=16/32/64\) | `main.tex:630`; `sections/finite_elements.tex:208` | `fe-evidence/mms-convergence.json` `time.*.orders.*.difference_orders`: min \(0.97830\), max \(1.39688\) | **MATCH** |
| MMS spatial orders p \(2.00/2.00\), \(u_x\) \(2.99/2.96\), \(u_y\) \(3.00/2.96\) | `sections/finite_elements.tex:204-206` | `mms-convergence.json` `space.orders.*.naive_orders` | **MATCH** |
| conformal suite 186 named checks | `sections/experiments.tex:181` | `build/conformal/verification.json` → `checks_passed: 186` (and 186 keys in `checks`) | **MATCH** |
| 65 per-state identities (5×13) | `sections/experiments.tex:182-184` | `checks` key histogram: `legacy_state0..4` × 13 = 65 | **MATCH** |
| largest constitutive error \(2.5\times10^{-9}\) | `sections/experiments.tex:187` | `max_constitutive_identity_error = 2.4549890331732928e-09` | **MATCH** |
| tensor suite 273 states / 13 stiffnesses | `sections/experiments.tex:191` | `build/weighted-stress/tensor-verification.json` → `total_states: 273`, `materials: 13` | **MATCH** |
| \(2.2\times10^{-16}\), \(-3.3\times10^{-16}\) | `sections/finite_elements.tex:72` | `build/fabric/fabric-verification.json` → `H_reconstruction_max_abs_diff = 2.2204e-16`, `H_det_minus_one = -3.3307e-16` | **MATCH** |
| \(\lVert\mathbb D:\mathbf e_3\rVert=1.6\times10^{-16}\), \(\mathbb D:\mathbf e_6=\mathbf 0\) | `sections/finite_elements.tex:74-75` | same file → `D4_e3_norm = 1.5823e-16`, `D4_e6_norm = 0.0` | **MATCH** |
| rotation invariance \(2.5\times10^{-16}\) | `sections/finite_elements.tex:76` | `rotation_invariance_norm = 2.4965e-16` | **MATCH** |
| worst probe diff \(4.9\times10^{-15}\) | `sections/finite_elements.tex:79-81` | `worst_probe_abs_diff = 4.884981308350689e-15` | **MATCH** |
| conformal limit agreement \(1.9\times10^{-14}\) | `sections/finite_elements.tex:86-88` | `conformal_cross_check` max `abs_diff = 1.8742e-14` (`sigma11`) | **MATCH** |
| fabric peaks \(4.36/4.99/5.52\times10^{-5}\), \(3.62\times10^{-5}\) | `sections/finite_elements.tex:112-116` | `figures/fe_fabric_mandel_peak.csv` → `4.3627593e-05, 4.9900848e-05, 5.5211051e-05`, iso `3.6163930e-05` | **MATCH** |
| refined peaks \(3.61/4.35/4.97/5.50\times10^{-5}\) | `sections/finite_elements.tex:127-129` | `figures/fe_fabric_contours.csv` → `p_max = 3.6061943e-05, 4.3491366e-05, 4.9736591e-05, 5.5031354e-05` | **MATCH** |
| displacement peaks \(5.18/5.14/2.38/5.26\times10^{-5}\) | `sections/finite_elements.tex:131-133` | same CSV → `u_mag_max = 5.1826395e-05, 5.1371552e-05, 2.3818364e-05, 5.2586920e-05` | **MATCH** |
| 38 self-checks, peak overshoot 5.4659 % at \(t=0.01516535\) | `site/evidence.json` `categories.analytical.summary` | `site/reports/mandel-reference.json`: 38 checks all `passed`; `central_overshoot.ratio-1 = 5.46586e-2`, `time = 0.015165352045764979` | **MATCH** |

The manuscript's own numbers are internally careful: the coarse `fabric_mandel` peaks (\(3.62,4.36,4.99,5.52\))
are correctly distinguished from the refined \(40\times8\) contour peaks (\(3.61,4.35,4.97,5.50\)), matching the
two distinct frozen CSVs.

---

## 5. REQUIRED items

### R2-C1 — Shipped requirements do not cover a script the shipped reproduction instructions require

**Locations.** `examples/requirements.txt:1-4` (also inside the archive as `examples/requirements.txt`);
archive `README.md` (entry in `build/anisotropic-biot-2026-09-20-v2.zip`);
`examples/plot_fabric_contours.py:40`.

**Finding.** `examples/requirements.txt` declares only:

```
numpy>=2,<3
scipy>=1.14,<2
matplotlib>=3.8,<4
```

The embedded supplement's `README.md` states the reproduction procedure as *"Extract the archive, then
run from its root in a Python environment: `python3 -m pip install -r examples/requirements.txt` … "* and
then instructs, to regenerate two article figures:

```
python3 examples/plot_fabric_contours.py   --runs fe-evidence/runs --output figures
```

That script imports `netCDF4` unconditionally (`examples/plot_fabric_contours.py:40: import netCDF4`), and
uses it at line 73. `netCDF4` appears in **no** requirements file in the snapshot
(`examples/requirements.txt`, `agent_environment/requirements/*.txt`). The figure manifest itself records
that `netCDF4 1.7.4` was used (`figures/fe_fabric_contours-plot-manifest.json`, `versions.netCDF4`), so the
dependency is real and known to the tooling.

**Consequence.** A reproducer following the shipped, self-contained supplement instructions in a fresh
Python environment gets `ModuleNotFoundError: No module named 'netCDF4'` and cannot regenerate
`fe_fabric_contours.{pdf,png}` or `fe_fabric_diffusion.{pdf,png}`. The archive README explicitly claims these
figures "are reproducible from the extracted archive"; with the shipped requirement set they are not.

**Requested fix.** Add `netCDF4` (with a supported range) to `examples/requirements.txt` and re-package the
supplement so the shipped requirements match the shipped reproduction commands.

---

## 6. OPTIONAL notes

### R2-O1 — Version skew between the archive's copy of a plotting script and the digest the figure manifest pins

`figures/fe_fabric_contours-plot-manifest.json:45` declares
`"examples/plot_fabric_contours.py": "8eaa896dfdeeae0ced6c892a0266cbb8bd58fdc402b8cce8607fba74e6c14efe"`,
which matches the repository copy. The copy shipped inside `build/anisotropic-biot-2026-09-20-v2.zip`
hashes to `9c2bc8aa8cafc091d64dc0c3dc5928c885799734f7968e5964fb13345fd07e0d`. The only difference is one
appended string in the `limitations` list about the Exodus wall-clock line. Each digest surface is
internally correct and the archive's own manifest is self-consistent, so no claim is false, and freezing an
older script inside a versioned archive is defensible — but two shipped digest surfaces describe the *same
path* with different bytes without noting the skew. Consider annotating the archive or re-syncing the
bundled script so a reader recomputing hashes across surfaces is not surprised.

### R2-O2 — Companion-scoped source manifest cannot be verified inside this snapshot

`references/notes/weighted-stress-source-manifest.json:6-12` lists `source_sha256` for companion-repository
paths (`paper/main.tex`, `paper/defs.tex`, `paper/sections/…`, `all.bib`, `author_style_profile_2026-07-27.md`,
`AGENTS.md`). Six of these paths do not exist in this snapshot, and the `AGENTS.md` digest
(`9138064e…`) does not match the repo's own `AGENTS.md`. This is expected — the file records
`companion_commit: e62234c8…` and is companion-scoped, and I am barred from inspecting sibling repositories
— but nothing in the snapshot lets an independent reader reproduce those digests. A one-line note that the
paths resolve against the named companion commit (not this repository) would remove the ambiguity.

### R2-O3 — Archive README vs repository README

`build/anisotropic-biot-2026-09-20-v2.zip` ships its own `README.md`
(`sha256 038e981a…`) which differs from the repository `README.md` (`sha256 f1d80c4b…`). This is
appropriate — the archive carries a self-contained supplement README — and is recorded here only so the
two surfaces are not mistaken for a mismatch.

---

## 7. Isolation self-report

During the initial orientation I ran a recursive `find` over the snapshot that traversed the `reviews/`
directory before its output was filtered with `grep -v '/reviews/'`. **No review filename, verdict,
acceptance count, or report content was displayed or read.** All subsequent traversal used
`os.walk` with `reviews` pruned. I did not read the working-tree manuscript, did not open any file under
`reviews/`, did not run the held suites (`validation/`, `examples/verify_*.py`), and did not touch any
sibling repository. Scratch work was confined to `/tmp`. The only file I wrote is this report.

---

## 8. Summary

Every declared digest surface verifies byte-for-byte: the source manifest (608 paths), the FE evidence
manifest (317 files, digests and byte counts), all 57 run provenance records (including 513 source hashes),
the three figure plot manifests, the site evidence allowlist (41 artifacts), the scientific snapshot (47
sources), the site validator, the supplement archive's internal manifest (68 payload digests, exact payload
coverage), and the report-local digests. Every quoted scalar, range, and figure value I could locate in
`main.tex` and `sections/*.tex` reproduces in a frozen artifact, and the key constitutive scalars
(\(K_s=28\), \(B_0=0.7000/0.7583/0.7917\), \(G_{\text{iso}}=16.8\), \(G=0.75\), \(B=0.6\), storage \(17/80\))
recompute correctly from the printed matrices and parameters. The manuscript's quantitative claims are
honestly scoped (demonstrations flagged as demonstrations, no order above one asserted, synthetic
parameters declared).

The single required fix is R2-C1: a shipped dependency (`netCDF4`) is missing from the shipped requirements
file, which breaks two advertised reproduction commands of the self-contained supplement. This is a small,
mechanical completeness defect, not a numerical or digest failure.

VERDICT: MINOR REVISION

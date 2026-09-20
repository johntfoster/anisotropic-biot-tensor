# Round-14 Independent Review — Reviewer 2

**Charge:** physics / source fidelity and packaging completeness.

**Independence statement.** This pass was performed against the frozen snapshot
only. I did not read any other reviewer's report, any prior-round directory, or
any prior verdict. Scratch work was done in `/tmp/r14-r2` (a writable copy of the
snapshot) and `/tmp/r14zip`; the snapshot itself was not modified. All numeric
claims below were re-derived by me from the frozen artifacts, not taken from the
package's prose.

---

## 1. Reviewed version, snapshot ID, and integrity result

- Repository: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor`
- Frozen snapshot: `.agent-runtime/review-snapshots/round-14` (read-only, `dr-xr-xr-x`)
- Declared `SNAPSHOT_ID` in `round-14/SNAPSHOT_ID`:
  `061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69`

Integrity of the manifest and of every file it lists **passes**:

```
$ sha256sum .agent-runtime/review-snapshots/round-14/source-manifest.json
061a92feee93641668978ab0ecec033d0b9fe0d20ad74efbcb9ec0bf1a60ea69  .../source-manifest.json
```

`source-manifest.json` hash equals `SNAPSHOT_ID`. Hashing every listed entry:

```
listed 441  ok 441  mismatch 0  missing 0
```

**Integrity: PASS (441/441).** No integrity failure; the audit proceeds.

Note on scope limitation: the snapshot ships no MOOSE binary (`anisotropic_biot-opt`)
and no Exodus output; therefore `moose_app/scripts/verify_constitutive.py` (C++ AD
law vs the independent Python oracle) and any re-solve of the FE decks could not be
re-executed. Per the charge, I audited the recorded artifacts and independently
reproduced the NumPy/SciPy Python suites. This is stated as a limitation.

---

## 2. Independent verification evidence (literal commands and outputs)

### 2.1 Packaging: every declared hash in the mandated files resolves

All commands run from the frozen snapshot root (read-only).

Mandated declaration families — **all resolve with matching hashes, 0 mismatches**:

```
site/evidence.json artifacts ........ total=22  ok=22  mismatch=0 missing=0
site/scientific-snapshot.json files . total=33  ok=33  mismatch=0 missing=0
site/reports/*.json (source_sha256 + artifacts)  total=7  ok=7  mismatch=0 missing=0
fe-evidence/manifest.json ........... total=206 ok=206 mismatch=0 missing=0
source-manifest.json ................ total=441 ok=441 mismatch=0 missing=0
```

Report-internal references checked explicitly (all resolve):

```
site/reports/conformal-verification.json  source_sha256 -> examples/conformal_model.py, examples/verify_conformal.py  OK
site/reports/fluid-coupling-verification.json source_sha256 -> examples/conformal_model.py, examples/verify_fluid_coupling.py OK
site/reports/mandel-reference.json source_sha256 -> validation/mandel_reference.py OK
site/reports/mandel-reference.json artifacts -> site/reports/mandel-probes.csv, mandel-profiles.csv OK
```

### 2.2 Manuscript file targets resolve

`\embedfile` (1), `\includegraphics` (5), `\input` (6) — all resolved:

```
OK  build/conformal-2026-09-20-v1.zip          (embedfile payload)
OK  build/conformal/pressure_response.pdf
OK  build/conformal/directional_response.pdf
OK  build/conformal/rotation_response.pdf
OK  build/conformal/constrained_layer.pdf
OK  build/conformal/shear_response.pdf
OK  sections/{experiments,finite_elements,limits,logarithmic_derivative,stress_reconstruction}.tex
OK  provenance/ai_use_statement.tex
```

Code-and-data availability paragraph paths — all present in the snapshot:
`examples/conformal_model.py`, `examples/conformal_experiments.py`,
`examples/verify_conformal.py`, `moose_app/`, `validation/`, `fe-evidence/runs/`,
`fe-evidence/mms-convergence.json`, `figures/`, `site/evidence.json` — **all exist**.
The `build/main.log` contains **0** "undefined reference/citation" warnings.

### 2.3 Embedded supplement archive verifies

```
$ unzip -q build/conformal-2026-09-20-v1.zip ; sha256sum -c (manifest-driven)
zip internal manifest: version conformal-2026-09-20-v1 total 33 ok 33 mismatch 0 missing 0
zip files not in manifest : []
manifest files not in zip : []
```

The availability paragraph's statement ("`manifest.json` identifies its version and
SHA-256 hashes of all payload files") is accurate: 33 payload files + the manifest.

### 2.4 Independent reproduction of the Python suites (exact match to records)

Run in `/tmp/r14-r2` (writable copy). Every value reproduced is **bit-identical**
to the recorded report.

```
$ python3 validation/mandel_reference.py --self-check
38 checks; central_overshoot ratio = 1.0546586069998425 at t = 0.015165352045764979
→ 5.4659% peak overshoot at t = 0.01516535   (matches site/reports/mandel-reference.json)

$ python3 examples/verify_conformal.py
checks_passed=186  legacy_identities_rechecked=67
max_constitutive_identity_error = 2.4549890331732928e-09   (record identical)
observed_orders energy_stress [2.0003930,2.0000982,2.0000246,2.0000062]
observed_orders pore_volume   [2.0002117,2.0000529,2.0000132,2.0000034]
observed_orders pressure      [1.9999905,2.0002802,2.0002913,1.9891499]
Per-check error-by-error delta vs site/reports/conformal-verification.json: max |Δ| = 0; pass-flag mismatches = 0

$ python3 examples/verify_fluid_coupling.py
count=110  passed=true  maximum_scaled_error=8.086725789002713e-09   (record identical, 8.09e-09)

$ python3 examples/verify_tensor.py
total_states=273 (13 materials x 21) ; errors byte-identical to record

$ python3 examples/verify_reconstruction.py
errors byte-identical to record (compliance 1.39e-16, work_equivalence 5.04e-10,
unjacketed 5.09e-14, ...); minimum_drained_eigenvalue=1.8415045063808817

$ python3 validation/mms_reference.py --output-dir /tmp/mmsref
exit 0 ; smallest_Cd_eigenvalue=11.999999999999993 ; solid_storage=0.0125
```

The C++/Python constitutive parity record (`cpp-python-constitutive.json`,
41 states, `value_absolute_error=6.394884621840902e-14`) is internally consistent
but its producer requires the compiled binary, so it could not be re-executed here
(limitation, §1).

### 2.5 Constitutive law and kernels implement the stated equations (source fidelity)

Read against `moose_app/include/utils/ConformalLaw.h` (`Conformal::Law::evaluate`) and
`sections/stress_reconstruction.tex` / `sections/limits.tex`:

| Implementation (`ConformalLaw.h`) | Paper equation | Check |
|---|---|---|
| `s.sigma = phi/J * tau - I*((1-solid)*p)`, `tau=F*L*F^T` | total stress \(\sigma=\frac{\phi_{s0}}J\bar\tau_s-(1-\phi_s)pI\) (eq. total-stress-phase-energy) | matches |
| `rho = rho0*exp(p/Kf)` | \(\bar\rho_f=\bar\rho_{f0}\exp(p/K_f)\) (eq. fe-fluid-eos) | matches |
| `flux = -mobility*J*rho*(invF*invF^T)*gradp` | \(\mathbf Q_f=-\frac{J\bar\rho_f k}{\mu_f}\mathbf F^{-1}\mathbf F^{-T}\mathrm{Grad}\,p\) (eq. fe-reference-darcy-law) | matches |
| `residual = Ks*(q0-target)+alpha*p*y0`, `target = K/(phi*Ks)*logJ - alpha/(3Ks)*tr(Cs:dev)` | \(0=K_s\ln\bar J+\alpha p\bar J-\frac K{\phi_{s0}}\ln J+\frac\alpha3\,\mathbf I{:}\mathbb C_s{:}\mathrm{dev}\,\varepsilon\), \(\alpha=1-\frac K{\phi_{s0}K_s}\) (eq. anisotropic-mineral-eos) | matches |
| `cd = phi*cs - phi*alpha/(9*Ks)*outer(ci,cj)` | \(\mathbb C^d=\phi_{s0}\mathbb C_s-\frac{\phi_{s0}}{9K_s}\alpha(\mathbb C_s{:}\mathbf I)\otimes(\mathbb C_s{:}\mathbf I)\) (eq. drained-stiffness-restriction) | matches |
| `B = I - y/(J*stability)*(K*I - phi*alpha/3*F*LB*F^T)`, `stability=Ks+alpha*p*y`, `LB=∫(I+sD)^{-1}dev(Cs:I)(I+sD)^{-1}ds` | explicit Biot tensor (eq. anisotropic-biot-explicit) | matches |
| `tensorRowCdInverseCs = phi*I - phi*alpha/(3Ks)*Cs:I` → isotropic limit `(1-K/Ks)I` | \(\mathbf B_0=\mathbf I-\mathbb C^d{:}\mathbb C_s^{-1}{:}\mathbf I\) (eq. reference-biot-compatibility) | matches |
| linear `storage = (1-phi)/Kf + phi*alpha/Ks` | \(\frac1{\bar\rho_{f0}}\partial_p m_f=(1-\phi_{s0})/K_f+S_s\), \(S_s=\frac{\phi_{s0}}{K_s}\alpha\) (eq. reference-solid-storage) | matches |

Mineral EOS signs/factors, distention \(\phi_s=\phi_{s0}\bar J/J\), and the exponential
fluid EOS all reconcile algebraically with the manuscript. No sign or factor
discrepancy found.

### 2.6 Comparability honesty, load-limit, and demonstration wording vs per-run data

Aggregating all 38 `fe-evidence/runs/*/analysis.json`:

- Partial family (`partial_0/30/30_coarse/30_fine`) has `reference_comparable = false`
  and omits all reference-normalized metrics — consistent with the stated square
  domain `[-1,1]x[-1,1]` (verified in `input.i`) versus the slender Mandel reference
  `[-1,1]x[-0.1,0.1]` (verified in `anisotropic_0/input.i`). **No non-comparable run
  backs a verification claim**: `site/evidence.json` marks `finite_deformation`
  status `pending` with `evidence: []`, and the analytical/implementation/convergence
  evidence lists reference only comparable artifacts/MMS.
- Six anisotropic runs (0, 30, 30-coarse, 30-fine, 45, 90): `pressure_max` 0.7549–0.8575
  (claim 0.75–0.86), `platen` 0.732–0.7754 (claim 0.73–0.78), `edge_ux` 1.611–1.780
  (claim 1.61–1.78), `profile_max` 0.755–0.875 (claim 0.75–0.88) — **all match**.
- Force balance: max `force_relative` over the *demonstration* runs = 2.052e-10
  (`partial_30`), exactly as claimed ("at most about 2.1e-10, largest 2.052e-10").
  (The overall max across all runs is 1.637e-9 for `linear_coarse`, a non-demonstration
  refinement case; the claim is correctly scoped to demonstration runs.)
- Load-limit floor: `pressure_max_normalized` = 0.0032209 / 0.003448 / 0.005706 at
  loads 1e-4 / 1e-3 / 1e-2 → the claimed ~3.2e-3 floor that does not decay is correct.
- MMS orders match `site/reports/mms-convergence.json` exactly: spatial naive orders
  ux 2.9917/2.9585, uy 2.9983/2.9600, p 1.9966/2.0008; temporal successive-difference
  orders nx=16 (1.0932, 0.9783, 1.0152), nx=32 (1.3969, 1.0183, 1.1252),
  nx=64 (1.3964, 1.0762, 1.2519).
- "isotropic Mandel spatial refinement is non-monotone at the finest level" is
  confirmed by `figures/fe_mandel_refinement.csv` (h=0.05→4.58e-4 rising to
  h=0.025→6.36e-4).

The abstract and `sections/finite_elements.tex` ("Scope of these results") correctly
withhold any quantitative finite-deformation verification and any experimental
validation claim. **Comparability and wording are honest.**

### 2.7 Global scan for unresolvable hash declarations

Every 64-hex token in every shipped text file, tested against the set of all file
hashes in the frozen snapshot:

```
total 64-hex tokens in shipped text files : 4790
resolvable                               : 1320
unresolvable                             : 3470
```

Breakdown of the 3,470 unresolvable tokens:

```
declared run-output digests in 38x fe-evidence/runs/*/provenance.json
  (solution.e + solution_profile_*.csv not shipped) ........ 3419
binary_sha256 in the same provenance files (compiled binary not shipped) 38
external/companion-source digests in references/notes/ ... 12
   weighted-stress-source-manifest.json (8) + notes (4)
declared-with-wrong-target (path exists, hash differs):
   fe-evidence/runs/linear_coarse/provenance.json
   source_sha256["moose_app/include/utils/ConformalLaw.h"] ... 1
```

---

## 3. Findings with severity

**F1 — MODERATE (packaging completeness / declaration integrity).**
38 shipped `fe-evidence/runs/*/provenance.json` files declare 3,533 output SHA-256
digests in their `outputs` objects, of which **3,419** (the Exodus `solution.e` and
the per-step `solution_profile_*.csv` files) have **no resolvable target inside the
snapshot**. The same files additionally declare a `binary_sha256` (38 occurrences)
for a compiled application that is not shipped. `tools/materialize_fe_evidence.py`
copies only six per-run files and deliberately guards only `run.log`
("Every run provenance that declares a run.log must ship it, so the declared digest
resolves inside the evidence directory") — leaving the rest of `outputs` declaring
digests a verifier cannot resolve. Under the charge's standard ("no shipped file may
declare hashes or paths that do not resolve inside the snapshot") this is a genuine,
large mismatch: **3,469 declared-but-unresolvable hashes** (3,419 outputs + 38
binaries + 12 external).

**F2 — MODERATE (source fidelity / run traceability).**
Exactly one recorded run is out of line with the shipped sources.
`fe-evidence/runs/linear_coarse/provenance.json` records

```
source_sha256["moose_app/include/utils/ConformalLaw.h"] = 8bf5c9a79dcbeea9dab091d68479b15d6553d114546a3ab28e7e5bab06f4f0e2
binary_sha256                                          = ab89ce4bcb821e5f62012187f294a36130fc51b3402e5fac829de06e54a249de
```

whereas the shipped `ConformalLaw.h` hashes to
`ca18175b202ebf1cba65c499f59ee1039d4a8611c3d27764adc229e329cd613c`, and the other
**37/38** runs record that same hash and binary
`ff0272fc279fcf91f6acd0c4a2e0ce436e8b165ad68b15549c27e6845dfdd31e`. Thus
`linear_coarse` was produced by a different source/binary snapshot than the one that
ships. The run does not appear in any figure, report, or claim
(`grep linear_coarse` hits only `fe-evidence/manifest.json` and `source-manifest.json`),
so it does not corrupt a published result — but it is a shipped evidence file whose
recorded source/binary digests do not correspond to the shipped source, i.e. the run
is not reproducible from the snapshot.

**F3 — LOW (documentation vs shipment).**
`fe-evidence/README.md` and the `materialize_fe_evidence.py` docstring state that each
`runs/<case>/` "holds ... the per-run analysis (`analysis.json`) ...". Three cases
(`jacobian_0.0001`, `jacobian_1e-05`, `jacobian_1e-06`) ship **no** `analysis.json`.
The absence is recorded in `fe-evidence/manifest.json` `missing` but not disclosed in
the README that describes the directory contents.

**F4 — LOW / informational (non-resolving absolute paths).**
88 shipped files embed absolute paths into an unstaged runtime directory
`.agent-runtime/moose-fe-goal-2026-09-20/...` that does not exist in the snapshot:
the 38 provenance `command` arrays, `site/reports/mms-convergence.json` `runs_dir`,
and two `validation/reference-data/*.md` documents that name it as the default output
directory. These are provenance/output-location references rather than claims about
snapshot content, and they do not affect reproducibility of the Python suites, but
they are paths that do not resolve inside the snapshot.

**Non-findings (checked, no defect).** The constitutive law and kernels match the
stated equations (total stress vs drained `-pB`, exponential fluid EOS,
current-configuration Darcy law, mineral EOS signs/factors, distention, explicit
anisotropic Biot tensor, drained compliance restriction, reference Biot and solid
storage); the analytical Mandel reference reproduces (38 checks, 5.4659% overshoot);
all mandated manifests and manuscript targets resolve; the embedded archive's internal
manifest verifies 33/33; the load-limit and demonstration wording matches the per-run
data; and no non-comparable run backs a verification claim.

---

## 4. Required corrections

**R1 (from F2) — Reconcile or disclose the `linear_coarse` provenance.** *Why:* a
shipped evidence file asserts a source digest and a binary digest that the shipped
snapshot does not contain, so that run cannot be reproduced from the package and the
one shipped snapshot's provenance is internally inconsistent with itself (37/38 vs
1/38). Correct by either (a) re-running `linear_coarse` with the shipped application
and refreshing its `provenance.json`, or (b) adding an explicit note in
`fe-evidence/README.md` (and/or a field in `fe-evidence/manifest.json`) that
`linear_coarse` was recorded against a superseded source/build and is retained as
historical provenance only. *Effort:* minutes; no scientific result changes.

**R2 (from F1) — Stop declaring digests the package cannot satisfy, or disclose the
subset.** *Why:* the charge requires that no shipped file declare hashes/paths that do
not resolve inside the snapshot; the 38 provenance files currently declare 3,419
unshipped run-output digests plus 38 unshipped binary digests. Correct by either
(i) extending the existing `materialize_fe_evidence.py` discipline beyond `run.log` —
record in `fe-evidence/manifest.json` (or README) a per-case flag that
`provenance.json["outputs"]` enumerates the *source run's complete* output set while
only the listed subset ships; or (ii) shipping the raw `solution.e` and per-step
profiles; or (iii) pruning/annotating the unshipped entries. The lowest-risk fix is the
explicit disclosure, since the current README already describes the shipped subset
accurately and the raw dumps are large.

**R3 (from F3) — Align the `fe-evidence/README.md` description with the shipped
tree.** *Why:* the README states each case holds `analysis.json`, but three cases do
not; a reader verifying "every case has its analysis" fails. Correct by qualifying the
README (e.g., "the per-run analysis where one was produced; see `manifest.json`
`missing`") or by generating the three missing files.

---

## 5. Optional suggestions

- Ship `solution.e` (or the per-step profile CSVs) for at least the load-limit and
  refinement families so an independent party can re-derive the per-run analyses from
  raw fields without rebuilding MOOSE; this would also close F1/R2 at the source.
- Record the compiled `anisotropic_biot-opt` digest once in `fe-evidence/README.md`
  and note it is intentionally not shipped, so the `binary_sha256` field is
  self-documenting.
- Replace the absolute `.agent-runtime/...` paths in shipped JSON/Markdown with
  repository-relative paths (or mark them as historical) to avoid dangling references
  (F4).
- Consider a lightweight `tools/check_evidence_integrity.py` that fails when any
  shipped declaration (manifest or provenance) does not resolve, so future rounds
  catch F1/F2 automatically.
- The external digests in `references/notes/` (companion repo, `gajo_fulltext`) are
  reasonable as provenance of inspected external sources; a one-line note that they
  are external would prevent them being read as snapshot-integrity claims.

---

## 6. Verdict

The frozen snapshot is internally sound where it matters for the science: integrity
passes 441/441; every mandated manifest declaration and manuscript target resolves;
the embedded supplement manifest verifies 33/33; the constitutive law and kernels
match the stated equations; the Mandel reference and all four Python verification
suites reproduce bit-identically to the recorded values; comparability is honest
(partial runs are explicitly non-comparable and back no claim); and the load-limit and
demonstration wording matches the per-run data.

The package nevertheless ships evidence files that declare digests and paths that do
not resolve inside the snapshot — most substantially the 3,419 unshipped per-run
output digests (plus 38 binary digests) in the provenance records, and one run
(`linear_coarse`) whose recorded source and binary digests do not match the shipped
sources. None of these alter a published numerical result, but they are packaging /
traceability defects that a completeness audit must require to be closed. This is not
a scientific failure and not a rejection; it is a bounded, low-risk revision.

VERDICT: MINOR REVISION

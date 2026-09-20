# Round-15 independent review — Reviewer 2 (physics, source fidelity, packaging completeness)

## 1. Reviewed version, snapshot id, integrity result

- Manuscript: "An anisotropic Biot tensor from mineral stress and distention work" (`main.tex`, `build/main.pdf`).
- Snapshot (frozen, read-only): `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-15`
- Working copy: `/tmp/r15rev2` (`cp -r <snapshot> /tmp/r15rev2 && chmod -R u+w /tmp/r15rev2`)
- SNAPSHOT_ID recorded in `<snapshot>/SNAPSHOT_ID`:

```
$ cat <snapshot>/SNAPSHOT_ID
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617
```

- Step-1 command and output:

```
$ sha256sum <snapshot>/source-manifest.json
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617  <snapshot>/source-manifest.json
```

The digest of `source-manifest.json` equals the recorded SNAPSHOT_ID. **Integrity check PASSES.**

- Every path listed in `source-manifest.json` was hashed inside the snapshot:

```
listed 438 ok 438 mismatch 0 missing 0
```

```
$ python3 - <<'EOF'   # hashes every path in source-manifest.json
...
listed 438 ok 438 mismatch 0 missing 0
EOF
```

No mismatch, no missing file. Integrity therefore also holds for the full manifest, not only for the manifest file itself.

## 2. Independent verification evidence

All commands below were run on the writable copy `/tmp/r15rev2` with conda env `moose`
(`numpy 2.4.2`, `scipy 1.17.1`, `matplotlib 3.10.8`, Python 3.10). The snapshot ships no compiled MOOSE
binary, so the coupled solver results were audited by re-deriving from the recorded raw artifacts
(`analysis.json`, `solution.csv`, `provenance.json`, `reference_comparison.csv`, `figures/*.csv`), while the
Python suites were re-executed.

### 2.1 Declared digests / paths resolve inside the snapshot

| Declaration | Command | Result |
| --- | --- | --- |
| `source-manifest.json` (438 paths) | SHA-256 of every listed path | 438 ok, 0 mismatch, 0 missing |
| `fe-evidence/manifest.json` `files[]` (202 entries) | recompute SHA-256 + byte count | 202 ok, 0 mismatch, 0 missing |
| `fe-evidence/manifest.json` `cases[]` (38) | compare with `fe-evidence/runs/*` dirs | 38 declared, 38 on disk, no extras |
| `site/evidence.json` `artifacts[]` (23) | recompute SHA-256 | 23 ok, 0 mismatch, 0 missing |
| evidence ID references | resolve every ID used in categories/cases/figures | 0 dangling |
| `site/scientific-snapshot.json` `files[]` (33) | recompute SHA-256 | 33 ok, 0 mismatch, 0 missing |
| per-run `provenance.json` `source_sha256` (456 entries) | recompute SHA-256 of shipped sources | 456 ok, 0 mismatch, 0 missing |
| per-run `input_sha256` (38) | recompute SHA-256 of shipped `input.i` | 38 ok, 0 mismatch |
| embedded supplement archive, inner `manifest.json` (33 payload files) | recompute SHA-256 of zip payload | 33 ok, 0 mismatch (archive internally consistent) |
| archive bytes embedded in the PDF | `pdfdetach -saveall build/main.pdf` then compare | `cec4b5ff…` == shipped `build/conformal-2026-09-20-v1.zip` |
| site builder validation | `python3 tools/build_verification_site.py --validate-only` | `{"manifest": "valid", "artifacts": 23, "scientific_checks_executed": false}` |
| citation keys | 22 `\cite…` keys vs 22 bib keys | all cited keys resolve; all bib keys cited |

Literal excerpts:

```
fe manifest files listed 202 ok 202 mismatch 0 missing 0
cases declared 38 disk 38
evidence.json artifacts ok 23 mismatch 0 missing 0
dangling evidence id refs: []
scientific-snapshot ok 33 mismatch 0 missing 0
provenance source entries checked: 456 input hashes checked: 38
problems: 0
```

```
$ pdfdetach -list build/main.pdf
1 embedded files
1: conformal-2026-09-20-v1.zip
$ pdfinfo build/main.pdf | grep Pages
Pages:           22
```

### 2.2 Re-executed Python suites (run the commands from the README, not the prose)

```
$ python3 validation/mandel_reference.py --self-check
... "passed": true, 38 checks, "central_overshoot": {"ratio": 1.0546586069998425, "time": 0.015165352045764979} ...
```
Consistent with the published claim of 38 self-checks and 5.4659 % peak overshoot at t = 0.01516535.

```
$ python3 examples/verify_conformal.py
checks_passed: 186
max_constitutive_identity_error: 2.4549890331732928e-09
observed_orders: {"energy_stress": [2.0004, 2.0001, 2.00002, 2.00001], "pore_volume": [...~2.000...],
                  "pressure": [1.99999, 2.00028, 2.00029, 1.98915]}
legacy_states: 5 states × 13 identities = 65
```
Consistent with "186 named checks", "65 … five states times thirteen per-state identities" and
"largest absolute error … 2.5×10⁻⁹". The build/conformal/verification.json check set shows
`categories: {implementation: 139, analytical: 44, convergence: 3}` and no failed check.

```
$ python3 examples/verify_fluid_coupling.py
{"scope": "Fluid EOS and reference-mass derivatives; not FE verification", "count": 110,
 "passed": true, "maximum_scaled_error": 8.086725789002713e-09}
```
Consistent with "110 checks, max scaled error 8.09e-09".

```
$ python3 examples/verify_tensor.py
materials: 13, states_per_material: 21, total_states: 273, all errors < 1.8e-9
$ python3 examples/verify_reconstruction.py
materials: 20, incompatible_pairs_rejected: 20, compliance error 1.4e-16, unjacketed 5.1e-14
```
Consistent with "273 finite states across 13 mineral stiffnesses" and "twenty additional mineral
stiffnesses".

### 2.3 Independent re-derivation of the physics numbers (from the shipped model/artifacts)

Recomputed with `examples/conformal_model.py` and the shipped CSV/JSON data:

- `K_s = 28 K_*` for the example mineral stiffness; `0 < K = 7 < φ_s0 K_s = 16.8`. ✔ (paper claim)
- Reference Biot from `B_0 = I − ℂ^d:ℂ_s⁻¹:I`: `diag = [0.700000, 0.758333, 0.791667]` ✔ (paper: 0.7000, 0.7583, 0.7917).
- Isotropic comparison mineral shear modulus `16.8 K_*` (mean of the five deviatoric modes ÷ 2) ✔.
- Drained compliance restriction, computed directly:
  `max|(ℂ^d)^{-1} − (φ_s0 ℂ_s)^{-1} − α/(9K) I⊗I| = 8.67e-18` ✔ rank-one spherical term.
- Mandel inputs: `α_dist = 1 − K/(φ_s0K_s) = 0.5556`, reference Biot `B_0 = 1 − K/K_s = 0.6`,
  drained `ℂ^d = isotropic(K=1, G=0.75)`, `1/M = (α−φ)/K_s + φ/K_f = 17/80 = 0.2125`,
  `K_u = K + α²M = 2.69412`, `ν = 0.2`, `S_s = φ_s0/K_s(1−K/(φ_s0K_s)) = 0.2`,
  total storage `(1−φ_s0)/K_f + S_s = 0.2125 = 17/80`. ✔ (hand recomputation matches the shipped deck inputs and `mandel-reference.json`).
- Pressure tangent identity (eq. `cauchy-pressure-tangent`), independent finite differences at a finite
  anisotropic state `F = shear_gradient(0.65)`, `p = 2`: `max|dσ/dp + B| = 5.2e-8` with `max|B| = 0.806` (FD-error level). ✔
- Pore-volume identity (eq. `biot-pore-volume-variation`): `δ(J−φ_s0J̄)/J = B:(δF F⁻¹)` reproduced to relative error 1e-7 / 6e-7 for two independent perturbations. ✔
- Isochoric shear experiment: anisotropic mineral changes volume (`J̄ = 0.967`, `B₁₂ = 0.01448`) while
  the isotropic comparison gives `B₁₂ = 0`; internal rotation `R_A` does not enter `B`, `J̄`, or the energy. ✔ (paper claims)
- `186`-check suite's `R_A`-independence and phase-stress/energy agreement confirmed by the re-run above.
- Finite-element diagnostics recomputed from `fe-evidence/runs/*/analysis.json`:
  - anisotropic family (6 runs): peak center pressure 0.206181–0.215774 at t = 0.002–0.004;
    max `force_relative` 1.2764e-10; max mobilized-mass residual 2.4699e-10. ✔ (site claim 0.2062–0.2158, ≤1.276e-10, ≤2.47e-10)
  - isotropic run: peak 0.223827, `force_relative` 3.2144e-12. ✔ (0.2238, 3.214e-12)
  - partial family (4 runs): peak 0.200515–0.201629 at t = 0.002–0.0035; max `force_relative` 2.0521e-10;
    max mobilized-mass residual 4.6363e-10. ✔ (0.2005–0.2016, ≤2.052e-10, ≤4.636e-10)
  - manufactured-solution orders recomputed from `mms_space_*` norms: ux 2.992/2.958, uy 2.998/2.960,
    p 1.997/2.001; temporal successive-difference orders nx=16 (1.093, 0.978, 1.015), nx=32 (1.397, 1.018, 1.125),
    nx=64 (1.396, 1.076, 1.252). ✔ (site claim exactly)
  - finite-load floor: `figures/fe_load_limit.csv` gives 0.0032209 at `nonlinear_load_0.0001, nx=20, dt=1e-3`. ✔ ("floors at about 3.2e-3")
  - Jacobian decks: `max_relative_difference` 2.39e-7 < contract target 1e-6, `passed: true`. ✔

### 2.4 Source fidelity of kernels/materials to the stated equations

Read `moose_app/include/utils/ConformalLaw.h`, `moose_app/src/materials/ConformalMaterial.C`,
`moose_app/src/kernels/ReferenceBalance.C`, `moose_app/src/main.C`, and the postprocessors, and traced each
residual/property to the manuscript equations:

- `τ̂_s = F [∂log C/∂C : T] Fᵀ` implemented as a Gauss–Legendre resolvent integral
  `Σ_n (I+Dx_n)^{-1} T (I+Dx_n)^{-1} w_n`; this is the exact Fréchet derivative in
  `eq:log-frechet-spectral-form`. ✔
- `B = I − J̄/(J[K_s+αpJ̄]){K I − (φ_s0/3)α F[∂log C/∂C : dev(ℂ_s:I)]Fᵀ}` matches
  `eq:anisotropic-biot-explicit` term by term (`devCsI = ℂ_s:I − 3K_s I` equals `dev(ℂ_s:I)`). ✔
- `σ = (φ_s0/J)τ̄_s − (1−φ_s)p I` matches `eq:total-stress-phase-energy`; `P = JσF^{-T}` matches
  `eq:fe-total-first-piola`; momentum kernel `∇φ_i·P_iJ` matches `eq:fe-momentum-residual`. ✔
- Fluid EOS `ρ̄_f = ρ̄_{f0}exp(p/K_f)`, `m_f = ρ̄_f(J−φ_s0J̄)`, `Q_f = −Jρ̄_f (k/μ_f) F⁻¹F⁻ᵀ Grad p`,
  Backward-Euler mass kernel match `eq:fe-fluid-eos`…`eq:fe-fluid-residual`. ✔
- `ℂ^d = φ_s0ℂ_s − (φ_s0/(9K_s))α(ℂ_s:I)⊗(ℂ_s:I)` matches `eq:drained-stiffness-restriction`. ✔
- Deck inputs are the stated synthetic parameters; the isotropic decks use `isotropic_stiffness(28,16.8)`
  and the linear reference decks `isotropic_stiffness(2.5, 5/6)` with `linear_reference = true`. ✔
- `validation/equation_to_moose_map.yml` and `validation/theory_traceability.yml` are consistent with the
  sources and with `main.tex` (Q2 displacement, Q1 pressure, backward Euler on reference fluid mass).

I found no physics, convention, or parameter error in the manuscript, the model, or the evidence, and no
misstatement of an equation by a kernel or material.

## 3. Findings with severity

**Finding 1 — Severity: Low (packaging/provenance inconsistency; requires action).**
The shipped supplement archive `build/conformal-2026-09-20-v1.zip` is one revision behind the shipped
sources. Its payload copies of two repository files differ from the same paths in the snapshot:

```
$ python3 <compare zip payload vs repository>      # (excerpt)
Entries whose ZIP payload differs from same path in repository:
  README.md
     zip:  4af375dfffbeb4ef9c904315e912ca5864fe740f98fd52c31e420abc2c53a924
     repo: ba62b25c4bc50a9223d65a4255b6c91d6d3bab0c8d6638b9b83bcda2dc4fa684
  build/conformal/verification.json
     zip:  fb1b8b70d19342e89b4c3d4bca02013c190af34090da34b5dca5479afa434af8
     repo: 6ffa6e02427b6178ed9aeb64e8c6f1a15603682f6730934dfcd818eeae7b2d0a
  examples/verify_conformal.py
     zip:  47c098923e0945aca742950cdea27b65fbfa4212ad481494a7aeb18cfa837f2d
     repo: 412f0fb8afe994d1718289a1850c36ac00d76ef5a1fc05b0b42aceda3351a3cb
```

The archive's internal `manifest.json` is self-consistent (33/33 payload hashes match), but the archived
`build/conformal/verification.json` is a **provenance record whose declared source digest does not resolve
against the shipped sources**:

```
zip  source_sha256: {"conformal_model.py": "035928ba…", "verify_conformal.py": "47c09892…"}
                     versions: {python 3.10.12, numpy 2.2.6, scipy 1.15.3}
repo source_sha256: {"examples/conformal_model.py": "035928ba…", "examples/verify_conformal.py": "412f0fb8…"}
                     versions: {python 3.10.12, numpy 1.26.4, scipy 1.15.3}
```

The scientific content is unaffected: the two report bodies contain the identical 186 checks with identical
values, and the only source difference is the `source_sha256` key prefix (`examples/`), plus the recorded
NumPy version. The manuscript's own reference to this report is
`site/reports/conformal-verification.json` (sha256 `6ffa6e02…`), which is `build/conformal/verification.json`
in the repository and is **not** the copy inside the embedded archive (`fb1b8b70…`). Because the archive's
README states it "contains the exact numerical sources, parameters, figure data, figures, verification
reports, and software versions used in the article", the mismatch is a declaration that does not hold.

**Finding 2 — Severity: Low (informational, no action strictly required).**
Several shipped evidence records declare paths that intentionally lie outside this frozen snapshot. They are
provenance identifiers, not reproducible-in-snapshot paths, and I list them only so the record is complete:

- `fe-evidence/mms-convergence.json` `"runs_dir": "/home/jfoster/.../.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs"`,
  and every per-run `provenance.json` `command[]` binary/deck path under the same runtime directory.
- `references/notes/weighted-stress-reconsideration.md` declares
  `references/pdfs/gajo-2010-compressible-constituents.pdf` (not shipped).
- `provenance/manuscript-export.json` lists `.latexmkrc`, `.vscode`, `Makefile`, `agent_environment`,
  `agent_workflows` (not shipped).
- `provenance/weighted-stress-source-manifest.json` records companion-repository paths (`paper/main.tex`,
  `all.bib`, …) and a companion `AGENTS.md` hash `9138064e…` that differs from this repository's
  `AGENTS.md` (`618ec2de…`); correctly labelled as companion-source provenance.
- The supplement archive omits `examples/verify_fluid_coupling.py` and its report, although the
  fluid-coupling check is cited as implementation evidence (see optional suggestion 2).

**Finding 3 — Severity: Low (informational; stale statement in the shipped review policy README).**
`reviews/README.md` states "The final 13-page PDF builds without warnings", while the shipped
`build/main.pdf` is 22 pages and `build/main.log` contains one `Underfull \hbox` (badness 1137, lines 25–32).
The sentence sits in the paragraph scoped to the archived round-7 snapshot ("The reviewed scientific
snapshot is `round-7/source-sha256.txt`"), and the README's round tables stop at round 7 while this snapshot
is round 15; the round-4/round-7 evidence files it cites are not shipped. No scientific claim depends on it.

## 4. Required corrections

1. **Re-package (and re-embed) the numerical supplement so its payload matches the shipped sources and
   reports.** Re-run `python3 examples/verify_conformal.py` and then
   `python3 tools/package_numerical_supplement.py`, and rebuild/refresh the PDF attachment
   (`\embedfile … build/conformal-2026-09-20-v1.zip`), so that the archived `build/conformal/verification.json`
   declares `source_sha256.verify_conformal.py = 412f0fb8…` and the archive's `examples/verify_conformal.py`
   equals the shipped copy. *Why required:* the archive is shipped evidence; its `verification.json` is a
   provenance record that currently declares a source digest (`47c09892…`, `numpy 2.2.6`) inconsistent with
   the shipped source (`412f0fb8…`, `numpy 1.26.4`), and the published report
   (`site/reports/conformal-verification.json`, `6ffa6e02…`) is not the copy a reader obtains from the
   supplement, contradicting the archive README's "exact numerical sources … used in the article".
   Alternatively, if the archive is intended to be an immutable `v1` build, the archive README must stop
   claiming to contain the exact sources and state the revision boundary explicitly.

No physics, source-fidelity, or numerical correction is required.

## 5. Optional suggestions

1. Soften the archive README wording from "the exact numerical sources … used in the article" to a statement
   of the archive's version and provenance, so a later repository edit cannot falsify it.
2. Consider adding `examples/verify_fluid_coupling.py` and
   `site/reports/fluid-coupling-verification.json` to the supplement archive (or state in
   `sections/experiments.tex` that the archive covers only the conformal constitutive suite), since the
   fluid-coupling checks are cited as implementation evidence.
3. Refresh the `reviews/README.md` "final PDF" sentence to name the archived snapshot explicitly (e.g. "the
   round-7 PDF, 13 pages") so it cannot be read as describing the current 22-page PDF.
4. Consider listing the supplement archive itself as an `artifacts` entry (kind `supplement`) in
   `site/evidence.json` so the published archive is on the hash-verified publication allowlist.

## 6. Review limitations

- The snapshot ships no compiled MOOSE binary, an Exodus `solution.e`, or the per-step
  `solution_profile_*.csv` dumps; the coupled finite-element results could therefore not be re-solved. I
  audited them by recomputing every reported diagnostic from the shipped `analysis.json`, `solution.csv`,
  `reference_comparison.csv`, and `figures/*.csv`, plus the reported Jacobian, mass-balance, force-balance
  and platen-equality contracts. This confirms the records are internally consistent and arithmetically
  match the manuscript, but it does not independently reproduce the solver run.
- Environment drift: the re-run suites used Python 3.10.12 / NumPy 2.4.2 / SciPy 1.17.1, whereas the shipped
  reports record NumPy 1.26.4 (repo) and 2.2.6 (archive). All re-run values matched the shipped reports
  within the stated tolerances, but hash-level reproduction of JSON/PDF bytes was not attempted (and the
  archive README states platform differences need not reproduce bytes).
- I could not verify the external provenance claims that depend on sources outside the snapshot: the
  companion manuscript commit `223901199e33…` (cited in `references.bib`), the parent revision `eafd009…`
  (`provenance/branch_history.md`), the companion inspection commit `e62234c8…`, the Gajo (2010) full-text
  digest, and `site/evidence.json` `provenance.source_revision` `ecfe4a22…`. The snapshot is not a Git
  checkout, so these hashes/commits were accepted as declared, not confirmed.
- Per the review policy, I did not read any other reviewer's report, any other `reviews/round-*` directory,
  or any prior-round verdict; only `reviews/README.md` was available and was read as shipped policy.
- `main.tex` was inspected for equation/notation consistency against the model and evidence, not
  copy-edited line by line; prose quality is outside this charge.

VERDICT: MINOR REVISION

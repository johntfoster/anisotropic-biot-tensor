# Reviewer 2 report — Round 20

Scope: independent simulated peer review of the frozen snapshot
`.agent-runtime/review-snapshots/round-20` only. Emphasis: physics and source
fidelity, packaging/reproducibility, evidence coverage. All scratch work was
done under `/tmp/r20`; no snapshot file was modified.

## 1. Snapshot identity and manifest

| Item | Value |
|---|---|
| Declared `SNAPSHOT_ID` | `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b` |
| `sha256(source-manifest.json)` (observed) | `542eab1bb76847fbbe65596374191d99ffeb287b216651398c0ebfb37895aa0b` |
| Match | **YES** |
| Manifest entries | 534 |
| Files present on disk | 536 (534 listed + `SNAPSHOT_ID` + `source-manifest.json`) |
| Re-hashed, hash OK | 534 |
| Missing | **0** |
| Hash mismatch | **0** |
| Listed files absent from disk | 0 |
| Unlisted files present | 2 (`SNAPSHOT_ID`, `source-manifest.json`; self-referential, expected) |

Integrity is clean. Every manifest digest reproduces exactly.

## 2. Physics and source fidelity

### 2.1 Internal consistency of the derivation (independently re-checked)

I rebuilt the key algebra rather than trusting the text:

- `F = A F̄`, `A = a^{1/3} R_A` (main.tex:eq. `spherical-distention`). Then
  `C̄ = F̄^T F̄ = a^{-2/3} C` with `R_A` cancelling
  (main.tex:eq. `conformal-mineral-metric`). Correct: the internal rotation
  drops out of the mineral metric, so a volume-only distention energy makes
  the response independent of `R_A`. This is the central physical claim and it
  holds.
- Rotated mineral stress `σ̄_s = R_A σ̂_s R_A^T`
  (main.tex:eq. `rotated-mineral-cauchy`). I checked it is **not** an
  independent postulate but is implied by the phase balance: from
  `τ' = φ_s0(τ̄_s + p J̄ I)` together with the virtual-work identity
  `φ_s0 τ̂_s = R_A^T τ' R_A − φ_s0 p J̄ I`
  (main.tex:eq. `distention-mineral-energy-work`, `constitutive-kirchhoff-phase-stress`),
  the rotation relation follows exactly because the pressure term is isotropic.
- Volume-fraction identities are mutually consistent: `J φ_s = φ_s0 J̄` follows
  from `J ρ_s = φ_s0 ρ̄_s0` and `J̄ = ρ̄_s0/ρ̄_s`, and gives both
  `τ' = φ_s0(τ̄_s + p J̄ I)` and `σ = (φ_s0/J) τ̄_s − (1−φ_s) p I`. No factor
  inconsistency found.
- Pore-volume variation `δ(J − φ_s0 J̄)/J = B:(δF F^{-1})`
  (main.tex:eq. `biot-pore-volume-variation`) follows from the push-forward
  identity `(A F^T):(δF F^{-1}) = A:δF`; verified.
- **Biot tensor reduction checked.** At `F = I`, `p = 0`,
  `∂log C/∂C` is the identity on symmetric tensors, so the explicit expression
  (main.tex:eq. `anisotropic-biot-explicit`) reduces to
  `B_0 = I − C^d:C_s^{-1}:I` (limits.tex:eq. `reference-biot-compatibility`).
  I confirmed this reduction symbolically from
  `C^d = φ_s0 C_s − (φ_s0/9K_s)(1 − K/(φ_s0 K_s))(C_s:I)⊗(C_s:I)`
  (stress_reconstruction.tex:eq. `drained-stiffness-restriction`). The two
  expressions agree identically. The isotropic branch of the explicit formula
  also reproduces limits.tex:eq. `reconstructed-isotropic-source-biot`.
- Claim in main.tex that a cubic mineral gives `dev(C_s:I) = 0` (so `B` stays
  spherical) is correct: cubic symmetry makes the three normal diagonal entries
  of `C_s:I` equal.
- Constitutive signs/conventions (`σ = φ_s σ̄_s − (1−φ_s) p I`,
  `τ' = J σ'`) are self-consistent throughout; the scalar companion limit
  (stress_reconstruction.tex, `equivalent-volumetric-energy`) stacks correctly.

### 2.2 Numerical values asserted in the text — reproduced from the shipped reports

| Claim (text) | Evidence in snapshot | Observed | Status |
|---|---|---|---|
| Reference Biot components `0.7000, 0.7583, 0.7917` (experiments.tex) | `build/weighted-stress/states.tex:1`, `build/conformal/experiments.json` `reference_B`, `pressure.dat:2` | `0.7, 0.75833…, 0.79166…` | matches |
| `K_s = 28 K_*` | recomputed `(1/9) I:C_s:I` from eq. `example-mineral-stiffness` | `28.000` | matches |
| Isotropic comparison `μ_s = 16.8 K_*` = "mean of the five deviatoric modes ÷ 2" (experiments.tex) | recomputed eigenvalues of the deviatorically projected `C_s` | `{20,24,28,42.967,53.033}`, mean `33.6`, `/2 = 16.8` | matches |
| Mandel reference `G = 0.75`, `α = 0.6`, total storage `17/80` (finite_elements.tex) | recomputed `φ_s0 μ_s = 0.75`; `1 − K/K_s = 0.6`; `(1−φ_s0)/K_f + S_s = 0.0125 + 0.2 = 0.2125 = 17/80` | matches | matches |
| Conformal suite "186 named checks", largest identity error `2.5×10^{-9}` (experiments.tex) | ran `examples/verify_conformal.py`; `build/conformal/verification.json` | `checks_passed = 186`; `max_constitutive_identity_error = 2.4549890331732928e-09` | matches |
| "65 per-state identities (five states × thirteen)" | `legacy_states` length 5 | `5 × 13 = 65` | matches |
| Spherical-gauge "273 finite states across 13 mineral stiffnesses" | `build/weighted-stress/tensor-verification.json` | `total_states = 273`, `materials = 13` | matches |
| Fabric probe "worst absolute difference `4.9×10^{-15}`" (finite_elements.tex) | ran `examples/verify_fabric.py` | `worst probe-field absolute difference = 4.885e-15` | matches |
| Conformal reduction "to `1.9×10^{-14}`" | `examples/verify_fabric.py` output | max diff `1.874e-14` | matches (rounds to 1.9e-14) |
| Peak centre pressures `6.28/5.10/3.95×10^{-5}` vs `5.13×10^{-5}` uncoupled (finite_elements.tex) | `figures/fe_fabric_mandel_peak.csv` | `6.2803e-5, 5.1022e-5, 3.9461e-5, 5.1326e-5`; peak = final time (0.003) | matches |
| "normalized pressure discrepancy remains about `3.2×10^{-3}`" at `nx=20, dt=10^{-3}` (main.tex:556) | `fe-evidence/runs/nonlinear_load_0.0001/analysis.json` (`nx=20, dt=0.001`) | `pressure_max_normalized = 0.003220919735602341` | matches |
| MMS spatial convergence ≈ 2nd order (finite_elements.tex) | `fe-evidence/mms-convergence.json` | `ux_l2` difference order `2.997`, `p_l2` `1.995` | matches |

Every headline number I could pin to a shipped artifact reproduces.

### 2.3 Citation and novelty fidelity

- I resolved **all 36** bibliography DOIs against Crossref and compared
  author/journal/volume/pages/year. All agree; the only differences are LaTeX
  en-dash vs ASCII page separators. Two benign metadata notes:
  `dehghanipentamerodio2019` is dated 2019 in `references.bib` while Crossref
  carries an online-2018/issue-2019 date; `flory1961` and
  `macminnetal2016`/`uno2022` have Crossref page fields that are truncated or
  absent (article numbers), which the bib fills correctly.
- `fosterxu2025` resolves to *J. Mech. Phys. Solids* **204**, 106263 (2025),
  matching `references.bib`. (Note: the workspace `AGENTS.md` note cites
  `204:105259`; that workspace note is stale and is **not** a manuscript
  defect.)
- Novelty differentiation from Cowin-type fabric poroelasticity is explicit and
  correct. Introduction states the fabric "does not stand in for anisotropic
  elastic constants of the solid, but enters the distention energy of the pore
  space", and `sections/pore_fabric.tex` restates the distinction and the
  fabric-as-isotropic-function-of-invariants requirement, citing
  `cowin1985fabric`, `turnercowin1987`, `cowin2004fabric`,
  `cowinmehrabadi2007`, `moesencardosocowin2012`. Each cited work is about the
  elasticity-tensor/fabric-tensor relation or anisotropic poroelastic
  coefficients assigned to the solid, exactly as described. `hudson1981`
  (oriented cracks) and `thompsonwillis1991` (tensor structure of anisotropic
  poroelasticity) support the sentences they attach to.
- Scope honesty is good: the abstract, `sections/experiments.tex` and
  `sections/finite_elements.tex` repeatedly state that the FE demonstrations
  are implementation verification of the constant reference tangent and
  finite-load demonstrations, not quantitative verification of the nonlinear
  law, and that there is no experimental validation. The partial-drainage runs
  are explicitly excluded from verification claims
  (finite_elements.tex, "Scope of these results"). I found no overclaiming.

### 2.4 Source-fidelity items not resolvable inside the snapshot

Two attribution claims could not be checked because the cited sources
(Drumheller 2000; Gajo 2010) are not in this snapshot and the review scope
forbids reading the live library:

- main.tex (Discussion) cites `\citet[section~8.9]{drumheller2000}` for the
  "equilibrium similarity transformation" commutation condition.
- limits.tex cites `\citep[eqs.~(3.27),(3.32),(3.34)]{gajo2010}` for the
  equivalence of the isotropic mineral-volume equation to Gajo's model.

These are plausible and consistent with the surrounding argument, but the
exact section/equation anchors are unverified here. Flagged as a limitation of
this review, not as a defect.

## 3. Packaging and reproducibility

### 3.1 Archive contents vs. claims

`build/anisotropic-biot-2026-09-20-v2.zip` — SHA-256
`bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53`,
55 entries (54 payload + `manifest.json`).

- Internal `manifest.json` declares `"version": "anisotropic-biot-2026-09-20-v2"`
  and 54 payload SHA-256 hashes; all 54 files resolve and match; no extra files.
- Contents match the claims in `sections/experiments.tex` (Code and data
  availability) and `README.md`: numerical sources (`examples/*.py`,
  `requirements.txt`), figure/parameter data (`build/conformal/*.csv`,
  `build/weighted-stress/*`), verification reports
  (`build/conformal/verification.json`, `build/fabric/fabric-verification.json`,
  `build/weighted-stress/*-verification.json`), a reproduction `README.md` and
  a file-hash `manifest.json`, `LICENSE`/`LICENSES.md`/`licenses/CC-BY-4.0.txt`.
- The pore-fabric constitutive law and registration material ship as claimed:
  `moose_app/include/utils/FabricLaw.h`,
  `moose_app/include/materials/FabricMaterial.h`,
  `moose_app/src/materials/FabricMaterial.C`, and the decks
  `moose_app/inputs/{fabric_probe.i, conformal_probe.i, fabric_mandel.i}`,
  plus the recorded `fe-evidence/runs/**/solution.csv` histories the fabric
  scripts read. The claim that the **rest** of the coupled FE implementation is
  *not* in the archive is also accurate.

### 3.2 Embedded attachment vs. on-disk archive

```
$ pdfdetach -list build/main.pdf
1 embedded files
1: anisotropic-biot-2026-09-20-v2.zip

$ sha256sum (on-disk)      = bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53
$ sha256sum (pdfdetach -saveall) = bd8c1aceae334c8576b96047f9f90951a4865c7caee7c177600a8936e2e7fe53
$ cmp -> BYTE_IDENTICAL
```

The embedded archive is byte-identical to the on-disk archive. `build/main.log`
ends with `Output written on main.pdf (28 pages, 648772 bytes)` with no LaTeX
errors. All seven `\includegraphics` targets referenced by the sources exist on
disk.

### 3.3 Documented reproduction commands (run in `/tmp/r20/ext`)

The archive `README.md` documents, for the fabric material:

```sh
python3 examples/verify_fabric.py
python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots
```

Observed:

```
$ python3 examples/verify_fabric.py        # EXIT=0
case                              B_par        B_per         ln_h      Jbar      sigma22
fabric_probe_iso               0.883871     0.883871        0.005     0.993677   -0.0202258
fabric_probe_coup_a0           0.850654      0.91027   0.00418052     0.994135   -0.0198106
fabric_probe_coup_a45          0.850654      0.91027  -0.00035695     0.993638   -0.0199924
fabric_probe_coup_a90          0.850654      0.91027  -0.00489442     0.993142   -0.0200899
fabric_probe_conformal              0.6          0.6     1.25e-14     0.997778       -0.017
fabric_probe_stiffaxial        0.883871     0.883871     1.25e-08     0.993677   -0.0239758
fabric_probe_softaxial         0.883871     0.883871    0.0078125     0.993677   -0.0181164
limits:
  no_coupling_isotropic_biot: anisotropy = -1.110223e-16
  coupling_gives_anisotropy: anisotropy = -5.961556e-02
  frozen_shape_isotropic_biot: anisotropy = 1.110223e-16
conformal reduction vs reviewed ConformalMaterial:
  J       1.005000000000 vs 1.005000000000  diff 0.000e+00
  Jbar    0.997777777778 vs 0.997777777778  diff 2.220e-15
  sigma11 0.005500000000 vs 0.005500000000  diff 1.874e-14
  sigma22 -0.017000000000 vs -0.017000000000  diff 1.500e-14
  solid_fraction 0.893532338308 vs 0.893532338308  diff 2.220e-15
worst probe-field absolute difference = 4.885e-15
```

```
$ python3 examples/plot_fabric_results.py --runs fe-evidence/runs --output build/fabric-plots   # EXIT=0
{ "figures": 2,
  "missing": [
    {"family": "fabric_probe_a0",  "reason": "Recorded scalar history is absent"},
    {"family": "fabric_probe_a45", "reason": "Recorded scalar history is absent"},
    {"family": "fabric_probe_a90", "reason": "Recorded scalar history is absent"}],
  "files": ["fe_fabric_mandel.pdf","fe_fabric_mandel.png","fe_fabric_mandel_history.csv",
            "fe_fabric_mandel_peak.csv","fe_fabric_probe.csv","fe_fabric_probe.pdf",
            "fe_fabric_probe.png"] }
```

`verify_fabric.py` reproduces the manuscript's headline fabric numbers (worst
probe-field difference `4.885e-15` = text's `4.9e-15`; conformal reduction
`1.874e-14` = text's `1.9e-14`). The Mandel history and peak CSVs regenerate
byte-identically and the Mandel figure is byte-identical (14444 bytes).

**Defect (required correction) — the pore-fabric probe figure is not
reproducible from the shipped evidence.** The manuscript figure
`figures/fe_fabric_probe.pdf` (referenced at finite_elements.tex, Figure
`fe-fabric-probe`) draws panel (c) "Distention shape response" from the three
families `fabric_probe_a0`, `fabric_probe_a45`, `fabric_probe_a90`. Those runs
are absent from `fe-evidence/runs` (they do not appear in
`fe-evidence/manifest.json` `cases`) and are absent from the archive's
`fe-evidence/runs` payload; the only reference to them anywhere is the plotter's
`SHAPE_CASES` list (`examples/plot_fabric_results.py:59-61`). Consequences:

- Regenerating with the documented command omits panel (c) entirely and prints
  `Shape-response probes absent`; the produced
  `fe_fabric_probe.pdf` is 20085 bytes vs. the shipped 20396 bytes and the
  rendered panels differ (shipped PDF shows panel (c) with numeric ticks; the
  regenerated PDF does not).
- The shipped figure data file `figures/fe_fabric_probe.csv` contains three
  extra rows for `fabric_probe_a0/a45/a90` (with blank `sigma11`, `sigma22`,
  `solid_fraction`) that the documented reproduction does not produce
  (11 vs. 8 lines).
- The figure caption asserts "Values are the recorded material-point outputs
  with no fitted curve"; the referenced outputs are recorded only at an
  unshipped runtime location, so a reader cannot obtain them from the artifact.

The underlying numbers are internally consistent, but the manuscript figure and
its data file are not reproducible from the registered/shipped evidence. Either
promote the three runs into `fe-evidence/runs` + `fe-evidence/manifest.json` +
the archive, or regenerate and re-ship `figures/fe_fabric_probe.pdf` and
`figures/fe_fabric_probe.csv` from `fe-evidence/runs` so the figure matches
what the documented command yields.

### 3.4 Packaging minor notes (optional)

- `examples/plot_fabric_results.py:44` sets `DEFAULT_RUNS` to
  `.agent-runtime/anisotropic-fabric-goal-2026-09-20/runs`, an unshipped
  runtime path; the archive README correctly passes `--runs fe-evidence/runs`,
  so this is only a default-value clarity issue.
- `fe-evidence/manifest.json` / `fe-evidence/mms-convergence.json` record
  `runs_dir` as an absolute runtime path outside the artifact
  (`.agent-runtime/moose-fe-goal-2026-09-20/implementation/runs`). Metadata
  only; it does not affect digest resolution.
- `site/reports/tensor-verification.json` records `numpy 1.26.4` while the
  archive's `build/weighted-stress/tensor-verification.json` records
  `numpy 2.2.6`; the site copy appears stale relative to the archived copy.

## 4. Evidence-manifest coverage

`fe-evidence/manifest.json` inspected against the tree:

| Check | Result |
|---|---|
| Run directories under `fe-evidence/runs` | 50 |
| Cases registered in `manifest.json.cases` | 50 |
| Directory registered but absent | 0 |
| Directory present but unregistered | **0** |
| Files registered in `manifest.json.files` | 278 |
| Registered digests that resolve + match on disk | **278 / 278** |
| Files under `runs/` present but unregistered | **0** |

Every run directory is registered and every recorded digest resolves on disk.
The `not_applicable` list (28 `reference_comparison.csv` paths) is an explicit
declaration of per-case non-applicability, not a coverage hole. No unregistered
directory or file was found.

The one provenance gap is the manuscript-side fabric probe families described
in §3.3, which are referenced by a shipped figure but exist neither as
directories under `fe-evidence/runs` nor as registered cases.

## 5. Findings

### Required

1. **Probe figure not reproducible from shipped evidence** (§3.3).
   `figures/fe_fabric_probe.pdf` panel (c) and `figures/fe_fabric_probe.csv`
   include the families `fabric_probe_a0/a45/a90`, whose runs are absent from
   `fe-evidence/runs`, from `fe-evidence/manifest.json.cases`, and from the
   embedded archive. The documented reproduction command
   (`examples/plot_fabric_results.py --runs fe-evidence/runs ...`) produces a
   different figure and reports `Shape-response probes absent`. Ship/register
   those runs, or regenerate and re-ship the figure and its CSV from the
   registered runs.

### Optional

1. `site/reports/tensor-verification.json` reports `numpy 1.26.4` while the
   archived `build/weighted-stress/tensor-verification.json` reports
   `2.2.6`; refresh the site report so software-version records agree.
2. `examples/plot_fabric_results.py` default `--runs` points at an unshipped
   runtime directory; set the default to `fe-evidence/runs` for the archived
   context.
3. `references.bib` `dehghanipentamerodio2019` year (2019) diverges from the
   Crossref online year (2018); confirm the intended issue year.
4. Drumheller §8.9 and Gajo eq. (3.27)/(3.32)/(3.34) anchors could not be
   verified within the snapshot; confirm against the source papers.

### Not defects (checked and clean)

- Snapshot integrity: `SNAPSHOT_ID` matches; 534/534 digests OK; 0 missing,
  0 mismatch.
- Archive payload vs internal manifest: 54/54 OK; embedded PDF attachment
  byte-identical to the on-disk archive.
- Evidence coverage: 50/50 run directories registered, 278/278 digests
  resolve, 0 unregistered files.
- Physics: derivation internally consistent, key reductions verified
  independently; isotropic/cubic/deviatoric limits correct.
- All headline numerical claims reproduce from shipped reports; all 36
  bibliography entries match Crossref metadata.
- Scope/limitation statements are honest; no overclaiming detected.

VERDICT: MINOR REVISION

# Round 19 — Reviewer 2 (physics, source fidelity, packaging)

Scope: independent review of the frozen snapshot only
(`/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-19`),
declared `SNAPSHOT_ID = ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682`.
All hashing was performed on that snapshot. Scratch work was confined to `/tmp`. No manuscript
or snapshot file was modified.

---

## 1. Snapshot identity and manifest

| Check | Result |
|---|---|
| `sha256(source-manifest.json)` | `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682` |
| Declared `SNAPSHOT_ID` (file) | `ceb3783ac7945cc3f8c31c4d6be514fae873d316a18f3c163dcb78fcb4b6d682` |
| Match | **YES** |
| Manifest entries | 534 |
| Missing files | 0 |
| Hash mismatches | 0 |
| Files present but unlisted | 2 — `SNAPSHOT_ID`, `source-manifest.json` (both self-referential and expected) |

The manifest hash equals the declared snapshot identity, and every listed file resolves to the
recorded digest. Snapshot integrity is clean.

## 2. Artifact presence and hash fidelity

Independent re-hash of every manifest entry (534/534) reproduced the recorded SHA-256 exactly.
The two unlisted files are the manifest itself and the `SNAPSHOT_ID` file, which cannot list
themselves; this is not a discrepancy.

Secondary artifact sets were also re-hashed against their own recorded digests:

- `site/evidence.json` — 32 artifacts, 9 figure entries, 4 cases, 5 reproduction commands,
  5 status categories. Every artifact path exists and every recorded SHA-256 matches. Every
  `figures[].artifact` reference resolves to a declared artifact; all 9 figure paths exist.
- `site/scientific-snapshot.json` — 41 file entries, all present, all digests match; includes the
  new fabric sources (`FabricLaw.h`, `FabricMaterial.h`, `FabricMaterial.C`, `fabric_probe.i`,
  `conformal_probe.i`, `fabric_mandel.i`, `verify_fabric.py`, `plot_fabric_results.py`).
- `fe-evidence/manifest.json` — 202 listed files, all digests and byte sizes match, 0 missing.
  **However, coverage is incomplete**: 11 `runs/fabric_*` case directories (≈55 files: `input.i`,
  `provenance.json`, `analysis.json`, `solution.csv`, `run.log`, `solution_profile_*.csv`) exist
  under `fe-evidence/runs/` but appear in neither the manifest's `cases` (38 entries) nor its
  `files` list. See finding R2-03.
- Supplement archive internal manifest — see §4.

## 3. Equation-to-code traceability

Mapping of `sections/pore_fabric.tex` to `moose_app/include/utils/FabricLaw.h`,
`moose_app/src/materials/FabricMaterial.C` and the decks:

| Manuscript | Code | Status |
|---|---|---|
| `eq:fabric-distention-polar` (A = R_A G^{1/2}) | `FabricLaw.h` header; `evaluate()` builds `epsbar` via E_d | traced |
| `eq:fabric-volume-ratio`, `eq:fabric-tensor` (a = (det G)^{1/2}, H = a^{-2/3}G) | `ln_a = √3·x₀`, `distention_a = exp(ln_a)`, `s.J = 1+tr ε`, `s.y = 1+tr ε̄` | traced |
| `eq:fabric-distention-stress` (S_d = 2∂W_d/∂G) | `S_d = D4 : E_d`, `dd[i][j]` TI moduli, Mandel basis e1–e5 | traced (linearized form, see R2-05) |
| `eq:fabric-equilibrium` (stationarity over G) | `(Dd + φG)x = φ(g + p√3 ê₁)`, `solve = inv(Dd + φG)` | traced (linearized form, see R2-05) |
| `eq:fabric-compliance-restriction` ((C^d)^{-1} = (φ_s0 C_s)^{-1} + D^{-1}) | `A6 = inv6(scale(csm, phi)) + Dp`, `cdm = inv6(A6)`, Dp is the 5-direction (Moore-Penrose) inverse | traced |
| `eq:fabric-transverse-h`, `eq:fabric-transverse-strain`, `eq:fabric-shape-equilibrium`, `eq:fabric-transverse-biot` | five-modulus TI `dd[][]`, `fabric_angle` triad {m,p1,p2}, `b_par/b_per/anisotropy` | traced |
| `eq:fabric-biot-tensor` (finite-deformation fabric Biot tensor) | **no direct code trace**; `bvec = eI − C^d:Cs^{-1}:eI` implements the reference limit `eq:reference-biot-compatibility` only | gap (see R2-05) |
| `eq:fabric-equivalent-energy` (nonlinear W_d + φ_s0 W̄_s) | `energy = ½φ ε̄:C_s:ε̄ + ½ x:Dd:x` | traced (linearized form, see R2-05) |

Deck cross-checks:
- `moose_app/inputs/fabric_probe.i` prescribes `ux = 0.01x`, `uy = −0.005y`, `p = 0.02`, single
  QUAD4 element, all four nodes constrained → exactly ε = diag(0.01, −0.005, 0), J = 1.005. The
  recorded `figures/fe_fabric_probe.csv` shows J = 1.005 for every probe case. Consistent.
- `moose_app/inputs/conformal_probe.i` is the paired cross-check deck; its header documents the
  parameter map `drained_bulk = K ↔ fabric_volume_modulus = 3K/α`, `α = 1 − K/(φK_s)`, and the
  recorded cross-check reproduces the conformal material. Consistent.
- `moose_app/inputs/fabric_mandel.i` uses an isotropic, unrotated mineral (`angle = 0`) and varies
  only `fabric_angle`/`fabric_coupling`, isolating the fabric. Consistent with the manuscript claim.

Code with no manuscript equation: the diagnostic properties `stability` (= K_s, a scalar stability
constant rather than the manuscript's stability domain), `P22`, and the linearized `s.J = 1+tr ε`.
These are diagnostics, not constitutive claims, but they are undocumented in the traceability map.

`validation/equation_to_moose_map.yml` contains entries for `ConformalMaterial`, `ReferenceMomentum`,
`ReferenceFluidMass` and the platen constraint, and **no entry for `FabricMaterial`/`FabricLaw`**.
`validation/theory_traceability.yml` likewise contains no fabric entry (grep for "fabric" in
`validation/` returns nothing). See R2-04.

## 4. Supplement and PDF packaging

**Archive extraction and internal verification** (`build/anisotropic-biot-2026-09-20-v2.zip`,
303 868 bytes, sha256 `869018460c2c137ca621d1dde1fb09556186b010afcabb75c577c8fc325822c5`):

- 43 files; internal `manifest.json` declares `version = anisotropic-biot-2026-09-20-v2` and 42
  SHA-256 digests. Every declared digest matches the extracted payload; no payload file is
  missing; the only file not covered by the internal manifest is `manifest.json` itself. The
  archive does **not** contain a copy of itself (verified via `unzip -l`).
- Contents cover `build/conformal/*` (figure PDFs, CSVs, `verification.json`, `experiments.json`),
  `build/fabric/fabric-verification.json`, `build/weighted-stress/*`, `examples/*.py`,
  `manifest.json`, `README.md`, licenses, and the fabric MOOSE sources
  (`FabricLaw.h`, `FabricMaterial.h/.C`, `fabric_probe.i`, `fabric_mandel.i`, `conformal_probe.i`).
- The archive's copy of each fabric MOOSE source is byte-identical to the frozen snapshot copy
  (verified by direct SHA-256 comparison for all six files).

**PDF embedding**: `pdfdetach -list build/main.pdf` reports exactly one embedded file,
`anisotropic-biot-2026-09-20-v2.zip`; extracted bytes hash to
`869018460c2c137ca621d1dde1fb09556186b010afcabb75c577c8fc325822c5`, identical to the on-disk
archive. The PDF therefore embeds the same archive that ships in `build/`.

**Documented reproduction commands run outside the checkout** (extracted to
`/tmp/r19zip`, Python 3.10.12 / NumPy 1.26.4 / SciPy 1.15.3):

| Command | Result |
|---|---|
| `python3 examples/verify_conformal.py` | exit 0; `checks_passed = 186`, `legacy_identities_rechecked = 67`, `max_constitutive_identity_error = 2.4549890331732928e-09` — **identical** to the archived `build/conformal/verification.json` |
| `python3 examples/verify_tensor.py` | exit 0; `materials = 13`, `total_states = 273`, errors identical to `site/reports/tensor-verification.json` |
| `python3 examples/verify_reconstruction.py` | exit 0; `materials = 20`, `incompatible_pairs_rejected = 20`, `minimum_drained_eigenvalue = 1.8415045063808817` — identical to archived report |
| `python3 examples/conformal_experiments.py` | exit 0; regenerated `experiments.json` differs from the archived file in exactly **one** leaf value: `/versions/numpy` (1.26.4 vs archived 2.2.6). All 168 other leaf values, including every recorded stress, modulus and Biot component, are identical |
| `python3 examples/weighted_stress.py` | exit 0 |
| `python3 examples/verify_fabric.py` | **FAILS** — `FileNotFoundError: .../.agent-runtime/anisotropic-fabric-goal-2026-09-20/runs/fabric_probe_iso/solution.csv` |
| `python3 examples/plot_fabric_results.py` | exit 0 but emits no figures (`"files": []`, `"reason": "Recorded scalar history is absent"`) |

**Manuscript-named supplement does not match the shipped archive.** `sections/experiments.tex:212`
states the supplement "is embedded in the PDF as `conformal-2026-09-20-v1.zip`", and `README.md:45`
states "The packaging command creates `build/conformal-2026-09-20-v1.zip`". The packaging script
(`tools/package_numerical_supplement.py:10`, `VERSION = 'anisotropic-biot-2026-09-20-v2'`),
`main.tex:26–27`, `tools/build_review_snapshot.py:63`, and the actual PDF attachment all use
`anisotropic-biot-2026-09-20-v2.zip`. See R2-01.

**PDF currency and reference resolution**: `build/main.pdf` (28 pages, LuaTeX 1.14.0,
CreationDate 2026-09-20 19:55:05 CDT) is newer than every source it compiles — `main.tex`
(19:54:59), `sections/pore_fabric.tex` (19:54:51), `sections/finite_elements.tex` (19:54:47),
`references.bib` (19:30) — and is newer than the embedded archive (19:54:00). `build/main.log`
contains no `undefined` reference, no multiply-defined label, and no unresolved citation warning
(all `Warning` lines are package boilerplate). All 7 `\includegraphics` targets exist; all 36
`\cite`/`\citep`/`\citet` keys resolve against `references.bib`, with no unused bibliography
entries. The PDF build is current against the frozen sources.

## 5. Physical claims vs raw run data

Every quantitative claim attached to the anisotropic-fabric work was checked against the cited
raw artifacts.

- **Rotated-fabric peak pressures** (`sections/finite_elements.tex`, §"Pore-fabric demonstration"):
  manuscript states 6.28e-5 (fabric axis along X₁), 5.10e-5 (45°), 3.95e-5 (other in-plane axis),
  and 5.13e-5 for the uncoupled deck. `figures/fe_fabric_mandel_peak.csv` gives
  6.2802893621317e-05, 5.1021552207674e-05, 3.9461329623663e-05 and 5.1325507554021e-05. Matches
  to the quoted precision.
- **"Each peak coincides with the final recorded state rather than a transient overshoot"**:
  `figures/fe_fabric_mandel_history.csv` shows monotone rise with `peak_center_pressure ==
  final_center_pressure` and `final_time = 0.003` for all four cases. Confirmed.
- **Platen/force consistency**: `fe-evidence/runs/fabric_mandel_coup_a0/analysis.json` records
  `platen_max = platen_min = -9.5040330693321e-06` (rigid-platen equality holds to round-off),
  `stability_min = stability_max = 2.5`. Consistent with the reported kinematic plate.
- **Independent re-implementation agreement**: manuscript states a worst absolute difference of
  4.9e-15 over B∥, B⊥, distention strains, volume ratios, stresses and solid fraction, and 1.9e-14
  for the conformal reduction. `build/fabric/fabric-verification.json` records
  `worst_probe_abs_diff = 4.884981308350689e-15` and a conformal cross-check maximum of
  1.87436871579294e-14 (`sigma11`). Matches.
- **Direction dependence and its mechanism**: the manuscript's central physical claim is that with
  an isotropic mineral the Biot tensor stays spherical unless the volume–axial distention coupling
  is nonzero. `figures/fe_fabric_probe.csv` supports this in both directions: the three uncoupled
  probes (`fabric_probe_a0/a45/a90`) all give `B_anisotropy ≈ 1.1e-16` with
  `B_par = B_per = 0.7230769`, while `drained_c11` differs by orientation (1.0000 / 1.6490 /
  1.5192) — i.e. the drained compliance is transversely isotropic while B stays spherical, exactly
  as `sections/pore_fabric.tex` states. The coupled probes (`fabric_probe_coup_a*`) give a common
  `B_anisotropy = −0.05961556` with `B_par = 0.8506544`, `B_per = 0.9102700`. The claim is
  substantiated by the data, not merely asserted.
- **Conformal experiment reference values** (`sections/experiments.tex`): stated reference Biot
  components 0.7000, 0.7583, 0.7917. `build/conformal/experiments.json` `highlights.reference_B`
  = [0.7, 0.7583333333333333, 0.7916666666666667]. Matches.
- **Mandel reference constants** (`sections/finite_elements.tex`): φ_s0 = 0.9, K_s = 2.5,
  K = 1, K_f = 8, drained shear G = 0.75, reference Biot coefficient 0.6, total storage 17/80.
  `site/reports/mandel-reference.json`: `K = 1.0`, `G = 0.75`, `alpha = 0.6`,
  `M = 4.705882352941177` (= 1/0.2125 = 80/17), `Ku = 2.6941176` (= K + α²M). Self-consistent and
  matches the manuscript.
- **Check counts**: "186 named checks" and "65 per-state identities (five states × thirteen
  identities)" — `build/conformal/verification.json` has `checks_passed = 186` with
  `legacy_state0..4` × 13 identities = 65. "273 finite states across 13 mineral stiffnesses" —
  `tensor-verification.json` `materials = 13`, `total_states = 273`. "110 checks, max scaled error
  8.09e-09" — `fluid-coupling-verification.json` `count = 110`,
  `maximum_scaled_error = 8.086725789002713e-09`. "41 finite states … 6.4e-14" —
  `cpp-python-constitutive.json` `states = 41`, `value_absolute_error = 6.394884621840902e-14`.
  "38 self-checks (peak overshoot 5.4659% at t = 0.01516535)" — `mandel-reference.json` has 38
  checks with `central_overshoot.ratio = 1.0546586069998425` at
  `time = 0.015165352045764979`. All counts and quoted values match their raw artifacts.
- **Verification-evidence numbers** (`site/evidence.json`, `finite_deformation` category):
  0.2062–0.2158 peak pressure over 6 anisotropic runs, 0.2238 isotropic comparison,
  `force_relative ≤ 1.276e-10`, normalized mass balance ≤ 2.47e-10, and the corresponding partial
  family values all match `site/reports/finite-deformation-summary.json`.
- **Positive phase volumes / stability**: `experiments.json` records `solid_fraction_range =
  [0.4343494142123065, 0.6000000000000001]`, `min_scalar_stability = 28.0`,
  `max_mineral_residual = 3.452793606584237e-14`. The manuscript's "all plotted states satisfy
  positive phase volumes and the scalar stability condition" is consistent.

No physical claim inspected was found to be contradicted by the raw data it cites. The manuscript's
own scoping statements (force-controlled demonstrations, synthetic parameters, no
finite-deformation quantitative verification, no experimental validation) are consistently
reproduced across `sections/finite_elements.tex`, `site/evidence.json` and
`fe-evidence/README.md`.

## 6. Findings

**R2-01 — REQUIRED. Stale supplement filename in the manuscript and README.**
Location: `sections/experiments.tex:212`; also `README.md:45`.
Issue: Both documents name the embedded numerical supplement `conformal-2026-09-20-v1.zip`.
The archive actually shipped and embedded is `anisotropic-biot-2026-09-20-v2.zip`
(`tools/package_numerical_supplement.py:10`, `main.tex:26–27`, `tools/build_review_snapshot.py:63`).
Evidence: `pdfdetach -list build/main.pdf` → one embedded file,
`anisotropic-biot-2026-09-20-v2.zip`; its extracted SHA-256
(`869018460c…`) equals the on-disk archive. A reader following the manuscript's extraction
instruction searches for a filename that does not exist. Fix: update both strings to the shipped
archive name (or re-name the archive consistently).

**R2-02 — REQUIRED. Documented supplementary reproduction command fails outside the checkout.**
Location: `examples/verify_fabric.py:29` (`RUNS = ROOT / ".agent-runtime/anisotropic-fabric-goal-2026-09-20/runs"`);
documented in the archive `README.md` ("Extract the archive, then run from its root … `python3
examples/verify_fabric.py`") and in `site/evidence.json` `reproduction[4]`.
Issue: The extracted archive contains no `--runs` argument, so the script resolves a hard-coded run
directory that exists only in the authoring checkout. Running the documented command from the
extracted archive root raises
`FileNotFoundError: .../.agent-runtime/anisotropic-fabric-goal-2026-09-20/runs/fabric_probe_iso/solution.csv`
and writes no `build/fabric/fabric-verification.json`. Evidence: reproduced in `/tmp/r19zip`.
This is the one supplementary command that does not reproduce; every other documented command
(`verify_conformal.py`, `verify_tensor.py`, `verify_reconstruction.py`,
`conformal_experiments.py`, `weighted_stress.py`) ran successfully and reproduced its recorded
numbers. Fix: accept a runs-directory argument, or ship the required recorded `solution.csv`
files with the archive, or correct the README to state the required input.

**R2-03 — REQUIRED. `fe-evidence/manifest.json` does not cover the fabric run directories it is
intended to certify.**
Location: `fe-evidence/manifest.json`; `fe-evidence/runs/fabric_*` (11 case directories).
Issue: The manifest lists 202 files with verified digests but its `cases` (38) and `files` entries
contain no `fabric_*` case. The 11 fabric run directories — carrying the raw deck, provenance,
per-run analysis, scalar history and solver log that back the paper's fabric-probe and
rotated-fabric numbers — are therefore present on disk without the digest registration that every
other run in the same evidence tree receives. Evidence: walk of `fe-evidence/` versus the manifest's
path set; the fabric files also appear in no `not_applicable` or `provenance_outputs_unshipped`
entry. Fix: register the fabric runs in the evidence manifest (or state explicitly, in
`fe-evidence/README.md`, why they are excluded and where their digests are pinned).

**R2-04 — OPTIONAL. Validation traceability maps omit the new fabric material.**
Location: `validation/equation_to_moose_map.yml`, `validation/theory_traceability.yml`.
Issue: `equation_to_moose_map.yml` enumerates `ConformalMaterial`, `ReferenceMomentum`,
`ReferenceFluidMass` and the platen constraint, with no `FabricMaterial`/`FabricLaw` object; a grep
for "fabric" across `validation/` returns nothing. Since Round 19 adds a full section of new
equations and a new material, the map that the repository uses for equation-to-code traceability no
longer covers the manuscript. Evidence: file contents. Fix: add `FabricMaterial` with its equation
list and approximation note.

**R2-05 — OPTIONAL. Nonlinear fabric equations have only a reference-state code trace.**
Location: `sections/pore_fabric.tex` `eq:fabric-equivalent-energy`, `eq:fabric-equilibrium`,
`eq:fabric-biot-tensor`; `moose_app/include/utils/FabricLaw.h` (`evaluate()` rejects
`linear == false`).
Issue: The header comment and `FabricMaterial` default both state the law is the "reference-state
(linearized)" response, and `evaluate()` throws unless `linear_reference = true`. The code honours
the linearized stationarity of `W_d + φ/2 (ε−E_d):C_s:(ε−E_d) + φ p tr(ε−E_d)` and the reference
Biot limit `eq:reference-biot-compatibility`, but not the general finite-deformation equilibrium
`eq:fabric-equilibrium` or Biot tensor `eq:fabric-biot-tensor`. The manuscript does say the material
"evaluates the reference-state" response and that the coupled runs are demonstrations, so this is
scoped rather than hidden; making the mapping explicit at the equation sites (rather than only in
`sec:fe-fabric`) would remove the residual ambiguity for a reader mapping equations to decks.

**R2-06 — OPTIONAL. Two different "‑v1" labels coexist with the "‑v2" supplement.**
Location: `site/evidence.json:3` (`"version": "fabric-2026-09-20-v1"`);
`tools/register_fabric_evidence.py:97`.
Issue: The companion site manifest is versioned `fabric-2026-09-20-v1` while the article supplement
is `anisotropic-biot-2026-09-20-v2`. Together with R2-01 this means "v1"/"v2" no longer identify a
single artifact family. This is cosmetic but is the root of the R2-01 mismatch.

**R2-07 — OPTIONAL. `plot_fabric_results.py` default invocation produces no figures.**
Location: `examples/plot_fabric_results.py`, invoked by `site/evidence.json` `reproduction[4]` and
the archive README.
Issue: Run without `--runs`, the script exits 0 but writes `"files": []` and reports
`"reason": "Recorded scalar history is absent"` for each case. The archive README documents the
`--runs` form for this script, but the site's reproduction command omits it, so the documented
"Pore-fabric distention verification" command reproduces no figure.

## 7. Overall assessment

**Correctness.** The physics reviewed is internally consistent and its implementation is faithful.
The phase-work balance, the rotation cancellation for a symmetric stress, the spherical rank-one
compliance restriction and its relaxation to the fabric-symmetric form are correctly reflected in
both the manuscript and the code. Every quantitative claim I could attach to a raw artifact —
fabric probe B∥/B⊥, distention strains, drained compliance by orientation, rotated-fabric peak
pressures, platen equality, Mandel constants, and all reported check counts — matches the recorded
numbers to the quoted precision. The independent NumPy re-implementation agrees with the compiled
material at 4.9e-15, and the C++/Python constitutive comparison at 6.4e-14 over 41 states. I found
no physics error and no unsupported physical claim.

**Novelty and significance.** The tensorial distention law is a genuine extension: replacing scalar
dilation with a symmetric positive definite distention whose unimodular part is a pore-fabric tensor
supplies a constitutive route from reaction-induced pore fabric to a directionally anisotropic Biot
tensor, and it relaxes the rank-one drained-compliance restriction of the conformal model to a
fabric-symmetric form. The demonstrated mechanism — directional pressure coupling from the
volume–axial distention modulus behind an isotropic mineral — is a clean, falsifiable prediction
that the recorded probe data supports. The result is modest in scope (elastic, synthetic
parameters, reference-state material implementation) but the scope is stated honestly and
repeatedly.

**Engineering relevance.** The construction gives a defensible way to carry measured pore fabric
into a finite-deformation poroelastic formulation, which is the practical gap the introduction
identifies. Extrapolating it to field or laboratory data will require the plastic/reaction-driven
fabric evolution the authors explicitly place out of scope.

**Packaging.** Snapshot integrity, artifact hashing, the archive's internal manifest, and the PDF
embedding are all exact. The defects are documentational and manifest-coverage, not scientific:
one stale supplement filename in the manuscript and README (R2-01), one documented supplementary
reproduction command that cannot run from the extracted archive (R2-02), and the fabric run
directories missing from the evidence manifest (R2-03). All three are correctable without new
science or new runs. I verified that the archive contains no stale copy of any fabric source and
that the PDF is built after all of its sources, so the fixes do not invalidate the present results.

Because three required, verifiable, non-scientific defects remain in the packaging and
reproducibility surface — one of them a documented command that fails — this snapshot is not
ACCEPT, but nothing found justifies MAJOR REVISION.

VERDICT: MINOR REVISION

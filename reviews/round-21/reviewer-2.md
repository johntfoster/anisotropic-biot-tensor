# Independent review — Round 21, Reviewer 2

**Emphasis:** physics, source fidelity and packaging.
**Snapshot under review:** `.agent-runtime/review-snapshots/round-21`
**Declared SNAPSHOT_ID:** `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`
**Manuscript:** "An anisotropic Biot tensor from mineral stress and distention work"
**Method:** read-only inspection of the frozen snapshot; all scratch work (archive
extraction, builds, re-runs) done in `/tmp`. No snapshot file was modified.

This review is scoped to whether the pore-fabric physics claims match the evidence
actually present, whether the cited literature says what is attributed to it, and
whether the shipped packaging (supplement archive and FE-evidence registry)
reproduces. All findings below are backed by a reproduced command and its output.

---

## 1. Integrity

- `sha256(snapshot/source-manifest.json)` = `f4c43aeea1590c8e166d3ffab342e5da92094443e55b4df4d47b69bbad8c673f`,
  which equals the declared `SNAPSHOT_ID`. **Match.**
- Re-hashed every path in the manifest: **549 / 549 entries present and
  hash-identical; 0 missing, 0 mismatched.**
- Files present on disk but unlisted: exactly `SNAPSHOT_ID` and
  `source-manifest.json` (both are snapshot metadata, not manuscript payload).
  No unlisted manuscript, code, data or figure file. **Clean.**
- `site/scientific-snapshot.json` pins 41 files; all 41 exist and all 41 hashes
  match the working tree.

> ID `INT-1` (location: `source-manifest.json`, whole file) — **no defect**.

---

## 2. Physics and source fidelity

### 2.1 Fabric-dependent anisotropy and transverse isotropy (`sections/pore_fabric.tex`)

- `H = a^{-2/3} G`, `det H = 1` (eq. `fabric-tensor`, lines 77–82): holds.
- Transverse-isotropy ansatz `H = h^{-2} m⊗m + h(I − m⊗m)` (eq.
  `fabric-transverse-h`, lines 280–284): `det H = h^{-2}·h·h = 1` ✓, eigenvalues
  `{h^{-2}, h, h}` are the squared principal shape ratios as claimed (lines 86–88).
- Distention logarithmic strain eq. `fabric-transverse-strain` (lines 291–294):
  from `ln G = (2/3)ln a I + ln h (I − 3 m⊗m)` one gets
  `E_d = ½ ln G = (ln a /3) I + ln h(½ I − 3/2 m⊗m)`; **the printed expression is
  correct.**
- Claim (lines 303–305) that `J̄ = J/a` is independent of `h`, so the shape balance
  `{shape-equilibrium}` has no pressure conjugate: correct — `a` depends only on
  `det G`, not on the deviatoric `H`.

### 2.2 Direction-dependent pore pressure — reproduced from the FE runs

`sections/finite_elements.tex` lines 252–256 assert peak centre pressures
6.28e-5 (fabric along X1), 5.10e-5 (45°), 3.95e-5 (other in-plane axis) and 5.13e-5
with the volume–axial coupling switched off. Recomputing `max(center_pressure)`
directly from the shipped run histories:

| run | recomputed peak | paper | `figures/fe_fabric_mandel_peak.csv` |
|---|---|---|---|
| `fabric_mandel_coup_a0` | 6.2802893621e-05 | 6.28e-5 | 6.2802893621317e-05 |
| `fabric_mandel_coup_a45` | 5.1021552208e-05 | 5.10e-5 | 5.1021552207674e-05 |
| `fabric_mandel_coup_a90` | 3.9461329624e-05 | 3.95e-5 | 3.9461329623663e-05 |
| `fabric_mandel_iso` | 5.1325507554e-05 | 5.13e-5 | 5.1325507554021e-05 |

Run histories, figure CSV and text agree to all printed digits, and peak == final
recorded state in every case, supporting the claim that each peak "coincides with
the final recorded state rather than a transient overshoot" (line 255–256).
The four `fabric_mandel_*` decks share a byte-identical `input.i`
(`sha256 89be4736…`) and differ only by a single recorded override
(`fabric_coupling=0` for `iso`; `fabric_angle=0/45/90` for the coupled runs), which
is exactly the "same deck with the volume–axial coupling switched off" comparison.

- `figures/fe_fabric_mandel_peak.csv` and `figures/fe_fabric_probe.csv` regenerate
  **byte-identically** from `examples/plot_fabric_results.py --runs fe-evidence/runs`.
- The probe figure PDF text confirms the caption structure: panels
  "(a) Reference Biot tensor", "(b) Directional coupling from the fabric",
  "(c) Distention shape response"; the Mandel figure has "(a) Center-pressure
  history" and "(b) Directional pressure response". Figures match their captions.

### 2.3 Reference-state numbers (`sections/experiments.tex`)

- `sections/experiments.tex` line 25 claims reference Biot components
  **0.7000, 0.7583, 0.7917**. Independently recomputing
  `B₀ = I − C^d : C_s^{-1} : I` from eq. `drained-stiffness-restriction` with the
  printed `C_s`, φ_s0 = 0.6, K = 7, K_s = 28 gives
  **0.70000000, 0.75833333, 0.79166667** — and the two places also reproduce the
  shipped `experiments.json` `highlights.reference_B`. **Match.**
- `experiments.tex` lines 28–30 claim the isotropic comparison mineral shear
  modulus is 16.8 K\*. The five deviatoric modes of `C_s` are the two deviatoric
  normal eigenvalues of the 3×3 block (≈42.8, ≈53.2) and the three shears
  (20, 24, 28); their mean is 33.6 and half is **16.8**, matching
  `experiments.json.isotropic_comparison.mu`. **Match.**

### 2.4 Verification magnitudes claimed in prose

| claim (location) | recomputed |
|---|---|
| conformal suite 186 named checks (`experiments.tex` 180) | `verification.json checks_passed = 186` ✓ |
| 65 per-state identities, 5 states × 13 (`experiments.tex` 181) | 5×13 = 65 ✓ |
| largest constitutive identity error 2.5e-9 (`experiments.tex` 186) | `max_constitutive_identity_error = 2.4549890e-09` ✓ |
| spherical-gauge suite 273 states / 13 stiffnesses (`experiments.tex` 191) | `tensor-verification.json`: 13, 21, 273 ✓ |
| fabric material vs NumPy worst diff 4.9e-15 (`finite_elements.tex` 217–219) | `verify_fabric.py`: **4.885e-15** ✓ |
| volume-only limit vs ConformalMaterial 1.9e-14 (`finite_elements.tex` 224–226) | `conformal_cross_check` max abs diff **1.874e-14** ✓ |
| finite-load pressure floor ≈3.2e-3 at nx=20, dt=1e-3 (`main.tex` 556) | `fe_load_limit.csv`: 3.2209e-3 ✓ |
| linear step-refinement 3.7e-3 / 7.1e-3, ratio 1.94 (`main.tex` 559–560) | 3.65796e-3 / 7.10392e-3, ratio 1.942 ✓ |
| MMS temporal orders 0.98–1.40 at nx=16/32/64 (`main.tex` 561–562) | `mms-convergence.json` difference_orders span 0.978–1.397 ✓ |

### 2.5 Citation fidelity (`references.bib`)

- All **36** distinct `\cite` keys used across `main.tex` and `sections/*.tex`
  resolve to entries in `references.bib`; **no** bibliography entry is uncited
  (the multiline `\citep{dehghanipentamerodio2019, dehghanizilian2021}` on
  `main.tex` 160–161 is genuinely cited).
- Spot-checked every attribution used to support the fabric/reaction narrative:
  `cowin1985fabric` (elasticity tensor as isotropic function of fabric tensor),
  `turnercowin1987`, `moesencardosocowin2012` (symmetry-invariant form),
  `cowin2004fabric`/`cowinmehrabadi2007` (fabric formulation of anisotropic
  poroelasticity), `hudson1981` (crack fabric), `rudgekelemen2010`, `jons2017`
  (3D microtomography), `uno2022` (reaction fracturing/self-accelerating flow),
  `putnis2002/2009`, `ruizagudo2014`, `geisler2007`, `altreewilliams2015`
  (interface-coupled dissolution–precipitation). Every entry exists, and the
  sentences attribute claims consistent with the cited titles/venues. The
  introduction's explicit disclaimer (`main.tex` 137–141) that the fabric is
  attached to the *distention energy* rather than standing in for the solid's
  anisotropic elastic constants is an accurate statement of the departure from
  the Cowin line of work. **No overstatement of a source found; nothing uncited.**

> IDs `PHYS-1 … PHYS-6`, `CITE-1` — no required defect identified.

---

## 3. Supplement archive (`build/anisotropic-biot-2026-09-20-v2.zip`)

- The archive is **byte-identical** to the file embedded in `build/main.pdf`
  (`pdfdetach -saveall build/main.pdf` yields `sha256 f24b3d01…`, the same as the
  on-disk zip). Attachment present: `anisotropic-biot-2026-09-20-v2.zip` (1 embedded file).
- **Self-consistency:** the archive's own `manifest.json` lists 57 payload files;
  on a clean extraction **0 missing, 0 hash mismatches, 0 unlisted payload files**.
- **Self-containedness:** extracted to a clean directory, the reproduction
  commands in the archive README ran to completion with no repository checkout:
  `weighted_stress.py`, `verify_reconstruction.py`, `verify_tensor.py`,
  `verify_conformal.py`, `conformal_experiments.py`, `verify_fabric.py` — all
  exit 0 — plus
  `plot_fabric_results.py --runs fe-evidence/runs` which regenerates the two
  fabric figures and their CSVs byte-identically.
- `verify_fabric.py` reproduces the archived `build/fabric/fabric-verification.json`
  with **zero numeric differences** (deep-compared to the snapshot copy) and the
  printed worst probe-field difference 4.885e-15.
- The archive ships `moose_app/include/utils/FabricLaw.h`,
  `moose_app/include/materials/FabricMaterial.h`, `moose_app/src/materials/FabricMaterial.C`
  and the decks `fabric_probe.i`, `conformal_probe.i`, `fabric_mandel.i`, together
  with the recorded run histories `examples/verify_fabric.py` reads — matching the
  list claimed in `sections/experiments.tex` lines 220–226.

> ID `PKG-1` — no required defect. See OPT-1/OPT-2 for non-blocking wording notes.

---

## 4. FE-evidence registry (`fe-evidence/manifest.json`)

- Registry lists exactly the **53** run directories present on disk
  (no unregistered runs, no phantom entries).
- Every shipped file under `fe-evidence/` is registered in `files[]`
  (293 entries); the only files not listed are `README.md` and `manifest.json`
  themselves.
- The per-run `analysis_present` / `reference_comparison_present` flags match the
  files on disk for all 53 runs.
- Cross-check of the recorded `source_sha256` digests in every
  `runs/*/provenance.json` against the shipped `moose_app/` sources:
  **456 digests checked, 0 mismatches.**
- The coupled fabric runs registered there are the exact runs behind Figures
  `fe_fabric_probe` and `fe_fabric_mandel`; their values match the figures (Section 2.2).

> ID `REG-1` — no required defect.

---

## 5. Manuscript build (packaging cross-check)

`latexmk -lualatex -halt-on-error` on a writable copy rebuilds `main.pdf`
(28 pages, 651795 bytes — identical byte size to the snapshot PDF), the final log
contains **0 undefined references and 0 undefined citations**, all seven
`\includegraphics` targets exist, and the supplementary ZIP remains embedded.
The hash difference versus the snapshot PDF is confined to PDF metadata/timestamps,
which the archive README expressly declares non-reproducible across platforms.

> ID `BUILD-1` — no required defect.

---

## REQUIRED changes

**None.** I could not demonstrate a defect in any physics claim, citation
attribution, registry entry, archive hash, or reproduction step. Every headline
number I could independently recompute reproduced as printed.

---

## OPTIONAL notes (non-blocking)

- **OPT-1 — README wording.** The archive README states "The models are synthetic
  homogeneous constitutive calculations, not physical validation or
  finite-element simulations," while the same archive ships MOOSE finite-element
  run histories (`fe-evidence/runs/*/solution.csv`) and FE decks. The sentence is
  true of the conformal models it introduces, but read in isolation it can be
  mistaken for a claim about the whole archive. Consider "The *conformal* models …"
  for clarity. (Location: archive `README.md`, paragraph 1.)
- **OPT-2 — Deck runnability.** The archive ships `moose_app/inputs/*.i` but not
  the application build scaffolding (`Makefile`, `AnisotropicBiotApp.C`, `main.C`,
  `ReferenceBalance`), so those decks cannot be executed from the archive alone.
  This is already disclosed in `sections/experiments.tex` lines 226–231; an
  explicit one-line note next to the decks would prevent a reader from expecting
  a runnable build.
- **OPT-3 — "verified" vs "checked against".** The abstract
  (`main.tex` 48–50) says the FE implementation is "verified against … the
  constant-coefficient consolidation reference". The manuscript itself is candid
  that this comparison floors at ≈3.2e-3 and is a discretization floor
  (`main.tex` 555–562). The disclosure is adequate; if a more conservative verb
  ("checked against") is desired at the abstract level it would remove any
  residual ambiguity, but this is editorial only.
- **OPT-4 — provenance pin.** `site/evidence.json` records
  `provenance.source_revision = ecfe4a22…` with the note that the base commit
  predates the working revision. Accurate and disclosed; a short statement of
  which files are covered by that revision versus the working tree would make the
  pin easier to audit.

---

## Verdict rationale

Integrity is exact (549/549). The pore-fabric physics claims — fabric-dependent
anisotropy, transverse isotropy of `H`, and the direction-dependent pore-pressure
coupling — are each matched by the evidence actually shipped, and the fabricated
comparisons (reference Biot, isotropic shear modulus, Mandel peaks, figure CSVs)
reproduce to printed precision. Citations are complete and faithful. The
supplement archive is self-contained, internally hash-consistent, byte-identical
to the PDF attachment, and its reproduction instructions run end-to-end and
regenerate the archived verification output exactly. The FE registry covers every
run directory with verified source digests. The manuscript rebuilds without
undefined references. No required change is supported by evidence; the only
observations are optional wording/packaging clarifications.

VERDICT: ACCEPT

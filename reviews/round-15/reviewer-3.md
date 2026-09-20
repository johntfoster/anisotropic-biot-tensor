# Round-15 independent review 3 — prose, notation, significance, claim/artifact consistency

Reviewer charge: notation conventions and their exceptions; scope statements
(implementation verification vs. finite-load demonstration vs. physical
validation); consistency between abstract, introduction/roadmap, results,
conclusions and `site/evidence.json`; citation and cross-reference resolution;
and whether every quantitative claim in the manuscript and in `site/evidence.json`
is backed by a listed artifact with a resolving path and digest.

## 1. Reviewed version and integrity

Frozen snapshot: `/home/jfoster/projects/research/reactive_transport/anisotropic-biot-tensor/.agent-runtime/review-snapshots/round-15`
Working copy: `/tmp/r15rev3` (`cp -r <snapshot> /tmp/r15rev3 && chmod -R u+w /tmp/r15rev3`)

```
$ sha256sum "$SNAP/source-manifest.json"
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617  .../round-15/source-manifest.json

$ cat "$SNAP/SNAPSHOT_ID"
8e0c68f50d7c70131d7e81762db2b7282c53dfb17fb86500e315807d4a350617
```

Manifest digest equals the recorded `SNAPSHOT_ID`. Every path listed in
`source-manifest.json` was then hashed:

```
listed 438 ok 438 mismatch 0 missing 0
```

Integrity result: **PASS** (438/438 listed paths present and byte-identical).

## 2. Audit evidence

Commands were run in `/tmp/r15rev3` (writable copy of the snapshot). No other
review directory was opened; only `reviews/README.md` is shipped, as stated.

### 2.1 Citation resolution

```
$ python3  # extract \cite keys (multiline-aware) and compare to references.bib
citekeys 22
used not in bib: []
bib not cited: []
```

All 22 `\cite*` keys used in `main.tex`, `sections/*.tex`, and
`provenance/ai_use_statement.tex` resolve to entries in `references.bib`; no
bibliography entry is orphaned.

### 2.2 Cross-reference resolution

```
labels 106
unresolved refs: []
```

All `\ref`/`\eqref`/`\cref` targets resolve. (Forty-eight labels are defined
but never `\ref`-ed; that is normal for numbered display equations and is not
a defect.)

Equation numbering was reconstructed in document order to check the numeric
equation references used in `validation/reference-data/README.md`:

```
40 eq:drained-stiffness-restriction
57 eq:reference-biot-compatibility
58 eq:reference-solid-storage-definition
59 eq:reference-solid-storage
60 eq:reference-storage-compatibility
total numbered equations: 88
```

So the validation note's "equations (40), (57), and (58)–(60)" point to the
drained stiffness restriction, the reference Biot relation, and the reference
storage relations — the intended targets.

### 2.3 `site/evidence.json` artifact paths and digests

All 23 declared artifacts were checked against the filesystem, against the
digest recorded in `evidence.json`, and against `source-manifest.json`:

```
fe-mandel-history        exists=True digest_match=True in_manifest=True manifest_match=True
... (23 rows, all True for every artifact) ...
scientific-snapshot      exists=True digest_match=True in_manifest=True manifest_match=True
```

Every artifact path resolves, every declared SHA-256 matches the file, and each
file's digest also matches the snapshot manifest. Category `evidence` id lists
(`analytical`, `implementation`, `convergence`, `finite_deformation`) all point
to artifacts that exist.

### 2.4 Quantitative claim recomputation

- Mandel reference (`site/reports/mandel-reference.json`): `checks` count = 38,
  `passed = true`; `central_overshoot.ratio = 1.0546586069998425`,
  `time = 0.015165352045764979`. `evidence.json` states "38 self-checks (peak
  overshoot 5.4659% at t = 0.01516535)" — **confirmed** (1.0546586 → 5.4659%).
- Fluid coupling (`site/reports/fluid-coupling-verification.json`):
  `count = 110`, `passed = true`, `maximum_scaled_error = 8.086725789002713e-09`.
  `evidence.json` states "110 checks, max scaled error 8.09e-09" — **confirmed**.
- C++/Python constitutive (`site/reports/cpp-python-constitutive.json`):
  `states = 41`, `value_absolute_error = 6.394884621840902e-14`.
  Manuscript/evidence "6.4e-14 over 41 finite states" — **confirmed**.
- Manufactured solution (`site/reports/mms-convergence.json`): spatial
  `naive_orders` ux 2.9917/2.9585, uy 2.9983/2.9600, p 1.9966/2.0008;
  temporal `difference_orders` nx=16 1.0932/0.9783/1.0152, nx=32
  1.3969/1.0183/1.1252, nx=64 1.3959/1.0761/1.2518 (ux/uy/p).
  `evidence.json` values — **confirmed**.
- Finite-deformation summary (`site/reports/finite-deformation-summary.json`):
  anisotropic peak pressure 0.20618–0.21577, peak time 0.002–0.004,
  `force_relative_max = 1.2764e-10`, `discrete_mass_mobilized_relative_max =
  2.4699e-10`; isotropic peak 0.22383, forcing 3.2144e-12; partial peak
  0.20052–0.20163, time 0.002–0.0035, forcing 2.0521e-10, mass 4.6363e-10.
  All `evidence.json` numbers — **confirmed**.
- Small-load error floor: `figures/fe_load_limit.csv` gives
  `pressure_max_normalized = 0.003220919735602341` at load 1e-4, nx=20, dt=1e-3
  (and 3.4479e-3 at 1e-3, 5.7060e-3 at 1e-2). The conclusion's "floors at about
  \(3.2\times10^{-3}\) at \(nx=20, dt=10^{-3}\)" — **confirmed**.
- Reference Biot components (§4.1, "0.7000, 0.7583, 0.7917"): recomputed from
  `eq:drained-stiffness-restriction` and `eq:reference-biot-compatibility` with
  the printed `C_s` matrix, `phi_s0=0.6`, `K=7`:
  `B0 = [0.7, 0.75833333, 0.79166667, 0, 0, 0]` — **confirmed**. The extra
  compliance `(C^d)^{-1} - (phi_s0 C_s)^{-1}` came out as the rank-one spherical
  matrix `0.009259 * ones(3,3)` with zero shear entries — the stated "spherical,
  rank-one contribution" — **confirmed**.
- Isotropic comparison shear modulus (§4.1, "16.8 K_*", "mean of the five
  deviatoric stiffness modes of C_s, divided by two"): eigenvalues of the
  deviatoric projection of `C_s` are `[20, 24, 28, 42.9668, 53.0332]`, mean
  33.6, half 16.8 — **confirmed**. `K_s = 28 K_*` and `K=7 < phi_s0 K_s = 16.8`
  — **confirmed**.
- FE reference parameters (`sections/finite_elements.tex`): `phi_s0=0.9`,
  `Ks=2.5`, `mu_s=5/6`, `K=1`, `Kf=8`, `G=phi_s0*mu_s=0.75`,
  `alpha=1-K/Ks=0.6`, `1/M = 0.2 + 0.1/8 = 17/80 = 0.2125`. All — **confirmed**;
  they also match `mandel-reference.json` (`K=1.0, G=0.75, alpha=0.6,
  M=4.705882..., mobility=1.5, a=1.0, b=0.1`).
- Conformal verification counts (§4.5): `checks_passed = 186`, `checks` dict
  length 186; the five per-state identity groups (`legacy_state0..4`) each hold
  exactly 13 checks → 65; `legacy_identities_rechecked = 67` = 65 + 2 reference
  Biot/rank-one relations. `max_constitutive_identity_error =
  2.4549890331732928e-09` → the manuscript's "2.5e-9" — **confirmed**.
- Tensor suite (§4.5): `materials = 13`, `total_states = 273` —
  **confirmed**.
- Positivity/stability (§4.5, "All plotted states satisfy positive phase
  volumes and the scalar stability condition"): minimum `scalar_stability`
  across plotted CSVs is 28.0 (pressure), 29.12 (shear), 29.13 (rotation),
  28.0 (layer); minimum `solid_fraction` 0.434, minimum `mineral_volume` 0.894
  — **confirmed**.
- Isotropic claims (§4.2): along the isochoric shear path the isotropic
  material has a single distinct `mineral_volume`, a single distinct
  `(B11,B22,B33)`, and `B12 ≡ 0` — **confirmed**.
- Embedded supplement: `pdfdetach -list build/main.pdf` → "1 embedded files /
  1: conformal-2026-09-20-v1.zip". The archive's own `manifest.json` verifies
  internally (`ok 33 mismatch 0 missing 0 of 33`) and lists every payload entry
  (no unlisted payload). `build/main.log` shows a clean build: 22 pages, no
  undefined references/citations, and a single `Underfull \hbox` warning.

### 2.5 Scope-statement consistency

The abstract, introduction roadmap, `sections/finite_elements.tex` ("Scope of
these results"), and conclusions agree, and they agree with `evidence.json`
categories: constitutive/fluid/reference/convergence checks **passed**;
`finite_deformation` **pending**; `physical_validation` **not_performed**. The
rotated-anisotropy and partial-drainage runs are consistently described as
force-controlled demonstrations with a kinematic rigid platen, not quantitative
nonlinear verification and not experimental validation. No scope overclaim was
found.

## 3. Findings

**F1 (minor, required). Mass-flux bar convention is self-contradicted.**
`main.tex` §2 states the convention: "a bar on a mass-flux measure denotes its
referential normalization." In `sections/finite_elements.tex` §5.1 the Darcy
volume flux is `\mathbf q` ("measured per current area"), and "its referential
mass flux is `\mathbf Q_f`" — referential, but unbarred — while the weak form
uses the barred, also-referential boundary scalar `\bar Q_f` ("outward mass
flux", with `\mathbf Q_f\cdot\mathbf N=\bar Q_f`). Two referential mass-flux
symbols are barred inconsistently relative to the manuscript's own stated
convention, and no exception is declared.

**F2 (minor). Shipped README references a tool that is not in the snapshot.**
`README.md` states: "Run `tools/agentctl check --profile manuscript` for the
local manuscript tooling check. The shared workflow submodule is present and
version-pinned." The snapshot contains no `tools/agentctl` and no
`.gitmodules`; `tools/` holds only the `*.py` scripts. The command as written
cannot be run from the shipped artifact, and the "version-pinned submodule"
claim is not verifiable from the snapshot (no git metadata shipped).

**F3 (minor). Check-suite description is broader than the artifact.**
`sections/experiments.tex` §4.5 calls the 65 per-state identities "the 65
rotation, virtual-work, and volume-response checks (five states times
thirteen per-state identities)". The count is exactly right (5 × 13, verified
in `conformal-verification.json`), but the thirteen per-state identities also
include true-metric, logarithmic-strain, rotated-mineral-stress, scalar
pressure equilibrium, full phase-balance-from-energy, and pressure-tangent
checks, which are not "rotation, virtual-work, or volume-response".

## 4. Required corrections

1. **Resolve the mass-flux bar inconsistency (F1).** Why required: the
   manuscript publishes an explicit notation convention and then violates it in
   the same document without an exception, so a reader cannot decode
   `\mathbf Q_f` vs `\bar Q_f` from the stated rule. Either (a) add one sentence
   to the §2 convention paragraph recording the exception (referential
   mass-flux *vector* written `\mathbf Q_f`, its boundary normal value written
   `\bar Q_f`), or (b) rename the vector to a barred symbol and give the
   boundary scalar a distinct name to avoid collision. No equation changes are
   implied.

2. **Correct or qualify the `tools/agentctl` instruction (F2).** Why required:
   it is a reproducibility instruction in the shipped artifact that cannot be
   executed, and the accompanying submodule claim cannot be checked; either add
   the tool/verification path or state that it is not part of this artifact.

## 5. Optional suggestions

- S1: In `sections/experiments.tex` §4.5, describe the 65 checks by their
  actual content (thirteen per-state identities across five states) rather than
  the narrower "rotation, virtual-work, and volume-response" label (F3).
- S2: The abstract ("verified against a manufactured solution of the constant
  reference tangent and exercised on ... demonstrations") omits the
  constant-coefficient consolidation-reference verification that the
  introduction, finite-element section, and conclusions all report. Adding the
  consolidation reference to the abstract sentence would make the abstract
  scope exactly match the body.
- S3: In `site/evidence.json`, the `analytical` category carries
  `status: "passed"` while its summary also reports a finite-load FE
  demonstration that floors rather than converges. Splitting the analytical
  self-check status from the finite-load demonstration status would remove any
  chance of reading the demonstration as a passed analytical gate.
- S4: `site/evidence.json`'s finite-deformation summary says "at mineral
  orientations 0, 30, 45, 90 (coarse and fine meshes) degrees"; only the 30°
  orientation has coarse/medium/fine meshes, so the parenthetical could be
  attached to 30° alone for clarity.

## 6. Review limitations

- This review verifies prose, notation, cross-references, citation resolution,
  and claim-versus-artifact consistency. It does not independently re-derive
  the mathematics or re-run the MOOSE solves; quantitative claims were
  recomputed only where the shipped CSV/JSON artifacts contain the underlying
  data, and were otherwise traced to a resolving artifact and digest.
- The archive `build/conformal-2026-09-20-v1.zip` is explicitly a frozen v1
  supplement; two of its payloads (`examples/verify_conformal.py`,
  `build/conformal/verification.json`) differ byte-wise from the same-named
  repository files. The archived `verification.json` nevertheless reports the
  same 186 checks and the same maximum error as the repository
  `site/reports/conformal-verification.json`, so no numeric inconsistency was
  found; the manuscript and archive README both state the archive is
  independent of any repository commit.
- No prior-round report, verdict, or `reviews/round-*` directory was read; only
  `reviews/README.md` was available, per snapshot policy.
- Git history and submodule state are not shipped, so F2's submodule claim is
  assessed only as "not verifiable from this snapshot".

VERDICT: MINOR REVISION

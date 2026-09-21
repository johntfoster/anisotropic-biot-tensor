# Round 23 — revision response

Frozen round reviewed: `.agent-runtime/review-snapshots/round-23`
(`SNAPSHOT_ID 53af8afca869198eb1560733c6b9f0377accc0570d36b9dcbeddecc36142ddc5`, 556 files).

Revision tree frozen: `.agent-runtime/review-snapshots/round-24`
(`SNAPSHOT_ID 1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423`, 591 files).

All three reviewers returned MINOR REVISION. Every REQUIRED item below is closed on the
round-24 tree, and the contour-field deliverable requested by the author is added.

## R1 (Reviewer 1, required) — storage coefficient

Accepted and fixed. The manuscript's own reference total storage is
`(1 - φ_s0)/K_f + S_s` with the solid storage
`S_s = (φ_s0/K_s)(1 - K/(φ_s0 K_s))` (sections/limits.tex eq. `reference-solid-storage`;
sections/finite_elements.tex eq. `fe-reference-total-storage`), where `K` is the drained
bulk modulus. The conformal law uses exactly this through `alpha = 1 - K/(φ K_s)`
(ConformalLaw.h), and it is what reproduces `17/80`.

The fabric law instead wrote `alpha_eff = (b_par + 2 b_per)/3 = 1 - K/K_s` (the mean Biot
coefficient) and `storage = (1 - φ)/K_f + φ·alpha_eff/K_s`, which is larger than the correct
value by `(1 - φ)K/K_s²`. Because `verify_fabric.py` replicated that expression and `mass`
was absent from the compared fields, the shipped verification could not see the error, and
the coupled `fluid_mass` property carried a storage 1.4–7.5 % too large.

Fix applied, in three places that now agree on one definition:

1. `moose_app/include/utils/FabricLaw.h` — the drained bulk modulus `Kd` is read from the
   drained stiffness `C^d` (`Kd = Σ_{i,j≤3} C^d_ij / 9`) and the storage becomes
   `(1 - φ)/K_f + (φ/K_s)(1 - Kd/(φ K_s))`. The now-unused `alpha_eff` member is removed.
2. `examples/verify_fabric.py` — the same expression mirrors the code
   (`Kd = Cd[:3,:3].sum()/9`), and `"mass"` is added to `FIELDS`.
3. `moose_app/inputs/fabric_probe.i` — a `mass` postprocessor
   (`ADElementIntegralMaterialProperty`, `mat_prop = fluid_mass`) records the material-point
   fluid mass so the independent check can compare it.

Verification after the fix: `examples/verify_fabric.py` reproduces every compared field
including `mass` (conformal-limit mass `0.10725` = `0.1 + 0.003 + 0.2125·0.02`, i.e. storage
`17/80`), worst probe-field difference `4.885e-15`, conformal reduction still `1.9e-14`. All
15 fabric decks plus `conformal_probe_ref` were re-run with the rebuilt app (recorded
`application_library_sha256` changed; `exit 0` for all). The coupled pressures moved slightly:
peak centre pressure is now `3.62e-5` (uncoupled), `4.36e-5` (0°), `4.99e-5` (45°), `5.52e-5`
(90°), and sections/finite_elements.tex:312-316 was updated to these values.

## Reviewer 2

Required:
- **Duplicate limitation entry** (site/evidence.json) — de-duplicated to one pore-fabric
  limitation (the superset wording retained; 6 limitations now).
- **Duplicate note entry** (fe-evidence/manifest.json) — de-duplicated to one `runs/fabric_*`
  note (the superset wording retained; 5 notes now).
- **Machine-specific absolute path** — `runs_dir` in `site/reports/mms-convergence.json` and
  `fe-evidence/mms-convergence.json` is now the repository-relative `fe-evidence/runs`.

Optional:
- **O2** (full documented suite) — APPLIED. Re-ran `weighted_stress.py`,
  `verify_reconstruction.py`, `verify_tensor.py`, `verify_conformal.py`,
  `conformal_experiments.py`, and `verify_fabric.py`; all exit 0.
- **O3** (manifest self-declaration) — NOTED, no change. A self-hashing manifest that does
  not declare itself (and the archive manifest that does not declare its own README) is the
  conventional, self-consistent form; the outer digests are verified externally.
- **O4** (path-traversal literals in site/test_builder.py) — DECLINED, no change. Those
  strings are inputs to the path-sanitization rejection test (`test_traversal_and_hidden_paths_rejected`),
  not shipped data.
- **O5** (source-revision provenance) — APPLIED. `site/evidence.json` `provenance.source_revision`
  is now the current HEAD `ab46ebe44b7f7a08c06f31b1f2c8a77deb7e464c`, and the note states the
  base commit is the current working revision.

## Reviewer 3

Required:
- **Undefined p1, p2** — FIXED. sections/pore_fabric.tex now introduces
  `\mathbf p_1, \mathbf p_2` as orthonormal vectors spanning the plane normal to
  `\mathbf m` before the `e3`, `e6` definitions.
- **Overloaded e-family / Mandel-index collision** — FIXED. The retained directions are now
  written with symbols `e1 = I/√3`, `e2 = √(3/2)(m⊗m − I/3)`, and a one-line note states that
  `e1,…,e6` label a fabric-adapted orthonormal basis of symmetric tensors, not the Mandel
  component indices of eq. `example-mineral-stiffness`.

Optional prose/notation notes (1–7) were considered; none changes a quantitative result. The
`G`/`\mathbf G` letter reuse (note 1) is already disambiguated by bold-vs-italic and is left
unchanged to avoid introducing a new symbol late in the cycle.

## Contour-field deliverable (author request)

Four refined coupled decks (`moose_app/inputs/fabric_contour.i`) on the same `1 × 0.1`
quarter-Mandel domain, boundary conditions, material and fabric parameters, and time
integration as `fabric_mandel.i`, but on a `nx=40, ny=8` (QUAD9) mesh and with `dt = 0.0003`
(`end_time = 0.003`) so the Exodus output carries eleven evenly spaced field snapshots.
Variants: isotropic (no coupling) and fabric axis 0°, 45°, 90° (coupling 0.4, isotropic
unrotated mineral). All four run `exit 0` and are recorded under
`fe-evidence/runs/fabric_contour_{iso,a0,a45,a90}/` with `input.i`, `provenance.json`,
`run.log`, `solution.csv`, `solution.e` (Exodus kept), and `analysis.json`.

`examples/plot_fabric_contours.py` reads only the recorded Exodus fields (netCDF4) and emits:

- `figures/fe_fabric_contours.{pdf,png}` — rows `p` and `|u|`, columns iso/0°/45°/90° at the
  common final recorded time, filled contours, colourbars, equal aspect, domain outline,
  fabric-axis indicator. `figures/fe_fabric_contours.csv` records the plotted extrema and the
  pressure-maximum location.
- `figures/fe_fabric_diffusion.{pdf,png}` — pressure snapshots at six recorded times for the
  isotropic and 45° cases on a shared colour scale, showing the Mandel-type drainage front.
  `figures/fe_fabric_diffusion.csv` records the per-case/per-time extrema and pressure-maximum
  location.

The pressure field is a genuine diffusion pattern, not uniform or degenerate: it is largest
on the `X1 = 0` symmetry line and falls to zero at the drained edge `X1 = 1`, with a drainage
boundary layer that advances into the strip over time (the tiny negative round-off values at
the drained nodes are floating-point zero). Numbers quoted in the manuscript come only from
the CSV sidecars: refined peak pressures `3.61e-5 / 4.35e-5 / 4.97e-5 / 5.50e-5` and
displacement-magnitude peaks `5.18e-5 / 5.14e-5 / 2.38e-5 / 5.26e-5`. The two figures are
added to `sec:fe-fabric` (fig. `fe-fabric-contours`, `fe-fabric-diffusion`) with a paragraph
that states these are demonstrations on synthetic parameters and makes no mesh-convergence
claim. The reduced axisymmetric law (span(e1,e2), `NDIR = 2`) is retained throughout; the
superseded five-modulus form is not reintroduced.

## Downstream regeneration

- Manuscript: `latexmk -lualatex … main.tex` exit 0, **33 pages**, 0 undefined
  references/citations, 0 overfull boxes, 0 multiply-defined.
- `fe-evidence/manifest.json` (317 files / 57 cases), `site/evidence.json` (41 artifacts),
  `site/scientific-snapshot.json` (46 files) re-digested; no stale digest.
- Companion site rebuilt; link check passed (`.agent-runtime/site`).
- Supplement archive `build/anisotropic-biot-2026-09-20-v2.zip` rebuilt (69 files,
  SHA-256 `46ef65aad77df01de64054108c5a0b0ec4a91718a73123f620f1793f6cba2c54`) including the
  contour deck, contour script, runner, and contour run histories + Exodus fields.
- PDF embedded attachment is byte-identical to the on-disk archive (same SHA-256 and filename).

## Round-24 freeze

`tools/build_review_snapshot.py round-24` →
SNAPSHOT_ID `1dea9e121e8d763dc0b4008d9b430026a17d600fbdd67d5f085a7d6f2617b423`, 591 files.

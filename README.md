# An anisotropic Biot tensor from mineral stress and distention work

The manuscript derives the elastic energy from the current-volume-weighted
mineral and fluid stresses. It follows the companion's reversible work and
volumetric-energy construction, with a dilation-times-rotation distention
gradient and an objective anisotropic mineral law. A volume-only distention
energy makes the response independent of the internal rotation; mineral
stresses are rotated into the mixture frame before phase averaging. Reproducing the drained logarithmic Hooke law
restricts the compliances: the drained compliance minus the mineral
compliance divided by the reference solid fraction must produce spherical
strain alone. The Biot tensor follows from the resulting
mineral-volume equation.

The canonical manuscript is `main.tex`; its only bibliography is
`references.bib`. `build/main.pdf` is the sole preview. The paper builds
without a companion repository.

## Build

Use a complete TeX Live installation with LuaLaTeX, unicode-math, Latin
Modern Math, latexmk, and BibTeX. Upright bold Greek and Latin tensor symbols
use `\mathbf{}` for second-order tensors and vectors; fourth-order
stiffness and compliance tensors use `\mathbb{}`. Build from the repository root:

```sh
python3 -m pip install -r examples/requirements.txt
python3 examples/weighted_stress.py
python3 examples/verify_reconstruction.py
python3 examples/verify_tensor.py
python3 examples/verify_conformal.py
python3 examples/conformal_experiments.py
python3 examples/verify_fabric.py
python3 examples/plot_fe_verification.py
python3 examples/fabric_insight.py
python3 examples/plot_fabric_comparison.py
python3 tools/verify_scalar_probe.py --analyze-only
python3 tools/package_numerical_supplement.py
latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

On an Ubuntu/Debian installation missing LuaLaTeX font support,
`python3 tools/provision_luatex.py` downloads and unpacks the distribution's
`texlive-luatex` package into ignored runtime storage. It does not install
system packages. Use the environment settings reported by the provisioning script for a
local fallback. A complete system installation needs no fallback.

Generate the tables and figures before the LaTeX build with the commands
above. The conformal experiments use NumPy, SciPy, and Matplotlib. Build
products, CSV data, and verification JSON stay under `build/`.
The packaging command creates `build/anisotropic-biot-2026-09-22-v3.zip`, embedded
as an attachment in the article PDF. It contains standalone numerical sources,
data, figures, reproduction instructions, and a file-hash manifest. Extract it
with an attachment-capable PDF viewer or `pdfdetach -saveall build/main.pdf`.
Run all verification commands below before packaging to include their reports.

## Independent verification

After installing `examples/requirements.txt`, run:

```sh
python examples/verify_reconstruction.py
python examples/verify_tensor.py
python examples/verify_conformal.py
python3 tools/check_dependency_profile.py manuscript
```

The first script checks work equivalence, full drained compatibility,
reference stress/storage, scalar recovery, and the finite unjacketed path.
The second compares independently computed intrinsic mineral phase stresses
with numerical derivatives of the mixture energy, then verifies the
pressure and mineral-volume derivatives at general finite tensor states.
It includes different stress and strain directions, repeated stretches,
and rigid rotations. The build does not automatically run these tests.
Legacy spherical-gauge checks write to `build/weighted-stress/`. The
conformal verification and experiments write data, figure PDFs, and exact
environment versions to `build/conformal/`. These are homogeneous
constitutive experiments, not finite-element simulations or material
calibration. See `examples/conformal_model.py` for the equation mapping.

`examples/finite_pressure.py` belongs to the archived earlier formulation;
it does not generate current manuscript results. Earlier reviews retain
their original hashes and are not acceptance evidence for the current paper.
See `reviews/README.md` for the active review cycle.

The pore-fabric distention law is re-checked independently with
`python3 examples/verify_fabric.py`, which compares a NumPy re-implementation
of the section equations with the recorded runs under `fe-evidence/runs`
(refresh them with `python3 tools/rerun_fabric_decks.py` followed by
`python3 tools/rerun_fabric_decks.py --analysis-only`). Its figures are drawn
by `python3 examples/plot_fabric_results.py --runs fe-evidence/runs`. The
refined (\(40\times4\)) contour runs are recorded under
`fe-evidence/runs/fabric_contour_*`. Refresh them, and the figures that hash
them, in this order:

```
python3 tools/rerun_fabric_contours.py    # decks, evidence, figures, manifest
python3 tools/check_figure_manifests.py   # re-hash every declared digest
```

`tools/rerun_fabric_contours.py` runs the four decks, rewrites their recorded
Exodus fields, then rebuilds `figures/fe_fabric_contours.csv`,
`figures/fe_fabric_diffusion.csv` and
`figures/fe_fabric_contours-plot-manifest.json` from those fields, and finally
re-verifies the manifest. The order is the point: the plot manifest hashes the
Exodus files, so a manifest written before the decks would ship a stale
`input_sha256`. The manifest is generated by
`examples/plot_fabric_contours.py`, which hashes the artifacts it just read
rather than copying a stored value, and `tools/check_figure_manifests.py`
recomputes every declared input and output digest from disk (run
`make figures` for both steps). The decks write with a relative output base, so
the Exodus `title` attribute is the stable string `solution.e` rather than a
temporary host path. The recorded field arrays are bit-identical across
regenerations; the framework header echoed into the Exodus information records
carries the run wall clock, so the raw file digest changes with the run time
even though the fields do not, and the manifest is regenerated with them.

The finite-element verification displays are assembled from the recorded
artifacts with `python3 examples/plot_fe_verification.py`, which writes the
manufactured-solution, temporal-order, finite-load-floor, and
reference-comparison figures used in `sections/finite_elements.tex`.

## Instructions and provenance

Read `AGENTS.md` and `author_style_profile.md` first. Adapted manuscript
skills are under `agent_local/skills/biot-*/`. Their pinned source and the
scope of the transfer are recorded in
`provenance/companion-guidance-transfer.md`.
The manuscript tooling check is `tools/agentctl check --profile manuscript`.
`tools/agentctl` is a link into a separate shared-agent-workflows checkout
(`.agent/shared`), so the check belongs to the working checkout and is not part
of this artifact; no shipped result, figure, or evidence file depends on it.
The source comparison and current derivation record are in
`references/notes/weighted-stress-reconsideration.md`.

## Experiments that distinguish tensor coupling

The main-text fabric figures use pressure-induced shear reactions, a coupled
scalar-versus-tensor consolidation study, and finite pure shear with equilibrated
pore volume and shape. Generate the material results and plot the recorded
coupled histories with:

```sh
python3 examples/fabric_insight.py
python3 examples/plot_fabric_comparison.py
```

The finite material calculation uses an isotropic mineral and commuting
mineral stress and distention. It checks all spatial stress components and
the pressure tangent on this restricted family; it does not implement a
general noncoaxial finite fabric law. The coupled comparison uses the reference
linear law. Its scalar approximation preserves the mean pressure reaction,
drained stiffness, storage and isotropic mobility, with reciprocal coupling
in stress and mass. It loads an initially resting strip and follows drainage.

To regenerate the coupled histories, build the application in the verified
MOOSE environment and run:

```sh
.agent/shared/skills/setup-moose-conda/scripts/moose_conda_env.sh run -- make -C moose_app -j2
.agent/shared/skills/setup-moose-conda/scripts/moose_conda_env.sh run -- python tools/run_fabric_comparison.py
python3 examples/plot_fabric_comparison.py
```

Recorded histories and run provenance are under `fe-evidence/insight/`.
Material results, comparison diagnostics and paper-ready figures are generated
under `build/insight/`. Run both generators before packaging the supplement
and building the manuscript. All parameters are synthetic.

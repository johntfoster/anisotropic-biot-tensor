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
The packaging command creates `build/conformal-2026-09-20-v1.zip`, embedded
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

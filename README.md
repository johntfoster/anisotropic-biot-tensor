# Mineral-volume compatibility and anisotropic pressure coupling at finite deformation

This self-contained theoretical extension develops the one-solid/one-fluid
anisotropic generalization of the finite-deformation Biot construction in
Foster and Xu (2025).

Build from this repository's root:

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=build main.tex
```

The build requires Python 3 (standard library), LuaLaTeX, BibTeX, latexmk,
and PGFPlots. The tracked `.latexmkrc` regenerates numerical tables and plot
data under `build/examples/`; no pre-existing generated figures are needed.

The central finite-deformation definition is `eq:finite-biot-tensor`; its
experimental interpretation is `eq:cauchy-pressure-tangent`. The quadratic
reduction is `eq:linear-biot-tensor`. The paper distinguishes the drained
stiffness `C^d`, constrained stiffness `C^c`, daughter energy coefficient `C`,
mineral stiffness `H`, and skeleton--mineral coupling `D`. The unjacketed
compatibility condition `eq:compatible-mineral-tangent` distinguishes the
effective mineral-volume tangent from the isolated mineral modulus.

The synthetic examples in `sections/experiments.tex` are reproducible with:

```sh
python3 examples/finite_pressure.py
```

Optional independent tensor, energy, and finite-difference checks require
NumPy and SciPy. Use a repository-local environment:

```sh
python3 -m venv .agent-runtime/venvs/numerics
.agent-runtime/venvs/numerics/bin/pip install -r examples/requirements.txt
.agent-runtime/venvs/numerics/bin/python examples/verify_tensor.py
```

The checks include noncoaxial deformations and sampled acoustic tensors;
they do not establish global ellipticity. Results are synthetic constitutive
predictions, not experimental validation. Full-text citation evidence is
recorded in `references/notes/novelty-evidence.md`. Simulated peer reviews and
responses are recorded under `reviews/` and are not journal editorial decisions.

# An anisotropic Biot tensor from finite-deformation mixture kinematics

This self-contained theoretical extension develops the one-solid/one-fluid
anisotropic generalization of the finite-deformation Biot construction in
Foster and Xu (2025).

Build from this repository's root:

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=build main.tex
```

The central finite-deformation definition is equation
`\eqref{eq:finite-biot-tensor}`.  The generalized-Hooke result is equation
`\eqref{eq:linear-biot-tensor}`.  The paper explicitly distinguishes the
drained skeleton stiffness `\mathbb C^d`, constrained skeleton stiffness
`\mathbb C`, mineral stiffness `\mathbb H`, and independently calibrated
skeleton--mineral coupling `\mathbb D`.

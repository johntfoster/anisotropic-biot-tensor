# Vision

This repository develops a self-contained theoretical paper for one elastic
solid and one fluid. The derivation begins with current-volume-weighted
phase stresses and reversible work, follows the companion's equivalent
volumetric energy construction, and extends it to an anisotropic mineral
with a logarithmic generalized Hooke law.

The current model permits a scalar dilation times a proper rotation, with
an objective anisotropic mineral energy and volume-only distention energy.
The internal rotation changes the mineral stress frame but cancels from
physical response when that stress is rotated into the mixture frame. It preserves the full
spatial phase stress balance and derives the restriction required to
reproduce a complete drained logarithmic Hooke law. The additional drained
compliance must produce spherical strain alone. Skeleton and mineral
stiffness tensors are therefore not arbitrary independent inputs.
The mineral equation determines the finite-deformation Biot tensor and
recovers the isotropic scalar law, reference stress/storage coefficients,
and a finite homogeneous unjacketed path.

The paper uses `\mathbb{}` for fourth-order tensors, upright bold
`\mathbf{}` for second-order tensors and vectors, and John Foster's
explanatory prose. New notation is introduced only when necessary.
Assumptions, derived restrictions, and experimental validation are kept
explicit. Anisotropy due to pore shape and nonspherical distention requires
additional mechanics and is not supplied by a logarithmic spring analogy.

The canonical root is `main.tex` and the sole bibliography is
`references.bib`. Source evidence, reproducible checks, and independent
simulated reviews accompany the manuscript. Generated outputs remain in
ignored runtime/build directories. The paper has no external build dependency.

# Independent Mandel reference

`../mandel_reference.py` evaluates the classical, constant-coefficient,
plane-strain consolidation solution. It is an analytical reference, not a
finite-element solver or evidence that a coupled finite-element test passed.
The implementation is original Python under Apache-2.0; no MOOSE source was
copied. NumPy and SciPy are required.

Run from the repository root:

```sh
python3 validation/mandel_reference.py --self-check
```

Generated CSV files, hashes, parameters, and the self-check report go to
`.agent-runtime/moose-fe-goal-2026-09-20/reference/`. Use `--output-dir` to
select another ignored output directory. `--load` sets the mean compressive
traction; the default unit load is a normalization, not a finite-strain load
recommendation. The code can also be imported directly:

```python
from validation.mandel_reference import MandelParameters, MandelSolution
reference = MandelSolution(MandelParameters())
fields = reference.evaluate(x=0.0, y=0.1, t=0.03, load=1e-3)
```

Coordinates and time broadcast as NumPy arrays. Returned fields are pressure,
both in-plane displacements, normal strains and stresses, fluid content, and
horizontal Darcy flux. `modes` is the eigenfunction count; `tail_bound` bounds
the dimensionless Gaussian tail before field prefactors. The default tail
tolerance is `1e-13`. A requested positive time requiring more than 20,000
modes raises an error rather than silently truncating. At exactly zero, the
code uses the exact undrained bulk limit. The self-check increases the mode
cap explicitly when testing the approach to that limit.

## Geometry, force, and units

The full rectangle is `[-a,a] × [-b,b]`, with plane strain in the third
direction. Impermeable, frictionless rigid plates impose uniform normal
displacement with fixed total force. The vertical faces are traction-free
and drained. `load=q` denotes mean compressive traction, so the compressive
force magnitude on the full top is `2*a*q` per unit out-of-plane thickness.
The quarter-domain top resultant is `a*q`. Positive displacement follows the
coordinate axes, and top displacement is negative under compression.

At `t=0`, values are the uniform undrained post-load bulk state, including
its extrapolated boundary trace. At any positive time, pressure on `x=±a`
is zero. The initial corner discontinuity is not assigned a spurious unique
classical value. The reported `qx=0` at zero time belongs to the sealed
undrained trace, not the singular initial drained-edge flux.

The code uses dimensional time and coordinates in any one consistent unit
system. Dimensionless time is `c*t/a²`, with

```
c = mobility / (1/M + alpha²/(K + 4G/3)).
```

Pressure divided by `q`, horizontal displacement divided by `q*a/G`, and
vertical displacement divided by `q*b/G` remove load and dimension factors.
Here `q` is the load, not the returned Darcy flux `qx`.

## Connection to the paper

The isotropic reference limit uses the manuscript's equations (40), (57),
and (58)–(60), with the additional fluid EOS and Darcy closure stated in the
FE formulation. The compatible inputs are

```
phi_s0=0.9, Ks=2.5, mu_s=5/6, K=1, Kf=8, mobility=1.5,
G=phi_s0*mu_s=0.75, alpha=1-K/Ks=0.6,
S_s=phi_s0/Ks*(1-K/(phi_s0*Ks))=0.2,
1/M=S_s+(1-phi_s0)/Kf=17/80,
a=1, b=0.1.
```

This gives `Ku=229/85`, `c=3.8216560509554145`, `nu=0.2`,
`nu_u=0.3726273726273726`, and `p(0+)/q=0.4795204795204795`.
The full nonlinear exponential density and mineral-volume response do not
obey the constant-coefficient series at finite load. Convergence to this
reference must be shown as load tends to zero.

## Numerical construction and independent checks

The positive roots satisfy `tan(z)=(1-nu)/(nu_u-nu)*z`. The solver brackets
one root in each interval `(n*pi,(n+1/2)*pi)`, excluding the zero root,
and solves `sin(z)/z-ratio*cos(z)=0`. This avoids evaluating tangent close
to a pole. A Gaussian integral bounds omitted modal factors. Displacement,
strain, pressure gradient, and flux use analytic series derivatives.

Self-checks cover root residuals, exact initial and drained limits, the
drainage boundary, zero horizontal stress throughout the body, uniform
platen displacement, integrated platen force, series tolerance refinement,
and integrated fluid-content rate plus edge discharge. The center pressure
has a resolved maximum about 5.466% above its initial value at
`t=0.01516535205` for these parameters. These checks test the reference
itself; they do not count toward coupled MOOSE verification.

## Sources inspected

- Cheng and Detournay, *A direct boundary element method for plane strain
  poroelasticity* (1988), [DOI](https://doi.org/10.1002/nag.1610120508).
  The bibliographic record identifies the classical reference; its full text
  was not retrieved in this task.
- *Multiphysics modelling in PyLith: poroelasticity* (2023),
  [Appendix D, equations D9–D14](https://academic.oup.com/gji/article/235/3/2442/7283140).
  The inspected full text gives the initial state and complete displacement
  and pressure series, including interior horizontal displacement.
- [Official MOOSE poroelasticity tests](https://mooseframework.inl.gov/modules/porous_flow/tests/poro_elasticity/poro_elasticity_tests.html).
  The installed `mandel.py` was inspected as a separate reference for its
  parameter conventions. Its fixed twelve-root series and analytical platen
  prescription were not reused as a force-controlled numerical solution.

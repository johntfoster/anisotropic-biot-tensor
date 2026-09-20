# Independent anisotropic manufactured solution

`validation/mms_reference.py` generates exact fields and source functions for
the constant reference tangent of the manuscript's model. It imports no
application material, residual, or automatic-differentiation implementation.
The mineral stiffness is the manuscript's equation (65), with material axes
actively rotated by +30 degrees about the third axis. Plane strain retains
the three-dimensional stiffness and out-of-plane stress.

## Reproduce and use

Run from the repository root:

```sh
python3 validation/mms_reference.py
```

The command requires NumPy and SymPy. Default output directory:
`.agent-runtime/moose-fe-goal-2026-09-20/reference/`. It writes:

- `mms-functions.i`: a complete MOOSE `[Functions]` block with ParsedFunctions
  `exact_ux`, `exact_uy`, `exact_p`, `body_x`, `body_y`, and `mass_source`.
- `mms-expressions.json`: the same decimal expressions for a deck generator.
- `mms-fixed-points.json`: exact-field/source values at three specified points.
- `mms-report.json`: independent tensors, parameters, source/data hashes,
  versions, and numerical-difference verification.

Use the exact fields in FunctionDirichletBC on all four edges, and zero initial
displacement and pressure. The source signs are for kernels whose forcing
residual is `-test*source`; therefore the displacement BodyForce functions
are `body_x` and `body_y`, and the pressure BodyForce is `mass_source`.
The implementation agent confirmed these conventions before generation.

## Reference material and measures

The inputs are reference solid fraction 0.6, drained spherical modulus 7,
fluid bulk modulus 8, reference fluid density 1, and mobility 1.5. The
orthonormal Mandel stiffness uses ordering 11, 22, 33, 23, 13, 12 and
sqrt(2)-weighted shear strains. A proper active rotation acts on each of
the four Cartesian stiffness indices; the sign is not an internal-frame gauge.

The independent reference derives drained stiffness by **inverting the
compliance addition**, equation (43), rather than duplicating the application
material's rank-one stiffness calculation. Equation (57) gives `B0` and
equation (60) gives solid storage. Their source labels are
`eq:drained-compliance-restriction`, `eq:reference-biot-compatibility`, and
`eq:reference-storage-compatibility`.

The derived values are

```
B0 = [[0.7145833333333333, -0.02525907427704613, 0],
      [-0.02525907427704613, 0.74375, 0],
      [0, 0, 0.7916666666666666]],
S_s = 0.0125,
S = S_s + (1-phi_s0)/Kf = 0.0625.
```

All fields use the same reference coordinates and consistent nondimensional
stress, length, time, and density units. The linearized constitutive laws are

```
sigma = Cd:epsilon - B0*p,
m = rho0*((1-phi_s0) + B0:epsilon + S*p),
Q = -rho0*mobility*grad(p).
```

Thus `mass_source` is reference **mass** per reference volume per time.
Reference density happens to equal one here; it is retained symbolically so
the normalization is explicit. The constant reference fluid mass contributes
no time derivative. These are reference-tangent laws, not the finite-strain
exponential EOS or Piola flux transformation.

## Fields and forcing

For `(x,y)` in the unit square, with `U=P=0.01`, prescribe

```
u_x = U*sin(pi*x)*sin(pi*y)*sin(t),
u_y = U*cos(pi*x)*sin(pi*y)*sin(t),
p   = P*cos(pi*x)*cos(pi*y)*sin(t).
```

The script forms the exact strain, constant-tangent stress, mass, and flux
with symbolic arithmetic, then evaluates the independent strong forms

```
b_i = -d_j sigma_ij,
s = d_t m + d_j Q_j.
```

This is equivalent to the analytic contraction described in the verification
contract. Both mixed displacement derivatives and the off-diagonal pressure
coupling are exercised. The chosen pressure has nonzero curvature in both
directions, so flow has a nonzero divergence. Body force vanishes initially;
the mass source generally does not because the fields have nonzero initial
rates. This is consistent with zero initial fields.

## L2 errors and convergence

At a time `t`, the exact L2 norm of each scalar field over the unit square is
`abs(sin(t))/200`; the displacement-vector norm is
`sqrt(2)*abs(sin(t))/200`. Compare squared FE errors integrated over area,
not unweighted nodal differences. Component relative errors divide by the
scalar norm at a nonzero comparison time. Recommended comparison time is
`t=0.2`; do not normalize by the zero initial norm.

For smooth fields, Q2 displacement and Q1 pressure should approach L2 orders
three and two as space is refined with temporal error suppressed. Backward
Euler should approach first order under independent time refinement. The
reference values and forcing verification do not count as these coupled FE
convergence results.

## Reference verification

The script independently differences stress and mass/flux evaluations at
three interior points using four step sizes. Both body-force and fluid-source
errors decrease quadratically before roundoff. At the final `h=1e-4`, the
largest body error is about `3.3e-8` and mass error about `1.5e-9`, below the
fixed `1e-7` thresholds. Decimal ParsedFunction expressions agree with the
exact symbolic values within `3.4e-16`. Exact initial fields are zero.
The smallest drained stiffness eigenvalue is 12, and total storage is positive.
Generated files are hashed in the report. No MOOSE solve is performed by this
script; passing it establishes only the independently generated reference.

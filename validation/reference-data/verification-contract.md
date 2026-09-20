# Coupled FE verification contract

This contract separates checks of the material, reference series, coupled
discretization, and physical model. A successful site build or a prescribed
analytical displacement is not evidence for a force-controlled coupled solve.
Numerical tolerances below are the planned criteria, fixed before reviewing
the coupled results; failures require diagnosis rather than weakened gates.

## 1. Constitutive and coupling measures

Keep three-dimensional constitutive tensors in a two-dimensional plane-strain
mesh, with `F33=1`. Compute total first Piola stress from the full phase stress,
not drained stress minus pressure times the instantaneous Biot tensor. Check
the material-point oracle and independent differences for the mineral root,
phase volumes, Cauchy and Piola stresses, pressure derivative, stored energy,
and fluid mass. The benchmark reference tangent must use the paper's derived
drained tensor, not an independently assigned shear stiffness.

Verify the assembled coupled Jacobian using directional differences of the
residual with respect to both displacements and pressure. Record the step
refinement study; a target relative error of `1e-6` applies away from singular
branches. Material-only checks cannot replace this assembled check.

## 2. Linear isotropic Mandel gate

Use the complete parameter set and force convention in `README.md`.
The top platen has one unknown normal displacement and a global resultant
constraint. Pointwise uniform traction alone does not enforce rigid loading.
An analytically prescribed platen motion can test the constitutive/flow
subsystem but must remain separately labeled.

Initialize the consistent undrained post-load displacement and pressure.
The exact initial boundary discontinuity is excluded from pointwise curve
error. If using a load ramp instead, either convolve the step reference with
that ramp or demonstrate ramp-duration convergence. Starting unstressed at
the first finite backward-Euler step is a load-increment method; report and
refine the first time step instead of claiming exact post-load initialization.

Use at least three spatial and three temporal resolutions, varying them
independently. Compare pressure profiles, center overshoot and its timing,
top displacement, lateral displacement, total platen reaction, and discharge.
Normalize pressure error by the initial interior pressure, and displacement
error by the magnitude of final drained displacement; do not divide by a
time-dependent quantity approaching zero. Target resolved curve error is
`0.5%`. Report both maximum and space/time-integrated errors. An observed
overshoot alone is insufficient. The reference truncation error is much
smaller than this tolerance and is recorded independently.

The top resultant must equal the prescribed force to the nonlinear algebraic
tolerance. Record the actual solver tolerance, residual, and force error;
numerical agreement of a single probe does not establish force balance.

## 3. Nonlinear small-load limit

Run the actual finite-deformation material, storage, and transformed flux
with load scales `1e-2, 1e-3, 1e-4` relative to drained `K`, or a documented
equivalent sequence. Compare load-normalized fields with the same analytical
reference. Separate the load-dependent discrepancy from mesh/time error by
resolving the latter first. Constant-coefficient analytical agreement at
finite load is not expected and must not be imposed by replacing the
nonlinear mass law with the reference tangent's storage.

## 4. Conservation

Integrate actual reference fluid mass over the reference domain. With the
outward-positive reference mass flux, check

```
m_total(t)-m_total(t0) + integral(t0,t) Q_out dt - integral(t0,t) S_mass dt = 0.
```

For backward Euler, also check the discrete time-step identity using the
end-step flux and source consistently. A trapezoidal postprocessing integral
is a different approximation and must not be substituted silently.
Normalize the residual by the larger of mobilized mass and integrated absolute
discharge/source, with a declared dimensional floor at times before drainage.
Do not normalize only by the much larger initial fluid mass. Report absolute
error as well. Before the FE results are inspected, use `1e-3` relative mass
error as the conservation target; explain any discretization/reconstruction
error from the actual boundary flux extraction separately.

## 5. Independent anisotropic manufactured solution

A constant-reference-tangent test can independently verify off-axis tensor
couplings. In a unit square set

```
u_x = U sin(pi*x) sin(pi*y) sin(t),
u_y = U cos(pi*x) sin(pi*y) sin(t),
p   = P cos(pi*x) cos(pi*y) sin(t).
```

Use the rotated three-dimensional drained stiffness `Cd`, reference Biot
tensor `B0`, and total reference storage `S=1/M`; preserve plane strain.
Define the body force and mass source independently by analytic derivatives:

```
b_i = -Cd_ijkl * d_j d_l u_k + B0_ij * d_j p,
s   = S*p_t + B0_ij*d_j u_i,t - mobility*Laplacian(p).
```

Minor symmetry accounts for the symmetric strain in the first expression.
For example, `Laplacian(p)=-2*pi²*p`; mixed derivatives of both displacement
components are nonzero. Prescribe the exact displacement and pressure on
all boundaries and start from their zero initial values. Compute the forcing
with independently written analytic tensor contractions, not by invoking the
application's residual or automatic differentiation of its implementation.
For Q2 displacement and Q1 pressure, target the expected smooth-solution L2
orders (three and two) in a spatial study with small time error, and first
order in time for backward Euler. Identify any loss of observed order before
acceptance. This is a small-strain tensor-coupling gate, not a verification of
the nonlinear constitutive law or finite-deformation flux transformation.

## 6. Finite-load anisotropic and partial-drainage studies

Rotate mineral material axes, not the arbitrary internal representation.
Use the full rectangle for off-axis anisotropy unless every imposed symmetry
is proved; a quarter-domain reflection restriction can suppress the physical
shear and displacement modes being measured. Keep hydraulic mobility isotropic
to isolate elastic pressure-coupling effects. Use the same fluid law and
drainage conditions for the isotropic comparison.

Partial-edge drainage produces genuinely two-dimensional pressure gradients.
Report pressure maps, displacement, shear stress, Biot off-diagonal components,
conservation, and refinement. Pressure-edge corner singularities can reduce
global convergence order; distinguish this demonstration from the smooth
manufactured solution. Record positive phase volumes, root branch stability,
and general tangent stability along the path. Scalar mineral-volume stability
alone is not full coupled stability. These are numerical demonstrations, not
comparisons with the classical isotropic series or experimental validation.

## 7. Required provenance and publication boundary

Each run records application/source hashes, input-deck hash, compiler and
framework versions, mesh and time step, command, exit status, solver tolerance,
diagnostic extrema, and output hashes. A frozen failed run remains evidence.
Publication claims must point to actual completed gates and cannot borrow
acceptance from an earlier material-only manuscript. Regenerated plots must
read the preserved run data. The source/reference checks here supply no
coupled-FE acceptance verdict until those runs are completed and assessed.

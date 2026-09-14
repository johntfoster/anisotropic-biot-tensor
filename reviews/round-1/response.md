# Response to round 1

Verdicts: reviewer 1 ACCEPT; reviewer 2 MAJOR REVISION; reviewer 3 ACCEPT.
Although two reviewers accepted, substantive requests from reviewer 2 were
addressed and the changed paper is sent to a fresh round. Those initial votes
are not represented as votes on the revised source.

## Reviewer 1

- Explicitly write classical solid storage as a:(B0−phi_f0 I), with the
  microisotropic and fully isotropic forms, and attribute the established
  coefficient to inspected Zhao–Borja Eqs. (17), (29), (42).
- Remove the development-history adjective “corrected” from the energy check.
- Retain the reference-only compatibility and finite-state admissibility scope.

## Reviewer 2

1. Recast compatibility as classical storage expressed in q coordinates.
   State that kappa restores existing storage freedom to a restricted ansatz,
   not a new poroelastic coefficient. Abstract, introduction, comparison table,
   identification section, and conclusions now state this distinction.
2. Add three compatible anisotropic intrinsic solids at fixed measured drained
   stiffness. Exhibit C, D and kappa explicitly, verify the reduced energy,
   both unjacketed conditions and positive phase fractions. Varying the
   deviatoric block at nonzero volumetric–deviatoric coupling changes intrinsic
   compliance and the required D:I. This connects the fixed-D projection
   example to the physically constrained family without claiming that the two
   experiments isolate the same mechanism.
3. Add a second fully hyperelastic volume-penalty continuation. It has identical
   reference Hessian and complete zero-pressure condensed response, but a
   different finite-pressure response. Quantify confined-layer differences
   and derive the distinct stress curvature measurable at fixed deformation.
   Explicitly state nonuniqueness and that the two models are not bounds.
4. Add the necessary finite-strain integrability condition on a proposed Biot
   tensor. A spatially constant nonspherical tensor violates it on an open
   coaxial strain domain, explaining the prescribed-path comparator's limits.
5. Further public full-text retrieval attempts for Foster–Xu failed. Existing
   provenance is retained and the evidence gap is recorded. The user has been
   asked for a local source path; no inaccessible equation has been declared
   independently verified.

## Reviewer 3

- Explain exactly which components are independently implemented and which
  constants/root solver are shared.
- Add automatic analytical initial layer-slope assertions, compatible daughter
  reconstruction checks, and a potential/pressure/acoustic check of the second
  hyperelastic continuation.
- Add software versions and the state/direction for the alternative acoustic
  minimum to diagnostics.
- Use decimal reaction-axis tick labels for readability.

## Validation

LuaLaTeX/latexmk build succeeds. Original tensor checks retain pressure error
7.01e-8 and minimum sampled acoustic eigenvalue 2.10654 K*. The alternate
potential/pressure checks have maximum error 2.75e-10 and minimum sampled
acoustic eigenvalue 2.10380 K*. Compatible anisotropic examples satisfy both
unjacketed residuals and sampled porosity exceeds 0.13. These numerical checks
are not claims of global ellipticity or experimental material validation.

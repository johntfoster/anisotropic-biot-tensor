# Independent derivation and correctness review

This is simulated AI peer review, not journal acceptance. The reviewed artifact is the immutable snapshot `.agent-runtime/review-snapshots/insight-round-1`. All source locations below are relative to that snapshot. I did not consult other reviewers' reports or acceptance counts.

## Snapshot integrity and scope

The SHA-256 digest of `source-manifest.json` is `a5289ef83d1b55941719abcd663ad6792debdf728698e833c9f99d998174d18f`. It equals both the supplied snapshot identifier and the contents of `SNAPSHOT_ID`. I independently re-hashed every one of the 713 listed files: **zero missing files and zero digest mismatches**.

I read the snapshot's `AGENTS.md`, `VISION.md`, author profile, root macros and manuscript, included scientific sections, and applicable acceptance-cycle and derivation-auditor instructions. I examined the finite fabric driver, compiled reference fabric implementation, reference verification source, recorded finite verification results, and generated scalar-comparison summary. I inspected rendered PDF pages 13–14 (fabric work and equilibrium), 29 (consolidation comparison), and 30 (finite benchmark). Equations and plotted quantities on those pages are legible and consistent with the inspected source.

The mathematical assessment covers the conformal construction, phase work, pressure transformation, logarithmic-stress conversion, reference limits, fabric restriction, and reported numerical scope. I did not rerun the coupled MOOSE suite, rebuild the frozen PDF, or conduct a fresh full-text citation audit. Those limitations do not affect the explicit algebraic implementation defect below.

## Required change

### D1 — Use the fabric equilibrium's general solid storage in the compiled material

**Location:** `moose_app/include/utils/FabricLaw.h:506–515`, used in fluid mass at line 615; related claims in `sections/finite_elements.tex` under “Fluid mass and the transport closure” and `sections/fabric_studies.tex:52–58`.

The compiled fabric law accepts and rotates a general positive-definite anisotropic mineral stiffness, constructs its general drained stiffness and Biot tensor, and solves the retained fabric equilibrium. Its solid storage, however, is calculated as

`Ss = phi/Ks - Kd/Ks^2`,

where `Ks = I:Cs:I/9` and `Kd = I:Cd:I/9`. This reduction is valid for an isotropic mineral, including the mineral used in the new plots. It is not generally the fixed-deformation mineral-volume derivative for the accepted anisotropic inputs with shape-changing distention.

Let the columns of `L` be the orthonormal retained distention directions and let `t = L^T I`. The equilibrium used by the implementation itself gives

`Ss = phi^2 t^T (D + phi L^T Cs L)^(-1) t`.

Equivalently, the general compliance expression already consistent with the manuscript is

`Ss = phi I:Cs^(-1):I - I:Cs^(-1):Cd:Cs^(-1):I`.

**Concrete evidence:** I evaluated these expressions independently with the mineral Mandel matrix in `sections/experiments.tex:10–18`, `phi = 0.9`, the new fabric moduli `(kv, ka, kc) = (5.4, 1, 0.4)`, and fabric angle 45 degrees. The equilibrium gives `Ss = 0.030090340364165323`; the compiled formula gives `0.030004593064413946`, a relative discrepancy of about 0.285%. Thus fluid mass and the implementation's own mineral-volume response disagree for this admissible input. The discrepancy is algebraic, not a discretization issue.

**Requested correction:** Compute storage from the retained equilibrium operator or the general compliance expression, and check at least one anisotropic-mineral fabric state by differentiating its mineral volume with pressure. An alternative is an explicit, enforced supported-input restriction that prevents the currently accepted cases for which the shortcut is invalid. Updating the general coefficient is the more natural local correction because the rest of this material already supports anisotropic mineral stiffness.

**Impact:** This does not invalidate the reported isotropic-mineral fabric histories, scalar/tensor differences, or commuting finite benchmark. It is a bounded defect in the supplied general material implementation and its consistency with the governing mineral-volume definition. A local correction and focused validation should suffice; no reconstruction of the manuscript's theory is indicated.

## Derivation findings

### D2 — Conformal phase work and pressure derivative are consistent

**Locations:** `main.tex`, labels `eq:distention-mineral-energy-work`, `eq:equivalent-mixture-mineral-energy`, `eq:energy-returned-effective-stress`, `eq:finite-biot-tensor`, and `eq:cauchy-pressure-tangent`; `sections/stress_reconstruction.tex`; `sections/logarithmic_derivative.tex`.

The mineral and mixture volume normalizations are carried consistently. The skew internal-rotation variation performs no work against symmetric stress, while the rotated mineral stress is retained in the complete phase balance. Differentiating the conformal energy at fixed mineral volume gives the deviatoric mineral stress plus the distention mean stress; the pressure equilibrium supplies the missing mineral mean stress. This verifies the full tensor balance, rather than only its trace. The material logarithm derivative is retained for noncoaxial anisotropy, including its repeated-eigenvalue limit.

The pressure envelope gives `dW'/dp = phi Jbar`; mixed differentiation then yields `d sigma/dp = -B` at fixed deformation. The paper correctly distinguishes this tangent from the finite stress increment and integrates it over pressure. The reference compliance restriction, reference storage expression, isotropic reduction, and selected unjacketed path are consistent with the same energy.

### D3 — The fabric work restriction is explicit and sufficient for the reported finite family

**Location:** `sections/pore_fabric.tex:161–211`, especially `eq:fabric-phase-work` and `eq:fabric-commuting-work`.

Direct contraction of the multiplicative variation produces the displayed similarity-transformed mineral stress. It becomes the prescribed mineral-energy work when the distention stretch commutes with the mineral stress. The manuscript states this additional condition before using the finite construction and explicitly excludes a general noncoaxial finite extension. The reference quadratic law remains available without assuming a finite commuting path. The retained-subspace minimization and Moore–Penrose compliance expression are also consistent: complementary modes are kinematically frozen, rather than allowed to minimize a zero-stiffness distention energy.

### D4 — The finite benchmark checks complete spatial stress and the pressure tangent

**Locations:** `sections/fabric_studies.tex:117–167`; `examples/fabric_insight.py`, functions `finite`, `candidate_energy`, and `verify`; `build/insight/verification.json`.

The pure stretch, isotropic mineral, and axisymmetric distention share principal axes. Their common axes being oblique does not make the state noncoaxial, and the paper correctly avoids that claim. The unreduced spectral-energy check perturbs all nine deformation-gradient entries at the converged commuting states; it is a full spatial-stress derivative check, not a trace check. Re-solving under pressure increments preserves the admissible family and checks its full pressure tangent.

I performed a separate direct 3-by-3 tensor calculation using SciPy matrix exponential/logarithm and an independently assembled two-variable equilibrium, without importing the manuscript driver. Over the nine combinations `gamma = (-0.4, 0, 0.45)` and `p = (0, 0.3, 0.8)`, central differences with deformation step `5e-5` gave a maximum full spatial-stress discrepancy of `1.03779e-8`; pressure step `1e-5` gave `1.40048e-11`. These reproduce the reported scales. The recorded step sequence also decreases the stress derivative error approximately fourfold per step halving, and the reference-limit orders agree with the quoted values.

These checks support first derivatives at the admissible states and the explicitly stated commuting-family result. They do not prove a general finite constitutive extension or stability against every deformation mode; the manuscript does not claim either.

### D5 — The scalar comparison preserves reciprocity and has a clear scientific scope

**Locations:** `sections/fabric_studies.tex:52–109`; `moose_app/src/materials/FabricMaterial.C:107–120`; `build/insight/comparison_summary.tex`.

The scalar approximation replaces the pressure-coupling tensor in both stress and fluid mass. The compiled signs agree with the displayed equations, preserving their common thermodynamic coupling. Holding drained stiffness, fixed-strain storage, and mobility fixed isolates the effect of this substitution. Internal fabric outputs are expressly excluded from a mineral-volume interpretation for the scalar approximation. Positive fixed-strain storage and drained stiffness suffice for the stated positive energy in strain and fluid content.

The comparison reports time-history norms and combined space/time sensitivity rather than an unsupported convergence order. Its isotropic mineral makes the storage shortcut in D1 exact for these particular runs. The finite-element claims distinguish reference-tangent verification, finite-load demonstrations, and experimental validation appropriately.

## Optional notes

No optional change is needed for this review's conclusion. The commuting specialization and synthetic-material scope should remain explicit when correcting D1.

MINOR REVISION

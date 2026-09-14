# Simulated JMPS review — reviewer 2, round 2

**Overall verdict: ACCEPT**

This is an independent simulated peer review, not a journal decision. I reviewed the revised version recorded in `reviews/round-2/source-sha256.txt`, verified every listed hash, and assessed the response against my round-1 report. ACCEPT here means that I find no substantive revision necessary within the paper's stated theoretical scope; it is not a claim of exhaustive historical-priority verification or experimental validation.

The revised manuscript addresses my three substantive objections. Its defensible contribution is now a connected constitutive analysis: classical storage diagnoses a restricted mineral-energy ansatz; an explicit compatible anisotropic family separates stiffness-block bookkeeping from compliance effects; and finite-state integrability and two hyperelastic continuations identify information that reference calibration cannot determine. This is more useful to a mechanics reader than presenting the coordinate transformation or the classical storage condition as a new principle. The claims now fit what is demonstrated.

## Assessment of the prior requests

### 1. Classical storage and novelty: addressed

At `main.tex:815–834`, `eq:classical-solid-storage` and `eq:microisotropic-solid-storage` explicitly identify `phi_s0^2/h` with classical solid storage. The attribution to Zhao–Borja Eqs.(17), (29), and (42) agrees with the full-text evidence inspected in round 1. The manuscript also states that the added `kappa` restores existing constitutive freedom to a restricted energy decomposition rather than introducing a new independent physical coefficient. The abstract, introduction, comparison table, and conclusions consistently adopt that narrower claim.

I independently recover `S_s = a:(B0 − phi_f0 I)` by substituting `B0 = I − Cd:a`; the stated isotropic-intrinsic-solid specialization follows immediately. The paper does not need a new storage law to be useful. Its contribution is the explicit demonstration of why a particular identification of the mineral curvature fails, together with the ensuing finite-deformation constitutive restrictions and identification tests. The new integrability and continuation analyses supply the additional mechanics content missing from the initial version.

### 2. Compatible anisotropic intrinsic solids: addressed

The new subsection in `sections/experiments.tex:117–183` connects the constrained projection calculation to a family satisfying both reference unjacketed conditions. The daughter reconstruction is explicit. In particular, the proposed `D` has `D:I = t`, and its projected symmetric contribution cancels the deviatoric mineral contribution to `Cc`. Consequently `Cc = C`, and the prescribed drained tensor, mixed tangent, and effective mineral curvature are recovered.

The expression for `a` follows by inversion of the mineral tensor's two-dimensional volumetric–axial-deviatoric block. This is a particularly useful addition: at nonzero cross-block coupling, changing the deviatoric stiffness changes the hydrostatic *compliance* even when `Pdev:H:I` stays fixed. Compatibility then requires a change in `D:I`. The revised discussion explains why the fixed-coupling and compatible-family comparisons answer different questions and does not attribute all measured directionality uniquely to one daughter tensor.

The positive reduced energy and sampled phase-fraction checks support the stated example. They are not a homogenization proof for a specified pore geometry, and the paper appropriately confines the microscopic compatibility claim to the reference response. I do not require a new microstructural simulation to support the narrower constitutive result now claimed.

### 3. Finite-pressure nonuniqueness and engineering significance: addressed

The volume-penalty energy in `sections/experiments.tex:348–414` provides the requested substantive test of higher-order constitutive freedom. Expanding about the reference state gives the same Hessian as the logarithmic penalty; at zero pressure, both penalties vanish at `q = r:epsilon`, leaving exactly the same condensed drained energy at every deformation. Nevertheless their finite-pressure responses differ.

I independently checked the volume-penalty equilibrium, pore-volume derivative, and positive-branch curvature `h_p = h Jbar_V^2`. The pressure-independent but deformation-dependent Biot tensor is correct. The reported comparison now distinguishes freezing a reference stress tangent from choosing a different fully hyperelastic continuation. The text explicitly says that the two continuations are neither bounds nor uniquely selected by reference data.

The fixed-deformation pressure-curvature discriminator is also correct. It turns the nonuniqueness observation into a specific additional measurement, while acknowledging experimental resolution and the reversible pressure range. The paper does not claim that the large-strain percentages describe real claystone or establish a universal engineering error threshold. This theoretical sensitivity study, coupled with a measurable discriminator, adequately addresses my concern without requiring a consolidation transient or new experimental campaign.

## New integrability result and overall mathematical assessment

At `main.tex:335–353`, mixed-derivative symmetry gives `partial_j(J B_i) = partial_i(J B_j)` on the stated coaxial logarithmic-strain domain. If the spatial components are constant, `partial_i J = J` requires equality of those components. The conclusion is correctly restricted to a smooth hyperelastic pore-volume potential on an open strain domain; it does not exclude anisotropic reference tangents or objective rate theories. This is a concise, useful restriction on a commonly tempting finite-state approximation.

I found no new mathematical inconsistency in the changes. The previously checked envelope theorem, pressure tangent, objectivity, scalar condensation, storage, and distinction between local mineral stability and finite-strain ellipticity remain consistent. The additions strengthen the paper's constitutive argument rather than merely expanding its numerical illustrations.

## Verification and remaining evidence limits

I inspected both numerical scripts and freshly ran `.agent-runtime/venvs/numerics/bin/python examples/verify_tensor.py`. The checks passed: original pressure-tangent maximum discrepancy was approximately `7.01e-8`; the alternative potential/pressure discrepancy was `2.74e-10`; sampled acoustic minima were approximately `2.10654 K*` and `2.10380 K*`. The compatible mineral examples satisfy the implemented checks and have minimum sampled porosities above 0.13. These are numerical local checks, not a proof of global ellipticity.

I also independently checked the analytical pressure-curvature formula with forward pressure differences at the three prescribed predeformations; discrepancies were below `6.1e-11`. Re-evaluating the standard-library layer solver reproduced the stated end extensions and reaction stresses for both continuations. The scripts share material constants and a scalar root solver as the manuscript now explains; their general tensor derivative implementation is separate.

The Foster–Xu full text remains unavailable in this review environment, so the detailed equation-number correspondence to that predecessor remains **not independently verified**. I read the updated evidence note and do not treat a failed retrieval as successful verification. This is a remaining provenance-check limitation, not evidence of an incorrect attribution; the present derivation is self-contained and its novelty argument no longer rests on an unsupported claim that conjugacy or storage is new. No citation-count ranking or exhaustive priority claim is made.

No further substantive changes are requested. The acceptance assessment is for this theoretical constitutive study with its present qualifications, not for a validated rock model or a general theorem about all anisotropic porous microstructures.

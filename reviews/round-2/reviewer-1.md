# Simulated JMPS review — reviewer 1, round 2

**Overall verdict: ACCEPT**

This is an independent simulated review, not an actual journal decision. Acceptance means no substantive change is required within the stated scope. I reassessed the revised results rather than carrying forward the round-1 vote.

## Scope and overall assessment

I read `reviews/round-1/response.md`, the revised manuscript and experiments, and the changed numerical implementations against `reviews/round-2/source-sha256.txt`. My round-1 review documents the unchanged conjugacy, constrained reduction, unjacketed loading, and stability arguments. This report independently assesses the new storage interpretation, compatible anisotropic reconstruction, integrability condition, and second hyperelastic continuation. No source or code was edited.

The revised paper makes its contribution more precise and more convincing. It now explicitly identifies the effective mineral-volume curvature as a representation of classical solid storage, and does not claim a new independent poroelastic coefficient. The compatible anisotropic examples connect the projected stiffness-block calculation to the physical constraints that alter its interpretation. Most usefully, the second hyperelastic energy demonstrates that identical reference data and an identical complete drained response do not identify finite-pressure behavior. The pressure-curvature discriminator makes that nonuniqueness testable in principle. These are worthwhile constitutive insights, without implying experimental validation or a new general principle of poromechanics.

## Independent checks of the revised mechanics

1. **Classical storage (`main.tex:815–834`).** From `B0 = I-Cd:a`, contraction gives `a:(B0-phi_f0 I) = phi_s0 tr(a)-a:Cd:a`. This equals `phi_s0^2/h` under the compatibility condition. Taking `a=I/(3Ks)` gives `(tr(B0)/3-phi_f0)/Ks`, and taking B0 spherical recovers `(B-phi_f0)/Ks`. The revised interpretation is algebraically exact and resolves the risk of presenting an existing storage relation as a new coefficient.

2. **Compatible daughter reconstruction (`sections/experiments.tex:118–143`).** The proposed D satisfies `D:I=t`, because the projected mineral block annihilates I. Right multiplication by Pdev eliminates its rank-one term, giving `D:Pdev=-Pdev:H:Pdev/2`. Its adjoint supplies the other half, so the daughter contribution cancels in Cc and yields Cc=C. The prescribed C then condenses exactly to Cd; the added kappa supplies the required h. The construction uses no unjustified major symmetry of D. Positivity is correctly claimed on the constrained state space, not on arbitrary independent skeleton and mineral strains.

3. **Anisotropic compliance (`sections/experiments.tex:145–182`).** In the orthonormal v,T subspace the mineral matrix is `[[3 phi_s0 Ks,c],[c,2 phi_s0 mu_s+beta]]`. Inverting this two-by-two block against `phi_s0 sqrt(3) v` gives precisely the stated a. Consequently changing beta at nonzero c changes hydrostatic compliance, even though the direct volumetric–deviatoric stiffness block remains unchanged. The manuscript correctly explains that compatibility also changes D:I; this does not contradict the fixed-D comparison.

4. **Integrability (`main.tex:335–354`).** Along diagonal stretches, `dPhi/depsilon_i=J B_i`. Commutation of the two strain derivatives gives the stated necessary condition. If the spatial principal components are constant on an open coaxial strain domain, differentiation of J forces every pair of them to be equal. The conclusion is properly limited to the smooth hyperelastic volume-potential setting and the specified open domain. It does not prohibit reference tensors or one-dimensional path approximations. No sufficiency claim is made.

5. **Second energy and branch (`sections/experiments.tex:347–381`).** Write `y=exp(q)` and `E=exp(r:epsilon)`. The alternative pressure equilibrium reduces to `h(y-E)+phi_s0 p=0` on y>0, giving the reported mineral volume. The condensed potential is exactly the drained energy plus `phi_s0 p E - phi_s0^2 p^2/(2h)-pJ`. Differentiation therefore gives the reported pore volume and pressure-independent, deformation-dependent Biot tensor. Its q curvature at equilibrium is `h y^2>0`. The shared reference Hessian follows by expanding `y-E=q-r:epsilon+O(strain^2)`, and the identical drained energy follows by setting y=E. The positivity restriction and collapse limit are explicit.

6. **Pressure curvature (`sections/experiments.tex:395–413`).** For the logarithmic penalty, at zero pressure `q_p=-phi_s0 E/h` and `z_p=phi_s0 E/h`. Differentiating `exp(q)/(1+z)` produces two equal contributions and hence the stated factor of two in `B_i,p=2 phi_s0^2 r_i E^2/(Jh)`. The alternative tensor has zero pressure derivative. Since `sigma_p=-B`, the stress-curvature sign is also correct.

## Numerical evidence

I reran `examples/verify_tensor.py` successfully with the repository numerics interpreter. The original maximum pressure error remains 7.0061e-8 and its sampled acoustic minimum is 2.10654. For the alternative potential, the maximum pressure/potential discrepancy is 2.7433e-10 and the sampled acoustic minimum is 2.10380. The three compatible mineral cases have h values 24.39759, 26.39026, and 25.31873; their sampled minimum porosities are 0.13921, 0.13224, and 0.13511, respectively. The added analytical layer-slope assertions pass.

I separately evaluated the new zero-pressure curvature using second-order forward pressure differences at axial logarithmic strains -0.2, 0, and 0.2. The largest absolute discrepancy from the analytic formula was 6.01e-11. I also independently called the two layer solves: at p/Ks=0.1, the alternative extension is 0.2987681 and its reaction divided by Ks is -0.04336005, with porosity 0.40911. Its extension differs from the logarithmic law by 2.3637%; at p/Ks=0.01 that difference is 0.1892%. These reproduce the revised reported values.

## Blocking findings and limitations

No blocking finding was identified. The paper's conclusions remain conditional on its chosen elastic energies and isotropic-distention kinematics. Reference compatibility does not establish exact finite-pressure constituent equivalence, and the two continuations are neither material validation nor bounds over all admissible laws. The manuscript explicitly preserves those limitations. Sampled acoustic positivity is appropriately reported as local numerical evidence, not global ellipticity.

I have not independently completed the historical citation/full-text audit. In particular, the recorded access gap for Foster–Xu persists; the response does not misrepresent that source as freshly verified. My acceptance rests on the self-contained mechanics and the appropriately narrowed contribution, and does not certify exhaustive historical priority. No additional editorial changes are necessary for my recommendation.

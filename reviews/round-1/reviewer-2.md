# Simulated JMPS review — reviewer 2, round 1

**Overall verdict: MAJOR REVISION**

This is an independent simulated peer review, not a journal decision. I reviewed the version recorded in `reviews/round-1/source-sha256.txt`; all five hashes were verified. The emphasis is novelty, attribution, physical interpretation, and significance for mechanics readers. No manuscript or numerical source was modified.

The manuscript is clear about several important limitations and its principal differentiation identities appear internally sound. I nevertheless do not consider it ready for acceptance in JMPS. Its proposed central contribution must be distinguished more sharply from the established storage compatibility of linear poroelasticity, and the finite-deformation examples need a stronger connection to the claimed constitutive mechanism. These are substantive issues, not requests for cosmetic restructuring.

## 1. The central compatibility result needs an explicit comparison with established storage, not merely a new coordinate expression

**Locations:** `main.tex:669–755`, particularly `eq:compatible-mineral-tangent`; `main.tex:777–792`; introduction and abstract.

The extra unjacketed condition is correctly derived. However, independently eliminating the manuscript's mineral coordinate shows why it is not automatically a new constitutive principle. Write the solid contribution to the reference fluid-storage coefficient as `S_s = phi_s0^2/h`. The manuscript's compatibility equation gives

`S_s = phi_s0 tr(a) − a:Cd:a = a:(B0 − phi_f0 I)`.

For an isotropic intrinsic solid this is

`S_s = [tr(B0)/3 − phi_f0]/Ks`,

and in the fully isotropic case it becomes `(B − phi_f0)/Ks`. Adding fluid compressibility gives the familiar storage coefficient. Thus the two-condition calculation recovers both the classical stress coupling and classical storage in the chosen `(e,q)` coordinates. It exposes an inconsistent assignment of the fixed-skeleton curvature in the restricted daughter energy; it does not, by itself, establish a previously unknown compatibility requirement of poroelasticity.

This assessment is supported by inspected full texts. Zhao–Borja, published PDF pp.4–7, Eqs.(17), (29), and (42), uses `beta = tr(b)/3 − phi_f` and the pressure-rate coefficient `beta/Ks + phi_f/Kf`. Its isotropic-mineral storage is exactly the expression above. Braun et al., local preprint p.4, Eqs.(14)–(15), explicitly introduces an additional poroelastic parameter for porosity response beyond the stress–strain coefficients and relates the Biot and skeleton moduli to fluid compressibility and unjacketed pore response. These are stronger antecedents for the manuscript's central issue than the present comparison table conveys.

**Required improvement:** Make the equivalence explicit, with full-text-supported attribution, and state the remaining contribution as a compatibility diagnosis of the restricted skeleton–mineral energy. Explain whether the proposed extra `kappa q^2/2` term is more than the independent storage parameter already present in a general poroelastic potential. Establish an additional substantive result—such as a physically justified restriction on the energy family or a testable nonlinear implication—rather than relying on the coordinate change and correction of the restricted ansatz as the principal novelty claim. This request does not imply that the algebra is wrong.

## 2. The mineral-anisotropy mechanism and the physically compatible examples are not yet connected

**Locations:** `main.tex:480–535`, `main.tex:596–635`, `main.tex:736–756`; `sections/experiments.tex:4–84`.

The projection `Pdev:H:I` follows correctly by substituting the isotropic-distention constraint into the quadratic energy. Its interpretation is carefully qualified in the conclusions. Nevertheless, the only example that varies mineral anisotropy explicitly does not enforce homogeneous-solid unjacketed compatibility. The finite-pressure and confined-layer examples then use an isotropic intrinsic bulk response and an independently specified reduced energy. They therefore do not demonstrate that the proposed *mineral-anisotropy* mechanism survives the additional compatibility requirements in a physically admissible homogeneous-constituent model.

There is also a constitutive-identification issue rather than just a numerical one: once `B0 = I − Cd:a` is imposed, changing the intrinsic mineral tensor changes `a`, and the previously freely chosen `D:I` generally has to change. Holding the daughter coupling fixed is an algebraic isolation experiment, but its compatibility with a realizable porous material is not established. The manuscript acknowledges this limitation; the acknowledgement does not supply the missing connection.

**Required improvement:** Construct at least one anisotropic-intrinsic-solid example satisfying both reference compatibility conditions, positive reduced curvature, and admissibility. Explicitly exhibit how the daughter coefficients, the added pore constraint, and the measured drained tensor relate. Demonstrate which part of the proposed mineral effect remains identifiable under those restrictions. A micromechanical benchmark would be particularly persuasive, but it is not the only possible route. The need is a defensible connection between the advertised mechanism and the compatible constitutive family.

## 3. The finite-pressure results demonstrate one chosen continuation, with limited evidence of engineering significance

**Locations:** `sections/experiments.tex:46–115`, `sections/experiments.tex:117–134`, confined-layer subsection; `main.tex:827–836`.

The homogeneous layer is a legitimate equilibrium boundary-value problem and the approximations satisfy their own traction conditions. The small-pressure checks and the explicit distinction between a tangent and a secant pressure response are useful. However, comparing a nonlinear constitutive model with a frozen reference tensor necessarily reveals nonlinear differences. The reported 9–11% discrepancies do not yet distinguish a newly identified material mechanism from the arbitrary higher-order continuation selected by the quadratic Hencky energy. The largest effects occur at roughly 30% extension and `p/Ks = 0.1`; the manuscript itself correctly notes the difficulty of reaching such a reversible regime in stiff-mineral rocks.

An explicit counterexample to reference-data uniqueness is available within the manuscript's setting: add `gamma (q − r:epsilon)^4/4`, with `gamma >= 0`, to `eq:example-hencky-energy`. This objective term leaves the entire zero-pressure condensed response and all reference second derivatives unchanged, including both unjacketed conditions, but changes finite-pressure equilibrium and coupling. Its mineral curvature contribution is nonnegative. Thus agreement with the reference data used here does not select the reported finite-pressure response.

**Required improvement:** Quantify sensitivity to a higher-order constitutive freedom of this kind, and identify the additional finite-pressure measurement that constrains it. Alternatively provide a microscopic or experimental basis for the chosen continuation. Demonstrate the practical consequence over an explicitly justified reversible regime, or recast the example as a constitutive sensitivity study with a clearly bounded significance claim. A full consolidation simulation is not required to resolve this issue.

## Attribution and mathematical assessment

- The finite-deformation identities based on the envelope theorem, mixed derivatives, and the push-forward of pore-volume sensitivity are sound under the stated smooth-branch assumption. Symmetry and objectivity follow as claimed. The manuscript properly distinguishes invertibility from positive mineral curvature and from finite-strain ellipticity.
- De Buhan et al., local full text p.911, Eq.(11), already gives a skeleton potential in deformation gradient and Lagrangian pore volume. Its introduction, pp.909–910, explicitly points to earlier finite-strain poroelasticity and micromechanical work; pp.918–919 analyze pressure-independent effective stress. The present acknowledgement is appropriate. The Legendre transform and tensor sensitivity should remain organizational identities rather than an independent novelty claim.
- Zhao–Borja's Eq.(23) is an objective rate law and Eqs.(26), (30), and (42) identify anisotropic coupling. The manuscript's account is substantially fair; extend the comparison to its storage coefficient, as requested above.
- Braun et al.'s full text supports the motivation for separately measuring elastic and pressure responses. It does not validate the numerical energy or parameters here, and the manuscript does not falsely claim that it does.
- Detailed comparisons with Foster–Xu Eqs.(33) and (39) could not be independently verified: the local full text is absent. This matters because the scalar-to-tensor extension is part of the provenance of the paper. Supply the actual predecessor text to complete that comparison. I do not infer an erroneous attribution from the access gap.

## Evidence and scope

Inspected source PDFs: `references/pdfs/debuhan1998.pdf`, `references/pdfs/zhao2020.pdf`, and `references/pdfs/braun2021.pdf`, including their relevant constitutive sections and surrounding assumptions. I also read `references/notes/novelty-evidence.md` and `references.bib`. Online attempts to reopen the author-hosted Zhao PDF and the Foster–Xu DOI failed in this review session; the substantive source assessments above use the local full texts. No Google Scholar counts were verified and no citation-count ranking or exhaustive historical-priority claim is made. Braun's references point to Brown–Korringa and Aichi–Tokunaga as further storage antecedents, but their full texts were not inspected here and they are not treated as verified replacements.

The present manuscript has a coherent analytical core and useful reproducibility work. Acceptance requires resolving the novelty and physical-significance questions above; neither correct symbolic differentiation nor successful numerical self-consistency checks resolves those questions alone.

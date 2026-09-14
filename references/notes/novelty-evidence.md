# Novelty and constitutive-comparison evidence

Access date: 2026-09-14. Canonical manuscript: `main.tex`; bibliography:
`references.bib`. This is a targeted full-text support audit, not a complete
priority search. No Google Scholar count was verified and no metric-based
canonical ranking is claimed. All descriptions below are paraphrases.

## Verified full texts

### de Buhan, Chateau, and Dormieux (1998)

- Title: The constitutive equations of finite strain poroelasticity in the
  light of a micro-macro approach. European Journal of Mechanics A/Solids
  17(6), 909–921. DOI: 10.1016/S0997-7538(98)90501-0.
- Full text: `references/pdfs/debuhan1998.pdf`, author manuscript deposited
  at https://hal.science/hal-01983081v1. Printed p.911 was also visually
  inspected because PDF text extraction imperfectly preserves formulas.
- Claim: finite-deformation energy potentials using pore volume and pressure
  conjugacy precede the present construction.
- Evidence: p.911, Eq.(11), skeleton potential Ψs(F,Jφ), first Piola stress
  ∂Ψs/∂F, pore pressure ∂Ψs/∂(Jφ). The page explicitly relates this formulation
  to fluid-mass formulations. P.917 Eqs.(38)–(43) recover it from the integral
  of solid energy over the reference solid domain and microscopic virtual work.
- Evidence: pp.918–919, Eqs.(45),(54)–(57), characterize a pressure-independent
  Terzaghi effective stress by the requirement that J(1−φ) depend only on p.
- Verdict: supports. Cite as prior finite-deformation volume-potential
  structure, not merely related background. Pressure-volume conjugacy and
  mixed-partial reciprocity must not be promoted as new principles.
- Manuscript-specific inference: replacing Jφ by J−φs0 Jbar recasts the same
  conjugate-volume structure; the explicit mineral equilibrium and constrained
  daughter-tensor specialization are the narrower contributions to assess.

### Zhao and Borja (2020)

- Title: A continuum framework for coupled solid deformation–fluid flow
  through anisotropic elastoplastic porous media. Computer Methods in Applied
  Mechanics and Engineering 369, 113225. DOI: 10.1016/j.cma.2020.113225.
- Full text: `references/pdfs/zhao2020.pdf`, author-hosted published PDF:
  https://web.stanford.edu/~borja/pub/cmame2020(2).pdf . The NSF copy at
  https://par.nsf.gov/servlets/purl/10169640 timed out, but the author copy succeeded.
- Evidence: pp.4–5 Eqs.(11)–(20), barotropic intrinsic constituent response;
  the term (p−ps)/Ks is discarded as order strain in Eq.(19), with verification
  promised in Section 5. P.5 Eq.(23) assumes a constant elastic moduli tensor
  and a Jaumann stress rate. Eqs.(26),(30) give ψ=I:Ce/(3Ks), b=I−ψ.
  P.6 Eq.(31) recovers isotropic 1−K/Ks; nearby text explicitly notes earlier
  micromechanical derivations by Cheng and Dormieux.
- Verdict: supports the constitutive comparison. Describe this as an objective
  rate formulation with anisotropic drained elastic moduli and scalar intrinsic
  solid bulk response. It is inaccurate to dismiss it as only infinitesimal
  kinematics. The present hyperelastic construction should explain its distinct
  finite-state energy and mineral-volume closure, not imply tensorial coupling
  or thermodynamic derivation is new.

### Wong (2017)

- Title: Anisotropic Poroelasticity in a Rock With Cracks. Journal of
  Geophysical Research: Solid Earth 122(10), 7739–7753.
  DOI: 10.1002/2017JB014315.
- Full text inspected: https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JB014315
- Evidence: Section 2.1 describes independent elastic, effective-stress, and
  storage coefficients; under microisotropy, Eqs.(4a,b) express directional
  Biot coefficients using stiffness. Equation image assets failed retrieval,
  so no fresh transcription of those images is claimed. Section 3.2 also
  discusses measured directional responses and their identification limits.
- Verdict: supports the stated qualitative microisotropic comparison and the
  need for assumptions on modulus-based identifications. Does not verify a
  general anisotropic-mineral tensor formula. Fix existing bibliography issue
  and pages to 10 and 7739–7753.

### Braun et al. (2021), existing citation key braun2020

- Title: Transversely Isotropic Poroelastic Behaviour of the Callovo-Oxfordian
  Claystone: A Set of Stress-Dependent Parameters. Rock Mechanics and Rock
  Engineering 54, 377–396. DOI: 10.1007/s00603-020-02268-z.
- Full text: `references/pdfs/braun2021.pdf`, preprint arXiv:2004.09277.
- Evidence: Section 2 distinguishes drained elastic properties from pressure
  coupling; Eqs.(33),(34) identify parallel/perpendicular Biot coefficients
  from drained and pore-pressure moduli. Section 3 introductory identification
  discussion treats overdetermined measurements as a consistency check. Its
  measured stress dependence motivates state-dependent characterization but
  does not validate a chosen present finite-deformation energy.
- Verdict: supports an engineering motivation and independent-measurement
  route. Preserve the distinction between measured response and synthetic
  illustrative calculations.

## Access gaps and scope limits

### Foster and Xu (2025), fosterxu2025

- Publisher record and section preview found for DOI 10.1016/j.jmps.2025.106263,
  JMPS 204, 106263. Preview of the correspondence section uses specific mineral
  volume and a pressure Legendre transform. This is insufficient for a fresh
  full-text comparison of equations.
- SSRN preprint 5172944 / DOI 10.2139/ssrn.5172944 was found, but the PDF
  endpoint returned an HTML access challenge; no false PDF was retained under
  `references/pdfs/`. Publisher full text was also unavailable.
- Verdict: not-verifiable for detailed fresh equation support. Existing source
  attribution can be preserved, but any newly strengthened comparison requires
  the actual full text. An author CV has inconsistent article-number metadata;
  prefer publisher metadata rather than replacing the existing DOI from that CV.

### Carroll (1979)

- Publisher metadata verified: An effective stress law for anisotropic elastic
  deformation. Journal of Geophysical Research 84(B13), 7510–7512.
  DOI: 10.1029/JB084iB13p07510.
- Publisher PDF returned an HTML access challenge; only abstract and metadata
  accessible. Abstract points to intrinsic versus structural anisotropy, but
  this is not sufficient equation evidence.
- Verdict: candidate-unverified / not-verifiable. Do not attribute an exact
  tensor identity to this source without reading the full text.

## Mathematical distinction for the revised manuscript

The homogeneous-solid unjacketed compatibility relation
B0=I−Cd:Ss:I can be presented with its own explicit loading argument when the
mineral compliance Ss is homogeneous and both external and pore pressures are
incremented equally. The isotropic Ss:I=I/(3Ks) specialization agrees with the
verified Zhao formula. The fully anisotropic formula was not directly verified
in the accessible original literature here; do not disguise the derivation as
an inspected Carroll equation.

The reduced curvature h at fixed skeleton deformation is not automatically an
intrinsic mineral bulk modulus. Under the restricted daughter-tensor energy it
has a particular value; imposing both unjacketed stress and mineral-volume
response can impose extra compatibility beyond stress-only calibration. The
manuscript must distinguish algebraic recovery of a Biot coefficient from
recovery of the complete classical constitutive response.

## Follow-up: classical storage and source-paper access

The Zhao–Borja full text also already supplies the classical storage term.
Published p.4 Eq.(17) defines β=tr(α)/3−φf; p.5 Eq.(29) places
β/Ks+φf/Kf in front of the pressure rate in mixture mass balance;
p.7 Eq.(42) identifies α=b=I−I:Ce/(3Ks). Consequently the coefficient is
(tr(b)/3−φf)/Ks+φf/Kf under those assumptions. This relation is established
background. Diagnosing whether a particular mineral-volume daughter energy
reproduces it is a constitutive-coordinate compatibility result, not discovery
of a new classical storage law. The intrinsic scalar Ks in Zhao must not be
silently identified with a general reduced fixed-skeleton curvature h.

A further bounded Foster–Xu full-text retrieval attempt checked the author's
public website, public GitHub repository inventory and the relevant
`nonlinear_biot_ad_implementation` repository tree, the standard SSRN delivery
endpoint, and the publisher PDF endpoint. No original-paper full text was
found in the inspected repository tree; SSRN again returned an HTML access
challenge. Therefore original-paper Eqs.(33) and (39) remain unverified in this
audit. No private repositories or accounts were accessed, and no authors were
contacted. This evidence limitation does not prevent independent verification
of the revised manuscript's own equations.

## Final local-source verification: Foster–Xu

A locally available author manuscript has now been copied into the standalone
repository as `references/pdfs/fosterxu2025.pdf`. Its title and authors agree
with the cited paper, but its title-page date is **June 22, 2026**; it is not
asserted to be the 2025 publisher version of record. The public retrieval gaps
above remain an accurate record of the earlier attempts. No external-repository
path is needed to inspect the copied evidence or to build this manuscript.

- Inspected full text: Section 4, printed pp.10–12, with surrounding definitions.
- Printed p.11, Eq.(33): transformed specific energy is e_tilde(F,p) =
  e(F,vbar) + p vbar. The adjacent conjugacy is p = −e_vbar; the transform
  gives e_tilde_p = vbar and e_tilde_F|p = e_F|vbar.
- Printed p.12, Eq.(39): B = 1 − (1/v0s) d(vbar)/dJ|p. The same page defines
  v0s = 1/rho_s0; intrinsic specific volume is 1/rhobar_s in Section 4.
- The current manuscript uses rho_s0 = phi_s0 rhobar_s0 and
  vbar = Jbar/rhobar_s0, so vbar/v0s = phi_s0 Jbar. Its normalization bridge
  and scalar formula follow exactly.
- Verdict: **supports**, for the equation text and numbering in this author
  manuscript. The Helmholtz/mixture-reference conversion is the current
  manuscript's explicit derivation. Publisher-version pagination/identity has
  not been independently checked against this later author copy.
- Publication metadata remains the previously verified DOI
  10.1016/j.jmps.2025.106263; the local PDF date is not used to change it.

PDF SHA-256: `468fadc1085ceb2d58e0f847810c01613b3f860834c2d2e2a18e5c8598572bc3`.

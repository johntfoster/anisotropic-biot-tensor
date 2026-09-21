# Round-26 independent review — reviewer 3 (prose / notation / significance)

Manuscript: *An anisotropic Biot tensor from mineral stress and distention work*
Snapshot: `.agent-runtime/review-snapshots/round-26`
Declared SNAPSHOT_ID: `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907`

Emphasis: prose, notation, and significance. Authoritative source rule applied:
all findings below are from files on disk in the frozen snapshot; no chat summary
and no other reviewer's or prior-round report was consulted.

## 1. Snapshot integrity

| Check | Result |
|---|---|
| `sha256(.agent-runtime/review-snapshots/round-26/source-manifest.json)` | `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907` |
| Declared SNAPSHOT_ID | `6e1afd9363639bdedf68ad4c42169710b7e74830e7d5fa83af91d3387c142907` |
| Manifest hash == declared ID | **YES** |
| Manifest entries | 591 |
| Entries re-hashed OK | **591** |
| MISSING | **0** |
| MISMATCH | **0** |

Every manifest entry was re-hashed from the frozen tree (all 591 resolved,
including `main.tex`, all six `sections/*.tex`, `build/main.pdf`, the evidence
JSON/CSV files, and all `fe-evidence/runs/**` cases). No integrity defect, so
no REQUIRED item arises from Step 1.

### Round-25 required fixes, re-verified independently

* **R25-3-1 (`\mathbf m` defined at first use).** The first occurrence of
  `\mathbf m` in document order is `sections/pore_fabric.tex:282`, and line 283
  defines it: "…the axial (degree-two) direction
  \(\mathbf e_2=\sqrt{3/2}\,(\mathbf m\otimes\mathbf m-\mathbf I/3)\), where
  \(\mathbf m\) is the unit material fabric axis". `\mathbf m` appears nowhere in
  `main.tex` or in any section input before `sections/pore_fabric`. **Fixed and
  correct.**
* **R25-3-2 (distention-strain sentence).** `sections/pore_fabric.tex:326–336`
  now reads: \(\mathbf E_{\mathrm{dis}}=\frac{\ln a}{3}\mathbf I
  +\ln h(\tfrac12\mathbf I-\tfrac32\mathbf m\otimes\mathbf m)\), "twice whose
  exponential, \(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\),
  reconstructs \eqref{eq:fabric-transverse-h}, whose unimodular eigenvalues are
  \(h^{-2},h,h\)." I verified this by hand: with
  \(2\mathbf E_{\mathrm{dis}}=\tfrac{2\ln a}{3}\mathbf I+\ln h\,(\mathbf I-3\mathbf m\otimes\mathbf m)\),
  spectral exponentiation gives
  \(\exp(2\mathbf E_{\mathrm{dis}})=a^{2/3}[h^{-2}\mathbf m\otimes\mathbf m
  +h(\mathbf I-\mathbf m\otimes\mathbf m)]=a^{2/3}\mathbf H=\mathbf G\), with
  \(\det\exp(2\mathbf E_{\mathrm{dis}})=a^2=\det\mathbf G\). A bare exponential of
  \(\mathbf E_{\mathrm{dis}}\) would give \(\mathbf G^{1/2}\) and be wrong by the
  stated factor of two; the text claims the factor of two correctly.
  **Fixed and correct.**
* **R25-2-1 (`eigenvalue ratio` retired).** The string "eigenvalue ratio"
  (case-insensitive) occurs **0** times in `main.tex` + `sections/*.tex`,
  **0** times in `site/evidence.json`, and **0** times in
  `site/scientific-snapshot.json`. The rewritten limitation string in
  `tools/register_fabric_evidence.py` now ends "…the reported shape scalar is
  the logarithm of the unimodular transverse fabric eigenvalue", and the stale
  entry is dropped via `STALE_PREFIX` before re-adding, so the registration is
  idempotent. **Fixed and correct** (one residue noted as O-9 below).

## 2. Findings

No REQUIRED item was found. Findings O-1 … O-11 are optional editorial polish;
each is reconciled below with the paper's own equations so the reader is not
blocked.

### NOTATION

**O-1 (OPTIONAL) — \(\mathbb{D}\) is used one subsection before it is defined.**
`sections/pore_fabric.tex:190` (in `sec:fabric-equilibrium`) refers to "the
retained subspace \(\operatorname{range}\mathbb{D}\) of `\cref{sec:fabric-biot}`:
on the complement \(\mathbb{D}\) vanishes…", but \(\mathbb{D}\) is only
introduced two subsections later at line 252–254
(\(W_{\mathrm{dis}}=\tfrac12\mathbf E_{\mathrm{dis}}:\mathbb{D}:\mathbf E_{\mathrm{dis}}\)).
Because the sentence carries an explicit forward cross-reference to
`sec:fabric-biot`, a reader is directed to the definition and is not blocked;
the natural fix is to state the quadratic-energy definition of \(\mathbb{D}\)
in `sec:fabric-energy` (where \(\mathbf E_{\mathrm{dis}}\) already lives) or to
repeat it once at line 190. Marked OPTIONAL, not REQUIRED, because the
cross-reference reconciles the forward use.

**O-2 (OPTIONAL) — the "intermediate frame" name for the barred distention
stress.** `main.tex:217` declares "A bar on a stress denotes its representation
in the mixture frame, whereas a hat denotes the true frame", while
`sections/pore_fabric.tex:120` calls \(\bar{\mathbf S}_{\mathrm{dis}}=2\partial
W_{\mathrm{dis}}/\partial\mathbf G\) "the symmetric distention stress per
reference mixture volume in the intermediate frame". I checked this against the
equations and there is **no** contradiction: `sec:fabric-kinematics` fixes
\(\mathbf R_A=\mathbf I\) for the remainder of the fabric section ("Throughout
the remainder we express the fabric and the mineral stiffness in a common
material frame"), so the intermediate frame and the mixture frame share an
orientation, and \(\bar{\mathbf S}_{\mathrm{dis}}\) is correctly conjugate to
\(\mathbf G\) in that frame. It is nevertheless the only barred stress in the
paper whose frame is named "intermediate" rather than "mixture"; harmonizing
the two words (or adding "the intermediate (mixture) frame" once) would spare
the reader a pause. OPTIONAL, since the usage is reconcilable.

**O-3 (OPTIONAL) — "unimodular eigenvalues".**
`sections/pore_fabric.tex:332` says "whose unimodular eigenvalues are
\(h^{-2},h,h\)". Read against `eq:fabric-tensor`, the eigenvalues of the
unimodular tensor \(\mathbf H\) are indeed \(h^{-2},h,h\) and \(\det\mathbf H=1\),
so the claim is true; but "unimodular eigenvalues" can be misread as
"eigenvalues of unit modulus" (which \(h^{-2},h,h\) are not). "the eigenvalues
of the unimodular tensor \(\mathbf H\) are …" removes the ambiguity.

**O-4 (OPTIONAL) — \(\mathbf e_4,\mathbf e_5\) are never written out.**
`sections/pore_fabric.tex:294–296` states "The labels
\(\mathbf e_1,\dots,\mathbf e_6\) denote this fabric-adapted orthonormal basis of
symmetric tensors", but only \(\mathbf e_1,\mathbf e_2,\mathbf e_3,\mathbf e_6\)
are given explicitly (lines 281–293). The two axis–shear modes involving
\(\mathbf m\) are left implicit, although the paragraph needs "the four
complementary modes" to be the \(\mathbf e_3,\mathbf e_6\) pair plus those two.
Since the retained pair \(\operatorname{span}(\mathbf e_1,\mathbf e_2)\) is
fully defined and the complement is only required to be annihilated by
\(\mathbb{D}\), a reader can proceed; giving \(\mathbf e_4,\mathbf e_5\)
explicitly would complete the stated basis.

**O-5 (OPTIONAL) — three same-letter families that are only separated by case,
style, or subscript.** Checked as requested:

* \(k\) = permeability (isotropic, current configuration, `sections/finite_elements.tex:46`)
  versus \(k_v,k_a,k_c\) = the distention-stiffness block in the fabric basis
  (`sections/pore_fabric.tex:285`). Different sections, and the stiffness entries
  are always subscripted, so no reading error is possible.
* italic \(G=0.75\) = drained shear modulus (`sections/finite_elements.tex:164`)
  versus bold \(\mathbf G\) = distention right Cauchy–Green tensor
  (`eq:fabric-distention-polar`). The paper's own style rule ("second-order
  tensors in upright bold") separates them, but the scalar \(G\) is not listed
  in the convention paragraph.
* \(\mathbf p_1,\mathbf p_2\) (orthonormal vectors spanning the plane normal to
  \(\mathbf m\), `sections/pore_fabric.tex:291`) versus the first Piola stress
  \(\mathbf P\) (`eq:piola-transform-general`, `eq:fe-total-first-piola`) and
  pressure \(p\). Upper/lower case plus subscript separates them cleanly.

None of these is a genuine double meaning; a single sentence in the convention
paragraph of `sec:kinematics` (which already handles \(d\) vs \(\mathrm{dis}\)
admirably) would close the loop.

**O-6 (OPTIONAL) — "eigenvalue_ratio" vocabulary survives in one shipped
report.** `site/reports/fabric-verification.json` still carries the field names
`H_eigenvalue_ratio_expected[0..2]` (values 0.9992863543052309, 1.000357013944851,
1.000357013944851). These are the *eigenvalues of \(\mathbf H\)*, i.e. the
squared shape ratios, not a description of \(\ln h\), and the file is generated
by `examples/verify_fabric.py`, so the manuscript's claim that no statement
describes \(\ln h\) as an "eigenvalue ratio" is unaffected — the phrase is absent
from the manuscript, from `site/evidence.json`, and from
`site/scientific-snapshot.json`. An editorial pass could rename the field for
consistency with the corrected terminology.

### PROSE / PRECISION

**O-7 (OPTIONAL) — one caveat is stated twice in a single paragraph.**
`sections/finite_elements.tex:279–288` says, first, "That agreement is an
implementation check, not an independent derivation: `verify_fabric.py`
re-derives the section equations but shares their modelling conventions with the
compiled material—the distention basis, the equilibrium, and the reported sign
convention for \(\ln h\)", and then, after the volume-only-limit sentence,
"This is an implementation check: the script shares the section's basis and
reported-scalar sign conventions, so it verifies the compiled material against
the equations rather than re-deriving the conventions themselves." The second
sentence repeats the first and its "This" follows the sentence about the
volume-only comparison while explaining the script-versus-material check.
Collapsing the two into one caveat (keeping the volume-only limit as a separate
sentence) would remove the redundancy. This is redundancy, not a contradiction
with any equation, so it is OPTIONAL and not a required correction.

**O-8 (OPTIONAL) — the abstract calls the material-point check "independent"
with a qualifier the body supplies only later.** The abstract and
`sec:conclusion` describe the check as being against "an independent
re-implementation of the section equations", while `sec:fe-fabric` correctly
explains that the script is separately coded but shares the section's basis,
equilibrium, and sign conventions. The two statements are reconcilable
("re-implementation" = independent code; "not … an independent derivation" =
shared conventions) and the same phrase is used in the shipped evidence label,
so I do not treat it as an overclaim; "a separately coded re-implementation"
would make the distinction impossible to miss.

**O-9 (OPTIONAL) — "shape of the mineral" in the introduction.** `main.tex:152`
reads "This conformal distention changes pore volume while leaving the shape of
the mineral unchanged", whereas `sections/pore-fabric.tex:7` says the conformal
specialization does "not change pore shape" and `main.tex:190` says "with no
shape-changing distention". The distention is a dilation times a rotation, so
the statement is true for either reading; "leaving the pore shape unchanged"
matches the rest of the paper and names the quantity the distention is actually
about.

**O-10 (OPTIONAL) — the parenthetical tautology \(h=\mathrm{e}^{\ln h}\).**
`sections/pore_fabric.tex:334–335` ("the logarithm of the unimodular transverse
fabric eigenvalue \(h=\mathrm{e}^{\ln h}\), not a projection of it") and the
caption at `sections/finite_elements.tex:304–305` both append the identity
\(h=\mathrm{e}^{\ln h}\), which carries no information, and the trailing "not a
projection of it" is left unexplained. "the logarithm of the unimodular
transverse eigenvalue \(h\) of `\eqref{eq:fabric-transverse-h}`" says the same
thing. The underlying claim is consistent with `eq:fabric-transverse-h` and
with the recorded eigenvalues, so this is style only.

**O-11 (OPTIONAL) — stiffness/compliance mixed in one sentence.**
`sections/pore_fabric.tex:297–300`: "Two stiffnesses selected independently
therefore satisfy the generalized restriction when their difference is this
distention compliance, not only a spherical contribution." The quantity that
must equal \(\mathbb{D}^{+}\) is the difference of *compliances*
(`eq:fabric-compliance-restriction`), so "their compliance difference is this
distention stiffness" would be precise. The neighbouring statement in
`sec:conclusion` ("Two independently selected anisotropic stiffnesses will
generally fail `\eqref{eq:drained-compliance-restriction}`") is unambiguous, so
the reader can recover the meaning from the equation itself.

### SIGNIFICANCE

Checked and found adequate; no finding raised.

* **Abstract.** The contribution is stated in the final third of the abstract
  ("Replacing the scalar dilation with a symmetric positive definite distention
  whose unimodular part is a pore-fabric tensor supplies the additional
  constitutive law for shape-changing distention: it relaxes the rank-one
  drained-compliance restriction to a fabric-symmetric compliance supported on
  the retained volumetric–axial distention subspace and yields an anisotropic
  Biot tensor driven by both mineral and pore-fabric anisotropy"), and the
  abstract explicitly disclaims quantitative finite-deformation verification
  and experimental validation for the demonstrations.
* **Introduction.** The gap is identified with a measured novelty claim ("Among
  the fabric-elasticity and fabric-poroelasticity constructions surveyed here,
  we are not aware of a tensorial distention law …"), and the route is
  differentiated from prior work by naming what it does *not* do — Cowin's
  fabric-elasticity and fabric-poroelasticity assign the fabric-dependent
  coefficients to the solid at small strain, whereas here "the fabric tensor
  does not stand in for anisotropic elastic constants of the solid, but enters
  the distention energy of the pore space". Thompson–Willis, Hudson, de Buhan,
  Foster–Xu, and Gajo are each cited for the specific relation they supply.
* **Conclusions.** The two-stage construction is restated, the anisotropic Biot
  tensor is derived from pore fabric behind an isotropic mineral, and the
  limitations (synthetic parameters, no laboratory comparison, fixed-step
  temporal floor, alternative distention mechanisms) are stated at the strength
  the evidence supports.

## 3. Overall assessment

The snapshot is intact: the manifest hash equals the declared SNAPSHOT_ID and
all 591 entries re-hash clean. The three round-25 required fixes are present and
correct, and each was re-derived here rather than taken on trust — in
particular the corrected distention-strain sentence, whose
\(\exp(2\mathbf E_{\mathrm{dis}})=\mathbf G=a^{2/3}\mathbf H\) claim I verified
by hand (the factor of two is right), and the removal of the "eigenvalue ratio"
description of \(\ln h\), which is absent from the manuscript and from
`site/evidence.json` (the log eigenvalue ratio would be \(-3\ln h\); the paper
does not claim otherwise anywhere). The fabric/distention symbol family is in
good order: \(\mathbf m\), \(\mathbf H\), \(h\), \(a\), \(\mathbf G\), the
\(\mathbf e\)-basis, and \(\mathbb{D}\) are each introduced before their general
use, with the single forward use of \(\mathbb{D}\) (O-1) explicitly
cross-referenced; \(d\) (drained) and \(\mathrm{dis}\) (distention) are kept
distinct by an explicit convention statement. Terminology is consistent
("transversely isotropic" throughout, "transverse isotropy" never spelled
differently), and the significance statement is honest and properly
differentiated from prior work. Every number I sampled reproduces from the
frozen artifacts (e.g. pressure floor \(3.2209\times10^{-3}\) at \(nx=20\),
\(dt=10^{-3}\); step-refinement ratio \(0.0071039/0.0036580=1.94\); reference
Biot components \(0.7,0.7583,0.7917\); the \(16.8K_*\) isotropic-comparison
shear modulus as the mean of the five deviatoric modes divided by two). The
findings above are editorial polish only and none of them leaves a reader
unable to reconcile a sentence with the paper's own equations, so no required
correction outstanding. The manuscript is acceptable as it stands.

VERDICT: ACCEPT

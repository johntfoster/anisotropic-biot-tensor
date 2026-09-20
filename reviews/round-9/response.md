# Response to independent simulated review — round 9

Reviewed snapshot: `1fa4b3bc4508cc6e9b9a305643bcb33ab50b748ad9ee173e2b90117c1287ec8a`.
All three reports collected. Theory ACCEPT; numerics ACCEPT; exposition MINOR
REVISION. The valid abstract-normalization concern is corrected despite two
acceptances. A new round assesses the changed scientific text.

| Comment | Disposition | Evidence and action |
| --- | --- | --- |
| R3-01, abstract compliance normalization | Accepted; required. | Abstract now states drained compliance equals mineral compliance divided by reference solid fraction plus spherical rank-one contribution. README uses the same normalization. Equation (43) and numerical implementation were already correct; no equations, code, data, or figures change. |
| R3-02, anisotropy without volume-shape coupling | Accepted; optional. | Added the explicit dev(Cs:I)=0 condition adjacent to the Biot formula, noting cubic shear anisotropy can coexist with spherical B. It follows directly from the displayed formula and usual cubic stiffness row sums. |
| R1-O1, admissible pressure-integration domain | Accepted; optional. | Qualified integration from zero as applying on an admissible pressure interval containing zero. No plotted path or equation changes. |
| R1-O2 / R9-R2-03, alternative archive hosting | Deferred optional publication convenience. | PDF embeds the tested numerical ZIP; all three reviewers extracted and checked it successfully. A future journal/DOI deposit can accompany publication, without claiming that it has already occurred. |
| R9-R2-01, permanent near-fold coverage | Retain as optional future coverage. | Reviewer's independent low-solid-fraction tests approached the fold to relative 1e-8 and passed, with volume error at most 5.15e-12. Permanent suite already checks stable tensile states, absent branch, invalid phase volume, and large positive pressure. No demonstrated unresolved defect. |

All other numerical/derivation findings were satisfactory; no required issue
is left unaddressed. Source changes are exclusively prose clarifications.
Numerical sources, data, archive, and displayed equations remain byte-identical
to the reviewed version. A fresh build and source comparison verify this claim.
